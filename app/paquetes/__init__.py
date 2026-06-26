from flask import Blueprint

paquetes_bp = Blueprint(
    "paquetes",
    __name__,
    url_prefix="/paquetes"
)

from . import routes