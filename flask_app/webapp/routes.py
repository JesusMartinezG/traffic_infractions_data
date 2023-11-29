from flask import render_template, request, Blueprint

bp = Blueprint('visualizer', __name__, template_folder='templates',)


@bp.route('/')
def index():
    return render_template('index.jinja2')