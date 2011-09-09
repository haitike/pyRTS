import pygame, sys
window_size = width, height = 800, 600

def background_redraw(tiless, screen):
    screen.fill((0,0,0))           
    for ydrw in range((height/tiless.get_height())+1):
        for xdrw in range((width/tiless.get_width())+1):
            screen.blit(tiless,(xdrw*tiless.get_width(),ydrw*tiless.get_height()))

class Worker(pygame.sprite.Sprite):
    def __init__(self,startx,starty):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("worker.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = startx
        self.rect.centery = starty
        self.target_location = startx, starty
        self.speedx, self.speedy = 0,0
        
    def update(self):
        if self.rect.centerx > self.target_location[0]:
            self.speedx = -1
        elif self.rect.centerx < self.target_location[0]:
            self.speedx = 1
        else:
            self.speedx = 0
            
        if self.rect.centery > self.target_location[1]:
            self.speedy = -1
        elif self.rect.centery < self.target_location[1]:
            self.speedy = 1
        else:
            self.speedy = 0

        self.rect.move_ip(self.speedx, self.speedy)

def main():
    pygame.init()
    screen = pygame.display.set_mode(window_size) #make window
    background = pygame.image.load('background.png')

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
        
        background_redraw(background, screen)
        
        workerSprite.update()
        workerSprite.draw( screen )        
        
        pygame.display.flip() #update the screen

if __name__ == '__main__': main()
