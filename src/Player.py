class Player:
    """
    The Player class is responsible for storing the status of the player as well
    as any items they might have.
    """

    def __init__(self, data):
        print('Initializing player...')
        self.init_player(data)

    def init_player(self, data):
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
            'items': [],
        }

    def get_inventory_text(self):
        text = ''

        if len(self.data['items']):
            for i, item in enumerate(self.data['items']):
                if i:
                    text = text + ', '
                if i + 1 == len(self.data['items']):
                    text = text + 'and a ' + item.name
                else:
                    text = text + 'a ' + item.name
        else:
            text = 'You have nothing on you.'

        return text
