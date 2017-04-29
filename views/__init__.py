from flask import Blueprint


views_bp = Blueprint('views', __name__, template_folder='templates')


# make sure to add new files to this list, otherwise you'll get a 404
__all__ = ['views_bp', 'pages']
