from flask import Blueprint

#Creamos el blueprint
lessons_bp = Blueprint('lessons', __name__, url_prefix='/lessons')