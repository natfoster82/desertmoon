from extensions import socket
from flask_socketio import emit, join_room
from command import Command


@socket.on('launch')
def on_launch(data):
    welcome_payload = {
        'handle': '',
        'text': 'Welcome, {0}, to project Desert Moon. For a list of available commands, type "/help" and hit enter'.format(data['handle'])
    }
    emit('log', welcome_payload)

@socket.on('join_room')
def on_join_room(room):
    join_room(room)


@socket.on('submit')
def on_submit(data):
    handle = data['handle']
    room = data['room']
    subject = data['subject']
    command = data['command']
    prompt_responses = data['prompt_responses']
    prompt = None
    default = ''

    if not prompt_responses:
        echo_payload = {
            'handle': handle,
            'text': command
        }
        emit('log', echo_payload, room=room)

    if command.startswith('/'):
        command_obj = Command(command, prompt_responses, room, subject, handle)
        command_obj.execute()
        if not command_obj.prompt and command_obj.logs:
            for log in command_obj.logs:
                emit('log', {'handle': '', 'text': log['text']}, room=log['room'])

        room = command_obj.room
        subject = command_obj.subject
        handle = command_obj.handle
        prompt = command_obj.prompt
        default = command_obj.default

    callback_payload = {
        'room': room,
        'subject': subject,
        'handle': handle,
        'prompt': prompt,
        'default': default
    }
    return callback_payload

