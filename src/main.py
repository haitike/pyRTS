from ConfigParser import SafeConfigParser
import data
from units import *
from player import Player
import pygame, sys

WINDOW_SIZE = width, height = 800, 600
SELECTION_EXTRAX, SELECTION_EXTRAY = 20, 20
MOUSE_CURSOR1 = None
MOUSE_CURSOR2 = (8, 8), (4,4), (24, 24, 24, 231, 231, 24, 24, 24), (0, 0, 0, 0, 0, 0, 0, 0)

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
    attack = False
    config = SafeConfigParser()
    config.read(data.filepath('config.ini'))
    fps = config.getfloat('configuration','fps')

    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE) #make window
    background = pygame.image.load(data.filepath('background.png'))
    MOUSE_CURSOR1 = pygame.mouse.get_cursor()

    #players
    players = [Player("Neutral"), Player("Good Guys", True, 50), Player("The Evil", True, 50), Player("Good Minions",True), Player("Bad Minions",True)]
    players[1].enemies = [2,4]
    players[2].enemies = [1,3]
    players[3].enemies = [2,4]
    players[4].enemies = [1,3]
    activePlayer = 1 # The player that is controlling the units

    # Initial Units
    players[0].units.add(Mineral(200,180,0))
    players[0].units.add(Mineral(200,300,0))
    players[0].units.add(Mineral(600,180,0))
    players[0].units.add(Mineral(600,300,0))
    players[1].units.add(Minion(300,100,1))
    players[1].units.add(RangedMinion(500,100,1))
    players[2].units.add(Minion(300,500,2))
    players[2].units.add(RangedMinion(500,500,2))
    players[3].units.add(Nexus(400,50,3,(400,100),(400,600)))
    players[4].units.add(Nexus(400,550,4,(400,500),(400,0)))

    # Main Loop
    clock=pygame.time.Clock()
    while 1:
        clock.tick(fps)

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if attack == False:
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
                            if unit.selected == True and unit.type == unit.ID_UNIT:
                                unit.move(event.pos)
                                for player in players:
                                    for target in player.units:
                                        if target.isPressed(pygame.mouse.get_pos()) and target.owner in players[unit.owner].enemies and target != unit and target.targetable == True:
                                            unit.attack(target)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        for unit in players[activePlayer].units:
                            if unit.type == unit.ID_UNIT and unit.selected == True:
                                pygame.mouse.set_cursor(*MOUSE_CURSOR2)
                                attack = True

            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        unit_in_cursor = False
                        for unit in players[activePlayer].units:
                            if unit.selected == True and unit.type == unit.ID_UNIT:
                                for player in players:
                                    for target in player.units:
                                        if target.isPressed(pygame.mouse.get_pos()) and target != unit and target.targetable == True:
                                            unit.attack(target)
                                            unit_in_cursor = True
                                if unit_in_cursor == False:
                                    unit.attack_move(event.pos)
                    pygame.mouse.set_cursor(*MOUSE_CURSOR1)
                    attack = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mouse.set_cursor(*MOUSE_CURSOR1)
                        attack = False

        # Updates and Draws
        background_redraw(background, screen)

        for i, player in enumerate(players):
            player.units.update(players)
            player.units.draw( screen )
        for i, player in enumerate(players):
            player.animations.update()
            player.animations.draw( screen )
            if i == activePlayer :
                color = 0,255,0
            elif i in players[activePlayer].enemies:
                color = 255,0,0
            else:
                color = 255,255,0
            for unit in player.units:
                if unit.targetable == True:
                    pygame.draw.rect(screen,(0,0,0),(unit.rect.left,unit.rect.top-7,unit.rect.width,3))
                    pygame.draw.rect(screen,color,(unit.rect.left,unit.rect.top-7,unit.rect.width*unit.getLifeBar(),3))
                if unit.selected == True:
                    multiRender([unit.name,"HP: "+str(int(unit.hp))+" / "+str(unit.max_hp),"Speed: "+str(unit.speed),"Damage: "+str(unit.damage), "Armor: "+str(unit.armor*100)+"%", "Attack Speed: "+str(unit.attack_speed)], font, True, (255,255,255),(620,480),screen)
                    pygame.draw.ellipse(screen,(0,255,0), unit.rect.inflate(SELECTION_EXTRAX,SELECTION_EXTRAY), 1)

        font = pygame.font.Font(None, 25)
        multiRender(["Player"+str(activePlayer)+":  "+players[activePlayer].name+"  "+str(players[activePlayer].gold)+" Gold"], font, True, (255,255,255),(520,0),screen)
        multiRender(["RightMouse: Move/Attack","MiddleMouse: Switch Player","A: Attack", "ESC: Cancel Order"], font, True, (255,255,255),(10,500),screen)
        pygame.display.flip() #update the screen

if __name__ == '__main__': main()
