import math
import pygame
import tools, game_data, groups
from animations import *

# Sprite _Layers
#  2) Blockers/Obtacles  3) Buildings  4) Units

class BaseObject(pygame.sprite.Sprite):

    # ACTIONS IDS
    ID_STOP, ID_MOVE, ID_ATTACK, ID_ATTACK_MOVE = range(4)

    # UNIT TYPE IDS
    ID_UNIT, ID_BUILDING, ID_NEUTRALSTUFF, ID_HERO  = range(4)

    # UNIT IDS
    ID_MINERAL = 0
    ID_NEXUS = 20
    ID_TURRET = 21
    ID_MINION = 50
    ID_RANGEDMINION = 51
    ID_TANK = 80

    def __init__(self, startx,starty,owner=None):
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
        self.size = 2
        self.max_hp = 100
        self.hp_regeneration = 0.0
        self.speed = 0
        self.damage = 0
        self.range = 100
        self.armor = 0
        self.attack_speed = 1
        self.vision = 150

    def unit_init(self):
        self.groups = groups.unitgroup, groups.allgroup, self.owner.unitgroup
        self._layer = 2
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.base_image = pygame.image.load(self.image_file)
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.centerx = round(self.trueX + game_data.camera[0])
        self.rect.centery = round(self.trueY + game_data.camera[1])
        self.hp = self.max_hp

    def update(self, seconds):
        if self.hp < self.max_hp: self.hp += self.hp_regeneration
        else: self.hp = self.max_hp

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
        pressed = False
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        pressed = True
        return pressed

    def getLifeBar(self):
        life = (self.max_hp - (self.max_hp - self.hp)) / float(self.max_hp)
        if life > 0: return life
        else: return 0
        
    def getEnemyDistance(self, enemy):
        if enemy != None: return math.sqrt((self.trueX - enemy.trueX) **2 + (self.trueY - enemy.trueY)**2)
        else: return None

    def getNewEnemy(self):
        units_in_range = []
        for enemy in self.owner.enemies:
            for target in enemy.unitgroup:
                if target != self and target.targetable == True:
                    if self.getEnemyDistance(target) < self.vision:
                        units_in_range.append((self.getEnemyDistance(target),target))
        if units_in_range == []:
            return None
        else:
            return sorted(units_in_range)[0][1]


class NeutralStuff(BaseObject):
    def __init__(self, startx,starty,owner=0):
        BaseObject.__init__(self,startx,starty,owner)
        self.type = self.ID_NEUTRALSTUFF
        self.targetable = False
        self.size = 3

class Building(BaseObject):
    def __init__(self, startx,starty,owner,creation_point=None,target_point=None):
        BaseObject.__init__(self,startx,starty,owner)
        self.type = self.ID_BUILDING
        self.build_timer = 0
        self.build_speed = 1
        self.unit_trained = None
        self.creation_point = creation_point
        self.target_point = target_point
        self.size = 3
        self._layer = 3

    def update(self,seconds):
        BaseObject.update(self,seconds)
        if self.unit_trained != None:
            self.build_timer += self.build_speed
            if self.build_timer > 200:
                newUnit = self.unit_trained(self.creation_point[0],self.creation_point[1],self.owner)
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
        self._layer = 4

    def update(self, seconds):
        BaseObject.update(self,seconds)
        if self.attack_timer <= 30: self.attack_timer += self.attack_speed
        if self.action == self.ID_STOP:
            self.target_enemy = self.getNewEnemy()
            if self.target_enemy == None:
                self.moveX = 0
                self.moveY = 0
                self.target_location = self.trueX, self.trueY
                self.attack_move_location = self.trueX, self.trueY
            else:
                self.action = self.ID_ATTACK
        elif self.action == self.ID_MOVE:
            self.update_move()
        elif self.action == self.ID_ATTACK:
            self.update_attack()
        elif self.action == self.ID_ATTACK_MOVE:
            self.target_enemy = self.getNewEnemy()
            if self.target_enemy == None:
                self.update_move()
            else:
                self.update_attack()

    def update_move(self):
            for unit in groups.unitgroup:
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

    def update_attack(self):
        if self.getEnemyDistance(self.target_enemy) < self.range:
            self.move((self.target_enemy.trueX, self.target_enemy.trueY), self.action)
            if self.attack_timer > 30:
                self.AttackAnimation(self, self.target_enemy ,self.damage, self.range )
                self.attack_timer = 0
        else:
            self.move((self.target_enemy.trueX, self.target_enemy.trueY), self.action)
            self.update_move()
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

class Hero(Unit):
    def __init__(self, startx,starty,owner=0):
        Unit.__init__(self,startx,starty,owner)
        #self.type = self.ID_HERO
        self.size = 4
        self.vision = 300
        self.hp_regeneration = 0.005
        self.level = 1
        self.exp = 0
        
