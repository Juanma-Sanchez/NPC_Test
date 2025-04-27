class Player:
    def __init__(self, strength:int, constitution:int, intelligence:int, agility:int, luck:int):
        self.stregnth = strength
        self.constitution = constitution
        self.intelligence = intelligence
        self.agility = agility
        self.luck = luck
        self.inventory = []

    def obtain(self, item):
        self.inventory.append(item)