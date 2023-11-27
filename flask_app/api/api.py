from flask import Blueprint
from flask import jsonify, request, g
from flask_app.api.models.datos_viales import inviales
from flask_app.database import db

bp = Blueprint('api',__name__, url_prefix='/api')

@bp.route('/getIncidentById/', methods=['GET'])
@bp.route('/getIncidentById/<id>', methods=['GET'])
def getCoordinatesById(id=1):
    incident = db.get_or_404(inviales,id)

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

@bp.route('/getCoordinatesByFilter/', methods=['GET'])
def getCoordinatesByFilter():
    args = request.args

    if 'creacion' in args:
        return db.get_or_404(db.select(inviales).filter_by(inicio=args['creacion']))
    
    registers = db.session.execute(db.select(db.metadata.tables['inviales'].c.latitud,db.metadata.tables['inviales'].c.longitud).limit(100).order_by(inviales.creacion))

    if registers:
        return jsonify([{'latitud': register.latitud, 'longitud': register.longitud} for register in registers])
    
    return 404