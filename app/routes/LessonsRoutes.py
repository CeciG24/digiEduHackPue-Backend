from flask import Blueprint
from flask import request, jsonify
from app.models.leccion import Leccion
from app import db

#Creamos el blueprint
lessons_bp = Blueprint('lessons', __name__, url_prefix='/lessons')

#CRUD lecciones
@lessons_bp.route("/", methods=['GET'])
def get_lecciones():
    try:
        lecciones = Leccion.query.all()
        
        # Mejor estructuración de los datos
        lecciones_data = [
            {
                "id": leccion.id_leccion,
                "id_modulo": leccion.id_modulo,
                "titulo": leccion.titulo,
                "contenido": leccion.contenido,
                "tipo": leccion.tipo,
                "orden": leccion.orden
            }
            for leccion in lecciones
        ]
        
        return jsonify({
            "success": True,
            "data": lecciones_data,
            "count": len(lecciones_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@lessons_bp.route("/lecciones", methods=["POST"])
def post_leccion():
    try:
        data = request.get_json()
        # Validar datos obligatorios
        if not data or not all(k in data for k in (
                "id_modulo",
                "titulo",
                "contenido",
                "tipo",
                "orden")):
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        TIPOS_PERMITIDOS=['teórica', 'práctica', 'quiz']
        if data["tipo"] not in TIPOS_PERMITIDOS:
            return jsonify({"error": f"Tipo debe ser uno de: {TIPOS_PERMITIDOS}"}), 400
        
        nueva_leccion = Leccion(
            id_modulo=data["id_modulo"],
            titulo=data["titulo"],
            contenido=data["contenido"],
            tipo=data["tipo"],
            orden=data["orden"],
        )

        db.session.add(nueva_leccion)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "titulo": nueva_leccion.titulo,
            "message": "leccion creada exitosamente",
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# Obtener lecciones por módulo
@lessons_bp.route("/modulo/<int:id_modulo>", methods=['GET'])
def get_lecciones_por_modulo(id_modulo):
    try:
        lecciones = Leccion.query.filter_by(id_modulo=id_modulo).all()

        if not lecciones:
            return jsonify({
                "success": False,
                "error": "No se encontraron lecciones para este módulo"
            }), 404

        lecciones_data = [
            {
                "id_leccion": leccion.id_leccion,
                "id_modulo": leccion.id_modulo,
                "titulo": leccion.titulo,
                "contenido": leccion.contenido,
                "tipo": leccion.tipo,
                "orden": leccion.orden
            }
            for leccion in lecciones
        ]

        return jsonify({
            "success": True,
            "data": lecciones_data,
            "count": len(lecciones_data)
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# Obtener una lección por su ID
@lessons_bp.route("/<int:id_leccion>", methods=['GET'])
def get_leccion_by_id(id_leccion):
    try:
        leccion = Leccion.query.get(id_leccion)
        if not leccion:
            return jsonify({
                "success": False,
                "error": "Lección no encontrada"
            }), 404

        leccion_data = {
            "id_leccion": leccion.id_leccion,
            "id_modulo": leccion.id_modulo,
            "titulo": leccion.titulo,
            "contenido": leccion.contenido,
            "tipo": leccion.tipo,
            "orden": leccion.orden
        }

        return jsonify({
            "success": True,
            "data": leccion_data
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500



@lessons_bp.route("/lecciones/<int:id>", methods=["PUT"])
def update_leccion(id):
    try:
        leccion = Leccion.query.get(id)
        if not leccion:
            return jsonify({"error": "leccion no encontrada"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

        # Actualizar campos si se proporcionan
        if "id_modulo" in data:
            if not data["id_modulo"].strip():
                return jsonify({"error": "El id_modulo no puede estar vacío"}), 400
            leccion.id_modulo = data["id_modulo"]

        if "titulo" in data:
            if not data["titulo"].strip():
                return jsonify({"error": "El titulo no puede estar vacío"}), 400
            leccion.titulo = data["titulo"]

        if "contenido" in data:
            leccion.contenido = data["contenido"]

        if "tipo" in data:
            leccion.tipo = data["tipo"]

        if "orden" in data:
            leccion.orden = data["orden"]

        db.session.commit()
        return jsonify({
            "message": "leccion actualizada con éxito",
            "id_leccion": leccion.id_leccion
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al actualizar leccion: {str(e)}"}), 500
    
@lessons_bp.route("/lecciones/<int:id>", methods=["DELETE"])
def delete_leccion(id):
    try:
        leccion = Leccion.query.get(id)
        if not leccion:
            return jsonify({"error": "leccion no encontrada"}), 404

        db.session.delete(leccion)
        db.session.commit()
        return jsonify({"message": "leccion eliminada con éxito"}), 202
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar leccion: {str(e)}"}), 500