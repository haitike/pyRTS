#!/usr/bin/env python
# GPL3: http://www.gnu.org/licenses/gpl-3.0.html
GAME_NAME = "pyRTS"
VERSION = " 0.2"

from src import game

if __name__ == '__main__':
    theGame = game.Game(GAME_NAME,VERSION)
    theGame.run()
