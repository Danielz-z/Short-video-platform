import mysql.connector
from math import ceil
from flask import flash, redirect, render_template, request, session, url_for

from dao import user_dao, video_dao
from services import video_service
from utils.db import get_db_connection

PAGE_SIZE = 10


def _require_login():
    return "user_id" in session


def register_video_routes(app):
    @app.route("/videos", methods=["GET", "POST"])
    def video_dashboard():
        if not _require_login():
            return redirect(url_for("login"))

        author_id = request.values.get("author_id") or session["user_id"]
        page = max(request.args.get("page", 1, type=int) or 1, 1)

        conn = get_db_connection()
        try:
            user = user_dao.get_user_by_id(conn, session["user_id"])
            total_videos = video_dao.count_user_videos(conn, session["user_id"])
            total_pages = max(ceil(total_videos / PAGE_SIZE), 1)
            page = min(page, total_pages)
            videos = video_dao.list_user_videos(conn, session["user_id"], PAGE_SIZE, (page - 1) * PAGE_SIZE)
            popular_videos = video_dao.get_hot_videos_by_author(conn, author_id)
        except mysql.connector.Error as err:
            flash(f"Query failed: {err}", "error")
            user, videos, popular_videos = {"username": session.get("username", "")}, [], []
            total_videos, total_pages = 0, 1
        finally:
            conn.close()

        return render_template(
            "video_dashboard.html",
            username=user["username"],
            user_id=session["user_id"],
            videos=videos,
            popular_videos=popular_videos,
            searched_author_id=author_id,
            page=page,
            total_pages=total_pages,
            total_videos=total_videos,
        )

    @app.route("/upload_video", methods=["GET", "POST"])
    def upload_video():
        if not _require_login():
            return redirect(url_for("login"))

        if request.method == "POST":
            conn = get_db_connection()
            try:
                video_service.upload_video(
                    conn,
                    request.form["title"],
                    request.form["url"],
                    session["user_id"],
                    request.form["field_id"],
                )
                conn.commit()
                flash("Video uploaded successfully", "success")
                return redirect(url_for("video_dashboard"))
            except mysql.connector.Error as err:
                conn.rollback()
                flash(f"Upload failed: {err}", "error")
            finally:
                conn.close()

        return render_template("upload_video.html")

    @app.route("/update_video", methods=["POST"])
    def update_video():
        if not _require_login():
            return redirect(url_for("login"))

        conn = get_db_connection()
        try:
            video_service.update_video(
                conn,
                request.form.get("video_id"),
                request.form.get("new_title"),
                session["user_id"],
            )
            conn.commit()
            flash("Video title updated successfully", "success")
        except PermissionError as err:
            flash(str(err), "error")
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f"Update failed: {err}", "error")
        finally:
            conn.close()
        return redirect(url_for("video_dashboard"))

    @app.route("/delete_video", methods=["POST"])
    def delete_video():
        if not _require_login():
            return redirect(url_for("login"))

        conn = get_db_connection()
        try:
            video_service.delete_video(conn, request.form.get("video_id"), session["user_id"])
            conn.commit()
            flash("Video deleted successfully", "success")
        except PermissionError as err:
            flash(str(err), "error")
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f"Delete failed: {err}", "error")
        finally:
            conn.close()
        return redirect(url_for("video_dashboard"))

    @app.route("/like_video", methods=["POST"])
    def like_video():
        if not _require_login():
            return redirect(url_for("login"))

        conn = get_db_connection()
        try:
            video_dao.like_video(conn, session["user_id"], request.form.get("video_id"))
            conn.commit()
            flash("Video liked successfully", "success")
        except mysql.connector.IntegrityError:
            conn.rollback()
            flash("You have already liked this video", "info")
        except mysql.connector.Error as err:
            conn.rollback()
            flash(f"Like failed: {err}", "error")
        finally:
            conn.close()
        return redirect(url_for("video_dashboard"))

    @app.route("/video/<video_id>")
    def view_video(video_id):
        if not _require_login():
            return redirect(url_for("login"))

        conn = get_db_connection()
        try:
            video = video_dao.get_video_detail(conn, video_id)
        finally:
            conn.close()

        if not video:
            flash("Video not found", "error")
            return redirect(url_for("video_dashboard"))
        return render_template("view_video.html", video=video)
