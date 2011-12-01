from pygame import sprite, Surface, draw
import game_data

class Minimap(sprite.Sprite):

    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = Surface((game_data.minimap_width, game_data.minimap_height))
        self.paintmap()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, game_data.height)
        self.factorx = game_data.minimap_width  * 1.0 / game_data.map_width
        self.factory = game_data.minimap_height *1.0 / game_data.map_height

    def paintmap(self):
        self.image.fill((0,155,0))
        draw.rect(self.image, (150,0,0), (0,0, game_data.minimap_width, game_data.minimap_height),1)

    def update(self, players):
        self.paintmap()
        draw.rect(self.image, (255,255,255), (round(-game_data.camera[0] * self.factorx,0),
                                                     round(-game_data.camera[1] * self.factory,0),
                                                     round(game_data.width * self.factorx, 0),
                                                     round(game_data.height * self.factory, 0)),1)
        for player in players:
            for unit in player.units:
                pos = unit.trueX, unit.trueY
                draw.circle(self.image, players[unit.owner].color, (int(pos[0] * self.factorx),
                                                  int(pos[1] * self.factory)), unit.size )