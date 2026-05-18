import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "short_video_platform"),
    "charset": "utf8mb4",
}

DB_POOL_NAME = os.getenv("DB_POOL_NAME", "short_video_pool")
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
BACKUP_DIR = Path(os.getenv("BACKUP_DIR", PROJECT_ROOT / "database" / "backup"))
