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
            # Past.
            [
                # Top row.
                [
                    {
                        'entry_text': 'you enter room 0 0 0. It is in the past. ',
                        'exits': [
                            'east',
                            'south',
                        ],
                        'items': [],
                        'containers': [],
                    },
                    {
                        'entry_text': 'you enter room 0 0 1. It is in the past. ',
                        'exits': [
                            'west',
                            'south',
                        ],
                        'items': [],
                        'containers': [],
                    }
                ],
                # Bottom row.
                [
                    {
                        'entry_text': 'you enter room 0 1 0. It is in the past. ',
                        'exits': [
                            'east',
                            'north',
                        ],
                        'items': [
                            {
                                'name': 'portal',
                                'directions': [
                                    'future'
                                ],
                                'activators': [
                                    'sword of time'
                                ],
                            },
                        ],
                        'containers': [],
                    },
                    {
                        'entry_text': 'you enter room 0 1 1. It is in the past. ',
                        'exits': [
                            'west',
                            'north',
                        ],
                        'items': [],
                        'containers': [],
                    }
                ],
            ],
            # Present.
            [
                # Top row.
                [
                    {
                        'entry_text': 'you enter room 1 0 0. ',
                        'exits': [
                            'east',
                            'south',
                        ],
                        'items': [
                            {'name': 'cat'},
                        ],
                        'containers': [
                            {
                                'name': 'chest',
                                'locked': True,
                                'items': [
                                    {'name': 'sword of time'},
                                ],
                                'activators': [
                                    'key',
                                ],
                            },
                        ],
                    },
                    {
                        'entry_text': 'you enter room 1 0 1. ',
                        'exits': [
                            'west',
                            'south',
                        ],
                        'items': [
                            {
                                'name': 'portal',
                                'directions': [
                                    'past'
                                ],
                                'activators': [
                                    'sword of time'
                                ],
                            },                        ],
                        'containers': [],
                    }
                ],
                # Bottom row.
                [
                    {
                        'entry_text': 'you enter room 1 1 0. ',
                        'exits': [
                            'east',
                            'north',
                        ],
                        'items': [],
                        'containers': [],
                    },
                    {
                        'entry_text': 'you enter room 1 1 1. ',
                        'exits': [
                            'west',
                            'north',
                        ],
                        'items': [
                            {'name': 'key'},
                        ],
                        'containers': [],
                    },
                ]
            ],
            # Future
            []
        ]

    def move_is_allowed(self, pos, direction):
        """Determines if a move from a position in a specified direction is
        allowed by the layout of the dungeon.
        """

        allowed = False

        room = self.data[pos['z']][pos['y']][pos['x']]

        for exit in room['exits']:
            if exit == direction:
                allowed = True

        # check if door is locked?

        return allowed

    def get_room_entry_text(self, pos):
        """Creates a string describing your entrance into the room, follwed by
        the available exits from the room, followed by the items and containers
        visible in the room.
        """
        text = self.data[pos['z']][pos['y']][pos['x']]['entry_text']

        text = text + self.get_room_layout_text(pos)

        text = text + self.get_room_look_text(pos)

        return text

    def get_room_layout_text(self, pos):
        """Creates a string describing the available exits from the room.
        """

        room = self.data[pos['z']][pos['y']][pos['x']]

        text = ''

        for exit in room['exits']:
            text = text + 'There is a door to the ' + exit + '. '

        return text

    def get_room_look_text(self, pos):
        """Creates a string listing the items and containers visible in the
        room.
        """
        text = ''

        # Get total number of things in room.
        room       = self.data[pos['z']][pos['y']][pos['x']]
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
            description = ''
            if container['locked']:
                description = description + 'locked '
            description = description + container['name']

            if i:
                text = text + ', '
            if i + len(items) + 1 == total_num and total_num != 1:
                text = text + 'and a ' + description
            else:
                text = text + 'a ' + description

            if not container['locked'] and len(container['items']):
                text = text + ' with '
                for i, container_item in enumerate(container['items']):
                    if i:
                        text = text + ', '
                    if i + 1 == total_num and total_num != 1:
                        text = text + 'and a ' + container_item['name']
                    else:
                        text = text + 'a ' + container_item['name']
                        text = text + ' inside'

        text = text + '. '

        return text

    def item_is_available(self, want_item, pos):
        """Determines whether a named item is available to the player in a room
        at a specified position.
        """
        room       = self.data[pos['z']][pos['y']][pos['x']]
        items      = room['items']
        containers = room['containers']
        available  = False

        for container in containers:
            if not container['locked']:
                items = items + container['items']

        for item in items:
            if item['name'] == want_item:
                available = True

        return available

    def take_item(self, want_item, pos):
        """Removes and returns the data for a named item in the room at a
        specified position.
        """
        room = self.data[pos['z']][pos['y']][pos['x']]

        items      = room['items']
        containers = room['containers']

        removed_item = None

        for item in items:
            if item['name'] == want_item:
                self.data[pos['z']][pos['y']][pos['x']]['items'].remove(item)
                removed_item = item

        if not removed_item:
            for c_index, container in enumerate(containers):
                container_items = container['items']
                for container_item in container_items:
                    if container_item['name'] == want_item:
                        self.data[pos['z']][pos['y']][pos['x']]['containers'][c_index]['items'].remove(container_item)
                        removed_item = container_item

        return removed_item
