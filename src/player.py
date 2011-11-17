import pygame.sprite

class Player():
    def __init__(self, name="Neutral Player", controllable=False, initial_gold=0):
        self.name = name
        self.units = pygame.sprite.RenderClear()
        self.animations = pygame.sprite.RenderClear()
        self.controllable = controllable
        self.gold = initial_gold
        self.enemies = None

    def isControllable(self):
        return self.controllable