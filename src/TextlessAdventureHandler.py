from AlexaBaseHandler import AlexaBaseHandler
from IntentManager import IntentManager


class TextlessAdventureHandler(AlexaBaseHandler):
    """
    Concrete implementation of the AlexaBaseHandler for Textless Adventure game.
    """

    def __init__(self):
        super(self.__class__, self).__init__()

    def _test_response(self, msg):
        session_attributes = {}

        card_title    = "Test Response"
        card_output   = "Test card output"
        speech_output = "You have routed through the {0} request.".format(msg)

        # If the user either does not reply to the welcome message or says
        #  something that is not understood, they will be prompted again with
        #  this text.
        reprompt_text      = "I'm sorry, I didn't quite catch that."
        should_end_session = True

        speechlet = self._build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session)

        return self._build_response(session_attributes, speechlet)

    def _generate_intent_response(self, data):
        session_attributes = {}

        card_title    = data['card_title'] or "Test Response"
        card_output   = data['card_output'] or "Test card output"
        speech_output = "You have invoked the {0} intent.".format(data['request_name'])

        # If the user either does not reply to the welcome message or says
        #  something that is not understood, they will be prompted again with
        #  this text.
        reprompt_text      = "I'm sorry, I didn't quite catch that."
        should_end_session = True

        speechlet = self._build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session)

        return self._build_response(session_attributes, speechlet)

    def on_processing_error(self, event, context, exc):
        print(type(exc))
        print(exc.args)
        print(exc)
        return self._test_response("on processing error")

    def on_launch(self, launch_request, session):
        return self._test_response("on launch")

    def on_session_started(self, session_started_request, session):
        return self._test_response("on session started")

    def on_intent(self, intent_request, session):
        # Let the IntentManager figure out what to do.
        intent_manager = IntentManager();
        data = intent_manager.manageIntent(intent_request, session)
        return self._generate_intent_response(data)

    def on_session_ended(self, session_end_request, session):
        return self._test_response("on session end")
