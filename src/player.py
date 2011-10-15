import pygame.sprite

class Player():
    def __init__(self, name="Neutral Player", controllable=False, initial_mineral=0):
        self.name = name
        self.units = pygame.sprite.RenderClear()
        self.controllable = controllable
        self.mineral = initial_mineral
        self.enemies = None

    def isControllable(self):
        return self.controllable
    
    def getSupply(self):
        supply = 0 
        for unit in self.units:
            supply += unit.supply
        return supply
