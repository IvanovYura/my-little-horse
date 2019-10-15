from psycopg2.sql import SQL, Identifier

from service.config import BaseConfig
from service.db.database import connect_with
from service.logger import logger
from psycopg2.extensions import connection, cursor as Cursor, ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import DatabaseError

SQL_CHECK_DB = '''
    SELECT 1 FROM pg_catalog.pg_database WHERE datname = %(db_name)s;
'''

SQL_CREATE_DB = '''
    CREATE DATABASE {db_name} WITH OWNER={db_user};
'''

SQL_CREATE_USERS_TABLE = '''
    CREATE TABLE  users (
        id SERIAL,
        name text NOT NULL,
        password text NOT NULL,
        is_admin boolean NOT NULL,

        PRIMARY KEY (id)
    );
'''

SQL_CREATE_USER = '''
    INSERT INTO users (
        name,
        password,
        is_admin
    )
    
    VALUES (%(name)s, %(password)s, %(is_admin)s);
'''


class InitDBError(Exception):
    pass


def _open_admin_connection() -> connection:
    # User and DB should be created by Postgres admin
    connection = connect_with(
        host=BaseConfig.DB_HOST,
        port=BaseConfig.DB_PORT,
        dbname=None,
        user=BaseConfig.DB_ADMIN_USER,
        password=BaseConfig.DB_ADMIN_PASSWORD,
    )

    # CREATE DB statement should be done outside of transaction block
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    return connection


def _open_user_connection() -> connection:
    return connect_with(
        host=BaseConfig.DB_HOST,
        port=BaseConfig.DB_PORT,
        dbname=BaseConfig.DB_NAME,
        user=BaseConfig.DB_USER,
        password=BaseConfig.DB_PASSWORD,
    )


def _create_db_user(user: str, password: str, cursor: Cursor):
    query = f'CREATE USER {user} WITH PASSWORD \'{password}\';'

    try:
        cursor.execute(query)
        logger.info(f'DB user {user} created')

    except DatabaseError:
        # ignore if user exists
        logger.warning(f'DB user {user} already existed')
        pass


def _create_db(db_name: str, cursor: Cursor):
    cursor.execute(SQL_CHECK_DB, {'db_name': db_name})
    exists = cursor.fetchone()

    if not exists:
        try:
            cursor.execute(SQL(SQL_CREATE_DB).format(
                db_name=Identifier(db_name),
                db_user=Identifier(db_name)),
            )
            logger.info(f'DB {db_name} is created successfully')
            return True
        except DatabaseError as e:
            raise InitDBError(f'Can not create DB {db_name}: {str(e)}')

    logger.warning(f'DB {db_name} already exists')
    return False


def _create_users_table(conn: connection):
    with conn.cursor() as cursor:
        cursor.execute(SQL_CREATE_USERS_TABLE)


def _create_admin_user(name: str, password: str, is_admin: bool, conn: connection):
    params = {
        'name': name,
        'password': password,
        'is_admin': is_admin,
    }
    with conn.cursor() as cursor:
        cursor.execute(SQL_CREATE_USER, params)
        logger.info(f'Admin user {name} is created successfully')


def init_db():
    admin_connection = _open_admin_connection()
    user_connection: connection = None

    try:
        with admin_connection.cursor() as cursor:
            _create_db_user(BaseConfig.DB_USER, BaseConfig.DB_PASSWORD, cursor)

            if _create_db(BaseConfig.DB_NAME, cursor):
                user_connection = _open_user_connection()

                _create_users_table(user_connection)
                _create_admin_user(BaseConfig.ADMIN_USER, BaseConfig.ADMIN_PASSWORD, True, user_connection)

                user_connection.commit()

    except (InitDBError, DatabaseError) as e:
        logger.error(f'Something went wrong: {str(e)}')
        exit(1)

    finally:
        admin_connection.close()

        if user_connection:
            user_connection.close()
