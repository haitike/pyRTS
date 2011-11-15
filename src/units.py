import math
import pygame
import data

class Unit(pygame.sprite.Sprite):

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
        self.max_hp = 100.0
        self.speed = 1.5

    def unit_init(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.image_file)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.trueX
        self.rect.centery = self.trueY
        self.hp = self.max_hp

    def update(self,players):
        self.rect.centerx = round(self.trueX)
        self.rect.centery = round(self.trueY)
        self.image.blit(self.image, self.rect)

    def changeImage(self,image_file):
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
        return ( (self.max_hp - (self.max_hp - self.hp)) / self.max_hp)

class Worker(Unit):
    supply = 1
    cost = 50
    building_time = 100.0

    def __init__(self, startx,starty,owner):
        Unit.__init__(self,startx,starty,owner)
        self.image_file = data.filepath("worker.png")
        self.image_file2 = data.filepath("worker_with_mineral.png")
        self.id = self.ID_WORKER
        self.name = "Worker"
        self.max_hp = 20.0
        self.type = "unit"
        self.harvest_amount = 10
        self.harvest_time = 100.0
        self.harvest_progress = 0
        self.with_mineral = False
        self.mineral_target = None

        self.unit_init()

    def update(self, players):
        if self.action == self.ID_STOP:
            self.moveX = 0
            self.moveY = 0
        elif self.action == self.ID_MOVE:
            for player in players:
                for unit in player.units:
                    if pygame.sprite.collide_rect(self, unit):
                        if unit.id == self.ID_MINERAL and self.with_mineral == False:
                            self.harvest(unit)
                        elif unit.id == self.ID_CC and unit.owner == self.owner and self.with_mineral == True:
                            self.returnCargo(players[unit.owner])
                        elif self != unit:
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

        elif self.action == self.ID_HARVEST:
            if self.harvest_progress <= 0:
                self.changeImage(self.image_file2)
                self.with_mineral = True
                self.mineral_target.hp -= self.harvest_amount
                self.action = self.ID_STOP
            else:
                self.harvest_progress -= 1.0

        self.rect.centerx = round(self.trueX)
        self.rect.centery = round(self.trueY)
        self.image.blit(self.image, self.rect)

    def move(self,target):
        self.action = self.ID_MOVE
        self.target_location = target

        dx = self.trueX - self.target_location[0]
        dy = self.trueY - self.target_location[1]

        tan = math.atan2(dy,dx) # find angle
        radians = math.radians(math.degrees(tan) + 180) # convert to radians

        self.moveX = math.cos(radians) * self.speed # cosine * speed
        self.moveY = math.sin(radians) * self.speed # sine * speed

    def harvest(self,mineral):
        self.harvest_progress = self.harvest_time
        self.mineral_target = mineral
        self.action = self.ID_HARVEST

    def getHarvestingProgress(self):
        return (self.harvest_time - self.harvest_progress) / self.harvest_time

    def returnCargo(self, player):
        player.mineral += self.harvest_amount
        self.with_mineral = False
        self.changeImage(self.image_file)


class Command_Center(Unit):
    cost = 400
    building_time = 1500.0

    def __init__(self, startx,starty,owner):
        Unit.__init__(self,startx,starty,owner)

        self.image_file =  data.filepath("command_center.png")
        self.id = self.ID_CC
        self.name = "Command_Center"
        self.type = "building"
        self.hp = 250.0

        self.unit_init()

    def update(self, players):
        if self.action == self.ID_STOP:
            pass
        if self.action == self.ID_BUILD:
            if self.building_progress <= 0:
                players[self.owner].units.add(Worker(self.rect.centerx,self.rect.centery+self.rect.height,self.owner))
                self.action = self.ID_STOP
            else:
                self.building_progress -= 1

    def train(self, players):
        if players[self.owner].mineral >= Worker.cost and self.action == self.ID_STOP:
            self.building_progress = Worker.building_time
            self.action = self.ID_BUILD
            players[self.owner].mineral -= Worker.cost
        else:
            sound = pygame.mixer.Sound(data.filepath("beep.wav"))
            sound.play()

    def getBuildingProgress(self):
        return (Worker.building_time - self.building_progress) / Worker.building_time

class Mineral(Unit):
    def __init__(self, startx,starty,owner):
        Unit.__init__(self,startx,starty,owner)

        self.image_file = data.filepath("mineral.png")
        self.id = self.ID_MINERAL
        self.name = "Mineral"
        self.type = "resourse"
        self.hp = 50.0
        self.targetable = False

        self.unit_init()

    def update(self, players):
        if self.hp <= 0:
            self.kill()
