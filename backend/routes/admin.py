import os
import subprocess
from datetime import datetime

import mysql.connector
from flask import flash, redirect, render_template, request, session, url_for

from config import BACKUP_DIR, DB_CONFIG
from dao import user_dao
from services import user_service
from utils.db import get_db_connection


def _require_admin():
    if "user_id" not in session:
        return False
    conn = get_db_connection()
    try:
        return user_service.is_admin(conn, session["user_id"])
    finally:
        conn.close()


def register_admin_routes(app):
    @app.route("/admin")
    def admin_dashboard():
        if not _require_admin():
            return redirect(url_for("login"))

        conn = get_db_connection()
        try:
            users = user_dao.list_users(conn)
        finally:
            conn.close()
        return render_template("admin_dashboard.html", users=users)

    @app.route("/admin/register", methods=["GET", "POST"])
    def register():
        if not _require_admin():
            return redirect(url_for("login"))

        if request.method == "POST":
            conn = get_db_connection()
            try:
                user_service.register_user(
                    conn,
                    request.form["username"],
                    request.form["phone_email"],
                    request.form["password"],
                    request.form.get("role", "user"),
                )
                conn.commit()
                flash("User created successfully", "success")
                return redirect(url_for("admin_dashboard"))
            except ValueError as err:
                flash(str(err), "error")
            except mysql.connector.Error as err:
                conn.rollback()
                flash("Username or email already exists" if err.errno == 1062 else f"Database error: {err}", "error")
            finally:
                conn.close()

        return render_template("register.html")

    @app.route("/admin/delete/<user_id>", methods=["POST"])
    def delete_user(user_id):
        if not _require_admin():
            return redirect(url_for("login"))
        if user_id == session["user_id"]:
            flash("You cannot delete the currently signed-in admin account", "error")
            return redirect(url_for("admin_dashboard"))

        conn = get_db_connection()
        try:
            user_dao.delete_user_graph(conn, user_id)
            conn.commit()
            flash("User deleted successfully", "success")
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f"Database error: {err}", "error")
        finally:
            conn.close()
        return redirect(url_for("admin_dashboard"))

    @app.route("/admin/edit/<user_id>", methods=["GET", "POST"])
    def edit_user(user_id):
        if not _require_admin():
            return redirect(url_for("login"))

        conn = get_db_connection()
        try:
            if request.method == "POST":
                try:
                    user_service.update_user(
                        conn,
                        user_id,
                        request.form["username"],
                        request.form["phone_email"],
                        request.form.get("password"),
                        request.form.get("role", "user"),
                        request.form.get("gender", "U"),
                    )
                    conn.commit()
                    flash("User updated successfully", "success")
                    return redirect(url_for("admin_dashboard"))
                except ValueError as err:
                    flash(str(err), "error")
                except mysql.connector.Error as err:
                    conn.rollback()
                    flash("Username or email already exists" if err.errno == 1062 else f"Database error: {err}", "error")

            user = user_dao.get_user_by_id(conn, user_id)
            return render_template("edit_user.html", user=user)
        finally:
            conn.close()

    @app.route("/admin/user/<user_id>", methods=["GET"])
    def view_user(user_id):
        if not _require_admin():
            return redirect(url_for("login"))

        conn = get_db_connection()
        try:
            user = user_dao.get_user_by_id(conn, user_id)
            videos = user_dao.get_recent_user_videos(conn, user_id) if user else []
            fans_count = user_dao.refresh_fans_count(conn, user_id) if user else 0
            conn.commit()
        finally:
            conn.close()
        return render_template("view_user.html", user=user, videos=videos, fans_count=fans_count)

    @app.route("/admin/backup", methods=["POST"])
    def backup_database():
        if not _require_admin():
            return redirect(url_for("login"))

        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        filename = BACKUP_DIR / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        command = [
            "mysqldump",
            "-h",
            DB_CONFIG["host"],
            "-u",
            DB_CONFIG["user"],
            DB_CONFIG["database"],
        ]
        env = os.environ.copy()
        env["MYSQL_PWD"] = DB_CONFIG["password"]

        try:
            with filename.open("w", encoding="utf-8") as file:
                subprocess.run(command, stdout=file, check=True, env=env)
            flash(f"Backup completed: {filename.name}", "success")
        except Exception as err:
            flash(f"Backup failed: {err}", "error")
        return redirect(url_for("admin_dashboard"))

    @app.route("/admin/restore", methods=["POST"])
    def restore_database():
        if not _require_admin():
            return redirect(url_for("login"))

        sql_file = BACKUP_DIR / os.path.basename(request.form.get("filename", ""))
        command = [
            "mysql",
            "-h",
            DB_CONFIG["host"],
            "-u",
            DB_CONFIG["user"],
            DB_CONFIG["database"],
        ]
        env = os.environ.copy()
        env["MYSQL_PWD"] = DB_CONFIG["password"]

        try:
            with sql_file.open("r", encoding="utf-8") as file:
                subprocess.run(command, stdin=file, check=True, env=env)
            flash("Restore completed", "success")
        except Exception as err:
            flash(f"Restore failed: {err}", "error")
        return redirect(url_for("admin_dashboard"))
