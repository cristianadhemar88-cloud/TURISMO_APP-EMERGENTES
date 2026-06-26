from flask import render_template, request, redirect, abort
from flask_login import login_required, current_user

from . import facturas_bp
from app.models import Factura, Pago
from datetime import date

from app.extensions import db
from flask import make_response
from reportlab.pdfgen import canvas
from io import BytesIO
from flask import send_file


@facturas_bp.route("/")
@login_required
def listar():

    facturas = Factura.query.all()

    return render_template(
        "facturas/listar.html",
        facturas=facturas
    )

@facturas_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    
    if current_user.rol.nombre == "Cliente":
        abort(403)

    pagos = Pago.query.all()

    if request.method == "POST":

        ultima_factura = Factura.query.order_by(
            Factura.id.desc()
        ).first()

        if ultima_factura:
            siguiente = ultima_factura.id + 1
        else:
            siguiente = 1

        nuevo_numero = f"FAC-{siguiente:04d}"

        factura = Factura(
            numero=nuevo_numero,
            fecha=date.fromisoformat(
            request.form["fecha"]
        ),
        total=float(
            request.form["total"]
        ),
        pago_id=int(
            request.form["pago_id"]
        )
    )

        db.session.add(factura)

        db.session.commit()

        return redirect("/facturas")

    return render_template(
        "facturas/nuevo.html",
        pagos=pagos
    )


@facturas_bp.route(
    "/editar/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def editar(id):
    
    if current_user.rol.nombre == "Cliente":
        abort(403)

    factura = Factura.query.get_or_404(id)

    pagos = Pago.query.all()

    if request.method == "POST":

        factura.numero = request.form["numero"]

        factura.fecha = date.fromisoformat(
            request.form["fecha"]
        )

        factura.total = float(
            request.form["total"]
        )

        factura.pago_id = int(
            request.form["pago_id"]
        )

        db.session.commit()

        return redirect("/facturas")

    return render_template(
        "facturas/editar.html",
        factura=factura,
        pagos=pagos
    )


@facturas_bp.route("/eliminar/<int:id>")
@login_required
def eliminar(id):
    
    if current_user.rol.nombre == "Cliente":
        abort(403)

    factura = Factura.query.get_or_404(id)

    db.session.delete(factura)

    db.session.commit()

    return redirect("/facturas")

@facturas_bp.route("/pdf/<int:id>")
@login_required
def generar_pdf(id):

    factura = Factura.query.get_or_404(id)

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setTitle(
        f"Factura_{factura.numero}"
    )

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawString(
        200,
        800,
        "FACTURA"
    )

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawString(
        50,
        740,
        f"Número: {factura.numero}"
    )

    pdf.drawString(
        50,
        720,
        f"Fecha: {factura.fecha}"
    )

    cliente = factura.pago.reserva.cliente

    pdf.drawString(
        50,
        680,
        f"Cliente: {cliente.nombre} {cliente.apellido}"
    )

    pdf.drawString(
        50,
        660,
        f"Monto: Bs. {factura.total}"
    )

    pdf.drawString(
        50,
        640,
        f"Método de pago: {factura.pago.metodo_pago}"
    )

    pdf.line(
        50,
        620,
        550,
        620
    )

    pdf.drawString(
        50,
        590,
        "Gracias por su compra."
    )

    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=False
    )