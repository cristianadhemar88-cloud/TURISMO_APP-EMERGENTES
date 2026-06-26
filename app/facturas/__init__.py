from flask import Blueprint

facturas_bp = Blueprint(
    "facturas",
    __name__,
    url_prefix="/facturas"
)

from . import routes