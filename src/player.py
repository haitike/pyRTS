from pygame import sprite

class Player():
    def __init__(self, name="Neutral Player", controllable=False, initial_mineral=0, color=(255,255,0), enemies=[]):
        self.name = name
        self.controllable = controllable
        self.mineral = initial_mineral
        self.enemies = enemies
        self.color = color
        self.unitgroup = sprite.Group()

    def isControllable(self):
        return self.controllable
