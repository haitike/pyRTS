import pygame, sys
window_size = width, height = 800, 600

# Worker Class
class Worker(pygame.sprite.Sprite):
    def __init__(self,startx,starty):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("worker.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = startx
        self.rect.centery = starty
        self.target_location = startx, starty
        self.speed = [0,0]
        
    def update(self):
        if self.rect.centerx > self.target_location[0]:
            self.speed[0] = -1
        elif self.rect.centerx < self.target_location[0]:
            self.speed[0] = 1
        else:
            self.speed[0] = 0
            
        if self.rect.centery > self.target_location[1]:
            self.speed[1] = -1
        elif self.rect.centery < self.target_location[1]:
            self.speed[1] = 1
        else:
            self.speed[1] = 0

        self.rect.move_ip((self.speed))

def main():
    pygame.init()
    screen = pygame.display.set_mode(window_size) #make window
           
    #BackGround
    tiless = pygame.image.load('canstock3554313.jpg')
    texture_size = tiless.get_width(), tiless.get_height()
    texture_amount = (width/texture_size[0])+1, (height/texture_size[1])+1

    # Sprites and Class Initiazations
    workerSprite = pygame.sprite.RenderClear()
    worker = Worker(150,150)    
    workerSprite.add(worker)

    # Main Loop
    clock=pygame.time.Clock()
    while 1:         
        clock.tick(30) #30 FPS
        # events        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                sys.exit()       
            if event.type == pygame.MOUSEBUTTONDOWN:
                worker.target_location = event.pos
        
        # Updates
        screen.fill((0,0,0)) #make redraw background black        
        workerSprite.update()
        
        # Draws
        for ydrw in range(texture_amount[1]):
            for xdrw in range(texture_amount[0]):
                screen.blit(tiless,(xdrw*texture_size[0],ydrw*texture_size[1])) #render the surface into the rectangle
        workerSprite.draw( screen )
        
        pygame.display.flip() #update the screen

if __name__ == '__main__': main()
