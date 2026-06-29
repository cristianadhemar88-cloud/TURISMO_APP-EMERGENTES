from flask import render_template, redirect, request, url_for, abort

from . import pagos_bp
from ..models import Pago, Reserva, Factura
from datetime import datetime
from ..extensions import db
from flask_login import current_user


@pagos_bp.route("/")
def listar_pagos():

    pagos = Pago.query.all()

    return render_template(
        "pagos/listar.html",
        pagos=pagos
    )


@pagos_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo_pago():

    if current_user.rol.nombre == "Cliente":
        abort(403)

    if request.method == "POST":

        pago = Pago(
            reserva_id=int(
                request.form["reserva_id"]
            ),
            monto=float(
                request.form["monto"]
            ),
            metodo_pago=request.form[
                "metodo_pago"
            ],
            fecha_pago=datetime.strptime(
                request.form["fecha_pago"],
                "%Y-%m-%d"
            ).date(),
            estado=request.form[
                "estado"
            ]
        )

        db.session.add(pago)

        db.session.commit()

        return redirect(
            url_for(
                "pagos.listar_pagos"
            )
        )

    reservas = Reserva.query.all()

    return render_template(
        "pagos/nuevo.html",
        reservas=reservas
    )


@pagos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_pago(id):

    if current_user.rol.nombre == "Cliente":
        abort(403)

    pago = Pago.query.get_or_404(id)

    if request.method == "POST":

        pago.reserva_id = int(
            request.form["reserva_id"]
        )

        pago.monto = float(
            request.form["monto"]
        )

        pago.metodo_pago = request.form[
            "metodo_pago"
        ]

        pago.fecha_pago = datetime.strptime(
            request.form["fecha_pago"],
            "%Y-%m-%d"
        ).date()

        pago.estado = request.form[
            "estado"
        ]

        db.session.commit()

        return redirect(
            url_for(
                "pagos.listar_pagos"
            )
        )

    reservas = Reserva.query.all()

    return render_template(
        "pagos/editar.html",
        pago=pago,
        reservas=reservas
    )


@pagos_bp.route("/eliminar/<int:id>")
def eliminar_pago(id):

    if current_user.rol.nombre == "Cliente":
        abort(403)

    pago = Pago.query.get_or_404(id)

    try:

        facturas = Factura.query.filter_by(
            pago_id=pago.id
        ).all()

        for factura in facturas:
            db.session.delete(factura)

        db.session.delete(pago)

        db.session.commit()

    except Exception as e:

        db.session.rollback()
        raise e

    return redirect(
        url_for(
            "pagos.listar_pagos"
        )
    )