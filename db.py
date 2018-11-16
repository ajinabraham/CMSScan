import sqlite3
from flask import g

DATABASE = 'db.db'


def get_db():
    dbo = getattr(g, '_database', None)
    if dbo is None:
        dbo = g._database = sqlite3.connect(DATABASE)
    return dbo


def init_db(app):
    with app.app_context():
        dbo = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            dbo.cursor().executescript(f.read())
        dbo.commit()


def dict_factory(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))
