from flask import Blueprint

#Creamos el blueprint
users_bp = Blueprint('users', __name__, url_prefix='/users')