from flask import render_template
from views import views_bp


@views_bp.route('/hello')
def hello():
    return 'Hello, world!'
