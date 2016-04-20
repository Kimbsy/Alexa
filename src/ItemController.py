class ItemController:
    """The ItemController class is responsible for facilitating the use of items
    by the Player in the Dungeon.

    Mainly it is used to absract complexity away from the IntentManager which
    already has enough to do.
    """

    def __init__(self, dungeon, player):
        self.dungeon = dungeon
        self.player  = player
        self.pos     = player.data['position']

    def use_item(self, item_name):
        """Uses the specified item.

        Returns a string describing the Player using the item.
        """
        if self.player.has_item(item_name):
            activated = self.item_has_use(item_name)
            if activated != False:
                return self.perform_actions(activated, item_name)

    def item_has_use(self, item_name):
        """Determines if the specified item has a use in the room the Player is
        currently in.
        """
        room       = self.dungeon.data[self.pos['z']][self.pos['y']][self.pos['x']]
        items      = room['items']
        containers = room['containers']

        for item in items:
            if 'activators' in item:
                for activator in item['activators']:
                    if activator == item_name:
                        return item

        for container in containers:
            if 'activators' in container:
                for activator in container['activators']:
                    if activator == item_name:
                        return container

        return False

    def perform_actions(self, activated, activator):
        """Performs the actions requireb by using the activator item on the
        activated item.
        
        Basically a giant switch based on the activator item and activated item
        """
        response = 'you use the ' + activator + ' on the ' + activated['name'] + '. '

        # @TODO: dis can haz logics
        
        return response
