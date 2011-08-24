
#program load

import pygame, sys
pygame.init() #load pygame modules
size = width, height = 1024, 768 #size of window
screen = pygame.display.set_mode(size) #make window

# back texture load

tiless = pygame.image.load('canstock3554313.jpg')
tamanotextura = tiless.get_width(), tiless.get_height()
cantidadtexturas = (width/tamanotextura[0])+1, (height/tamanotextura[1])+1

#main loop start

clock=pygame.time.Clock() #make a clock
while 1: #infinite loop
	clock.tick(30) #limit framerate to 30 FPS
	for event in pygame.event.get(): #if something clicked
		if event.type == pygame.QUIT: #if EXIT clicked
			sys.exit() #close cleanly
	screen.fill((0,0,0)) #make redraw background black
	
	# back print
	
	for ydrw in range(cantidadtexturas[1]):
		for xdrw in range(cantidadtexturas[0]):
			screen.blit(tiless,(xdrw*tamanotextura[0],ydrw*tamanotextura[1])) #render the surface into the rectangle
	
	# vsync
	
	pygame.display.flip() #update the screen