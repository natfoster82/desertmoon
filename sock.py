from extensions import socket
from flask_socketio import join_room, leave_room, emit
from helpers import random_string


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
    executed = True
    default = ''

    if not prompt_responses:
        echo_payload = {
            'handle': handle,
            'text': command
        }
        emit('log', echo_payload, room=room)

    if command.startswith('/'):
        split_command = command.split(' ', 1)
        verb = split_command[0][1:]
        try:
            params = split_command[1:]
        except IndexError:
            params = []
        
        if verb == 'help':
            help_payload = {
                'handle': '',
                'text': '/init - initialize a simulation\n\n/enter <simulation_id> - enter a saved or ongoing simulation'
            }
            emit('log', help_payload, room=room)
        elif verb == 'init':
            new_handle = prompt_responses.get('handle')
            if not new_handle:
                prompt = {'text': 'Enter a new handle:', 'key': 'handle'}
                default = handle
            else:
                leave_room(room)
                handle = new_handle
                new_room = str(random_string(8))
                join_room(new_room)
                room = new_room
                init_payload = {
                    'handle': '',
                    'text': '{0} has joined this simulation (Session ID: {1})'.format(handle, room)
                }
                emit('log', init_payload, room=room)
        elif verb == 'enter':
            new_room = params[0] if params else prompt_responses.get('session_id')
            new_handle = prompt_responses.get('handle')

            if not new_room:
                prompt = {'text': 'Session ID:', 'key': 'session_id'}
            elif not new_handle:
                prompt = {'text': 'Enter a new handle:', 'key': 'handle'}
                default = handle
            else:
                leave_room(room)
                handle = new_handle
                join_room(new_room)
                room = new_room
                init_payload = {
                    'handle': '',
                    'text': '{0} has joined this simulation (Session ID: {1})'.format(handle, room)
                }
                emit('log', init_payload, room=room)
        else:
            error_payload = {
                'handle': '',
                'text': 'Unrecognized command'
            }
            emit('log', error_payload)

    callback_payload = {
        'room': room,
        'subject': subject,
        'handle': handle,
        'prompt': prompt,
        'default': default,
        'executed': executed
    }
    return callback_payload


# class Command(object):
#     global_verbs = ['init', 'enter']
#     campaign_executors = {}
#
#     def __init__(self, room, command, prompt_responses):
#         self.room = room
#         self.campaign_parser = self.campaign_parsers.get(self.room)
#         split_command = command.split(' ', 1)
#         self.verb = split_command[0]
#         try:
#             self.params = split_command[1:]
#         except IndexError:
#             self.params = []
#         self.prompt_responses = prompt_responses
#
#     def execute(self):
#         if self.verb in self.global_verbs:
#             getattr(self, self.verb)()
#         elif self.campaign_parser:
#
#
# class Executor()
