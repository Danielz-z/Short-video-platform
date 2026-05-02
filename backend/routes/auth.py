from flask import flash, redirect, render_template, request, session, url_for

from services import user_service
from utils.db import get_db_connection


def register_auth_routes(app):
    @app.route("/")
    def home():
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            conn = get_db_connection()
            try:
                user = user_service.authenticate(conn, username, password)
            finally:
                conn.close()

            if user:
                session["user_id"] = user["user_id"]
                session["username"] = user["username"]

                conn = get_db_connection()
                try:
                    if user_service.is_admin(conn, user["user_id"]):
                        return redirect(url_for("admin_dashboard"))
                finally:
                    conn.close()
                return redirect(url_for("video_dashboard"))

            flash("Invalid username or password", "error")

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))
