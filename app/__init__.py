from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Ruta absoluta al archivo SQLite
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'database.sqlite')

    # Configuración de SQLAlchemy con SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensiones
    db.init_app(app)
    CORS(app)

    # Importar modelos
    from app.models import user, leccion,modulo,pdfleccion,progress,rutaAprendizaje  # agrega los que vayas creando

    # Registrar blueprints si los tienes (opcional)
    from app.routes.LessonsRoutes import lessons_bp
    app.register_blueprint(lessons_bp)

    from app.routes.UserRoutes import users_bp
    app.register_blueprint(users_bp)

    # Crear la BD si no existe
    with app.app_context():
        db.create_all()

    return app
