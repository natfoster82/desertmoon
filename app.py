from flask import Flask
from extensions import socket
from views import *
# must import this
import sock

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # register extensions
    socket.init_app(app)

    # register views
    app.register_blueprint(views_bp)

    return app
