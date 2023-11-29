from flask import Blueprint
from flask import request
from flask_app.api import api

bp = Blueprint('api',__name__, url_prefix='/api')


@bp.route('/getIncidentById/', methods=['GET'])
@bp.route('/getIncidentById/<id>', methods=['GET'])
def getCoordinatesById(id=1):
    return api.id_coordinates(id)


@bp.route('/getCoordinatesByFilter/', methods=['GET'])
def getCoordinatesByFilter():
    if request.method == 'GET':
        args = request.args
        return api.filter_coordinates(args)

    