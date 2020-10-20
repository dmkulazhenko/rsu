from flask import render_template

from rsu import mail
from rsu.models import User


def send_password_reset_email(user: User) -> None:
    token = user.get_reset_password_token()
    mail.send_email(
        subject="[RSU Shipment] Reset Your Password",
        recipients=user.email,
        text_body=render_template(
            "auth/email/reset_password_request.txt", user=user, token=token
        ),
        html_body=render_template(
            "auth/email/reset_password_request.html", user=user, token=token
        ),
    )
