from ConfigParser import SafeConfigParser
from pygame import font
import tools

config = SafeConfigParser()
config.read(tools.filepath('config.ini'))
fps = config.getfloat('configuration','fps')

WINDOW_SIZE = width, height = 1024,768
map_width = 1200
map_height = 1400

infobar_height = 150
infobar_color = (155,0,0)
infobar_fontcolor = (255,255,255)

minimap_width = 200
minimap_height = infobar_height
minimap_color = (0,155,0)
minimap_bordercolor = infobar_color

selectionbox_width = 200
selectionbox_height = infobar_height
selectionbox_color = (0,155,0)
selectionbox_bordercolor = infobar_color

camera = [- map_width/6 , 0]