from flask import current_app, g
from psycopg2 import connect
from werkzeug.local import LocalProxy


def open_connection():
    connection = g.get('connection')

    if connection is None:
        config = current_app.config
        connection = g.connection = connect(
            host=config['DB_HOST'],
            port=config['DB_PORT'],
            dbname=config['DB_NAME'],
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
        )
    return connection


def close_connection():
    connection = g.get('connection')

    if connection is not None:
        connection.close()


conn = LocalProxy(open_connection)
