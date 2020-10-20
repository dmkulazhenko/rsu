import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Type

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail as FlaskMail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config
from rsu.mail import Mail

bootstrap = Bootstrap()
db = SQLAlchemy()
flask_mail = FlaskMail()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()


def create_app(config_class: Type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)
    db.init_app(app)
    flask_mail.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app, flask_mail)
    migrate.init_app(app, db)

    from rsu.main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from rsu.auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp)

    if app.config["LOG_TO_STDOUT"]:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        logs_dir: Path = app.config["BASE_DIR"] / "logs"
        if not logs_dir.is_dir():
            logs_dir.mkdir()

        file_handler = RotatingFileHandler(
            "logs/rsu.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s "
                "[in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("RSU Startup")

    return app
