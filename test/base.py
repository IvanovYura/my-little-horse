import os

from psycopg2 import DatabaseError
from unittest import TestCase

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from service.config import TestConfig
from service.db.database import connect_with

config = TestConfig()


class TestBase(TestCase):
    TEST_DIR = os.path.dirname(os.path.abspath(__file__))
    RESOURCES_DIR = os.path.join(TEST_DIR, 'resources')

    FIXTURE_NAME = None

    def setUp(self):
        # admin connection is needed to create DB and DB user
        self.admin_conn = _open_admin_connection()

        with self.admin_conn.cursor() as cursor:
            create_db_user(config.DB_USER, config.DB_PASSWORD, cursor)
            create_db(config.DB_NAME, config.DB_USER, cursor)

        self.connection = _open_user_connection()

        with self.connection.cursor() as cursor:
            execute_sql(self.FIXTURE_NAME, cursor)

        self.connection.commit()

    def tearDown(self):
        self.connection.close()

        with self.admin_conn.cursor() as cursor:
            drop_db(config.DB_NAME, cursor)

        self.admin_conn.close()


def execute_sql(fixture_name, cursor):
    """
    Executes SQL code located in resources/fixture_name.

    Uses user connection, should be commit.
    """
    path_to_resource = os.path.join(TestBase.RESOURCES_DIR, fixture_name)

    with open(path_to_resource, 'r') as fixture:
        cursor.execute(fixture.read())


def create_db_user(user, password, cursor):
    query = f'CREATE USER {user} WITH PASSWORD \'{password}\';'

    try:
        cursor.execute(query)
    except DatabaseError:
        # ignore user exists
        pass


def create_db(dbname, user, cursor):
    try:
        drop_db(dbname, cursor)
        cursor.execute(f'CREATE DATABASE {dbname} WITH OWNER={user};')
    except DatabaseError:
        raise Exception('Something went wrong')


def drop_db(dbname, cursor):
    try:
        cursor.execute(f'DROP DATABASE IF EXISTS {dbname};')
    except DatabaseError:
        raise Exception(f'Could not remove test DB {dbname}.')


def _open_user_connection():
    # connection to test DB
    return connect_with(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
    )


def _open_admin_connection():
    connection = connect_with(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=None,
        user=config.DB_ADMIN_USER,
        password=config.DB_ADMIN_PASSWORD,
    )

    # DB should be created outside the transaction block
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    return connection
