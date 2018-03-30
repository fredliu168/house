from flask import Blueprint

api = Blueprint('api', __name__)

from . import house_api, scrap, images
