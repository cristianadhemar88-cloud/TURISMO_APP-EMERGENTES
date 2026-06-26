from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from . import clientes_bp
from ..models import Cliente
from ..extensions import db
from flask_login import current_user, login_required

@clientes_bp.route("/")
def listar_clientes():

    clientes = Cliente.query.all()

    return render_template(
        "clientes/listar.html",
        clientes=clientes
    )

@clientes_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo_cliente():

    if request.method == "POST":

        cliente = Cliente(
            nombre=request.form["nombre"],
            apellido=request.form["apellido"],
            telefono=request.form["telefono"],
            correo=request.form["correo"],
            ci=request.form["ci"]
        )

        db.session.add(cliente)

        db.session.commit()

        if current_user.rol.nombre == "Cliente":

            return redirect(
                url_for("reservas.nueva_reserva")
            )

        return redirect(
            url_for("clientes.listar_clientes")
        )

    return render_template(
        "clientes/nuevo.html"
    )


@clientes_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):

    cliente = Cliente.query.get_or_404(id)

    if request.method == "POST":

        cliente.nombre = request.form["nombre"]
        cliente.apellido = request.form["apellido"]
        cliente.telefono = request.form["telefono"]
        cliente.correo = request.form["correo"]
        cliente.ci = request.form["ci"]

        db.session.commit()

        return redirect(
            url_for("clientes.listar_clientes")
        )

    return render_template(
        "clientes/editar.html",
        cliente=cliente
    )


@clientes_bp.route("/eliminar/<int:id>")
def eliminar_cliente(id):

    cliente = Cliente.query.get_or_404(id)

    db.session.delete(cliente)

    db.session.commit()

    return redirect(
        url_for("clientes.listar_clientes")
    )