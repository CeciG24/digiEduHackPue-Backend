import os

from flask import request, jsonify
from app import db
import google.generativeai as genai
from flask import Blueprint
import json
from app.models.leccion import Leccion

API_KEY = "AIzaSyAK_Rdnf7HGgnn90A5asOytIEPd7QMI8zw"
genai.configure(api_key=API_KEY)

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

@ai_bp.route('/generate_content', methods=['POST'])
def generate_content():
    try:
        data = request.get_json() or {}
        prompt = data.get('prompt', '')

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Usar Gemini (API actual de Google)
        model = genai.GenerativeModel('gemini-2.5-pro')

        response = model.generate_content(prompt)

        # Extraer el texto generado
        generated_text = response.text

        return jsonify({
            "success": True,
            "generated_text": generated_text
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@ai_bp.route('/generate-test/<int:lesson_id>', methods=['POST'])
def generate_test(lesson_id):
    try:
        # Intentar obtener la lección por ID
        try:
            lesson = db.session.get(Leccion, lesson_id)
        except Exception:
            lesson = Leccion.query.get(lesson_id)

        if not lesson:
            return jsonify({"error": "Lección no encontrada"}), 404

        # Extraer texto real del modelo
        title = lesson.titulo or ""
        body = lesson.contenido or ""

        lesson_text = f"{title}\n\n{body}".strip()

        if not lesson_text:
            return jsonify({"error": "La lección no contiene texto"}), 404

        # Prompt
        prompt = (
            "Genera un test de 5 preguntas de opción múltiple para la siguiente lección.\n"
            "Cada pregunta debe incluir: 'question', 'options' (4 opciones), y 'answer' (índice correcto 0-3).\n"
            "Devuelve únicamente un JSON válido con la clave 'questions'.\n\n"
            f"Lección:\n{lesson_text}\n\n"
            "Salida esperada: {\"questions\":[{\"question\":\"...\",\"options\":[\"a\",\"b\",\"c\",\"d\"],\"answer\":2}]}"
        )

        model = genai.GenerativeModel('gemini-2.5-pro')

        response = model.generate_content(prompt)

        # Extraer el texto generado
        generated_text = response.text

        return jsonify({
            "success": True,
            "generated_text": generated_text
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@ai_bp.route('/list_models', methods=['GET'])
def list_models():
    try:
        models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                models.append({
                    'name': m.name,
                    'display_name': m.display_name,
                    'description': m.description
                })

        return jsonify({
            "success": True,
            "models": models
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500