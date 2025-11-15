from app import db
from datetime import datetime
import enum

class RolEnum(enum.Enum):
    ALUMNO="alumno"
    MAESTRO="maestro"

class User(db.Model):
    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña_hash = db.Column(db.String(255), nullable=False)
    rol =db.Column(db.Enum(RolEnum, name="rol_enum"),nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Usuario {self.nombre} ({self.email})>"