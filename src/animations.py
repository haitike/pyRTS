import pygame
import data
import math

class Animation(pygame.sprite.Sprite):
    image_file = data.filepath("placeholder.png") 
    duration = 15
    
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
    speed = 1
    
    def __init__(self, origin_unit, target_unit, damage):
        Animation.__init__(self,origin_unit.rect.centerx ,origin_unit.rect.centery)
        self.damage = damage
        self.target_unit = target_unit
        self.damage_done = False

        # Path Calculation
        dx = origin_unit.rect.centerx - target_unit.rect.centerx
        dy = origin_unit.rect.centery - target_unit.rect.centery
        tan = math.atan2(dy,dx)
        radians = math.radians(math.degrees(tan) + 180)
        self.moveX = math.cos(radians) * self.speed
        self.moveY = math.sin(radians) * self.speed

    def update(self):
        if self.timer > self.duration:
            self.kill()
        self.image.blit(self.image, self.rect)
        
        self.rect.centerx += self.moveX
        self.rect.centery += self.moveY        

        if self.damage_done == False: 
            if pygame.sprite.collide_rect(self, self.target_unit):
                self.target_unit.hp -= self.damage
                self.damage_done = True
        else:
            self.timer += 1
            
        if self.timer >= self.duration:
            self.kill()
                

class MinionAttack(Attack):
    image_file = data.filepath("minion_attack.png") 
    speed = 2
    duration = 10