import math
import pygame
import data
from animations import *

class BaseObject(pygame.sprite.Sprite):

    # ACTIONS IDS
    ID_STOP, ID_MOVE, ID_ATTACK = range(3)

    # UNIT TYPE IDS
    ID_UNIT, ID_BUILDING, ID_NEUTRALSTUFF, ID_CHASING = range(4)

    # UNIT IDS
    ID_MINERAL = 0
    ID_CC = 20
    ID_MINION = 50
    ID_RANGEDMINION = 51
    
    def __init__(self, startx,starty,owner=0):
        self.image_file = data.filepath("placeholder.png")

        # Unit Tecnical Stuff
        self.trueX = float(startx)
        self.trueY = float(starty)
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
        self.attack_speed = 1

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

class NeutralStuff(BaseObject):
    def __init__(self, startx,starty,owner=0):
        BaseObject.__init__(self,startx,starty,owner)
        self.type = self.ID_NEUTRALSTUFF
        self.targetable = False

class Building(BaseObject):
    def __init__(self, startx,starty,owner=0):
        BaseObject.__init__(self,startx,starty,owner)
        self.type = self.ID_BUILDING

class Unit(BaseObject):
    def __init__(self, startx,starty,owner=0):
        BaseObject.__init__(self,startx,starty,owner)
        self.AttackAnimation = MinionAttack
        self.type = self.ID_UNIT    
        self.target_location = self.trueX, self.trueY
        self.timer = 0
        self.target_enemy = None
        
    def update(self, players):
        BaseObject.update(self,players)
        
        if self.action == self.ID_STOP:
            self.moveX = 0
            self.moveY = 0
        elif self.action == self.ID_MOVE:
            for player in players:
                for unit in player.units:
                    if pygame.sprite.collide_rect(self, unit):
                        if self != unit:
                            self.action = self.ID_STOP
                        else:
                            dlength = math.sqrt((self.trueX - self.target_location[0]) **2 + (self.trueY - self.target_location[1])**2)
                            if dlength < self.speed:
                                self.trueX = self.target_location[0]
                                self.trueY = self.target_location[1]
                                self.action = self.ID_STOP
                            else:
                                self.trueX += self.moveX
                                self.trueY += self.moveY
        elif self.action == self.ID_ATTACK:
            if self.target_enemy.alive() == False:
                self.action = self.ID_STOP 
            self.timer += self.attack_speed
            if self.timer > 30:
                players[self.owner].animations.add(self.AttackAnimation(self, self.target_enemy ,self.damage ))
                self.timer = 0
        elif self.action == self.ID_CHASING:     
            pass

    def move(self,target):
        self.action = self.ID_MOVE
        self.target_location = target

        dx = self.trueX - self.target_location[0]
        dy = self.trueY - self.target_location[1]

        tan = math.atan2(dy,dx) # find angle
        self.image = pygame.transform.rotate(self.base_image, math.degrees(tan*-1)+90)
        radians = math.radians(math.degrees(tan) + 180) # convert to radians

        self.moveX = math.cos(radians) * self.speed # cosine * speed
        self.moveY = math.sin(radians) * self.speed # sine * speed

    def attack(self,target_unit):
        self.target_enemy = target_unit
        self.move(target_unit.rect)
        self.action = self.ID_ATTACK

class Hero(Unit):
    pass
