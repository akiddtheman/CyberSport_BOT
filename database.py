import sqlite3

connection = sqlite3.connect('cybersportuz.db')
sql = connection.cursor()

# sql.execute('CREATE TABLE tournament (name TEXT, id INTEGER, tournament TEXT, number TEXT);')

def add_player(name, id, tournament, number):
    connection = sqlite3.connect('cybersportuz.db')
    sql = connection.cursor()
    sql.execute('INSERT INTO tournament VALUES(?, ?, ?, ?);', (name, id, tournament, number))
    connection.commit()

def get_player(pk):
    connection = sqlite3.connect('cybersportuz.db')
    sql = connection.cursor()
    tournament = sql.execute('SELECT name, id, tournament, number FROM tournament WHERE id=?', (pk,))
    return tournament.fetchall()
