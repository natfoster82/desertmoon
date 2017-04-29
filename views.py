from flask import Blueprint, render_template


views_bp = Blueprint('views', __name__, template_folder='templates')


@views_bp.route('/')
def index():
    return render_template('index.html')
