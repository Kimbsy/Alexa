/**
 * This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
 * For additional samples, visit the Alexa Skills Kit developer documentation at
 * https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit/getting-started-guide
 */

// Route the incoming request based on type (LaunchRequest, IntentRequest,
// etc.) The JSON body of the request is provided in the event parameter.
exports.handler = function (event, context) {
  try {
    // console.log('event.session.application.applicationId=' + event.session.application.applicationId);

    /**
     * Uncomment this if statement and populate with your skill's application ID to
     * prevent someone else from configuring a skill that sends requests to this function.
     */
    /*
    if (event.session.application.applicationId !== 'amzn1.echo-sdk-ams.app.[unique-value-here]') {
         context.fail('Invalid Application ID');
     }
    */

    if (event.session.new) {
      onSessionStarted({requestId: event.request.requestId}, event.session);
    }

    if (event.request.type === 'LaunchRequest') {
      onLaunch(
        event.request,
        event.session,
        function callback(sessionAttributes, speechletResponse) {
          context.succeed(buildResponse(sessionAttributes, speechletResponse));
        }
      );
    } else if (event.request.type === 'IntentRequest') {
      onIntent(
        event.request,
        event.session,
        function callback(sessionAttributes, speechletResponse) {
          context.succeed(buildResponse(sessionAttributes, speechletResponse));
        }
      );
    } else if (event.request.type === 'SessionEndedRequest') {
      onSessionEnded(event.request, event.session);
      context.succeed();
    }
  } catch (e) {
    context.fail('Exception: ' + e);
  }
};

/**
 * Called when the session starts.
 */
function onSessionStarted(sessionStartedRequest, session) {
  setupDungeon(session);
  // console.log('onSessionStarted requestId=' + sessionStartedRequest.requestId + ', sessionId=' + session.sessionId);
}

/**
 * Called when the user launches the skill without specifying what they want.
 */
function onLaunch(launchRequest, session, callback) {
  // console.log('onLaunch requestId=' + launchRequest.requestId + ', sessionId=' + session.sessionId);

  // Dispatch to your skill's launch.
  getWelcomeResponse(callback);
}

/**
 * Called when the user specifies an intent for this skill.
 */
function onIntent(intentRequest, session, callback) {
  // console.log('onIntent requestId=' + intentRequest.requestId + ', sessionId=' + session.sessionId);

  var intent     = intentRequest.intent;
  var intentName = intentRequest.intent.name;

  // Dispatch to your skill's intent handlers
  if ('GoIntent' === intentName) {
    getGoResponse(intent, session, callback);
  } else if ('LookIntent' === intentName) {
    getLookResponse(intent, session, callback);
  } else if ('GetIntent' === intentName) {
    getGetResponse(intent, session, callback);
  } else if ('UseIntent' === intentName) {
    getUseResponse(intent, session, callback);
  } else if ('HelpIntent' === intentName) {
    getHelpResponse(intent, session, callback);
  } else if ('InventoryIntent' === intentName) {
    getInventoryResponse(intent, session, callback);
  } else if ('QuitIntent' === intentName) {
    getQuitResponse(intent, session, callback);
  } else {
    throw 'Invalid intent';
  }
}

/**
 * Called when the user ends the session.
 * Is not called when the skill returns shouldEndSession=true.
 */
function onSessionEnded(sessionEndedRequest, session) {
  // console.log('onSessionEnded requestId=' + sessionEndedRequest.requestId + ', sessionId=' + session.sessionId);
  // Add cleanup logic here
}




// --------------- A way to store data about the dungeon -----------------------

function setupDungeon(session) {
  var dungeon = new Dungeon();
  session.attributes = {};
  session.attributes.dungeon = dungeon;
}

function Dungeon(player, rooms) {
  this.rooms = rooms || [
    [
      {
        text: 'you enter room 0, 0. ',
        items: ['cat'],
        containers: [
          {
            name: 'chest',
            locked: true,
            items: ['sword']
          }
        ],
        enemies: []
      },
      {
        text: 'you enter room 0, 1. ',
        items: ['golf ball'],
        enemies: []
      }
    ],
    [
      {
        text: 'you enter room 1, 0. ',
        items: [],
        enemies: [
          {
            name: 'troll',
            hp: 100,
            atk: 20,
            def: 8,
            minGold: 20,
            maxGold: 40
          }
        ]
      },
      {
        text: 'you enter room 1, 1. ',
        items: ['key'],
        enemies: []
      }
    ]
  ];

  this.player = player || {
    hp: 100,
    atk: 10,
    def: 3,
    position: {
      x: 0,
      y: 0
    },
    gold: 0,
    items: []
  }

  this.xMax = this.rooms.length;
  this.yMax = this.rooms[0].length;

  this.getAvailableItems = function() {
    var x = this.player.position.x;
    var y = this.player.position.y;

    return this.rooms[x][y].items || [];
  };

  this.getAvailableContainers = function() {
    var x = this.player.position.x;
    var y = this.player.position.y;

    return this.rooms[x][y].containers || [];
  };

  this.removeItem = function(item) {
    var x = this.player.position.x;
    var y = this.player.position.y;

    var items = this.getAvailableItems();
    var index = items.indexOf(item);
    items.splice(index, 1);

    this.rooms[x][y].items = items;
  };

  this.getRoomEntryText = function() {
    var x = this.player.position.x;
    var y = this.player.position.y;

    var text = '';

    text += this.rooms[x][y].text;

    text += this.getRoomLayoutText();

    return text;
  };

  this.getRoomLayoutText = function() {
    var x = this.player.position.x;
    var y = this.player.position.y;

    var text = '';

    if (x - 1 >= 0) { // west is fine
      text += 'There is a door to the west. ';
    }
    if (x + 1 < this.xMax) { // east is fine
      text += 'There is a door to the east. ';
    }
    if (y - 1 >= 0) { // north is fine
      text += 'There is a door to the north. ';
    }
    if (y + 1 < this.yMax) { // south is fine
      text += 'There is a door to the south. ';
    }

    return text;
  };

  this.getRoomLookText = function() {

    var text = '';

    var items = this.getAvailableItems();
    var containers = this.getAvailableContainers();
    var totalLength = containers.length + items.length;

    if (totalLength) {
      text += 'you see ';
    } else {
      return 'You see nothing of use.';
    }

    // get text for items in room
    if (items) {
      for (var itemKey in items) {
        var item = items[itemKey];
        if (itemKey != 0) {
          text += ', ';
        }
        if (itemKey + 1 == totalLength && totalLength != 1) {
          text += 'and a ' + item;
        } else {
          text += 'a ' + item;
        }
      }
    }

    // get text for containers in room
    if (containers) {
      for (var containerKey in containers) {
        var container = containers[containerKey];
        if (containerKey + items.length != 0) {
          text += ', ';
        }
        if (parseInt(containerKey + items.length) + 1 == totalLength && totalLength != 1) {
          text += 'and a ' + container.name;
        } else {
          text += 'a ' + container.name;
        }
      }
    }

    return text;
  };

  this.getInventoryText = function() {

    text = '';

    items = this.player.items || [];

    if (items) {
      text += 'You have ';

      for (var itemKey in items) {
        var item = items[itemKey];
        if (itemKey != 0) {
          text += ', ';
        }
        if (itemKey + 1 == items.length && items.length != 1) {
          text += 'and a ' + item;
        } else {
          text += 'a ' + item;
        }
      }
    } else {
      return 'You hae nothing on you.';
    }

    return text;
  };
}











// --------------- Functions that control the skill's behavior -----------------------

function getWelcomeResponse(callback) {
  var cardTitle = intent.name;
  // If we wanted to initialize the session to have some attributes we could add those here.
  var sessionAttributes = {};
  var speechOutput = 'You find yourself in a dark room.';
  // If the user either does not reply to the welcome message or says something that is not
  // understood, they will be prompted again with this text.
  var repromptText = '';
  var shouldEndSession = false;

  callback(
    sessionAttributes,
    buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession)
  );
}

function getGoResponse(intent, session, callback) {

  // get dungeon data from session
  var dungeon = new Dungeon(session.attributes.dungeon.player, session.attributes.dungeon.rooms);

  var directionSlot = intent.slots.Direction;
  var direction = directionSlot.value;
  var speechOutput = 'You decide to go ' + direction + '. ';

  var moved = false;

  var xPos = dungeon.player.position.x;
  var yPos = dungeon.player.position.y;

  switch (direction) {
    case 'north':
      if (yPos > 0) {
        yPos -= 1;
        moved = true;
      }
      break;
    case 'south':
      if (yPos < dungeon.yMax - 1) {
        yPos += 1;
        moved = true;
      }
      break;
    case 'west':
      if (xPos > 0) {
        xPos -= 1;
        moved = true;
      }
      break;
    case 'east':
      if (xPos < dungeon.xMax - 1) {
        xPos += 1;
        moved = true;
      }
      break;
  }

  dungeon.player.position.x = xPos;
  dungeon.player.position.y = yPos;

  if (moved) {
    speechOutput += dungeon.getRoomEntryText();
  } else {
    speechOutput = 'You cannot travel ' + direction + '. ';
  }

  var cardTitle = intent.name;
  var repromptText = '';
  var shouldEndSession = false;

  var sessionAttributes = {dungeon: dungeon};

  callback(
    sessionAttributes,
    buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession)
  );
}

function getLookResponse(intent, session, callback) {

  // get dungeon data from session
  var dungeon = new Dungeon(session.attributes.dungeon.player, session.attributes.dungeon.rooms);

  var speechOutput = '';

  speechOutput += dungeon.getRoomLookText();
  
  var sessionAttributes = {dungeon: dungeon};

  var repromptText = '';
  var cardTitle = intent.name;
  var shouldEndSession = false;

  callback(
    sessionAttributes,
    buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession)
  );
}

function getGetResponse(intent, session, callback) {

  // get dungeon data from session
  var dungeon = new Dungeon(session.attributes.dungeon.player, session.attributes.dungeon.rooms);

  // get available items in room
  availableItems = dungeon.getAvailableItems();

  var itemSlot = intent.slots.Item;
  var item = itemSlot.value;

  var speechOutput = '';

  if (availableItems.indexOf(item) != -1) {
    speechOutput = 'You grab the ' + item;
    dungeon.player.items.push(item);
    dungeon.removeItem(item);
  } else {
    speechOutput = 'There is no ' + item;
  }

  var cardTitle = intent.name;

  var repromptText = '';
  var shouldEndSession = false;

  var sessionAttributes = {dungeon: dungeon};

  callback(
    sessionAttributes,
    buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession)
  );
}

function getUseResponse(intent, session, callback) {

  // get dungeon data from session
  var dungeon = new Dungeon(session.attributes.dungeon.player, session.attributes.dungeon.rooms);


  var cardTitle = intent.name;
  var speechOutput = '';
  var repromptText = '';
  var shouldEndSession = false;

  var sessionAttributes = {dungeon: dungeon};

  callback(
    sessionAttributes,
    buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession)
  );
}

function getInventoryResponse(intent, session, callback) {

  // get dungeon data from session
  var dungeon = new Dungeon(session.attributes.dungeon.player, session.attributes.dungeon.rooms);

  var speechOutput = '';

  speechOutput = dungeon.getInventoryText();

  var cardTitle = intent.name;
  var repromptText = '';
  var shouldEndSession = false;

  var sessionAttributes = {dungeon: dungeon};

  callback(
    sessionAttributes,
    buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession)
  );
}

function getHelpResponse(intent, session, callback) {

  // get dungeon data from session
  var dungeon = new Dungeon(session.attributes.dungeon.player, session.attributes.dungeon.rooms);

  var speechOutput = 'You are in a dungeon text adventure. Use voice commands to move around, find and use items and fight enemies.';
  speechOutput += ' The available commands are go, look around, get, use, help, quit.';

  console.log(speechOutput);

  var cardTitle = intent.name;
  var repromptText = '';
  var shouldEndSession = false;

  var sessionAttributes = {dungeon: dungeon};

  callback(
    sessionAttributes,
    buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession)
  );
}

function getQuitResponse(intent, session, callback) {

  // get dungeon data from session
  var dungeon = new Dungeon(session.attributes.dungeon.player, session.attributes.dungeon.rooms);

  var cardTitle = intent.name;
  var sessionAttributes = {};
  var speechOutput = '';
  var repromptText = '';
  var shouldEndSession = true;

  callback(
    sessionAttributes,
    buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession)
  );
}

// --------------- Helpers that build all of the responses -----------------------

function buildSpeechletResponse(title, output, repromptText, shouldEndSession) {
  return {
    outputSpeech: {
      type: 'PlainText',
      text: output
    },
    card: {
      type: 'Simple',
      title: 'SessionSpeechlet - ' + title,
      content: 'SessionSpeechlet - ' + output
    },
    reprompt: {
      outputSpeech: {
        type: 'PlainText',
        text: repromptText
      }
    },
    shouldEndSession: shouldEndSession
  };
}

function buildResponse(sessionAttributes, speechletResponse) {
  return {
    version: '1.0',
    sessionAttributes: sessionAttributes,
    response: speechletResponse
  };
}