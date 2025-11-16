from flask import Blueprint
from flask import request, jsonify
from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User, RolEnum
import bcrypt
import jwt
import datetime

users_bp = Blueprint('auth', __name__)
SECRET_KEY = "CAMBIA_ESTE_SECRETO"  # Usa variable de entorno real

# -------------------------
# REGISTRO
# -------------------------
@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    nombre = data.get("nombre")
    email = data.get("email")
    contraseña = data.get("contraseña")
    rol = data.get("rol")

    if not all([nombre, email, contraseña, rol]):
        return jsonify({"error": "Faltan campos"}), 400

    # Verificar que el rol sea válido
    try:
        rol_enum = RolEnum(rol)
    except ValueError:
        return jsonify({"error": "Rol inválido"}), 400

    # Verificar si el email ya existe
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "El correo ya está registrado"}), 400

    # Hash de contraseña
    hashed = bcrypt.hashpw(contraseña.encode("utf-8"), bcrypt.gensalt())

    # Crear usuario
    nuevo_usuario = User(
        nombre=nombre,
        email=email,
        contraseña_hash=hashed.decode("utf-8"),
        rol=rol_enum
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"message": "Usuario registrado exitosamente"}), 201


# -------------------------
# LOGIN
# -------------------------
@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    contraseña = data.get("contraseña")

    if not all([email, contraseña]):
        return jsonify({"error": "Faltan campos"}), 400

    usuario = User.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Verificar contraseña
    if not bcrypt.checkpw(contraseña.encode("utf-8"), usuario.contraseña_hash.encode("utf-8")):
        return jsonify({"error": "Contraseña incorrecta"}), 401

    # Crear JWT válido por 24 horas
    token = jwt.encode(
        {
            "id_usuario": usuario.id_usuario,
            "email": usuario.email,
            "rol": usuario.rol.value,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"token": token}), 200
