from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    POSTGRES_USER = 'learnhub_29a4_user'
    POSTGRES_PASSWORD = 'AcxyhV0FoFoe5DFp90DX15ltnpddlg7S'
    POSTGRES_DB = 'learnhub_29a4'
    POSTGRES_HOST = 'dpg-d4cgh549c44c738q9e00-a.oregon-postgres.render.com'
    POSTGRES_PORT = 5432  # como entero

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Carpeta para guardar PDFs
    app.config['PDF_UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads/pdfs')

    # Crear la carpeta si no existe
    os.makedirs(app.config['PDF_UPLOAD_FOLDER'],exist_ok=True)
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

    from app.routes.ModulosRoutes import modulo_bp
    app.register_blueprint(modulo_bp)

    from app.routes.RutaAprendizajeRoutes import rutas_bp
    app.register_blueprint(rutas_bp)

    from app.routes.AiRoutes import ai_bp
    app.register_blueprint(ai_bp)
    
    # Crear la BD si no existe
    with app.app_context():
        db.create_all()

    return app
