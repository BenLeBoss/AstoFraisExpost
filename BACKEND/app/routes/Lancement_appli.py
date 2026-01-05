from flask import Blueprint

lancement_bp = Blueprint('lancement', __name__)

@lancement_bp.route('/')
def index():
    return "Backend Flask OK !\n"
