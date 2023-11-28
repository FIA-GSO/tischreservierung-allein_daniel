import flask
from flask import request, jsonify
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Test</h1>'''

@app.route('/tische/all', methods=['GET'])
def alleTische():

    conn = sqlite3.connect('../buchungssystem.sqlite')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM tische;').fetchall()

    return jsonify(all_books)

@app.route('/tisch/nummer', methods=['GET'])
def tischNummer():

    conn = sqlite3.connect('../buchungssystem.sqlite')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    query_parameters = request.args

    id = query_parameters.get('id')

    result = cur.execute(f'select * from tische where tischnummer = "{id}";').fetchall()

    if not result:
        return page_not_found(404)

    return jsonify(result)

@app.route('/tisch/reservierungen', methods=['GET'])
def tischReservierung():

    conn = sqlite3.connect('../buchungssystem.sqlite')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    query_parameters = request.args

    time = query_parameters.get('time')
    date = query_parameters.get('date')

    gesamtes_datum = f"{date} {time}"

    result = cur.execute(f'select * from reservierungen where zeitpunkt = "{gesamtes_datum}";').fetchall()

    if not result:
        return page_not_found(404)

    return jsonify(result)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run()
