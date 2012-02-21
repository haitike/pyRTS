# GPL3: http://www.gnu.org/licenses/gpl-3.0.html
import sys, pygame
from menu import *
import game_data, engine

class Game():
    def __init__(self,name,version):
        self.running = True
        self.name = name
        self.version = version

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode(game_data.WINDOW_SIZE)#, pygame.FULLSCREEN)
        pygame.display.set_caption(self.name + self.version)
        menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
               [('Start Game', 1, None),
                ('Watch Replay',  2, None),
                ('Options',    3, None),
                ('Exit',       4, None)])
        menu.set_center(True, True)
        menu.set_alignment('center', 'center')
        state = 0
        prev_state = 1
        rect_list = []
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        while (self.running):
            if prev_state != state:
                pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
                prev_state = state

            e = pygame.event.wait()

            if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
                if state == 0:
                    rect_list, state = menu.update(e, state)
                elif state == 1:
                    print 'Start Game!'
                    state = 0
                    pygame.quit()
                    engine.main()
                elif state == 2:
                    print 'Watch Replay!'
                    state = 0
                elif state == 3:
                    print 'Options!'
                    state = 0
                else:
                    print 'Exit!'
                    pygame.quit()

            if e.type == pygame.QUIT:
                pygame.quit()

            pygame.display.update(rect_list)
