from flask_socketio import join_room, leave_room
from helpers import random_string, redis_store
from campaigns import CAMPAIGNS
import json


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
        self.prompt_responses = prompt_responses
        self.room = room
        self.subject = subject
        self.handle = handle
        self.prompt = None
        self.default = ''
        self.logs = []
        self.state = redis_store.get(self.room)
        if self.state:
            self.campaign = CAMPAIGNS.get(self.state['id'])
        else:
            self.campaign = None

    def execute(self):
        campaign_command_found = False
        if self.campaign:
            campaign_command_found = self.execute_campaign_command()

        if not campaign_command_found:
            method_name = 'execute_' + self.verb
            try:
                self.__getattribute__(method_name)()
            except AttributeError:
                self.logs.append({'text': 'Unrecognized command', 'room': None})

    def execute_campaign_command(self):
        return False

    def execute_init(self):
        campaign_id = self.params[0] if self.params else self.prompt_responses.get('campaign_id')
        new_handle = self.prompt_responses.get('handle')

        if not campaign_id:
            self.prompt = {'text': 'Case:', 'key': 'campaign_id'}
        elif not new_handle:
            self.prompt = {'text': 'Enter a new handle:', 'key': 'handle'}
            self.default = self.handle
        else:
            if campaign_id in CAMPAIGNS:
                leave_room(self.room)
                self.handle = new_handle
                new_room = str(random_string(8))
                state = CAMPAIGNS[campaign_id]['starting_state']
                redis_store.set(new_room, json.dumps(state))
                join_room(new_room)
                self.room = new_room
                self.logs.append({'text': '{0} has joined this simulation (Simulation ID: {1})'.format(self.handle, self.room), 'room': self.room})
                for log in state['logs']:
                    self.logs.append({'text': log, 'room': None})
            else:
                self.logs.append({'text': 'No case found with that ID', 'room': None})

    def execute_enter(self):
        new_room = self.params[0] if self.params else self.prompt_responses.get('simulation_id')
        new_handle = self.prompt_responses.get('handle')

        if not new_room:
            self.prompt = {'text': 'Simulation ID:', 'key': 'simulation_id'}
        elif not new_handle:
            self.prompt = {'text': 'Enter a new handle:', 'key': 'handle'}
            self.default = self.handle
        else:
            state = redis_store.get(new_room)
            if state:
                state = json.loads(state)
                leave_room(self.room)
                self.handle = new_handle
                join_room(new_room)
                self.room = new_room
                self.logs.append({'text': '{0} has joined this simulation (Simulation ID: {1})'.format(self.handle, self.room), 'room': self.room})
                for log in state['logs']:
                    self.logs.append({'text': log, 'room': None})
            else:
                self.logs.append({'text': 'No simulation found with that ID', 'room': None})

    def execute_help(self):
        self.logs.append({'text': '/init - initialize a simulation\n\n/enter <simulation_id> - enter a saved or ongoing simulation', 'room': None})
