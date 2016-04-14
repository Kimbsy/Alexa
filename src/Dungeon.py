class Dungeon:
    """The Dungeon class is responsible for storing the data and structure of the
    dungeon.

    It also has helper functions for describing the rooms.
    """

    def __init__(self, data):
        print('Initializing dungeon...')
        self.init_dungeon(data)

    def init_dungeon(self, data):
        """Initialises the data structure of the Dungeon object, 'data' argument
        can be used to populate dungeon data from session data.
        """
        self.data = data or [
            # Top row.
            [
                {
                    'text': 'you enter room 0, 0. ',
                    'items': [
                        {'name': 'cat'},
                    ],
                    'containers': [
                        {
                            'name': 'chest',
                            'locked': True,
                            'items': [
                                {'name': 'sword'},
                            ]
                        }
                    ],
                    'enemies': []
                },
                {
                    'text': 'you enter room 0, 1. ',
                    'items': [
                        {'name': 'golf ball'},
                    ],
                    'containers': [],
                    'enemies': []
                }
            ],
            # Bottom row.
            [
                {
                    'text': 'you enter room 1, 0. ',
                    'items': [],
                    'containers': [],
                    'enemies': [
                        {
                            'name': 'troll',
                            'hp': 100,
                            'attack': 20,
                            'defense': 8,
                            'minGold': 20,
                            'maxGold': 40
                        }
                    ]
                },
                {
                    'text': 'you enter room 1, 1. ',
                    'items': [
                        {'name': 'key'},
                    ],
                    'containers': [],
                    'enemies': []
                },
            ]
        ]

    def move_is_allowed(self, pos, direction):
        """Determines if a move from a position in a specified direction is
        allowed by the layout of the dungeon.
        """

        # @TODO: Make this based on a list of rooms each room connects to.

        max_x = len(self.data[0])
        max_y = len(self.data)

        allowed = True

        if direction == 'north':
            if pos['y'] - 1 < 0:
                allowed = False
        if direction == 'south':
            if pos['y'] + 1 >= max_y:
                allowed = False
        if direction == 'east':
            if pos['x'] + 1 >= max_x:
                allowed = False
        if direction == 'west':
            if pos['x'] - 1 < 0:
                allowed = False

        # check if door is locked?

        return allowed

    def get_room_entry_text(self, pos):
        """Creates a string describing your entrance into the room, follwed by
        the available exits from the room, followed by the items and containers
        visible in the room.
        """
        text = self.data[pos['y']][pos['x']]['text']

        text = text + self.get_room_layout_text(pos)

        text = text + self.get_room_look_text(pos)

        return text

    def get_room_layout_text(self, pos):
        """Creates a string describing the available exits from the room.
        """

        # @TODO Make this based on a list of rooms each room connects to.

        max_x = len(self.data[0])
        max_y = len(self.data)

        text = ''

        if pos['y'] - 1 >= 0:
            text = text + 'There is a door to the north. '
        if pos['y'] + 1 < max_y:
            text = text + 'There is a door to the south. '
        if pos['x'] + 1 < max_x:
            text = text + 'There is a door to the east. '
        if pos['x'] - 1 >= 0:
            text = text + 'There is a door to the west. '

        return text

    def get_room_look_text(self, pos):
        """Creates a string listing the items and containers visible in the
        room.
        """
        text = ''

        # Get total number of things in room.
        room       = self.data[pos['y']][pos['x']]
        items      = room['items']
        containers = room['containers']

        total_num = len(items) + len(containers)

        # Decide start of phrase.
        if total_num:
            text = text + 'You see '
        else:
            text = text + 'You see nothing of use. '

        # Get text for items in room
        for i, item in enumerate(items):
            if i:
                text = text + ', '
            if i + 1 == total_num and total_num != 1:
                text = text + 'and a ' + item['name']
            else:
                text = text + 'a ' + item['name']

        if len(containers):
            text = text + ' '

        # Get text for containers in room.
        for i, container in enumerate(containers):
            if i:
                text = text + ', '
            if i + len(items) + 1 == total_num and total_num != 1:
                text = text + 'and a ' + container['name']
            else:
                text = text + 'a ' + container['name']

        text = text + '. '

        return text

    def item_is_available(self, want_item, pos):
        """Determines whether a named item is available to the player in a room
        at a specified position.
        """
        room       = self.data[pos['y']][pos['x']]
        items      = room['items']
        containers = room['containers']
        available  = False

        for container in containers:
            if not container['locked']:
                items = items + containers['items']

        for item in items:
            print(item['name'])
            print(want_item)
            if item['name'] == want_item:
                available = True

        return available

    def take_item(self, want_item, pos):
        """Removes and returns the data for a named item in the room at a
        specified position.
        """
        room = self.data[pos['y']][pos['x']]

        items = room['items']

        for item in items:
            if item['name'] == want_item:
                self.data[pos['y']][pos['x']]['items'].remove(item)
                return item

