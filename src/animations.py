import pygame
import data
import math

class Animation(pygame.sprite.Sprite):
    image_file = data.filepath("placeholder.png")
    duration = 10

    def __init__(self,x, y):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = pygame.image.load(self.image_file)
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.trueX = float(x)
        self.trueY = float(y)
        self.timer = 0

    def update(self):
        self.rect.centerx = round(self.trueX)
        self.rect.centery = round(self.trueY)
        self.image.blit(self.image, self.rect)
        self.timer += 1

        if self.timer >= self.duration:
            self.kill()

class Attack(Animation):
    speed = 1
    duration_after_hit = 15

    def __init__(self, origin_unit, target_unit, damage, range):
        Animation.__init__(self,origin_unit.trueX ,origin_unit.trueY)
        self.damage = damage
        self.target_unit = target_unit
        self.damage_status = 0  # 0: No Damage  1: After-damage Animation 2: Number Animation
        self.hit = self.damage * (1.0 - self.target_unit.armor)
        self.duration = range / self.speed

        # Path Calculation
        dx = self.trueX - self.target_unit.trueX
        dy = self.trueY - self.target_unit.trueY
        tan = math.atan2(dy,dx)
        radians = math.radians(math.degrees(tan) + 180)
        self.moveX = math.cos(radians) * self.speed
        self.moveY = math.sin(radians) * self.speed

    def update(self):
        Animation.update(self)

        if self.damage_status == 0:
            if pygame.sprite.collide_rect(self, self.target_unit):
                self.target_unit.hp -= self.hit
                self.damage_status = 1
                self.timer = self.duration - self.duration_after_hit - 2
        elif self.damage_status == 1:
            if self.timer > (self.duration - 2):
                self.image = pygame.font.Font(None, 25).render(str(int(self.hit)), True, (255,255,255))
                self.rect = self.image.get_rect()
                self.rect.centerx = round(self.trueX)
                self.rect.centery = round(self.trueY)
                self.damage_status = 2
                self.timer = self.duration - 15

        if self.damage_status < 2:
                self.trueX += self.moveX
                self.trueY += self.moveY
        else:
            self.trueY -= 1.5

class MinionAttack(Attack):
    image_file = data.filepath("minion_attack.png")
    speed = 3.5
    duration_after_hit = 6.0

class RangedMinionAttack(Attack):
    image_file = data.filepath("bullet.png")
    speed = 8.0
    duration_after_hit = 1.0