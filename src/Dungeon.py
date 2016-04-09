class Dungeon:
    """
    The Dungeon class is responsible for storing the data and structure of the
    dungeon.

    It also has helper functions for describing the rooms.
    """

    def __init__(self, data):
        print('Initializing dungeon...')
        self.init_dungeon(data)

    def init_dungeon(self, data):
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
                    'enemies': []
                }
            ],
            # Bottom row.
            [
                {
                    'text': 'you enter room 1, 0. ',
                    'items': [],
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
                    'enemies': []
                },
            ]
        ]

    def get_room_layout_text(self, pos):
        max_x = len(self.data.rooms[0])
        max_y = len(self.data.rooms)

        text = ''

        if pos.x - 1 >= 0:
            text = text + "There is a door to the west. "
        if pos.x + 1 < max_x:
            text = text + "There is a door to the east. "
        if pos.y - 1 >= 0:
            text = text + "There is a door to the north. "
        if pos.x + 1 > max_y:
            text = text + "There is a door to the south. "

        return text
