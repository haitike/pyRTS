from pygame import sprite

class Player():
    def __init__(self, name="Neutral Player", controllable=False, initial_gold=0, color=(255,255,0), enemies=None):
        self.name = name
        self.controllable = controllable
        self.gold = initial_gold
        self.enemies = enemies
        self.color = color
        self.unitgroup = sprite.Group()

    def isControllable(self):
        return self.controllable