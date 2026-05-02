from contextlib import contextmanager

import mysql.connector

from config import DB_CONFIG


def get_db_connection():
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

