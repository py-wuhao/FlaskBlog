from flask import Blueprint

api = Blueprint('api', __name__)

from . import users, posts, errors, decorators, comments, authentication
