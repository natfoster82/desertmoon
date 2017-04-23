import eventlet
eventlet.monkey_patch()

from app import create_app
from extensions import socket


if __name__ == '__main__':
    application = create_app()
    socket.run(application, host='0.0.0.0', port=5000)
