from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection

SQL_SELECT_USER_BY_NAME = '''
    SELECT
        name,
        password,
        is_admin
        
    FROM users
    
    WHERE name = %(name)s;
'''


def fetch_user(name: str, conn: connection) -> dict:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(SQL_SELECT_USER_BY_NAME, {'name': name})
        user = cursor.fetchone()

    return user
