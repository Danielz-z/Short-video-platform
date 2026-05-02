import re
import uuid

from werkzeug.security import check_password_hash, generate_password_hash

from dao import user_dao


def validate_password(password):
    return bool(password and len(password) >= 8 and re.search(r"\d", password) and re.search(r"[A-Za-z]", password))


def is_admin(conn, user_id):
    user = user_dao.get_user_by_id(conn, user_id)
    return bool(user and "admin" in user["username"].lower())


def authenticate(conn, username, password):
    user = user_dao.get_user_by_username(conn, username)
    if not user:
        return None

    stored = user["password"]
    if stored.startswith(("pbkdf2:", "scrypt:")) and check_password_hash(stored, password):
        return user

    if stored == password:
        user_dao.update_password_hash(conn, user["user_id"], generate_password_hash(password))
        conn.commit()
        return user

    return None


def register_user(conn, username, phone_email, password):
    if not validate_password(password):
        raise ValueError("Password must be at least 8 characters and include letters and numbers")

    user_id = str(uuid.uuid4())
    password_hash = generate_password_hash(password)
    user_dao.create_user(conn, user_id, username, phone_email, password_hash)
    return user_id


def update_user(conn, user_id, username, phone_email, password, gender):
    if password:
        if not validate_password(password):
            raise ValueError("Password must be at least 8 characters and include letters and numbers")
        user_dao.update_user(conn, user_id, username, phone_email, gender, generate_password_hash(password))
    else:
        user_dao.update_user(conn, user_id, username, phone_email, gender)
