import math
import pygame
import tools, game_data
from animations import *

class BaseObject(pygame.sprite.Sprite):

    # ACTIONS IDS
    ID_STOP, ID_MOVE, ID_ATTACK = range(3)

    # UNIT TYPE IDS
    ID_UNIT, ID_BUILDING, ID_NEUTRALSTUFF, ID_ATTACK_MOVE = range(4)

    # UNIT IDS
    ID_MINERAL = 0
    ID_CC = 20
    ID_MINION = 50
    ID_RANGEDMINION = 51

    def __init__(self, startx,starty,owner=0):
        self.image_file = tools.filepath("placeholder.png")

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
        self.range = 100
        self.armor = 0
        self.attack_speed = 1
        self.vision = 150

    def unit_init(self):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = pygame.image.load(self.image_file)
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.centerx = round(self.trueX + game_data.camera[0])
        self.rect.centery = round(self.trueY + game_data.camera[1])
        self.hp = self.max_hp

    def update(self,players):
        self.rect.centerx = round(self.trueX + game_data.camera[0])
        self.rect.centery = round(self.trueY + game_data.camera[1])
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
    def __init__(self, startx,starty,owner,creation_point,target_point):
        BaseObject.__init__(self,startx,starty,owner)
        self.type = self.ID_BUILDING
        self.build_timer = 0
        self.build_speed = 1
        self.unit_trained = None
        self.creation_point = creation_point
        self.target_point = target_point

    def update(self,players):
        BaseObject.update(self,players)
        self.build_timer += self.build_speed
        if self.build_timer > 200:
            newUnit = self.unit_trained(self.creation_point[0],self.creation_point[1],self.owner)
            players[self.owner].units.add(newUnit)
            newUnit.attack_move(self.target_point)
            self.build_timer = 0

class Unit(BaseObject):
    def __init__(self, startx,starty,owner=0):
        BaseObject.__init__(self,startx,starty,owner)
        self.AttackAnimation = MinionAttack
        self.type = self.ID_UNIT
        self.target_location = self.trueX, self.trueY
        self.attack_timer = 30
        self.target_enemy = None
        self.attack_move_location = self.trueX, self.trueY

    def update(self, players):
        BaseObject.update(self,players)
        if self.attack_timer <= 30: self.attack_timer += self.attack_speed
        if self.action == self.ID_STOP:
            self.moveX = 0
            self.moveY = 0
            self.target_location = self.trueX, self.trueY
            self.attack_move_location = self.trueX, self.trueY
            self.target_enemy = None
        elif self.action == self.ID_MOVE:
            self.update_move(players)
        elif self.action == self.ID_ATTACK:
            self.update_attack(players)
        elif self.action == self.ID_ATTACK_MOVE:
            self.target_enemy = self.getNewEnemy(players)
            if self.target_enemy == None:
                self.update_move(players)
            else:
                self.update_attack(players)

    def update_move(self,players):
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

    def update_attack(self,players):
        if self.getEnemyDistance(self.target_enemy) < self.range:
            self.move((self.target_enemy.trueX, self.target_enemy.trueY), self.action)
            if self.attack_timer > 30:
                players[self.owner].animations.add(self.AttackAnimation(self, self.target_enemy ,self.damage, self.range ))
                self.attack_timer = 0
        else:
            self.move((self.target_enemy.trueX, self.target_enemy.trueY), self.action)
            self.update_move(players)
        if self.target_enemy.alive() == False:
            if self.action == self.ID_ATTACK_MOVE: self.target_location = self.attack_move_location
            else: self.action = self.ID_STOP

    def move(self,target, act_type=1): # 1 = Move
        self.action = act_type
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
        self.action = self.ID_ATTACK

    def attack_move(self, target):
        self.attack_move_location = target
        self.target_location = target
        self.move(target,3)
        self.action = self.ID_ATTACK_MOVE

    def getEnemyDistance(self, enemy):
        if enemy != None: return math.sqrt((self.trueX - enemy.trueX) **2 + (self.trueY - enemy.trueY)**2)
        else: return None

    def getNewEnemy(self,players):
        units_in_range = []
        for index in range(len(players)):
            if index in players[self.owner].enemies:
                for target in players[index].units:
                    if target != self and target.targetable == True:
                        if self.getEnemyDistance(target) < self.vision:
                            units_in_range.append((self.getEnemyDistance(target),target))
        if units_in_range == []:
            return None
        else:
            return sorted(units_in_range)[0][1]


class Hero(Unit):
    pass
