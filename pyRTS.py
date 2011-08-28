import pygame, sys
pygame.init()
size = width, height = 1024, 768
screen = pygame.display.set_mode(size) #make window

# back texture load

tiless = pygame.image.load('canstock3554313.jpg')
texture_size = tiless.get_width(), tiless.get_height()
texture_amount = (width/texture_size[0])+1, (height/texture_size[1])+1

#main loop start

clock=pygame.time.Clock() #make a clock
while 1: #infinite loop
    clock.tick(30) #limit framerate to 30 FPS
    for event in pygame.event.get():  #close cleanly
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((0,0,0)) #make redraw background black

    # print
    for ydrw in range(texture_amount[1]):
        for xdrw in range(texture_amount[0]):
            screen.blit(tiless,(xdrw*texture_size[0],ydrw*texture_size[1])) #render the surface into the rectangle
    pygame.display.flip() #update the screen
