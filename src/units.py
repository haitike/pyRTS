from base_units import *

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
        self.max_hp = 20
        self.type = "unit"
        self.speed = 1.5
        self.damage = 4
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


class Command_Center(Building):
    cost = 400
    building_time = 1500.0

    def __init__(self, startx,starty,owner):
        Building.__init__(self,startx,starty,owner)

        self.image_file =  data.filepath("command_center.png")
        self.id = self.ID_CC
        self.name = "Command_Center"
        self.type = "building"
        self.hp = 250

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

class Mineral(Building):
    def __init__(self, startx,starty,owner):
        Building.__init__(self,startx,starty,owner)

        self.image_file = data.filepath("mineral.png")
        self.id = self.ID_MINERAL
        self.name = "Mineral"
        self.type = "resourse"
        self.hp = 50
        self.targetable = False

        self.unit_init()
