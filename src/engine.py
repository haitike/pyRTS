# GPL3: http://www.gnu.org/licenses/gpl-3.0.html

import tools, game_data, groups
from infobar import *
from units import *
from player import Player
from text import Text
import pygame, sys

SELECTION_EXTRAX, SELECTION_EXTRAY = 20, 20
MOUSE_CURSOR1 = None
MOUSE_CURSOR2 = (8, 8), (4,4), (24, 24, 24, 231, 231, 24, 24, 24), (0, 0, 0, 0, 0, 0, 0, 0)

def background_redraw(tiless, screen):
    screen.fill((0,0,0))
    for ydrw in range((game_data.map_height/tiless.get_height())+1):
        for xdrw in range((game_data.map_width/tiless.get_width())+1):
            screen.blit(tiless,((xdrw*tiless.get_width() + game_data.camera[0]),(ydrw*tiless.get_height() + game_data.camera[1])))

def changePlayer( active, players): # Temporal function for switch the player
    if active +1 < len(players):
        active += 1
    else:
        active = 0

    if players[active].isControllable() == False:
        active = changePlayer(active,players)

    return active

def main():
    replay_list = []
    activePlayer = 1 # The player that is controlling the units
    attack = False  # True is controlls are in "attack mode" (clicking "A")

    pygame.init()
    screen = pygame.display.set_mode(game_data.WINDOW_SIZE, pygame.FULLSCREEN)
    #pygame.display.set_caption(GAME_NAME + VERSION)
    background = pygame.image.load(tools.filepath('background.png'))
    MOUSE_CURSOR1 = pygame.mouse.get_cursor()

    # Players
    players = [Player("Neutral"),
               Player("Good Guys", True, 50, (0,0,255)),
               Player("The Evil", True, 50, (255,0,0)),
               Player("Good Minions",True, 0, (128,0,128)),
               Player("Bad Minions",True, 0, (255,153,0))]
    players[1].enemies = [players[2], players[4]]
    players[2].enemies = [players[1], players[3]]
    players[3].enemies = [players[2], players[4]]
    players[4].enemies = [players[1], players[3]]

    # Iniciate the Minimap
    infobar = Infobar()

    # Iniciate the text
    text1 = Text("Player"+str(activePlayer)+":  "+players[activePlayer].name+"  "+str(players[activePlayer].gold)+" Gold", players[activePlayer].color,(10,0))
    for i, text in enumerate(["RightMouse: Move/Attack","MiddleMouse: Switch Player","A: Attack",  "Space: Reset Camera" , "ESC: Cancel Order", "CONTROL: Multi-Selection"]):
        Text(text, (255,255,255),(game_data.width-250,0+i*20))

    # Initial Units
    Mineral(350,280,players[0])
    Mineral(350,400,players[0])
    Mineral(750,280,players[0])
    Mineral(750,400,players[0])
    Nexus(550,150,players[3],(550,200),(550,1300))
    Turret(550,210,players[3])
    Nexus(550,1250,players[4],(550,1200),(550,100))
    Turret(550,1190,players[4])
    Tank(650, 300,players[1])

    # Main Loop
    clock=pygame.time.Clock()
    finish_game = False
    while not finish_game:
        milliseconds = clock.tick(game_data.fps)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame (float)

        # Scroll Stuff
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.mouse.get_pos()[0] > game_data.width - 2 :
            if game_data.camera[0] > -game_data.map_width + game_data.width: game_data.camera[0] -= 10
        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.mouse.get_pos()[0] < 2:
            if game_data.camera[0] < 0: game_data.camera[0] += 10
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.mouse.get_pos()[1] < 2:
            if game_data.camera[1] < 0: game_data.camera[1] += 10
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.mouse.get_pos()[1] > game_data.height - 2:
            if game_data.camera[1] > -game_data.map_height  + game_data.height - game_data.infobar_height: game_data.camera[1] -= 10

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_data.camera = [0,0]
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

            if attack == False:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if pygame.mouse.get_pos()[1] < (game_data.height - game_data.infobar_height):
                            for unit in players[activePlayer].unitgroup:
                                if unit.isPressed(pygame.mouse.get_pos()):
                                    if pygame.key.get_pressed()[pygame.K_LCTRL] == True and unit.selected == True: unit.selected = False
                                    else: unit.selected = True
                                else:
                                    if pygame.key.get_pressed()[pygame.K_LCTRL] == False: unit.selected = False
                        if infobar.minimap.isPressed(pygame.mouse.get_pos()):
                            posx, posy = infobar.minimap.getCamera(pygame.mouse.get_pos())
                            game_data.camera = [-posx/2, -posy/2]
                            #Minion(posx, posy, players[activePlayer])
                    if event.button == 2:
                        for unit in players[activePlayer].unitgroup: unit.selected = False
                        activePlayer = changePlayer(activePlayer, players)
                    if event.button == 3:
                        if pygame.mouse.get_pos()[1] < (game_data.height - game_data.infobar_height):
                            for unit in players[activePlayer].unitgroup:
                                if unit.selected == True and unit.ID_UNIT in unit.type:
                                    unit.move((event.pos[0] - game_data.camera[0],event.pos[1]  - game_data.camera[1]))
                                    replay_list.append("move")
                                    for target in groups.unitgroup:
                                        if target.isPressed(pygame.mouse.get_pos()) and target.owner in unit.owner.enemies and target != unit and target.targetable == True:
                                            unit.attack(target)
                                            replay_list.append("attack")

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        for unit in players[activePlayer].unitgroup:
                            if unit.ID_UNIT in unit.type and unit.selected == True:
                                pygame.mouse.set_cursor(*MOUSE_CURSOR2)
                                attack = True
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pos()[1] < (game_data.height - game_data.infobar_height):
                        if event.button == 1:
                            unit_in_cursor = False
                            for unit in players[activePlayer].unitgroup:
                                if unit.selected == True and unit.ID_UNIT in unit.type:
                                    for target in groups.unitgroup:
                                        if target.isPressed(pygame.mouse.get_pos()) and target != unit and target.targetable == True:
                                            unit.attack(target)
                                            replay_list.append("attack")
                                            unit_in_cursor = True
                                    if unit_in_cursor == False:
                                        unit.attack_move((event.pos[0] - game_data.camera[0],event.pos[1]  - game_data.camera[1]))
                                        replay_list.append("attack move")

                    pygame.mouse.set_cursor(*MOUSE_CURSOR1)
                    attack = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mouse.set_cursor(*MOUSE_CURSOR1)
                        attack = False

        # Updates and Draws
        background_redraw(background, screen)
        groups.allgroup.update(seconds)
        for unit in groups.unitgroup:
            if unit.targetable == True:
                pygame.draw.rect(screen,(0,0,0),(unit.rect.left,unit.rect.top-7,unit.rect.width,3))
                pygame.draw.rect(screen,unit.owner.color,(unit.rect.left,unit.rect.top-7,unit.rect.width*unit.getLifeBar(),3))
            if unit.selected == True:
                pygame.draw.ellipse(screen,(0,255,0), unit.rect.inflate(SELECTION_EXTRAX,SELECTION_EXTRAY), 1)

        font = pygame.font.Font(None, 25)
        text1.newmsg("Player"+str(activePlayer)+":  "+players[activePlayer].name+"  "+str(players[activePlayer].gold)+" Gold", players[activePlayer].color)
        groups.allgroup.draw(screen)
        pygame.display.flip( ) #update the screen

    replay_list.append("quit")
    print replay_list
    print pygame.event.Event
    pygame.quit()
