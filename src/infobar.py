from pygame import sprite, Surface, draw
from text import Text
from units import Unit
import game_data, groups

# Sprite _Layers
#  8) Infobar
#  9) Minimap | SelectionBox | HeroBox

class Infobar(sprite.Sprite):
    def __init__(self):
        self.groups = groups.allgroup
        self._layer = 8
        sprite.Sprite.__init__(self, self.groups)
        self.image = Surface((game_data.width, game_data.infobar_height))
        draw.rect(self.image, (150,0,0), (0,0, game_data.width, game_data.infobar_height),1)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, game_data.height)

        self.minimap = Minimap()
        SelectionBox()
        HeroBox()

    def update(self, seconds):
        #self.image = Surface((game_data.width, game_data.infobar_height))
        self.image.fill(game_data.infobar_color)

class Minimap(sprite.Sprite):

    def __init__(self):
        self.groups = groups.allgroup
        self._layer = 9
        sprite.Sprite.__init__(self, self.groups)
        self.image = Surface((game_data.minimap_width, game_data.minimap_height))
        self.paintmap()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, game_data.height)
        self.factorx = game_data.minimap_width  * 1.0 / game_data.map_width
        self.factory = game_data.minimap_height *1.0 / game_data.map_height

    def paintmap(self):
        self.image.fill(game_data.minimap_color)
        draw.rect(self.image, game_data.minimap_bordercolor, (0,0, game_data.minimap_width, game_data.minimap_height),1)

    def update(self, seconds):
        self.paintmap()
        draw.rect(self.image, (255,255,255), (round(-game_data.camera[0] * self.factorx,0),
                                                     round(-game_data.camera[1] * self.factory,0),
                                                     round(game_data.width * self.factorx, 0),
                                                     round((game_data.height - game_data.infobar_height) * self.factory, 0)),1)
        for unit in groups.unitgroup:
            pos = unit.trueX, unit.trueY
            draw.circle(self.image, unit.owner.color, (int(pos[0] * self.factorx),
                                                  int(pos[1] * self.factory)), unit.size )

    def isPressed(self,mouse):
        pressed = False
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        pressed = True
        return pressed

    def getCamera(self,mouse):
        posx = mouse[0]
        posy = mouse[1] - game_data.height + game_data.minimap_height

        return posx / self.factorx, posy / self.factory

class SelectionBox(sprite.Sprite):
    def __init__(self):
        self.groups = groups.allgroup
        self._layer = 9
        sprite.Sprite.__init__(self, self.groups)
        self.image = Surface((game_data.selectionbox_width, game_data.selectionbox_height))
        self.paintbox()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (game_data.width - game_data.selectionbox_width, game_data.height)
        self.text = []
        for x in range(6): self.text.append(Text("", game_data.infobar_fontcolor, (self.rect.left, self.rect.top + x*20)))

    def paintbox(self):
        self.image.fill(game_data.selectionbox_color)
        draw.rect(self.image, game_data.selectionbox_bordercolor, (0,0, game_data.selectionbox_width, game_data.selectionbox_height),1)

    def update(self, seconds):
        self.paintbox()
        selectedUnits = self.getSelectedUnits()
        if len(selectedUnits) == 1:
            if Unit.ID_HERO in selectedUnits[0].type:
                self.text[0].newmsg(selectedUnits[0].name + " (Lv: " + str(selectedUnits[0].level) + ")("+str(selectedUnits[0].exp)+"/"+str(selectedUnits[0].expPerLevel[selectedUnits[0].level])+")")
                self.text[1].newmsg("Vitality: "+str(int(selectedUnits[0].atributes[0])))
                self.text[2].newmsg("Energy: "+str(int(selectedUnits[0].atributes[1])))
                self.text[3].newmsg("Strength: "+str(int(selectedUnits[0].atributes[2])))
                self.text[4].newmsg("Dextery: "+str(int(selectedUnits[0].atributes[3])))
                self.text[5].newmsg("Inteligence: "+str(int(selectedUnits[0].atributes[4])))

            else:
                self.text[0].newmsg(selectedUnits[0].name)
                self.text[1].newmsg("HP: "+str(int(selectedUnits[0].hp))+" / "+str(selectedUnits[0].maxHP))
                self.text[2].newmsg("Speed: "+str(selectedUnits[0].speed))
                self.text[3].newmsg("Damage: "+str(selectedUnits[0].damage))
                self.text[4].newmsg("phRes: "+str(selectedUnits[0].phRes*100)+"%")
                self.text[5].newmsg("Attack Speed: "+str(selectedUnits[0].atSpeed))


        else:
            for x in self.text:
                x.newmsg("")
            if len(selectedUnits) > 1: self.text[0].newmsg("Units Selected: "+str(len(selectedUnits)))

    def getSelectedUnits(self):
        selected = []
        for unit in groups.unitgroup:
            if unit.selected == True:
                selected.append(unit)
        return selected

class HeroBox():
    pass
