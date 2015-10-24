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
  } else if ('ExitIntent' === intentName) {
    getExitResponse(intent, session, callback);
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
  // dungeon.xMax = dungeon.rooms.length;
  // dungeon.yMax = dungeon.rooms[0].length;

  session.attributes = {};
  session.attributes.dungeon = dungeon;
}

function Dungeon(player) {
  this.rooms = [
    [
      {
        text: 'you enter room 0, 0',
        items: ['sword']
      },
      {
        text: 'you enter room 0, 1',
        items: ['golf ball']
      }
    ],
    [
      {
        text: 'you enter room 1, 0',
        items: []
      },
      {
        text: 'you enter room 1, 1',
        items: ['key']
      }
    ]
  ];

  this.player = player || {
    position: {
      x: 0,
      y: 0
    }
  }

  this.xMax = this.rooms.length;
  this.yMax = this.rooms[0].length;

  this.getRoomText = function() {
    x = this.player.position.x;
    y = this.player.position.y;

    return this.rooms[x][y].text;
  };

  this.getAvailableItems = function() {
    x = this.player.position.x;
    y = this.player.position.y;

    return this.rooms[x][y].items;
  };
}











// --------------- Functions that control the skill's behavior -----------------------

function getGoResponse(intent, session, callback) {

  // get dungeon data from session
  var dungeon = new Dungeon(session.attributes.dungeon.player);

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
    speechOutput += dungeon.getRoomText();
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
  var dungeon = new Dungeon(session.attributes.dungeon.player);


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

function getGetResponse(intent, session, callback) {

  // get dungeon data from session
  var dungeon = new Dungeon(session.attributes.dungeon.player);

  // get available items in room
  availableItems = dungeon.getAvailableItems();

  var itemSlot = intent.slots.Item;
  var item = itemSlot.value;

  var speechOutput = '';

  if (availableItems.indexOf(item) != -1) {
    speechOutput = 'You grab the ' + item;
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
  var dungeon = new Dungeon(session.attributes.dungeon.player);


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

function getHelpResponse(intent, session, callback) {


  var cardTitle = intent.name;
  var speechOutput = '';
  var repromptText = '';
  var shouldEndSession = false;

  callback(
    sessionAttributes,
    buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession)
  );
}

function getExitResponse(intent, session, callback) {


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

// /**
//  * Sets the color in the session and prepares the speech to reply to the user.
//  */
// function setColorInSession(intent, session, callback) {
//   var cardTitle = intent.name;
//   var favoriteColorSlot = intent.slots.Color;
//   var repromptText = '';
//   var sessionAttributes = {};
//   var shouldEndSession = false;
//   var speechOutput = '';

//   if (favoriteColorSlot) {
//     favoriteColor = favoriteColorSlot.value;
//     sessionAttributes = createFavoriteColorAttributes(favoriteColor);
//     speechOutput = 'I now know your favorite color is ' + favoriteColor + '. You can ask me '+ 'your favorite color by saying, what's my favorite color?';
//     repromptText = 'You can ask me your favorite color by saying, what's my favorite color?';
//   } else {
//     speechOutput = 'I\'m not sure what your favorite color is, please try again';
//     repromptText = 'I\'m not sure what your favorite color is, you can tell me your '+ 'favorite color by saying, my favorite color is red';
//   }

//   callback(
//     sessionAttributes,
//     buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession)
//   );
// }

// function createFavoriteColorAttributes(favoriteColor) {
//   return {
//       favoriteColor: favoriteColor
//   };
// }

// function getColorFromSession(intent, session, callback) {
//   var cardTitle = intent.name;
//   var favoriteColor;
//   var repromptText = null;
//   var sessionAttributes = {};
//   var shouldEndSession = false;
//   var speechOutput = '';

//   if(session.attributes) {
//     favoriteColor = session.attributes.favoriteColor;
//   }

//   if(favoriteColor) {
//     speechOutput = 'Your favorite color is ' + favoriteColor + ', goodbye';
//     shouldEndSession = true;
//   }
//   else {
//     speechOutput = 'I\'m not sure what your favorite color is, you can say, my favorite color '+ ' is red';
//   }

//   // Setting repromptText to null signifies that we do not want to reprompt the user.
//   // If the user does not respond or says something that is not understood, the session
//   // will end.
//   callback(
//     sessionAttributes,
//     buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession)
//   );
// }

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
