class IntentManager:
    """
    The IntentManager class is responsible for determining which intent has been
    invoked, triggering further actions and creating the response for the
    TextlessAdventureHandler.
    """

    def manageIntent(self, intent_request, session):
        intent_name = intent_request['intent']['name']

        switch = {
            'GoIntent'       : self.getGoResponse,
            'LookIntent'     : self.getLookResponse,
            'UseIntent'      : self.getUseResponse,
            'HelpIntent'     : self.getHelpResponse,
            'InventoryIntent': self.getInventoryResponse,
            'QuitIntent'     : self.getQuitResponse,
        };

        return switch[intent_name](intent_request, session)

    # *************** #
    # Intent handlers #
    # *************** #

    def getGoResponse(self, intent_request, session):
        data = {
            'card_title'        : 'Go Request',
            'card_output'       : 'Go card output',
            'request_name'      : 'go',
            'should_end_session': False,
            'speech_output'     : '',
            'session_attributes': {},
        }

        direction = intent_request['intent']['slots']['Direction']['value']

        moved = False

        # Change the Player's position.
        print(session['attributes'])
        session_attributes = session['attributes']

        y_pos = session_attributes['player']['position']['y']
        x_pos = session_attributes['player']['position']['x']

        data['session_attributes'] = session_attributes

        if moved:
            data['speech_output'] = 'temp'
        else:
            data['speech_output'] = 'You cannot travel ' + direction + '. '

        return data

    def getLookResponse(self, intent_request, session):
        data = {
            'card_title'        : 'Look Request',
            'card_output'       : 'Look card output',
            'request_name'      : 'look',
            'should_end_session': True
        }

        return data
    
    def getUseResponse(self, intent_request, session):
        data = {
            'card_title'        : 'Use Request',
            'card_output'       : 'Use card output',
            'request_name'      : 'use',
            'should_end_session': True
        }

        return data
    
    def getHelpResponse(self, intent_request, session):
        data = {
            'card_title'        : 'Help Request',
            'card_output'       : 'Help card output',
            'request_name'      : 'help',
            'should_end_session': True
        }

        return data
    
    def getInventoryResponse(self, intent_request, session):
        data = {
            'card_title'        : 'Inventory Request',
            'card_output'       : 'Inventory card output',
            'request_name'      : 'inventory',
            'should_end_session': True
        }

        return data
    
    def getQuitResponse(self, intent_request, session):
        data = {
            'card_title'        : 'Quit Request',
            'card_output'       : 'Quit card output',
            'request_name'      : 'quit',
            'should_end_session': True
        }

        return data
