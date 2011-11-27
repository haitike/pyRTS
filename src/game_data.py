from ConfigParser import SafeConfigParser
import tools

WINDOW_SIZE = width, height = 800, 600

config = SafeConfigParser()
config.read(tools.filepath('config.ini'))
fps = config.getfloat('configuration','fps')

camera = [0,0]