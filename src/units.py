import math
import pygame
from constants import *
import data

class Unit(pygame.sprite.Sprite):    

    image_file = data.filepath("placeholder.png")
    
    owner = None
    id = None
    name = None
    
    trueX = 0.0 # Float Positions
    trueY = 0.0
    
    speed = 1.5 # Default General Speed for all units
    moveX = 0.0  # moveX and moveY are temporal speed variables for diagonals and such.
    moveY = 0.0

    action = actions.STOP   # Unit action begins in 0 (Stopeed)
    hp = 0
    supply = 0
    cost = 0
    building_time = 0
    building_progress = 0
    
    type = None
    selected = False
    targetable = True

    def __init__(self, startx,starty,owner):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.image_file)
        self.rect = self.image.get_rect()
        self.rect.centerx = startx
        self.rect.centery = starty
        self.trueX, self.trueY = float(startx) , float(starty)
        self.target_location = self.trueX, self.trueY
        self.owner = owner

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

class Worker(Unit):
    image_file = data.filepath("worker.png")
    image_file2 = data.filepath("worker_with_mineral.png")
    id = u_id.WORKER
    name = "Worker"
    hp = 20
    supply = 1
    cost = 50
    type = "unit"
    building_time = 100.0
    harvest_amount = 10
    harvest_time = 100.0
    harvest_progress = 0
    with_mineral = False
    mineral_target = None
    
    def update(self, players):                
        if self.action == actions.STOP:
            pass
        elif self.action == actions.MOVE:
            future_rect = pygame.Rect(self.rect)
            future_rect = future_rect.move(self.moveX,self.moveY)
            for player in players:
                for unit in player.units:
                    if future_rect.colliderect(unit.rect):            
                        if unit.id == u_id.MINERAL and self.with_mineral == False:
                            self.harvest(unit)
                        elif unit.id == u_id.CC and unit.owner == self.owner and self.with_mineral == True:
                            self.returnCargo(players[unit.owner]) 
                        elif self != unit:
                            self.action = actions.STOP
            if self.action == actions.MOVE:
                dlength = math.sqrt((self.trueX - self.target_location[0]) **2 + (self.trueY - self.target_location[1])**2)
                if dlength < self.speed:
                    self.trueX = self.target_location[0]
                    self.trueY = self.target_location[1]                
                    self.action = actions.STOP
                else:
                    self.trueX += self.moveX
                    self.trueY += self.moveY        
        
        
        elif self.action == actions.HARVEST:
            if self.harvest_progress <= 0:
                self.changeImage(self.image_file2)
                self.with_mineral = True
                self.mineral_target.hp -= self.harvest_amount
                self.action = actions.STOP
            else:
                self.harvest_progress -= 1.0
        
        self.rect.centerx = round(self.trueX) 
        self.rect.centery = round(self.trueY)
        self.image.blit(self.image, self.rect)
    
    def move(self,target):
        self.action = actions.MOVE
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
        self.action = actions.HARVEST
        
    def getHarvestingProgress(self):
        return ( (self.harvest_time - self.harvest_progress) / self.harvest_time)
    
    def returnCargo(self, player):
        player.mineral += self.harvest_amount
        self.with_mineral = False
        self.changeImage(self.image_file)
        
    
class Command_Center(Unit):
        image_file =  data.filepath("command_center.png")
        id = u_id.CC
        name = "Command_Center"
        type = "building"
        hp = 250
        cost = 400
        building_time = 1500.0
        
        def update(self, players):
            if self.action == actions.STOP:
                pass
            if self.action == actions.BUILD:
                if self.building_progress <= 0:
                    players[self.owner].units.add(Worker(self.rect.centerx,self.rect.centery+self.rect.height,self.owner))
                    self.action = actions.STOP
                else:
                    self.building_progress -= 1
                    
        def train(self, players):
            if players[self.owner].mineral >= Worker.cost and self.action == actions.STOP:
                self.building_progress = Worker.building_time
                self.action = actions.BUILD
                players[self.owner].mineral -= Worker.cost
            else:
                sound = pygame.mixer.Sound(data.filepath("beep.wav"))
                sound.play()
        
        def getBuildingProgress(self):
            return (Worker.building_time - self.building_progress) / Worker.building_time

class Mineral(Unit):
        image_file = data.filepath("mineral.png")
        id = u_id.MINERAL
        name = "Mineral"
        type = "resourse"
        hp = 50
        targetable = False
        
        def update(self, players):
            if self.hp <= 0:
                self.kill()
