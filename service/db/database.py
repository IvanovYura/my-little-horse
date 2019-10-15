from flask import current_app, g
from psycopg2 import connect
from werkzeug.local import LocalProxy
from psycopg2.extensions import connection


def open_connection() -> connection:
    connection = g.get('connection')

    if connection is None:
        config = current_app.config
        connection = g.connection = connect_with(
            host=config['DB_HOST'],
            port=config['DB_PORT'],
            dbname=config['DB_NAME'],
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
        )
    return connection


def connect_with(**params) -> connection:
    return connect(**params)


def close_connection():
    connection = g.get('connection')

    if connection is not None:
        connection.close()


conn = LocalProxy(open_connection)
