import os
from pathlib import Path


class Config:
    # Dirs
    BASE_DIR = Path(__file__).parent.absolute()

    # Logs
    LOG_TO_STDOUT = False

    # Mail
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT"))
    MAIL_USE_TLS = bool(int(os.environ.get("MAIL_USE_TLS")))
    MAIL_USE_SSL = bool(int(os.environ.get("MAIL_USE_SSL")))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DIR = BASE_DIR / "rsu" / "templates" / "mail"

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "RSU_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(BASE_DIR, "rsu.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Keys
    SECRET_KEY = os.environ.get("SECRET_KEY")
