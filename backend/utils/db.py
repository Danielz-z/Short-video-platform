from contextlib import contextmanager

import mysql.connector
from mysql.connector import pooling

from config import DB_CONFIG, DB_POOL_NAME, DB_POOL_SIZE

_pool = None


def get_connection_pool():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name=DB_POOL_NAME,
            pool_size=DB_POOL_SIZE,
            pool_reset_session=True,
            **DB_CONFIG,
        )
    return _pool


def get_db_connection():
    try:
        return get_connection_pool().get_connection()
    except mysql.connector.Error:
        return mysql.connector.connect(**DB_CONFIG)


@contextmanager
def db_cursor(dictionary=False, commit=False):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=dictionary)
    try:
        yield conn, cursor
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
