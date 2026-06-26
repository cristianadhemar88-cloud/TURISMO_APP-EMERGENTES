from flask import Blueprint

destinos_bp = Blueprint(
    "destinos",
    __name__,
    url_prefix="/destinos"
)

from . import routes