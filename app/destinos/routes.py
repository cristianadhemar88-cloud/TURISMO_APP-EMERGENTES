from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user

from ..extensions import db
from . import destinos_bp
from ..models import (
    Destino,
    Paquete,
    Reserva,
    Pago,
    Factura
)


@destinos_bp.route("/")
@login_required
def listar_destinos():

    destinos = Destino.query.all()

    return render_template(
        "destinos/listar.html",
        destinos=destinos
    )


@destinos_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_destino():

    if current_user.rol.nombre == "Cliente":
        abort(403)

    if request.method == "POST":

        destino = Destino(
            nombre=request.form["nombre"],
            departamento=request.form["departamento"],
            descripcion=request.form["descripcion"],
            latitud=float(request.form["latitud"]),
            longitud=float(request.form["longitud"])
        )

        db.session.add(destino)
        db.session.commit()

        return redirect(
            url_for("destinos.listar_destinos")
        )

    return render_template(
        "destinos/nuevo.html"
    )


@destinos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_destino(id):

    if current_user.rol.nombre == "Cliente":
        abort(403)

    destino = Destino.query.get_or_404(id)

    if request.method == "POST":

        destino.nombre = request.form["nombre"]
        destino.departamento = request.form["departamento"]
        destino.descripcion = request.form["descripcion"]
        destino.latitud = float(request.form["latitud"])
        destino.longitud = float(request.form["longitud"])

        db.session.commit()

        return redirect(
            url_for("destinos.listar_destinos")
        )

    return render_template(
        "destinos/editar.html",
        destino=destino
    )


@destinos_bp.route("/eliminar/<int:id>")
@login_required
def eliminar_destino(id):

    if current_user.rol.nombre == "Cliente":
        abort(403)

    destino = Destino.query.get_or_404(id)

    try:

        paquetes = Paquete.query.filter_by(
            destino_id=destino.id
        ).all()

        for paquete in paquetes:

            reservas = Reserva.query.filter_by(
                paquete_id=paquete.id
            ).all()

            for reserva in reservas:

                pagos = Pago.query.filter_by(
                    reserva_id=reserva.id
                ).all()

                for pago in pagos:

                    facturas = Factura.query.filter_by(
                        pago_id=pago.id
                    ).all()

                    for factura in facturas:
                        db.session.delete(factura)

                    db.session.delete(pago)

                db.session.delete(reserva)

            db.session.delete(paquete)

        db.session.delete(destino)

        db.session.commit()

    except Exception as e:

        db.session.rollback()
        raise e

    return redirect(
        url_for("destinos.listar_destinos")
    )