from flask import Blueprint
from flask import request, jsonify
from app.models.rutaAprendizaje import RutaAprendizaje
from app import db
from datetime import datetime

#Creamos el blueprint
rutas_bp = Blueprint('ruta', __name__, url_prefix='/rutas')

@rutas_bp.route("/", methods=['GET'])
def get_rutas():
    try:
        rutas = RutaAprendizaje.query.all()
        
        # Mejor estructuración de los datos
        rutas_data = [
            {
                "id": ruta.id_ruta,
                "titulo": ruta.titulo,
                "descripcion": ruta.descripcion,
                "nivel": ruta.nivel,
                "fecha_creacion": ruta.fecha_creacion.isoformat() if ruta.fecha_creacion else None
            }
            for ruta in rutas
        ]
        
        return jsonify({
            "success": True,
            "data": rutas_data,
            "count": len(rutas_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@rutas_bp.route("/rutas-aprendizaje", methods=["POST"])
def post_ruta():
    try:
        data = request.get_json()
        # Validar datos obligatorios
        if not data or not all(k in data for k in ("titulo", "descripcion", "nivel")):
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        NIVELES_PERMITIDOS=['básico', 'intermedio', 'avanzado']
        if data["nivel"] not in NIVELES_PERMITIDOS:
            return jsonify({"error": f"Nivel debe ser uno de: {NIVELES_PERMITIDOS}"}), 400
        nueva_ruta = RutaAprendizaje(
            titulo=data["titulo"],
            descripcion=data["descripcion"],
            nivel=data["nivel"],
            fecha_creacion=datetime.utcnow()
        )
        
        db.session.add(nueva_ruta)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "titulo": nueva_ruta.titulo,
            "message": "Ruta de aprendizaje creada exitosamente",
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
@rutas_bp.route("/update/<int:id>", methods=["PUT"])
def update_ruta(id):
    try:
        ruta = RutaAprendizaje.query.get(id)
        if not ruta:
            return jsonify({"error": "Ruta no encontrado"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

        # Actualizar campos si se proporcionan
        if "titulo" in data:
            if not data["titulo"].strip():
                return jsonify({"error": "El titulo no puede estar vacío"}), 400
            ruta.titulo = data["titulo"]

        if "descripcion" in data:
            ruta.descripcion = data["descripcion"]

        if "nivel" in data:
            ruta.nivel = data["nivel"]

        db.session.commit()
        return jsonify({
            "message": "Ruta actualizada con éxito",
            "id_ruta": ruta.id_ruta
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al actualizar ruta de aprendizaje: {str(e)}"}), 500
    
@rutas_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_ruta(id):
    try:
        ruta = RutaAprendizaje.query.get(id)
        if not ruta:
            return jsonify({"error": "Ruta no encontrada"}), 404

        db.session.delete(ruta)
        db.session.commit()
        return jsonify({"message": "Ruta eliminada con éxito"}), 202
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar ruta: {str(e)}"}), 500