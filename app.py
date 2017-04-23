from flask import Flask
from extensions import socket
# must import this
import sock

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    socket.init_app(app)

    return app
