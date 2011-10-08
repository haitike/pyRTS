# GPL3: http://www.gnu.org/licenses/gpl-3.0.html
#
# PyRTS v 0.1

import pygame, sys, math
WINDOW_SIZE = width, height = 800, 600
SELECTION_EXTRAX, SELECTION_EXTRAY = 20, 20
DATA = "data/"
FPS = 30
class actions:
    STOP = 0
    MOVE = 1
    BUILD = 2
    HARVEST = 3
class u_id:
    MINERAL = 0
    CC = 20
    WORKER = 50

def multiRender(lines, font, antialias, color, position, background):
    # RenderFont for multiple lines of text in a list.
    fontHeight = font.get_height()
    text = [font.render(line, antialias, color) for line in lines]
    for i in range(len(lines)):
        background.blit(text[i], (position[0],position[1]+(i*fontHeight)))

def background_redraw(tiless, screen):
    screen.fill((0,0,0))           
    for ydrw in range((height/tiless.get_height())+1):
        for xdrw in range((width/tiless.get_width())+1):
            screen.blit(tiless,(xdrw*tiless.get_width(),ydrw*tiless.get_height()))

def changePlayer( active, players): # Temporal function for switch the player
    if active +1 < len(players):
        active += 1
    else:
        active = 0

    if players[active].isControllable() == False:
        active = changePlayer(active,players)

    return active
        
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
    
class Unit(pygame.sprite.Sprite):    

    image_file = DATA+"placeholder.png"    
    
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
    image_file = DATA+"worker.png"
    image_file2 = DATA+"worker_with_mineral.png"
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
        image_file =  DATA+"command_center.png"
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
                sound = pygame.mixer.Sound(DATA+"beep.wav")
                sound.play()
        
        def getBuildingProgress(self):
            return (Worker.building_time - self.building_progress) / Worker.building_time

class Mineral(Unit):
        image_file = DATA+"mineral.png"
        id = u_id.MINERAL
        name = "Mineral"
        type = "resourse"
        hp = 50
        targetable = False
        
        def update(self, players):
            if self.hp <= 0:
                self.kill()

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE) #make window
    background = pygame.image.load(DATA+'background.png')

    #players
    players = [Player("Neutral"), Player("Good Guys", True, 50), Player("The Evil", True, 50)]
    players[1].enemies = 2
    players[2].enemies = 1
    activePlayer = 1 # The player that is controlling the units

    # Initial Units
    players[0].units.add(Mineral(300,100,0))
    players[0].units.add(Mineral(300,140,0))
    players[0].units.add(Mineral(300,180,0))
    players[0].units.add(Mineral(100,300,0))
    players[0].units.add(Mineral(130,300,0))
    players[0].units.add(Mineral(160,300,0))
    players[0].units.add(Mineral(600,100,0))
    players[0].units.add(Command_Center(425,525,0))
    players[1].units.add(Command_Center(125,125,1))
    players[1].units.add(Worker(75,75,1))
    players[1].units.add(Worker(175,75,1))
    players[1].units.add(Worker(75,175,1))
    players[1].units.add(Worker(175,175,1))
    players[2].units.add(Command_Center(425,125,2))
    players[2].units.add(Worker(375,75,2))
    players[2].units.add(Worker(475,75,2))
    players[2].units.add(Worker(375,175,2))
    players[2].units.add(Worker(475,175,2))

    
    # Main Loop
    clock=pygame.time.Clock()
    while 1:         
        clock.tick(FPS) #30 FPS
        
        # events        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                sys.exit()            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for unit in players[activePlayer].units:
                        if unit.isPressed(pygame.mouse.get_pos()):
                            unit.selected = True
                        else:
                            unit.selected = False
                if event.button == 2:    
                    for unit in players[activePlayer].units: unit.selected = False
                    activePlayer = changePlayer(activePlayer, players)
                if event.button == 3:
                    for unit in players[activePlayer].units:
                        if unit.selected == True and unit.type == "unit":  
                            unit.move(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    for unit in players[activePlayer].units:
                        if unit.id == u_id.CC and unit.selected == True:
                            unit.train(players)
        
        # Updates and Draws
        background_redraw(background, screen)

        for i, player in enumerate(players):
            player.units.update(players)
            player.units.draw( screen )
            if i == activePlayer :
                color = 0,255,0
            elif i == players[activePlayer].enemies:
                color = 255,0,0
            else:
                color = 255,255,0
            for unit in player.units:
                if unit.targetable == True:
                    pygame.draw.circle(screen,color,(unit.rect.topright),4)
                if unit.selected == True:
                    pygame.draw.ellipse(screen,(0,255,0), unit.rect.inflate(SELECTION_EXTRAX,SELECTION_EXTRAY), 1)
                if unit.action == actions.BUILD:
                    pygame.draw.rect(screen,color,(unit.rect.left,unit.rect.bottom,unit.rect.width*unit.getBuildingProgress(),5))
                if unit.action == actions.HARVEST:
                    pygame.draw.rect(screen,color,(unit.rect.left,unit.rect.bottom,unit.rect.width*unit.getHarvestingProgress(),5))
                    
        font = pygame.font.Font(None, 25)
        multiRender(["Player"+str(activePlayer)+":  "+players[activePlayer].name+"  "+str(players[activePlayer].mineral)+"M  "+str(players[activePlayer].getSupply())+"S"], font, True, (255,255,255),(480,0),screen)
        multiRender(["RightMouse: Move/Harvest","MiddleMouse: Switch Player","T Key: Train Worker"], font, True, (255,255,255),(550,520),screen)
        pygame.display.flip() #update the screen

if __name__ == '__main__': main()
