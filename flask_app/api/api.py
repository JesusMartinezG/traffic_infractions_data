from flask import Blueprint
from flask import jsonify, request, g
from flask_app.api.models.datos_viales import inviales
from flask_app.database import db
from sqlalchemy import and_

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
            'alcaldia_inicio': incident.alcaldia_inicio,
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

    conditions = []
    inicio = None
    fnal = None
    limit = 100

    table = db.metadata.tables['inviales']

    if 'creacion' in args:
        conditions.append(table.c.creacion == args['creacion'])
    if 'id' in args:
        conditions.append(table.c.id == args['id'])
    if 'inicio' in args:
        conditions.append(table.c.creacion >= args['inicio'])
    if 'final' in args:
        conditions.append(table.c.creacion <= args['final'])
    if 'dia_semana' in args:
        conditions.append(table.c.dia_semana.like(args['dia_semana']))
    if 'alcaldia_inicio' in args:
        conditions.append(table.c.alcaldia_inicio.like(args['alcaldia_inicio']))
    if 'alcaldia_cierre' in args:
        conditions.append(table.c.alcaldia_cierre.like(args['alcaldia_cierre']))
    if 'limit' in args:
        try:
            limit = min(int(args['limit']), 5000)
        except ValueError:
            pass
    
    
    
    if len(conditions):
        registers = db.session.execute(db.select(table.c.latitud,table.c.longitud).where(and_(*conditions)).limit(limit).order_by(inviales.creacion))
        return jsonify([{'latitud': register.latitud, 'longitud': register.longitud} for register in registers])
    else:
        registers = db.session.execute(db.select(db.metadata.tables['inviales'].c.latitud,db.metadata.tables['inviales'].c.longitud).limit(limit).order_by(inviales.creacion))

        if registers:
            return jsonify([{'latitud': register.latitud, 'longitud': register.longitud} for register in registers])
    
    return 'No data to show', 404