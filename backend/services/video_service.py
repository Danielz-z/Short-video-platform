import uuid

from dao import video_dao


def upload_video(conn, title, video_url, author_id, field_id):
    video_id = str(uuid.uuid4())
    video_dao.insert_video(conn, video_id, title, video_url, author_id, int(field_id))
    return video_id


def update_video(conn, video_id, title, current_user_id):
    author_id = video_dao.get_video_author(conn, video_id)
    if author_id != current_user_id:
        raise PermissionError("You can only update your own videos")
    video_dao.update_video_title(conn, video_id, title)


def delete_video(conn, video_id, current_user_id):
    author_id = video_dao.get_video_author(conn, video_id)
    if author_id != current_user_id:
        raise PermissionError("You can only delete your own videos")
    video_dao.delete_video_by_id(conn, video_id)
