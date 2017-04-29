from extensions import socket
from flask_socketio import join_room, leave_room, emit
from uuid import uuid4


@socket.on('connect')
def on_connect():
    print('user connected')


@socket.on('submit')
def on_submit(data):
    print(data)
    echo_payload = {
        'handle': data['handle'],
        'text': data['command']
    }
    emit('log', echo_payload, room=data['room'])

    split_command = data['command'].split(' ', 1)
    verb = split_command[0]
    try:
        params = split_command[1:]
    except IndexError:
        params = []

    if verb == 'init':
        room = str(uuid4())
        join_room(room)
        emit('room', room)
        join_payload = {
            'handle': 'Server',
            'timestamp': '',
            'text': 'Operator {0} has joined this simulation (Session ID: {1})'.format(data['handle'], room)
        }
        emit('log', join_payload, room=room)
    elif verb == 'join':
        if data['room']:
            leave_room(data['room'])
        room = params[0]
        join_room(room)
        emit('room', room)
        join_payload = {
            'handle': 'Server',
            'timestamp': '',
            'text': 'Operator {0} has joined this simulation (Session ID: {1})'.format(data['handle'], room)
        }
        emit('log', join_payload, room=room)
    else:
        error_payload = {
            'handle': 'Server',
            'timestamp': '',
            'text': 'Unrecognized command'
        }
        emit('log', error_payload)
