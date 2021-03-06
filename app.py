from flask import Flask
from flask_assets import Bundle
from extensions import socket, asset_env
from views import views_bp
# must import this for handlers to be registered
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
        'src/js/vendor/markdown-it.js',
        'src/js/vendor/vue.js' if app.debug else 'src/js/vendor/vue.js',
        'src/js/app.js',
        filters=None if app.debug else 'jsmin',
        output='gen/app.js'
    )

    asset_env.register('css', css)
    asset_env.register('js', js)

    # register views
    app.register_blueprint(views_bp)

    return app
