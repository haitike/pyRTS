import tools, game_data
from minimap import *
from units import *
from player import Player
import pygame, sys

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
    for ydrw in range((game_data.height/tiless.get_height())+1):
        for xdrw in range((game_data.width/tiless.get_width())+1):
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

    pygame.init()
    screen = pygame.display.set_mode(game_data.WINDOW_SIZE) #make window
    background = pygame.image.load(tools.filepath('background.png'))
    MOUSE_CURSOR1 = pygame.mouse.get_cursor()

    # Players
    players = [Player("Neutral"),
               Player("Good Guys", True, 50, (0,0,255)),
               Player("The Evil", True, 50, (255,0,0)),
               Player("Good Minions",True, 0, (150,50,255)),
               Player("Bad Minions",True, 0, (255,0,200))]
    players[1].enemies = [2,4]
    players[2].enemies = [1,3]
    players[3].enemies = [2,4]
    players[4].enemies = [1,3]
    activePlayer = 1 # The player that is controlling the units

    # Iniciate the Minimap
    minimap = pygame.sprite.RenderClear()
    minimap.add(Minimap())

    # Initial Units
    players[0].units.add(Mineral(200,180,0))
    players[0].units.add(Mineral(200,300,0))
    players[0].units.add(Mineral(600,180,0))
    players[0].units.add(Mineral(600,300,0))
    players[1].units.add(Minion(300,100,1))
    players[1].units.add(RangedMinion(500,100,1))
    players[2].units.add(Minion(300,500,2))
    players[2].units.add(RangedMinion(500,500,2))
    players[3].units.add(Nexus(400,50,3,(400,100),(400,1600)))
    players[3].units.add(Turret(500,250,3,(500,200),(400,1600)))
    players[4].units.add(Nexus(400,1550,4,(400,1500),(400,0)))
    players[4].units.add(Turret(500,1350,4,(500,200),(400,1600)))

    # Main Loop
    clock=pygame.time.Clock()
    while 1:
        clock.tick(game_data.fps)

        # Scroll Stuff
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.mouse.get_pos()[0] > game_data.width - game_data.width/25 :
            game_data.camera[0] -= 10
        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.mouse.get_pos()[0] < game_data.width/25:
            game_data.camera[0] += 10
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.mouse.get_pos()[1] < game_data.height/25:
            game_data.camera[1] += 10
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.mouse.get_pos()[1] > game_data.height - game_data.height/25 :
            game_data.camera[1] -= 10

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_data.camera = [0,0]
                    #for player in players:
                    #    for unit in player.units:
                    #        if unit.selected == True:
                    #            game_data.camera = [-unit.rect.centerx, -unit.rect.centery]

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
                                unit.move((event.pos[0] - game_data.camera[0],event.pos[1]  - game_data.camera[1]))
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
                                    unit.attack_move((event.pos[0] - game_data.camera[0],event.pos[1]  - game_data.camera[1]))
                    pygame.mouse.set_cursor(*MOUSE_CURSOR1)
                    attack = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mouse.set_cursor(*MOUSE_CURSOR1)
                        attack = False

        # Updates and Draws
        background_redraw(background, screen)
        minimap.update(players)
        minimap.draw(screen)
        for i, player in enumerate(players):
            player.units.update(players)
            player.units.draw( screen )
        for i, player in enumerate(players):
            player.animations.update()
            player.animations.draw( screen )
            for unit in player.units:
                if unit.targetable == True:
                    pygame.draw.rect(screen,(0,0,0),(unit.rect.left,unit.rect.top-7,unit.rect.width,3))
                    pygame.draw.rect(screen,player.color,(unit.rect.left,unit.rect.top-7,unit.rect.width*unit.getLifeBar(),3))
                if unit.selected == True:
                    multiRender([unit.name,"HP: "+str(int(unit.hp))+" / "+str(unit.max_hp),"Speed: "+str(unit.speed),"Damage: "+str(unit.damage), "Armor: "+str(unit.armor*100)+"%", "Attack Speed: "+str(unit.attack_speed)], font, True, (255,255,255),(game_data.width-160,game_data.height-120),screen)
                    pygame.draw.ellipse(screen,(0,255,0), unit.rect.inflate(SELECTION_EXTRAX,SELECTION_EXTRAY), 1)

        font = pygame.font.Font(None, 25)
        multiRender(["Player"+str(activePlayer)+":  "+players[activePlayer].name+"  "+str(players[activePlayer].gold)+" Gold"], font, True, players[activePlayer].color,(10,0),screen)
        multiRender(["RightMouse: Move/Attack","MiddleMouse: Switch Player","A: Attack", "Space: Reset Camera" , "ESC: Cancel Order"], font, True, (255,255,255),(game_data.width-250,0),screen)
        pygame.display.flip() #update the screen

if __name__ == '__main__': main()
