from flask_socketio import join_room, leave_room
from helpers import random_string


class Engine(object):
    def execute(self, command_obj):
        method_name = 'execute_' + command_obj.verb
        try:
            self.__getattribute__(method_name)(command_obj)
        except AttributeError:
            command_obj.log_text = 'Unrecognized command'


class GlobalEngine(Engine):
    def execute_init(self, command_obj):
        new_handle = command_obj.prompt_responses.get('handle')
        if not new_handle:
            command_obj.prompt = {'text': 'Enter a new handle:', 'key': 'handle'}
            command_obj.default = command_obj.handle
        else:
            leave_room(command_obj.room)
            command_obj.handle = new_handle
            new_room = str(random_string(8))
            join_room(new_room)
            command_obj.room = new_room
            command_obj.log_text = '{0} has joined this simulation (Simulation ID: {1})'.format(command_obj.handle, command_obj.room)

    def execute_enter(self, command_obj):
        new_room = command_obj.params[0] if command_obj.params else command_obj.prompt_responses.get('simulation_id')
        new_handle = command_obj.prompt_responses.get('handle')

        if not new_room:
            command_obj.prompt = {'text': 'Simulation ID:', 'key': 'simulation_id'}
        elif not new_handle:
            command_obj.prompt = {'text': 'Enter a new handle:', 'key': 'handle'}
            command_obj.default = command_obj.handle
        else:
            leave_room(command_obj.room)
            command_obj.handle = new_handle
            join_room(new_room)
            command_obj.room = new_room
            command_obj.log_text = '{0} has joined this simulation (Simulation ID: {1})'.format(command_obj.handle, command_obj.room)

    def execute_help(self, command_obj):
        command_obj.log_text = '/init - initialize a simulation\n\n/enter <simulation_id> - enter a saved or ongoing simulation'


ENGINES = {
    'global': GlobalEngine()
}
