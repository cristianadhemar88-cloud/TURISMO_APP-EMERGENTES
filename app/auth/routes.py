from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from werkzeug.security import check_password_hash

from . import auth_bp
from ..models import Usuario


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        correo = request.form.get("correo")
        password = request.form.get("password")

        usuario = Usuario.query.filter_by(
            correo=correo
        ).first()

        if usuario and check_password_hash(
            usuario.password,
            password
        ):

            login_user(usuario)

            return redirect(url_for("dashboard"))

        flash("Correo o contraseña incorrectos")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():

    logout_user()

    return redirect(url_for("auth.login"))