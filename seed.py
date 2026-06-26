from app import create_app
from app.extensions import db
from app.models import Rol, Usuario
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():

    # ==========================
    # ROLES
    # ==========================

    admin_rol = Rol.query.filter_by(nombre="Administrador").first()

    if not admin_rol:
        admin_rol = Rol(nombre="Administrador")
        db.session.add(admin_rol)

    empleado_rol = Rol.query.filter_by(nombre="Empleado").first()

    if not empleado_rol:
        empleado_rol = Rol(nombre="Empleado")
        db.session.add(empleado_rol)

    cliente_rol = Rol.query.filter_by(nombre="Cliente").first()

    if not cliente_rol:
        cliente_rol = Rol(nombre="Cliente")
        db.session.add(cliente_rol)

    db.session.commit()

    # ==========================
    # ADMINISTRADOR
    # ==========================

    admin = Usuario.query.filter_by(
        correo="admin@turismo.com"
    ).first()

    if not admin:

        admin = Usuario(
            nombre="Administrador",
            correo="admin@turismo.com",
            password=generate_password_hash("123456"),
            rol_id=admin_rol.id
        )

        db.session.add(admin)

    # ==========================
    # EMPLEADO
    # ==========================

    empleado = Usuario.query.filter_by(
        correo="empleado@turismo.com"
    ).first()

    if not empleado:

        empleado = Usuario(
            nombre="Empleado",
            correo="empleado@turismo.com",
            password=generate_password_hash("123456"),
            rol_id=empleado_rol.id
        )

        db.session.add(empleado)

    # ==========================
    # CLIENTE
    # ==========================

    cliente = Usuario.query.filter_by(
        correo="cliente@turismo.com"
    ).first()

    if not cliente:

        cliente = Usuario(
            nombre="Cliente",
            correo="cliente@turismo.com",
            password=generate_password_hash("123456"),
            rol_id=cliente_rol.id
        )

        db.session.add(cliente)

    db.session.commit()

    print("Datos iniciales creados correctamente.")