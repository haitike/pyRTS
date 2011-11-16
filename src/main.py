from ConfigParser import SafeConfigParser
import data
from units import *
from player import Player
import pygame, sys

WINDOW_SIZE = width, height = 800, 600
SELECTION_EXTRAX, SELECTION_EXTRAY = 20, 20

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

def main():

    config = SafeConfigParser()
    config.read(data.filepath('config.ini'))
    fps = config.getfloat('configuration','fps')

    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE) #make window
    background = pygame.image.load(data.filepath('background.png'))

    #players
    players = [Player("Neutral", True), Player("Good Guys", True, 50), Player("The Evil", True, 50)]
    players[1].enemies = 2
    players[2].enemies = 1
    activePlayer = 1 # The player that is controlling the units

    # Initial Units
    players[0].units.add(Mineral(300,100,0))
    players[0].units.add(Mineral(300,140,0))
    players[0].units.add(Mineral(300,180,0))
    players[0].units.add(Mineral(100,300,0))
    players[0].units.add(Mineral(140,300,0))
    players[0].units.add(Mineral(180,300,0))
    players[0].units.add(Mineral(600,100,0))
    players[0].units.add(Command_Center(425,425,0))
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
        clock.tick(fps)

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
                        if unit.id == Unit.ID_CC and unit.selected == True:
                            unit.train(players)
                if event.key == pygame.K_a:
                    for unit in players[activePlayer].units:
                        if unit.type == "unit" and unit.selected == True:
                            unit.attack(pygame.mouse.get_pos)

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
                pygame.draw.rect(screen,(0,0,0),(unit.rect.left,unit.rect.top-7,unit.rect.width,3))
                pygame.draw.rect(screen,color,(unit.rect.left,unit.rect.top-7,unit.rect.width*unit.getLifeBar(),3))
                #if unit.targetable == True:
                #    pygame.draw.circle(screen,color,(unit.rect.topright),4)
                if unit.selected == True:
                    multiRender([unit.name,"HP: "+str(unit.hp)+" / "+str(unit.max_hp),"Speed: "+str(unit.speed),"Damage: "+str(unit.damage)], font, True, (255,255,255),(580,520),screen)
                    pygame.draw.ellipse(screen,(0,255,0), unit.rect.inflate(SELECTION_EXTRAX,SELECTION_EXTRAY), 1)
                if unit.action == Unit.ID_BUILD:
                    pygame.draw.rect(screen,color,(unit.rect.left,unit.rect.bottom,unit.rect.width*unit.getBuildingProgress(),5))
                if unit.action == Unit.ID_HARVEST:
                    pygame.draw.rect(screen,color,(unit.rect.left,unit.rect.bottom,unit.rect.width*unit.getHarvestingProgress(),5))

        font = pygame.font.Font(None, 25)
        multiRender(["Player"+str(activePlayer)+":  "+players[activePlayer].name+"  "+str(players[activePlayer].mineral)+"M  "+str(players[activePlayer].getSupply())+"S"], font, True, (255,255,255),(480,0),screen)
        multiRender(["RightMouse: Move/Harvest","MiddleMouse: Switch Player","A: Atacar","T Key: Train Worker"], font, True, (255,255,255),(10,520),screen)
        pygame.display.flip() #update the screen

if __name__ == '__main__': main()
