import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_request(request_id):
    conn = get_db_connection()
    request = conn.execute('SELECT * FROM requests WHERE id = ?',
                        (request_id,)).fetchone()
    conn.close()
    if request is None:
        abort(404)
    return request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd12345'

@app.route('/')
def index():

	conn = get_db_connection()
	requests = conn.execute('SELECT * FROM requests').fetchall()
	conn.close()
	return render_template('index.html', requests = requests)

@app.route('/<int:request_id>')
def _request(request_id):
	
    request = get_request(request_id)
    return render_template('request.html', request=request)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        user = request.form['user']
        content = request.form['content']

        if not user:
            flash('Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO requests (user, content) VALUES (?, ?)',
                         (user, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')