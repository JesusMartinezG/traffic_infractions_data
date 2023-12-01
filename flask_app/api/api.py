from flask import jsonify, Response
from flask_app.api.models.datos_viales import inviales
from flask_app.database import db
from sqlalchemy import and_


def filter_coordinates(args):
    conditions = []
    limit = 200

    inviales_table = db.metadata.tables['inviales']

    if 'creacion' in args:
        conditions.append(inviales_table.c.creacion == args['creacion'])
    if 'id' in args:
        conditions.append(inviales_table.c.id == args['id'])
    if 'inicio' in args:
        conditions.append(inviales_table.c.creacion >= args['inicio'])
    if 'final' in args:
        conditions.append(inviales_table.c.creacion <= args['final'])
    if 'dia_semana' in args:
        conditions.append(inviales_table.c.dia_semana.like(args['dia_semana']))
    if 'alcaldia_inicio' in args:
        conditions.append(inviales_table.c.alcaldia_inicio.like(args['alcaldia_inicio']))
    if 'alcaldia_cierre' in args:
        conditions.append(inviales_table.c.alcaldia_cierre.like(args['alcaldia_cierre']))
    if 'limit' in args:
        limit = min(int(args['limit']), 5000) if args['limit'].isdigit() else limit

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