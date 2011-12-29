from pygame import sprite, font
import groups

# Sprite _Layers
#  10) Text 

class Text(sprite.Sprite):
    """a pygame Sprite displaying text"""
    def __init__(self, msg="The Python Game Book", color=(0,0,0), topleft=(0,0)):
        self.groups = groups.allgroup
        self.topleft = topleft
        self._layer = 10
        sprite.Sprite.__init__(self, self.groups)
        self.newmsg(msg,color)

    def update(self, seconds):
        pass

    def newmsg(self, msg, color=(0,0,0)):
        self.image =  self.write(msg,color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.topleft

    def write(self, msg="Placeholder", color=(0,0,0)):
        """write text into pygame surfaces"""
        myfont = font.Font(None, 25)
        mytext = myfont.render(msg, True, color)
        mytext = mytext.convert_alpha()
        return mytext