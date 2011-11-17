import pygame
import data

class Animation(pygame.sprite.Sprite):
    image_file = data.filepath("placeholder.png") 
    duration = 30
    
    def __init__(self,x, y):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = pygame.image.load(self.image_file)
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.timer = 0
    
    def update(self):
        self.image.blit(self.image, self.rect)
        self.timer += 1
        
        if self.timer >= self.duration:
            self.kill()

class Attack(Animation):
    def __init__(self,x,y,damage, origin_unit):
        Animation.__init__(self,x,y)
        self.damage = damage
        self.origin_unit = origin_unit
        self.damage_done = False
    
    def update(self,players):
        Animation.update(self)
        
        for player in players:
            for unit in player.units:
                if pygame.sprite.collide_rect(self, unit):
                    if self != unit and unit != self.origin_unit:
                        if self.damage_done == False: 
                            unit.hp -= self.damage
                            self.damage_done = True

class MinionAttack(Attack):
    image_file = data.filepath("minion_attack.png") 
    duration = 10