from flask import render_template, request, redirect, url_for, abort

from . import reservas_bp
from datetime import datetime
from flask_login import login_required, current_user

from ..extensions import db
from ..models import (
    Reserva,
    Cliente,
    Paquete,
    Pago,
    Factura
)


@reservas_bp.route("/")
def listar_reservas():

    reservas = Reserva.query.all()

    return render_template(
        "reservas/listar.html",
        reservas=reservas
    )


@reservas_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nueva_reserva():

    if request.method == "POST":

        reserva = Reserva(
            cliente_id=int(
                request.form["cliente_id"]
            ),
            paquete_id=int(
                request.form["paquete_id"]
            ),
            fecha=datetime.strptime(
                request.form["fecha"],
                "%Y-%m-%d"
            ).date(),
            estado=request.form["estado"]
        )

        db.session.add(reserva)

        db.session.commit()

        return redirect(
            url_for(
                "reservas.listar_reservas"
            )
        )

    clientes = Cliente.query.all()

    paquetes = Paquete.query.all()

    return render_template(
        "reservas/nuevo.html",
        clientes=clientes,
        paquetes=paquetes
    )


@reservas_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_reserva(id):

    if current_user.rol.nombre == "Cliente":
        abort(403)

    reserva = Reserva.query.get_or_404(id)

    if request.method == "POST":

        reserva.cliente_id = int(
            request.form["cliente_id"]
        )

        reserva.paquete_id = int(
            request.form["paquete_id"]
        )

        reserva.fecha = datetime.strptime(
            request.form["fecha"],
            "%Y-%m-%d"
        ).date()

        reserva.estado = request.form["estado"]

        db.session.commit()

        return redirect(
            url_for(
                "reservas.listar_reservas"
            )
        )

    clientes = Cliente.query.all()

    paquetes = Paquete.query.all()

    return render_template(
        "reservas/editar.html",
        reserva=reserva,
        clientes=clientes,
        paquetes=paquetes
    )


@reservas_bp.route("/eliminar/<int:id>")
def eliminar_reserva(id):

    if current_user.rol.nombre == "Cliente":
        abort(403)

    reserva = Reserva.query.get_or_404(id)

    try:

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

        db.session.commit()

    except Exception as e:

        db.session.rollback()
        raise e

    return redirect(
        url_for(
            "reservas.listar_reservas"
        )
    )