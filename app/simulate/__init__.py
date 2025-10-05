from flask import Blueprint

bp = Blueprint('simulate', __name__)

from app.simulate import routes
