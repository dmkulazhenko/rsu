from flask import Blueprint

bp = Blueprint("main", __name__)

from rsu.main import routes
