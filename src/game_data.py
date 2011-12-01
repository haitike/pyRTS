from ConfigParser import SafeConfigParser
import tools

WINDOW_SIZE = width, height = 800,600

config = SafeConfigParser()
config.read(tools.filepath('config.ini'))
fps = config.getfloat('configuration','fps')

map_width = 1200
map_height = 1400

minimap_width = 200
minimap_height = 150

camera = [- map_width/6 , 0]