from flask import render_template, request, redirect, url_for, abort

from . import paquetes_bp
from ..models import Paquete, Destino
from ..extensions import db
from flask_login import login_required, current_user


@paquetes_bp.route("/")
def listar_paquetes():

    paquetes = Paquete.query.all()

    return render_template(
        "paquetes/listar.html",
        paquetes=paquetes
    )

@paquetes_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo_paquete():
    
    if current_user.rol.nombre == "Cliente":
        abort(403)

    if request.method == "POST":

        paquete = Paquete(
            nombre=request.form["nombre"],
            descripcion=request.form["descripcion"],
            precio=float(request.form["precio"]),
            duracion=request.form["duracion"],
            destino_id=int(request.form["destino_id"])
        )

        db.session.add(paquete)
        db.session.commit()

        return redirect(
            url_for("paquetes.listar_paquetes")
        )

    destinos = Destino.query.all()

    return render_template(
        "paquetes/nuevo.html",
        destinos=destinos
    )


@paquetes_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_paquete(id):
    
    if current_user.rol.nombre == "Cliente":
        abort(403)

    paquete = Paquete.query.get_or_404(id)

    if request.method == "POST":

        paquete.nombre = request.form["nombre"]
        paquete.descripcion = request.form["descripcion"]
        paquete.precio = float(request.form["precio"])
        paquete.duracion = request.form["duracion"]
        paquete.destino_id = int(request.form["destino_id"])

        db.session.commit()

        return redirect(
            url_for("paquetes.listar_paquetes")
        )

    destinos = Destino.query.all()

    return render_template(
        "paquetes/editar.html",
        paquete=paquete,
        destinos=destinos
    )
    


@paquetes_bp.route("/eliminar/<int:id>")
def eliminar_paquete(id):
    
    if current_user.rol.nombre == "Cliente":
        abort(403)

    paquete = Paquete.query.get_or_404(id)

    db.session.delete(paquete)

    db.session.commit()

    return redirect(
        url_for("paquetes.listar_paquetes")
    )