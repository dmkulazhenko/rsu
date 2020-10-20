from threading import Thread
from typing import List, Union

from flask_mail import Message


class Mail:
    def __init__(self):
        self.flask_app = None
        self.flask_mail = None

    def init_app(self, flask_app, flask_mail):
        self.flask_app = flask_app
        self.flask_mail = flask_mail

    def _send_email_task(self, msg: Message) -> None:
        with self.flask_app.app_context():
            self.flask_mail.send(msg)

    def _send_email(
        self,
        subject: str,
        sender: str,
        recipients: List[str],
        text_body: str,
        html_body: str,
    ) -> None:
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        Thread(target=Mail._send_email_task, args=(self, msg)).start()

    def send_email(
        self,
        subject: str,
        recipients: Union[List[str], str],
        text_body: str,
        html_body: str,
    ) -> None:
        self._send_email(
            subject,
            self.flask_app.config["MAIL_USERNAME"],
            recipients if isinstance(recipients, list) else [recipients],
            text_body,
            html_body,
        )
