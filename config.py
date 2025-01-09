import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev"
    SITE_NAME = "Cursor Beauty"
    SITE_URL = "https://cursor.beauty"
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    MONGODB_SETTINGS = {"host": os.environ.get("MONGODB_URI")}
    MONGODB_DB = "cwbeauty"  # 修改为与 MongoDB URI 中相同的数据库名
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "dev"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    LANGUAGES = ["en", "zh"]
    DEFAULT_LANGUAGE = "en"
