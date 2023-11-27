from flask import Blueprint
from flask import jsonify, request, g
from flask_app.api.models.datos_viales import inviales
from flask_app.database import db

bp = Blueprint('api',__name__, url_prefix='/api')

@bp.route('/getCoordinatesByFilter/', methods=['GET'])
@bp.route('/getCoordinatesByFilter/<id>', methods=['GET'])
def getCoordinatesByFilter(id=1):
    incident = db.session.get_one(inviales,id)
    resp = {'id': incident.id,
            'folio': incident.folio,
            'creacion': incident.creacion,
            'dia_semana': incident.dia_semana,
            'cierre': incident.cierre,
            'tipo_incidente_c4': incident.tipo_incidente_c4,
            'alcalcia_inicio': incident.alcaldia_inicio,
            'latitud': incident.latitud,
            'longitud': incident.longitud,
            'codigo_cierre': incident.codigo_cierre,
            'clas_con_f_alarma': incident.clas_con_f_alarma,
            'tipo_entrada': incident.tipo_entrada,
            'alcaldia_cierre': incident.alcaldia_cierre,
            'colonia': incident.colonia
            }

    # return jsonify({'emote': 'Pepega', 'image-link':'https://pepegaclapwr.com/assets/rsz_pepega.png'})
    return jsonify(resp)

@bp.route('/hello', methods=['GET'])
def hello():
    return 'Hello'