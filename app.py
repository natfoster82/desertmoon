from flask import Flask
from flask_assets import Bundle
from extensions import socket, asset_env
from views import *
# must import this
import sock


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # register extensions
    socket.init_app(app)
    asset_env.init_app(app)

    # register assets
    css = Bundle(
        'src/scss/app.scss',
        filters='libsass',
        output='gen/app.css',
        depends='src/**/*.scss'
    )

    js = Bundle(
        'src/js/vendor/socket.io.js',
        'src/js/app.js',
        filters='jsmin',
        output='gen/app.js'
    )

    asset_env.register('css', css)
    asset_env.register('js', js)

    # register views
    app.register_blueprint(views_bp)

    return app
