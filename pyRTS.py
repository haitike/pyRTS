import pygame, sys, math
window_size = width, height = 800, 600

def background_redraw(tiless, screen):
    screen.fill((0,0,0))           
    for ydrw in range((height/tiless.get_height())+1):
        for xdrw in range((width/tiless.get_width())+1):
            screen.blit(tiless,(xdrw*tiless.get_width(),ydrw*tiless.get_height()))

class Unit(pygame.sprite.Sprite):
    trueX = 0.0
    trueY = 0.0

class Worker(Unit):
    def __init__(self,startx,starty):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("worker.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = startx
        self.rect.centery = starty
        self.trueX, self.trueY = startx * 1.0 , starty * 1.0
        self.target_location = self.trueX, self.trueY 
        self.action = 0   # Stopped
        
    def update(self):        
        if self.action == 0:# Stop
            pass
        elif self.action == 1: # Move
            self.rect.centerx = round(self.trueX) 
            self.rect.centery = round(self.trueY)
            self.image.blit(self.image, self.rect)
        
        if self.trueX > self.target_location[0]:
            self.trueX -= 0.5
        elif self.trueX < self.target_location[0]:
            self.trueX += 0.5
            
        if self.trueY > self.target_location[1]:
            self.trueY -= 0.5
        elif self.trueY < self.target_location[1]:
            self.trueY += 0.5
            
    
    def move(self,target):
        self.action = 1
        self.target_location = target
        
        # Pruebas:
        diagonal = math.sqrt( ((target[0]-self.trueX)**2) + ((target[1]-self.trueY)**2) )
        print self.trueX, self.trueY
        print diagonal

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
                worker.move(event.pos)
        
        # Updates
        background_redraw(background, screen)
        workerSprite.update()
        workerSprite.draw( screen )        
        pygame.display.flip() #update the screen

if __name__ == '__main__': main()
