from extensions import socket
from flask_socketio import join_room, leave_room, emit
from helpers import random_string, redis_store
from engines import ENGINES


@socket.on('launch')
def on_launch(data):
    join_room('lobby')
    welcome_payload = {
        'handle': '',
        'text': 'Welcome, {0}, to project Desert Moon. For a list of available commands, type "/help" and hit enter'.format(data['handle'])
    }
    emit('log', welcome_payload)


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
        room = command_obj.room
        subject = command_obj.subject
        handle = command_obj.handle
        prompt = command_obj.prompt
        default = command_obj.default

        command_obj.execute()

        if not command_obj.prompt and command_obj.log_text:
            emit('log', {'handle': '', 'text': command_obj.log_text}, room=room)



    callback_payload = {
        'room': room,
        'subject': subject,
        'handle': handle,
        'prompt': prompt,
        'default': default
    }
    return callback_payload



class Command(object):
    def __init__(self, command, prompt_responses, room, subject, handle):
        split_command = command.split(' ', 1)
        verb = split_command[0][1:]
        try:
            params = split_command[1:]
        except IndexError:
            params = []

        self.verb = verb
        self.params = params
        self.prompt_resposnes = prompt_responses
        self.room = room
        self.subject = subject
        self.handle = handle
        self.prompt = None
        self.default = ''
        self.log_text = ''

    def execute(self):
        state = redis_store.get(self.room)
        if state:
            campaign = state['campaign']
            engine = ENGINES.get(campaign, ENGINES['global'])
        else:
            engine = ENGINES['global']

        engine.execute(self)
