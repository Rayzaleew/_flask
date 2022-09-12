import sqlite3
import hashlib
from flask import Flask, render_template, request, url_for, flash, redirect, session
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


#app.config['SECRET_KEY'] = 'abcd12345'

@app.route('/')
def index():
	conn = get_db_connection()
	requests = conn.execute('SELECT * FROM requests ORDER BY created desc').fetchall()
	conn.close()
	return render_template('index.html', requests = requests)


@app.route('/<int:request_id>', methods= ('GET', 'POST'))
def _request(request_id):
    
    if request.method == 'POST':
        conn = get_db_connection()
        status = request.form['status']
        conn.execute('UPDATE requests SET status = ? WHERE id = ?', (status, request_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    _request = get_request(request_id)
    return render_template('request.html', request=_request)

@app.route('/<int:request_id>/feedback', methods= ('GET', 'POST'))
def feedback(request_id):
    _request = get_request(request_id)
    if request.method == 'POST':
        feedback_text = request.form['feedback_text']
        conn = get_db_connection()
        username = session['username']
        user_id = conn.execute('SELECT id FROM users WHERE username = ? ', (username,)).fetchall()
        conn.execute('INSERT INTO feedback (request_id, feedback_text, user_id) VALUES (?, ?, ?)',
                         (request_id, feedback_text, user_id[0][0]))
        conn.commit()
        conn.close()
    return render_template('feedback.html', request=_request)

@app.route('/feedbox')
def feedbox():
    conn = get_db_connection()
    requests = conn.execute('SELECT * FROM requests ORDER BY created desc').fetchall()
    #users = conn.execute('SELECT * FROM users ').fetchall()
    feedback = conn.execute('SELECT * FROM feedback INNER JOIN users ON feedback.user_id = users.id ORDER BY feedback.id desc').fetchall()
    conn.close()
    return render_template('feedbox.html', feedback=feedback, requests=requests)


@app.route('/create', methods=('GET', 'POST'))
def create():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    content = ""
    if request.method == 'POST':
        place = request.form['place']
        user = session['username']
        for product in  range(len(products)):
            number = request.form['number.' + str(product + 1)]
            if number != "0":
                content = content + products[product][1] + " x" + number + " "
            number = "0"
        comment = request.form['comment']

        if not place or not content:
            flash('Data is required!')
        else:
            #content = content + " x" + number + " "
            conn = get_db_connection()
            conn.execute('INSERT INTO requests (place, user, content, comment, status) VALUES (?, ?, ?, ?, ?)',
                         (place, user, content, comment, "Заявка принята"))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html', products = products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = get_db_connection()
        username = request.form['username']
        password = request.form['password']
        password = hashlib.md5(password.encode())
        password = password.hexdigest()
        user = conn.execute('SELECT * FROM users WHERE username = ?',
                        (username,)).fetchone()
        conn.close()
        if user is None:
            flash('Такого пользователя не существует!')
        elif password != user[2]:
            flash('Неверный пароль!')
        else:
            session.permanent = True
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/registration', methods= ['GET', 'POST'])
def registration():
    if request.method == 'POST':
        conn = get_db_connection()
        username = request.form['username']
        password = request.form['password']
        password_retype = request.form['password_retype']
        phone_number = request.form['phone_number']
        user = conn.execute('SELECT * FROM users WHERE username = ?',
                        (username,)).fetchone()
        conn.close()
        if user:
            flash('Пользователь уже существует!')
        elif password != password_retype:
            flash('Пароли не совпадют!')
        else:
            session['username'] = username
            password = hashlib.md5(password.encode())
            password = password.hexdigest()
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, password_hash, user_role, phone_number) VALUES (?, ?, ?, ?)',
                         (username, password, False, phone_number))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('registration.html')


@app.route('/logout')
def logout():
    # удалить из сессии имя пользователя, если оно там есть
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port= 4567)