import math
import pygame
import data

class BaseUnit(pygame.sprite.Sprite):

    # ACTIONS IDS
    ID_STOP, ID_MOVE, ID_BUILD, ID_HARVEST = range(4)

    # UNIT TYPES IDS
    ID_MINERAL = 0
    ID_CC = 20
    ID_WORKER = 50

    # STATIC ATRIBUTES
    supply = 0
    cost = 0
    building_time = 0.0

    def __init__(self, startx,starty,owner=0):
        self.image_file = data.filepath("placeholder.png")

        # Unit Tecnical Stuff
        self.trueX = float(startx)
        self.trueY = float(starty)
        self.target_location = self.trueX, self.trueY
        self.moveX = 0.0
        self.moveY = 0.0

        # Some Values
        self.owner = owner
        self.id = None
        self.name = None
        self.type = None
        self.selected = False
        self.targetable = True
        self.action = self.ID_STOP

        # Unit Atributes
        self.max_hp = 100
        self.speed = 0
        self.damage = 0

    def unit_init(self):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = pygame.image.load(self.image_file)
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.centerx = self.trueX
        self.rect.centery = self.trueY
        self.hp = self.max_hp

    def update(self,players):
        self.rect.centerx = round(self.trueX)
        self.rect.centery = round(self.trueY)
        self.image.blit(self.image, self.rect)
        
        if self.hp <= 0:
            self.kill()

    def changeImage(self,image_file):
        self.base_image = pygame.image.load(image_file)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()

    def isPressed(self,mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False

    def getLifeBar(self):
        return  (self.max_hp - (self.max_hp - self.hp)) / float(self.max_hp)

class Building(BaseUnit):
    pass

class Unit(BaseUnit):
    def move(self,target):
        self.image = pygame.transform.rotate(self.image,180)
        self.action = self.ID_MOVE
        self.target_location = target

        dx = self.trueX - self.target_location[0]
        dy = self.trueY - self.target_location[1]

        tan = math.atan2(dy,dx) # find angle
        self.image = pygame.transform.rotate(self.base_image, math.degrees(tan*-1)+90)
        radians = math.radians(math.degrees(tan) + 180) # convert to radians

        self.moveX = math.cos(radians) * self.speed # cosine * speed
        self.moveY = math.sin(radians) * self.speed # sine * speed

    def attack(self,target):
        pass    

class Hero(Unit):
    pass
