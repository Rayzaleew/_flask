import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# cur.execute("INSERT INTO products (name, number) VALUES (?, ?)",
#             ('Яйцо', '100')
#             )

# cur.execute("INSERT INTO products (name, number) VALUES (?, ?)",
#             ('Мука', '100')
#             )

# cur.execute("INSERT INTO products (name, number) VALUES (?, ?)",
#             ('Сгущеное молоко', '100')
#             )

# cur.execute("INSERT INTO products (name, number) VALUES (?, ?)",
#             ('Молоко', '100')
#             )

# cur.execute("INSERT INTO products (name, number) VALUES (?, ?)",
#             ('Сахар', '100')
#             )

# cur.execute("INSERT INTO products (name, number) VALUES (?, ?)",
#             ('Соль', '100')
#             )

# cur.execute("INSERT INTO products (name, number) VALUES (?, ?)",
#             ('Джем', '100')
#             )

# cur.execute("INSERT INTO products (name, number) VALUES (?, ?)",
#             ('Сыр', '100')
#             )

# cur.execute("INSERT INTO products (name, number) VALUES (?, ?)",
#             ('Сода', '100')
#             )

# cur.execute("INSERT INTO products (name, number) VALUES (?, ?)",
#             ('Уксус', '100')
#             )


connection.commit()
connection.close()