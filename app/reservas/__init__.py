from flask import Blueprint

reservas_bp = Blueprint(
    "reservas",
    __name__,
    url_prefix="/reservas"
)

from . import routes