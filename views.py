from flask import Blueprint, render_template, request
from helpers import random_string


views_bp = Blueprint('views', __name__, template_folder='templates')


@views_bp.route('/')
def index():
    handle = 'operator' + random_string(5, letters=False)
    room = request.args.get('simulation_id', 'lobby')
    return render_template('index.html', handle=handle, room=room)
