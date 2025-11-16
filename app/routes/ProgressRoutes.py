from flask import request, jsonify
from app import db
from flask import Blueprint
import json
from app.models.progress import Progress
from flask_jwt_extended import jwt_required, get_jwt_identity

progress_bp = Blueprint('progress', __name__, url_prefix='/progress')

@progress_bp.route('/update', methods=['POST'])
@jwt_required()
def update_progress():
    try:
        data = request.get_json() or {}
        lesson_id = data.get('lesson_id')
        progress_value = data.get('progress_value')

        if lesson_id is None or progress_value is None:
            return jsonify({"error": "lesson_id and progress_value are required"}), 400

        # Obtener el id del usuario a partir del JWT
        user_id = get_jwt_identity()
        if user_id is None:
            return jsonify({"error": "Invalid token or identity missing"}), 401

        # Buscar el progreso existente para el usuario autenticado
        progress = Progress.query.filter_by(user_id=user_id, lesson_id=lesson_id).first()

        if progress:
            # Actualizar el progreso existente
            progress.progress_value = progress_value
        else:
            # Crear un nuevo registro de progreso
            progress = Progress(user_id=user_id, lesson_id=lesson_id, progress_value=progress_value)
            db.session.add(progress)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Progreso actualizado correctamente"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@progress_bp.route('/', methods=['GET']) 
@jwt_required()
def get_progress():
    try:
        # Obtener el id del usuario a partir del JWT
        user_id = get_jwt_identity()
        if user_id is None:
            return jsonify({"error": "Invalid token or identity missing"}), 401

        # Obtener todos los registros de progreso para el usuario autenticado
        progress_records = Progress.query.filter_by(user_id=user_id).all()

        progress_list = [
            {
                "lesson_id": record.lesson_id,
                "progress_value": record.progress_value
            }
            for record in progress_records
        ]

        return jsonify({
            "success": True,
            "progress": progress_list
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500