from flask import Flask

from config import BASE_DIR, SECRET_KEY
from routes.admin import register_admin_routes
from routes.auth import register_auth_routes
from routes.video import register_video_routes


def create_app():
    app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))
    app.secret_key = SECRET_KEY

    register_auth_routes(app)
    register_admin_routes(app)
    register_video_routes(app)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
