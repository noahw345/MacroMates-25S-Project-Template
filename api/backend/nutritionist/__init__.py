from flask import Blueprint

nutritionist_bp = Blueprint('nutritionist', __name__)

from . import nutritionist_routes 