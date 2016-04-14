from Dungeon import Dungeon
from Player import Player


class IntentManager:
    """The IntentManager class is responsible for determining which intent has been
    invoked, triggering further actions and creating the response for the
    TextlessAdventureHandler.
    """

    def manageIntent(self, intent_request, session):
        intent_name = intent_request['intent']['name']

        switch = {
            'GoIntent'       : self.get_go_response,
            'LookIntent'     : self.get_look_response,
            'ShowExitsIntent': self.get_show_exits_response,
            'GetIntent'      : self.get_get_reponse,
            'UseIntent'      : self.get_use_response,
            'HelpIntent'     : self.get_help_response,
            'InventoryIntent': self.get_inventory_response,
            'QuitIntent'     : self.get_quit_response,
        };

        return switch[intent_name](intent_request, session)

    def get_go_response(self, intent_request, session):
        data = {
            'card_title'        : 'Go Request',
            'card_output'       : 'Go card output',
            'request_name'      : 'go',
            'should_end_session': False,
            'speech_output'     : '',
            'session_attributes': {},
        }

        direction = intent_request['intent']['slots']['Direction']['value']

        session_attributes = session['attributes']

        dungeon = Dungeon(session_attributes['dungeon_data'])
        player  = Player(session_attributes['player_data'])
        pos     = player.data['position']

        if dungeon.move_is_allowed(pos, direction):
            if direction == 'north':
                pos['y'] = pos['y'] - 1
            if direction == 'south':
                pos['y'] = pos['y'] + 1
            if direction == 'east':
                pos['x'] = pos['x'] + 1
            if direction == 'west':
                pos['x'] = pos['x'] - 1

            player.data['position'] = pos
            session_attributes['player_data'] = player.data

            data['speech_output'] = dungeon.get_room_entry_text(pos)
        else:
            data['speech_output'] = 'You cannot travel ' + direction + '. '

        data['session_attributes'] = session_attributes

        return data

    def get_look_response(self, intent_request, session):
        data = {
            'card_title'        : 'Look Request',
            'card_output'       : 'Look card output',
            'request_name'      : 'look',
            'should_end_session': False,
            'session_attributes': {},
        }

        session_attributes = session['attributes']

        dungeon = Dungeon(session_attributes['dungeon_data'])
        player  = Player(session_attributes['player_data'])

        data['speech_output'] = dungeon.get_room_look_text(player.data['position'])

        return data

    def get_show_exits_response(self, intent_request, session):
        data = {
            'card_title'        : 'Show Exits Request',
            'card_output'       : 'Show Exits card output',
            'request_name'      : 'show_exits',
            'should_end_session': False,
            'session_attributes': {},
        }

        session_attributes = session['attributes']

        dungeon = Dungeon(session_attributes['dungeon_data'])
        player  = Player(session_attributes['player_data'])

        data['speech_output'] = dungeon.get_room_layout_text(player.data['position'])

        return data

    def get_get_reponse(self, intent_request, session):
        data = {
            'card_title'        : 'Get Request',
            'card_output'       : 'Get card output',
            'request_name'      : 'get',
            'should_end_session': False,
            'session_attributes': {},
        }

        item = intent_request['intent']['slots']['Item']['value']

        session_attributes = session['attributes']

        dungeon = Dungeon(session_attributes['dungeon_data'])
        player  = Player(session_attributes['player_data'])
        pos     = player.data['position']

        if dungeon.item_is_available(item, pos):
            player.add_item(item)
            dungeon.remove_item(item, pos)
            data['speech_output'] = 'You take the ' + item

        return data
    
    def get_use_response(self, intent_request, session):
        data = {
            'card_title'        : 'Use Request',
            'card_output'       : 'Use card output',
            'request_name'      : 'use',
            'should_end_session': False,
            'session_attributes': {},
        }

        return data
    
    def get_help_response(self, intent_request, session):
        data = {
            'card_title'        : 'Help Request',
            'card_output'       : 'Help card output',
            'request_name'      : 'help',
            'should_end_session': False,
            'session_attributes': session['attributes']
            'speech_output'     : 'Textless adventure is a voice activated dungeon exploration game. Use voice commands to move around, interact with your environment and try to figure out why on earth you are in a dungeon. Developed by Dave Kimber and Sam Briggs.'
        }

        return data
    
    def get_inventory_response(self, intent_request, session):
        data = {
            'card_title'        : 'Inventory Request',
            'card_output'       : 'Inventory card output',
            'request_name'      : 'inventory',
            'should_end_session': False,
            'session_attributes': {},
        }

        session_attributes = session['attributes']

        player  = Player(session_attributes['player_data'])

        data['speech_output'] = player.get_inventory_text()

        data['session_attributes'] = session_attributes

        return data

    def get_quit_response(self, intent_request, session):
        data = {
            'card_title'        : 'Quit Request',
            'card_output'       : 'Quit card output',
            'request_name'      : 'quit',
            'should_end_session': True,
            'session_attributes': {},
        }

        return data
