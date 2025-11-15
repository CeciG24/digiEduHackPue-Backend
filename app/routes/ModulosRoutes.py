from flask import Blueprint
from flask import request, jsonify
from app.models.modulo import Modulo
from app import db
from datetime import datetime

#Creamos el blueprint
modulo_bp = Blueprint('modulo', __name__, url_prefix='/modulos')

#CRUD modulos
@modulo_bp.route("/", methods=['GET'])
def get_modulos():
    try:
        modulos = Modulo.query.all()
        
        # Mejor estructuración de los datos
        modulos_data = [
            {
                "id": modulo.id_modulo,
                "id_ruta": modulo.id_modulo,
                "titulo": modulo.titulo,
                "descripcion": modulo.descripcion,
                "orden": modulo.orden
            }
            for modulo in modulos
        ]
        
        return jsonify({
            "success": True,
            "data": modulos_data,
            "count": len(modulos_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# CRUD módulos - obtener módulos por ruta
@modulo_bp.route("/ruta/<int:id_ruta>", methods=['GET'])
def get_modulos_por_ruta(id_ruta):
    try:
        # Filtramos módulos por id_ruta
        modulos = Modulo.query.filter_by(id_ruta=id_ruta).all()

        # Estructuración de los datos
        modulos_data = [
            {
                "id_modulo": modulo.id_modulo,
                "id_ruta": modulo.id_ruta,
                "titulo": modulo.titulo,
                "descripcion": modulo.descripcion,
                "orden": modulo.orden
            }
            for modulo in modulos
        ]

        return jsonify({
            "success": True,
            "data": modulos_data,
            "count": len(modulos_data)
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@modulo_bp.route("/post-modulo", methods=["POST"])
def post_modulo():
    try:
        data = request.get_json()
        # Validar datos obligatorios
        if not data or not all(k in data for k in (
                "id_ruta",
                "titulo",
                "descripcion",
                "orden")):
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        nuevo_modulo = Modulo(
            id_ruta=data["id_ruta"],
            titulo=data["titulo"],
            descripcion=data["descripcion"],
            orden=data["orden"],
        )

        db.session.add(nuevo_modulo)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "titulo": nuevo_modulo.titulo,
            "message": "Modulo creado exitosamente",
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
@modulo_bp.route("/<int:id>", methods=["PUT"])
def update_modulo(id):
    try:
        modulo = modulo.query.get(id)
        if not modulo:
            return jsonify({"error": "modulo no encontrada"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

        # Actualizar campos si se proporcionan
        if "id_ruta" in data:
            if not data["id_ruta"].strip():
                return jsonify({"error": "El id_ruta no puede estar vacío"}), 400
            modulo.id_ruta = data["id_ruta"]

        if "titulo" in data:
            if not data["titulo"].strip():
                return jsonify({"error": "El titulo no puede estar vacío"}), 400
            modulo.titulo = data["titulo"]

        if "descripcion" in data:
            modulo.descripcion = data["descripcion"]

        if "orden" in data:
            modulo.orden = data["orden"]

        db.session.commit()
        return jsonify({
            "message": "modulo actualizado con éxito",
            "id_modulo": modulo.id_modulo
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al actualizar modulo: {str(e)}"}), 500
    
@modulo_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_modulo(id):
    try:
        modulo = Modulo.query.get(id)
        if not modulo:
            return jsonify({"error": "modulo no encontrado"}), 404

        db.session.delete(modulo)
        db.session.commit()
        return jsonify({"message": "modulo eliminado con éxito"}), 202
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar modulo: {str(e)}"}), 500