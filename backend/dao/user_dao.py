from datetime import datetime


def get_user_by_username(conn, username):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT user_id, username, password, role FROM users WHERE username = %s",
        (username,),
    )
    return cursor.fetchone()


def get_user_by_id(conn, user_id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    return cursor.fetchone()


def count_users(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS total FROM users")
    return cursor.fetchone()["total"]


def list_users(conn, limit=10, offset=0):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT user_id, username, phone_email, role, fans_count, register_time
        FROM users
        ORDER BY register_time DESC, user_id
        LIMIT %s OFFSET %s
        """,
        (limit, offset),
    )
    return cursor.fetchall()


def create_user(conn, user_id, username, phone_email, password_hash, role="user"):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users (user_id, username, phone_email, password, role, register_time)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (user_id, username, phone_email, password_hash, role, datetime.now()),
    )


def update_user(conn, user_id, username, phone_email, role, gender, password_hash=None):
    cursor = conn.cursor()
    if password_hash:
        cursor.execute(
            """
            UPDATE users
            SET username = %s, phone_email = %s, role = %s, password = %s, gender = %s
            WHERE user_id = %s
            """,
            (username, phone_email, role, password_hash, gender, user_id),
        )
    else:
        cursor.execute(
            """
            UPDATE users
            SET username = %s, phone_email = %s, role = %s, gender = %s
            WHERE user_id = %s
            """,
            (username, phone_email, role, gender, user_id),
        )


def delete_user_graph(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM likes WHERE user_id = %s", (user_id,))
    cursor.execute("DELETE FROM comments WHERE user_id = %s", (user_id,))
    cursor.execute(
        "DELETE FROM follows WHERE follower_id = %s OR followed_id = %s",
        (user_id, user_id),
    )
    cursor.execute(
        "DELETE FROM messages WHERE sender_id = %s OR receiver_id = %s",
        (user_id, user_id),
    )

    cursor.execute("SELECT video_id FROM videos WHERE author_id = %s", (user_id,))
    for (video_id,) in cursor.fetchall():
        cursor.execute("DELETE FROM video_tags WHERE video_id = %s", (video_id,))
        cursor.execute("DELETE FROM likes WHERE video_id = %s", (video_id,))
        cursor.execute("DELETE FROM comments WHERE video_id = %s", (video_id,))

    cursor.execute("DELETE FROM videos WHERE author_id = %s", (user_id,))
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))


def get_recent_user_videos(conn, user_id, limit=5):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT video_id, title, likes_count
        FROM videos
        WHERE author_id = %s
        ORDER BY upload_time DESC
        LIMIT %s
        """,
        (user_id, limit),
    )
    return cursor.fetchall()


def refresh_fans_count(conn, user_id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT COUNT(*) AS fans_count FROM follows WHERE followed_id = %s",
        (user_id,),
    )
    fans_count = cursor.fetchone()["fans_count"]
    cursor.execute(
        "UPDATE users SET fans_count = %s WHERE user_id = %s",
        (fans_count, user_id),
    )
    return fans_count


def update_password_hash(conn, user_id, password_hash):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password = %s WHERE user_id = %s",
        (password_hash, user_id),
    )
