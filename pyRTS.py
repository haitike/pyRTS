# GPL3: http://www.gnu.org/licenses/gpl-3.0.html
#
# PyRTS v 0.1

import pygame, sys, math
window_size = width, height = 800, 600

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
        self.supply = 0

    def isControllable(self):
        return self.controllable
    
class Unit(pygame.sprite.Sprite):    
    trueX = 0.0 # Float Positions
    trueY = 0.0
    
    speed = 1.5 # Default General Speed for all units
    moveX = 0.0  # moveX and moveY are temporal speed variables for diagonals and such.
    moveY = 0.0

    action = 0   # Unit action begins in 0 (Stopeed)

class Worker(Unit):
    def __init__(self, startx,starty):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("worker.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = startx
        self.rect.centery = starty
        self.trueX, self.trueY = float(startx) , float(starty)
        self.target_location = self.trueX, self.trueY 
        
    def update(self):        
        if self.action == 0:# Stop
            pass
        elif self.action == 1: # Move
            dlength = math.sqrt((self.trueX - self.target_location[0]) **2 + (self.trueY - self.target_location[1])**2)
            if dlength < self.speed:
                self.trueX = self.target_location[0]
                self.trueY = self.target_location[1]                
                self.action = 0
            else:
                self.trueX += self.moveX
                self.trueY += self.moveY
                
            self.rect.centerx = round(self.trueX) 
            self.rect.centery = round(self.trueY)
            self.image.blit(self.image, self.rect)
    
    def move(self,target):
        self.action = 1
        self.target_location = target
        
        dx = self.trueX - self.target_location[0] 
        dy = self.trueY - self.target_location[1]
        
        tan = math.atan2(dy,dx) # find angle
        radians = math.radians(math.degrees(tan) + 180) # convert to radians

        self.moveX = math.cos(radians) * self.speed # cosine * speed
        self.moveY = math.sin(radians) * self.speed # sine * speed
        

def main():
    pygame.init()
    screen = pygame.display.set_mode(window_size) #make window
    background = pygame.image.load('background.png')

    #players
    players = [Player("Neutral"), Player("Good Guys", True, 50), Player("The Evil", True, 50)]
    activePlayer = 1 # The player that is controlling the units

    # Initial Units
    players[1].units.add(Worker(150,150))
    players[2].units.add(Worker(250,50))  
    
    # Main Loop
    clock=pygame.time.Clock()
    while 1:         
        clock.tick(30) #30 FPS
        
        # events        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                sys.exit()            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:              
                    activePlayer = changePlayer(activePlayer, players)
                if event.button == 3:
                    for unit in players[activePlayer].units:
                        unit.move(event.pos)

        
        # Updates and Draws
        background_redraw(background, screen)

        for i, player in enumerate(players):
            player.units.update()
            player.units.draw( screen )
            if i == activePlayer :
                color = 0,255,0
            else:
                color = 255,0,0
            for j in player.units:
                pygame.draw.circle(screen,color,(j.rect.topright),4)
                
        font = pygame.font.Font(None, 25)
        text = font.render("Player"+str(activePlayer)+":  "+players[activePlayer].name+"  "+str(players[activePlayer].mineral)+"M  "+str(players[activePlayer].supply)+"S", True,(255,255, 255))
        screen.blit(text, (480,0))
        
        pygame.display.flip() #update the screen

if __name__ == '__main__': main()
