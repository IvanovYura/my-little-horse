from psycopg2.sql import SQL, Identifier

from service.config import Config
from service.db.database import connect_with
from service.logger import logger
from psycopg2.extensions import connection, ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import DatabaseError

SQL_CHECK_DB = '''
    SELECT 1 FROM pg_catalog.pg_database WHERE datname = %(db_name)s;
'''

SQL_CREATE_DB = '''
    CREATE DATABASE {db_name} WITH OWNER={db_user};
'''

# TODO: name should be unique
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


config = Config.create()


def _open_admin_connection() -> connection:
    # User and DB should be created by Postgres admin
    connection = connect_with(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=None,
        user=config.DB_ADMIN_USER,
        password=config.DB_ADMIN_PASSWORD,
    )

    # CREATE DB statement should be done outside of transaction block
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    return connection


def _open_user_connection() -> connection:
    return connect_with(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
    )


def _create_db_user(user: str, password: str, conn: connection):
    query = f'CREATE USER {user} WITH PASSWORD \'{password}\';'

    with conn.cursor() as cursor:
        try:
            cursor.execute(query)
            logger.info(f'DB user {user} created')

        except DatabaseError:
            # ignore if user exists
            logger.warning(f'DB user {user} already existed')
            pass


def _create_db(db_name: str, conn: connection):
    with conn.cursor() as cursor:

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
        _create_db_user(config.DB_USER, config.DB_PASSWORD, admin_connection)

        if _create_db(config.DB_NAME, admin_connection):
            user_connection = _open_user_connection()

            _create_users_table(user_connection)
            _create_admin_user(config.ADMIN_USER, config.ADMIN_PASSWORD, True, user_connection)

            user_connection.commit()

    except (InitDBError, DatabaseError) as e:
        logger.error(f'Something went wrong: {str(e)}')
        exit(1)

    finally:
        admin_connection.close()

        if user_connection:
            user_connection.close()
