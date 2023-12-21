from flask import render_template, request, Blueprint
from datetime import datetime

bp = Blueprint('webapp', __name__, template_folder='templates',)


@bp.route('/')
def index():
    return render_template('index.jinja2')

@bp.route('/map')
def map():
    return render_template('map.jinja2')

@bp.route('/chart')
def chart():
    return render_template('chart.jinja2')