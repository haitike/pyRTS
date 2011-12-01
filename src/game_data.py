from ConfigParser import SafeConfigParser
import tools

WINDOW_SIZE = width, height = 800,600

config = SafeConfigParser()
config.read(tools.filepath('config.ini'))
fps = config.getfloat('configuration','fps')

camera = [0,0]

map_width = 800
map_height = 1400

minimap_width = 200
minimap_height = 150