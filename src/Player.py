class Player:
    """The Player class is responsible for storing the status of the player as well
    as any items they might have.
    """

    def __init__(self, data):
        print('Initializing player...')
        self.init_player(data)

    def init_player(self, data):
        """Initialises the data structure of the Player object, 'data' argument
        can be used to populate player data from session data.
        """
        self.data = data or {
            'name'    : 'Anon',
            'hp'      : 100,
            'attack'  : 5,
            'defense' : 2,
            'gold'    : 0,
            'position': {
                'x': 0,
                'y': 0,
            },
            'items': [
                {'name': 'small pocket knife'},
                {'name': 'apple'},
            ],
        }

    def get_inventory_text(self):
        """Creates a string listing the items in the PLayer's inventory.
        """
        text = 'You have '

        items = self.data['items']

        if len(items):
            for i, item in enumerate(items):
                if i:
                    text = text + ', '
                if i + 1 == len(items):
                    text = text + 'and a ' + item['name']
                else:
                    text = text + 'a ' + item['name']
        else:
            text = 'You have nothing in your inventory.'

        return text

    def add_item(self, item):
        """Adds an item to the Player's inventory.
        """
        self.data['items'].append(item)
