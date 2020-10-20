from flask import (
    redirect,
    url_for,
    flash,
    request,
    render_template,
    current_app,
)
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse

from rsu.auth import bp
from rsu.auth.forms import (
    LoginForm,
    RegistrationForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
)
from rsu.auth.mail import send_password_reset_email
from rsu.models import User
from rsu.utils import FlashMessage, anonymous_user


@bp.route("/register", methods=["GET", "POST"])
@anonymous_user("main.index")
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        user.commit_to_db()

        flash(
            FlashMessage(
                FlashMessage.Color.GREEN,
                "Congratulations, you are now a registered user!",
            )
        )
        current_app.logger.info("Registered new user: %s", user)

        return redirect(url_for("auth.login"))

    return render_template(
        "auth/registration.html", title="Register", form=form
    )


@bp.route("/login", methods=["GET", "POST"])
@anonymous_user("main.index")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash(
                FlashMessage(
                    FlashMessage.Color.RED, "Invalid username or password"
                )
            )
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember_me.data)
        flash(FlashMessage(FlashMessage.Color.GREEN, "Successfully logged in"))
        current_app.logger.info("User %s logged in", user)

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)

    return render_template("auth/login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    current_app.logger.info("User %s logged out", current_user)
    logout_user()
    flash(FlashMessage(FlashMessage.Color.BLUE, "Successfully logged out"))
    return redirect(url_for("auth.login"))


@bp.route("/reset_password", methods=["GET", "POST"])
@anonymous_user("main.index")
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)

        flash(
            FlashMessage(
                FlashMessage.Color.BLUE,
                "Check your email for the instructions to reset your password",
            )
        )
        current_app.logger.info("User %s requested password reset", user)

        return redirect(url_for("auth.login"))
    return render_template(
        "auth/reset_password_request.html", title="Reset Password", form=form
    )


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
@anonymous_user("main.index")
def reset_password(token):
    user: User = User.verify_reset_password_token(token)
    if not user:
        flash(
            FlashMessage(
                FlashMessage.Color.RED,
                "Your password reset link is broken or expired",
            )
        )
        return redirect(url_for("main.index"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.commit_to_db()

        flash(
            FlashMessage(
                FlashMessage.Color.GREEN, "Your password has been reset."
            )
        )
        current_app.logger.info("User %s resetted password", user)

        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form)
