from .extensions import db
from flask_login import UserMixin


class Rol(db.Model):
    __tablename__ = "roles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    usuarios = db.relationship(
        "Usuario",
        backref="rol",
        lazy=True
    )

    def __repr__(self):
        return f"<Rol {self.nombre}>"


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    correo = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    rol_id = db.Column(
        db.Integer,
        db.ForeignKey("roles.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Usuario {self.nombre}>"
    

class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    apellido = db.Column(
        db.String(100),
        nullable=False
    )

    telefono = db.Column(
        db.String(20)
    )

    correo = db.Column(
        db.String(100),
        unique=True
    )

    ci = db.Column(
        db.String(20),
        unique=True
    )

    def __repr__(self):
        return f"<Cliente {self.nombre}>"


class Destino(db.Model):
    __tablename__ = "destinos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    departamento = db.Column(
        db.String(100),
        nullable=False
    )

    descripcion = db.Column(
        db.Text
    )

    latitud = db.Column(
        db.Float
    )

    longitud = db.Column(
        db.Float
    )

    imagen = db.Column(
        db.String(255)
    )

    def __repr__(self):
        return f"<Destino {self.nombre}>"


class Paquete(db.Model):
    __tablename__ = "paquetes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    descripcion = db.Column(
        db.Text
    )

    precio = db.Column(
        db.Float,
        nullable=False
    )

    duracion = db.Column(
        db.String(50)
    )

    destino_id = db.Column(
        db.Integer,
        db.ForeignKey("destinos.id"),
        nullable=False
    )

    destino = db.relationship(
        "Destino",
        backref="paquetes"
    )


class Reserva(db.Model):
    __tablename__ = "reservas"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    fecha = db.Column(
        db.Date,
        nullable=False
    )

    estado = db.Column(
        db.String(50),
        nullable=False,
        default="Pendiente"
    )

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id"),
        nullable=False
    )

    paquete_id = db.Column(
        db.Integer,
        db.ForeignKey("paquetes.id"),
        nullable=False
    )

    cliente = db.relationship(
        "Cliente",
        backref="reservas"
    )

    paquete = db.relationship(
        "Paquete",
        backref="reservas"
    )


class Pago(db.Model):
    __tablename__ = "pagos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    monto = db.Column(
        db.Float,
        nullable=False
    )

    metodo_pago = db.Column(
        db.String(50),
        nullable=False
    )

    fecha_pago = db.Column(
        db.Date,
        nullable=False
    )

    estado = db.Column(
        db.String(50),
        nullable=False,
        default="Pendiente"
    )

    reserva_id = db.Column(
        db.Integer,
        db.ForeignKey("reservas.id"),
        nullable=False
    )

    reserva = db.relationship(
        "Reserva",
        backref="pagos"
    )


class Factura(db.Model):
    __tablename__ = "facturas"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    numero = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    fecha = db.Column(
        db.Date,
        nullable=False
    )

    total = db.Column(
        db.Float,
        nullable=False
    )

    pago_id = db.Column(
        db.Integer,
        db.ForeignKey("pagos.id"),
        nullable=False
    )

    pago = db.relationship(
        "Pago",
        backref="facturas"
    )

    def __repr__(self):
        return f"<Factura {self.numero}>"