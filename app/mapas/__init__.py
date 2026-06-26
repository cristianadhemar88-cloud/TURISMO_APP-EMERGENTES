from flask import Blueprint

mapas_bp = Blueprint(
    "mapas",
    __name__,
    url_prefix="/mapas"
)

from . import routes