from datetime import datetime


def count_user_videos(conn, user_id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT COUNT(*) AS total FROM videos WHERE author_id = %s",
        (user_id,),
    )
    return cursor.fetchone()["total"]


def list_user_videos(conn, user_id, limit=10, offset=0):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT v.video_id, v.title, v.likes_count, v.upload_time, f.field_name
        FROM videos v
        LEFT JOIN fields f ON v.field_id = f.field_id
        WHERE v.author_id = %s
        ORDER BY v.upload_time DESC
        LIMIT %s OFFSET %s
        """,
        (user_id, limit, offset),
    )
    return cursor.fetchall()


def get_hot_videos_by_author(conn, author_id):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("GetHotVideosByAuthor", [author_id])
        rows = []
        for result in cursor.stored_results():
            rows.extend(result.fetchall())
        return rows
    except Exception:
        cursor.execute(
            """
            SELECT video_id, title, likes_count, author_id
            FROM videos
            WHERE author_id = %s
            ORDER BY likes_count DESC, upload_time DESC
            LIMIT 10
            """,
            (author_id,),
        )
        return cursor.fetchall()


def get_video_author(conn, video_id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT author_id FROM videos WHERE video_id = %s", (video_id,))
    row = cursor.fetchone()
    return row["author_id"] if row else None


def insert_video(conn, video_id, title, video_url, author_id, field_id):
    cursor = conn.cursor()
    try:
        cursor.callproc(
            "InsertNewVideo",
            [video_id, title, video_url, author_id, field_id, datetime.now()],
        )
    except Exception:
        cursor.execute(
            """
            INSERT INTO videos
                (video_id, title, video_url, author_id, field_id, upload_time)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (video_id, title, video_url, author_id, field_id, datetime.now()),
        )


def update_video_title(conn, video_id, title):
    cursor = conn.cursor()
    try:
        cursor.callproc("UpdateVideoTitle", [video_id, title])
    except Exception:
        cursor.execute(
            "UPDATE videos SET title = %s WHERE video_id = %s",
            (title, video_id),
        )


def delete_video_by_id(conn, video_id):
    cursor = conn.cursor()
    try:
        cursor.callproc("DeleteVideoById", [video_id])
    except Exception:
        cursor.execute("DELETE FROM video_tags WHERE video_id = %s", (video_id,))
        cursor.execute("DELETE FROM likes WHERE video_id = %s", (video_id,))
        cursor.execute("DELETE FROM comments WHERE video_id = %s", (video_id,))
        cursor.execute("DELETE FROM videos WHERE video_id = %s", (video_id,))


def like_video(conn, user_id, video_id):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO likes (user_id, video_id, like_time) VALUES (%s, %s, %s)",
        (user_id, video_id, datetime.now()),
    )
    cursor.execute(
        "UPDATE videos SET likes_count = likes_count + 1 WHERE video_id = %s",
        (video_id,),
    )


def get_video_detail(conn, video_id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT v.video_id, v.title, v.video_url, v.upload_time, v.likes_count,
               u.username AS author_name, f.field_name
        FROM videos v
        JOIN users u ON v.author_id = u.user_id
        LEFT JOIN fields f ON v.field_id = f.field_id
        WHERE v.video_id = %s
        """,
        (video_id,),
    )
    return cursor.fetchone()
