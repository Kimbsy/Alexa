from AlexaBaseHandler import AlexaBaseHandler
from IntentManager import IntentManager
from Dungeon import Dungeon
from Player import Player


class TextlessAdventureHandler(AlexaBaseHandler):
    """
    Concrete implementation of the AlexaBaseHandler for Textless Adventure game.

    This class takes requests from Alexa and returns responses to be spoken.
    """

    def __init__(self):
        super(self.__class__, self).__init__()

    def _test_response(self, msg):
        card_title         = 'Test Response'
        card_output        = 'Test card output'
        speech_output      = 'You have routed through the {0} request.'.format(msg)
        reprompt_text      = 'I\'m sorry, I didn\'t quite catch that.'
        should_end_session = True
        session_attributes = {}

        speechlet = self._build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session)

        return self._build_response(session_attributes, speechlet)

    def _generate_response(self, data):
        card_title         = data['card_title']
        card_output        = data['card_output']
        speech_output      = data['speech_output']
        reprompt_text      = 'I\'m sorry, I didn\'t quite catch that.'
        should_end_session = data['should_end_session']
        session_attributes = data['session_attributes']


        speechlet = self._build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session)

        return self._build_response(session_attributes, speechlet)

    def on_processing_error(self, event, context, exc):
        print(type(exc))
        print(exc.args)
        print(exc)
        data = {
            'card_title'        : 'ERROR',
            'card_output'       : 'An error has occured',
            'request_name'      : 'error',
            'should_end_session': True,
            'speech_output'     : 'An error has occured. ' + exc.args[0],
            'session_attributes': {},
        }
        return self._generate_response(data)

    def on_launch(self, launch_request, session):
        card_title         = 'Launch'
        card_output        = 'Launch card'
        speech_output      = ''
        reprompt_text      = 'I\'m sorry, I didn\'t quite catch that.'
        should_end_session = False

        dungeon = Dungeon(None)
        player  = Player(None)

        text = 'You find yourself in a dark room. It is cold. You are alone. '
        text = text + dungeon.get_room_look_text(player.data['position'])
        text = text + dungeon.get_room_layout_text(player.data['position'])

        speech_output = text

        session_attributes = {
            'dungeon_data': dungeon.data,
            'player_data': player.data,
        }

        speechlet = self._build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session)

        return self._build_response(session_attributes, speechlet)

    def on_session_started(self, session_started_request, session):
        return self._test_response('on session started')

    def on_intent(self, intent_request, session):
        # Let the IntentManager figure out what to do.
        intent_manager = IntentManager();

        data = intent_manager.manageIntent(intent_request, session)

        return self._generate_response(data)

    def on_session_ended(self, session_end_request, session):
        return self._test_response('on session end')
