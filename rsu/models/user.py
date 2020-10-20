from time import time
from typing import Optional, Union

import jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from rsu import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password: str) -> None:
        """Set new password for user."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check user password.

        :returns: True if password matches else False
        """
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in: int = 600) -> str:
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token: str):
        try:
            user_id = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )["reset_password"]
        except Exception as exc:
            current_app.logger.warning(
                "Error during reset token decoding: %s", exc
            )
            return
        return User.query.get(user_id)

    def __repr__(self):
        return "<User {}>".format(self.email)


@login_manager.user_loader
def _load_user(uid: Union[str, int]) -> Optional[User]:
    return User.query.get(int(uid))
