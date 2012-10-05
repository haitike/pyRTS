from pygame import sprite
from ids import *

class Player():
    def __init__(self, name="Neutral Player", controllable=False, initial_mineral=0, color=(255,255,0), enemies=[]):
        self.name = name
        self.controllable = controllable
        self.mineral = initial_mineral
        self.enemies = enemies
        self.color = color
        self.unitgroup = sprite.Group()
        self.supply = 0
        self.max_supply = 0
        self.update()

    def isControllable(self):
        return self.controllable

    def update(self):
        self.supply = 0
        for unit in self.unitgroup:
            if ID_UNIT in unit.types:
                self.supply += unit.supply_cost
                
        self.max_supply = 0
        for unit in self.unitgroup:
            if ID_BUILDING in unit.types:
                self.max_supply += unit.extra_max_supply
