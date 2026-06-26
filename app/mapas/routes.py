from flask import render_template

from . import mapas_bp
from ..models import Destino


@mapas_bp.route("/")
def mapa():

    destinos = Destino.query.all()

    return render_template(
        "mapas/mapa.html",
        destinos=destinos
    )