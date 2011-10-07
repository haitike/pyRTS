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
    
    #Variables
    trueX = 0.0 # Float Positions
    trueY = 0.0
    
    speed = 1.5 # Default General Speed for all units
    moveX = 0.0  # moveX and moveY are temporal speed variables for diagonals and such.
    moveY = 0.0

    action = actions.STOP   # Unit action begins in 0 (Stopeed)
    image_file = DATA+"placeholder.png"
    supply = 0
    cost = 0
    building_time = 0
    building_progress = 0
    
    type = None
    selected = False
    targetable = True

    def __init__(self, startx,starty):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.image_file)
        self.rect = self.image.get_rect()
        self.rect.centerx = startx
        self.rect.centery = starty
        self.trueX, self.trueY = float(startx) , float(starty)
        self.target_location = self.trueX, self.trueY 


    def update(self,players,active): 
            self.rect.centerx = round(self.trueX) 
            self.rect.centery = round(self.trueY)
            self.image.blit(self.image, self.rect)

    def move(self,target):
        pass

class Worker(Unit):
    image_file = DATA+"worker.png"
    supply = 1
    cost = 50
    type = "unit"
    building_time = 10
    
    def update(self, players,active):        
        if self.action == actions.STOP:
            pass
        elif self.action == actions.MOVE:
            dlength = math.sqrt((self.trueX - self.target_location[0]) **2 + (self.trueY - self.target_location[1])**2)
            if dlength < self.speed:
                self.trueX = self.target_location[0]
                self.trueY = self.target_location[1]                
                self.action = actions.STOP
            else:
                self.trueX += self.moveX
                self.trueY += self.moveY
                
            self.rect.centerx = round(self.trueX) 
            self.rect.centery = round(self.trueY)
            self.image.blit(self.image, self.rect)
            
            for player in players:
                for unit in player.units:
                    if pygame.sprite.collide_rect( self, unit):
                        if self != unit:
                            self.action = actions.STOP   
    
    def move(self,target):
        self.action = actions.MOVE
        self.target_location = target
        
        dx = self.trueX - self.target_location[0] 
        dy = self.trueY - self.target_location[1]
        
        tan = math.atan2(dy,dx) # find angle
        radians = math.radians(math.degrees(tan) + 180) # convert to radians

        self.moveX = math.cos(radians) * self.speed # cosine * speed
        self.moveY = math.sin(radians) * self.speed # sine * speed

class Command_Center(Unit):
        image_file =  DATA+"command_center.png"
        type = "building"
        cost = 400
        building_time = 150
        
        def update(self, players,active):
            if self.action == actions.STOP:
                pass
            if self.action == actions.BUILD:
                if self.building_progress <= 0:
                    players[active].units.add(Worker(self.rect.centerx,self.rect.centery+self.rect.height))
                    self.action = actions.STOP
                else:
                    self.building_progress -= 1.0/FPS
        def train(self, player):
            if player.mineral >= Worker.cost:
                self.building_progress = Worker.building_time
                self.action = actions.BUILD
                player.mineral -= Worker.cost
            else:
                sound = pygame.mixer.Sound(DATA+"beep.wav")
                sound.play()
        
        def getBuildingProgress(self):
            return (Worker.building_time - self.building_progress) / Worker.building_time

class Mineral(Unit):
        image_file = DATA+"mineral.png"
        type = "resourse"
        targetable = False

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
    players[0].units.add(Mineral(300,100))
    players[0].units.add(Mineral(600,100))
    players[0].units.add(Command_Center(425,525))
    players[1].units.add(Command_Center(125,125))
    players[1].units.add(Worker(75,75))
    players[1].units.add(Worker(175,75))
    players[1].units.add(Worker(75,175))
    players[1].units.add(Worker(175,175))
    players[2].units.add(Command_Center(425,125))
    players[2].units.add(Worker(375,75))
    players[2].units.add(Worker(475,75))
    players[2].units.add(Worker(375,175))
    players[2].units.add(Worker(475,175))

    
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
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        mouse_width, mouse_height = pygame.mouse.get_cursor()[0]
                        if unit.trueX - mouse_width < mouse_x < unit.trueX + unit.rect.width and unit.trueY - mouse_height < mouse_y < unit.trueY + unit.rect.height:
                            unit.selected = True
                        else:
                            unit.selected = False
                if event.button == 2:    
                    for unit in players[activePlayer].units: unit.selected = False
                    activePlayer = changePlayer(activePlayer, players)
                if event.button == 3:
                    for unit in players[activePlayer].units:
                        if unit.selected == True:  
                            unit.move(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    for unit in players[activePlayer].units:
                        if unit.type == "building" and unit.selected == True:
                            unit.train(players[activePlayer])
        
        # Updates and Draws
        background_redraw(background, screen)

        for i, player in enumerate(players):
            player.units.update(players,activePlayer)
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
                if unit.type == "building" and unit.action == actions.BUILD:
                    pygame.draw.rect(screen,color,(unit.rect.left,unit.rect.bottom,unit.rect.width*unit.getBuildingProgress(),5))
        
        font = pygame.font.Font(None, 25)
        multiRender(["Player"+str(activePlayer)+":  "+players[activePlayer].name+"  "+str(players[activePlayer].mineral)+"M  "+str(players[activePlayer].getSupply())+"S"], font, True, (255,255,255),(480,0),screen)
        multiRender(["RightMouse: Move/Harvest","MiddleMouse: Switch Player","T Key: Train Worker"], font, True, (255,255,255),(550,520),screen)
        pygame.display.flip() #update the screen

if __name__ == '__main__': main()
