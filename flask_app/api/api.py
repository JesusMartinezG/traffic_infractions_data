from flask import jsonify, Response
from flask_app.api.models.datos_viales import inviales
from flask_app.database import db
from sqlalchemy import and_
from functools import lru_cache

@lru_cache(maxsize=5)
def filter_coordinates(args):
    conditions = []
    limit = 200

    inviales_table = db.metadata.tables['inviales']

    valid_keys = {
        'creacion',
        'id',
        'dia_semana',
        'tipo_incidente_c4',
        'incidente_c4',
        'clas_con_f_alarma',
        'tipo_entrada',
        'alcaldia_inicio',
        'alcaldia_cierre',
        'colonia'
    }

    
    for key, value in args.items():
        if key == 'limit':
            limit = min(int(value), 5000) if value.isdigit() else limit
        elif key == 'inicio':
            conditions.append(inviales_table.c.creacion >= value)
        elif key == 'final':
            conditions.append(inviales_table.c.creacion <= value)
        elif key in valid_keys:
            conditions.append(getattr(inviales_table.c, key).like(value))


    if conditions:
        query = db.select(inviales_table.c.latitud, inviales_table.c.longitud).where(and_(*conditions)).limit(limit).order_by(inviales_table.c.creacion)
        registers = db.session.execute(query)
        return jsonify([{'latitud': register.latitud, 'longitud': register.longitud} for register in registers])

    query = db.select(inviales_table.c.latitud, inviales_table.c.longitud).limit(limit).order_by(inviales_table.c.creacion)
    registers = db.session.execute(query)

    if registers:
        return jsonify([{'latitud': register.latitud, 'longitud': register.longitud} for register in registers])

    return 'No data to show', 404


def id_coordinates(id):
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