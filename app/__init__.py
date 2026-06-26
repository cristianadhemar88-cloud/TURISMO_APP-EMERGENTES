from flask import Flask, render_template, redirect

from .extensions import db, migrate, login_manager

from flask_login import login_required, current_user

from .destinos import destinos_bp
from .mapas import mapas_bp
from .paquetes import paquetes_bp
from .reservas import reservas_bp
from .pagos import pagos_bp
from .facturas import facturas_bp
from .models import (
    Usuario,
    Cliente,
    Destino,
    Paquete,
    Reserva,
    Pago,
    Factura
)

from sqlalchemy import func


def create_app():

    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)

    migrate.init_app(app, db)

    login_manager.init_app(app)

    from . import models

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    from .auth import auth_bp
    from .clientes import clientes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(destinos_bp)
    app.register_blueprint(mapas_bp)
    app.register_blueprint(paquetes_bp)
    app.register_blueprint(reservas_bp)
    app.register_blueprint(pagos_bp)
    app.register_blueprint(facturas_bp)

    @app.route("/")
    def home():

        if current_user.is_authenticated:

            if current_user.rol.nombre == "Cliente":

                destinos = Destino.query.limit(6).all()

                paquetes = Paquete.query.limit(6).all()

                return render_template(
                    "cliente_inicio.html",
                    destinos=destinos,
                    paquetes=paquetes
                )   

        return render_template("index.html")

    @app.route("/dashboard")
    @login_required
    def dashboard():
        
        if current_user.rol.nombre == "Cliente":
            return redirect("/")

        total_clientes = Cliente.query.count()

        total_destinos = Destino.query.count()

        total_paquetes = Paquete.query.count()

        total_reservas = Reserva.query.count()

        total_pagos = Pago.query.count()
        
        total_facturas = Factura.query.count()

        total_ingresos = db.session.query(
            func.sum(Pago.monto)
        ).scalar() or 0

        ultimas_reservas = Reserva.query \
            .order_by(Reserva.id.desc()) \
            .limit(5) \
            .all()

        destinos = Destino.query.all()

        return render_template(
            "dashboard.html",
            total_clientes=total_clientes,
            total_destinos=total_destinos,
            total_paquetes=total_paquetes,
            total_reservas=total_reservas,
            total_pagos=total_pagos,
            total_facturas=total_facturas,
            total_ingresos=total_ingresos,
            ultimas_reservas=ultimas_reservas,
            destinos=destinos
        )
        

    return app