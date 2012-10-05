import math
import groups
from ids import *
from pygame import sprite

class pasTurretAttack():
    def __init__(self, unit,   animation,  damage=15,  atSpeed=1.0):
        self.attack_timer = 30
        self.AttackAnimation = animation
        self.damage = damage
        self.atSpeed = atSpeed
        self.unit = unit
        
    def update(self):
        if self.attack_timer <= 30: self.attack_timer += self.atSpeed
        target_enemy = self.getNewEnemy()
        if target_enemy != None:
            if self.attack_timer > 30:
                self.AttackAnimation(self.unit, target_enemy ,self.damage, self.unit.vision )
                self.attack_timer = 0
                
    def getEnemyDistance(self, enemy):
        if enemy != None: return math.sqrt((self.unit.trueX - enemy.trueX) **2 + (self.unit.trueY - enemy.trueY)**2)
        else: return None

    def getNewEnemy(self):
        units_in_range = []
        for enemy in self.unit.owner.enemies:
            for target in enemy.unitgroup:
                if target != self.unit and target.targetable == True:
                    if self.getEnemyDistance(target) < self.unit.vision:
                        units_in_range.append((self.getEnemyDistance(target),target))
        if units_in_range == []:
            return None
        else:
            return sorted(units_in_range)[0][1]
            
class pasHarvestMineral():
    def __init__(self,  unit,  h_amount=10,  h_speed=1.0):
        self.unit = unit
        self.harvest_amount = h_amount
        self.harvest_speed = float(h_speed)
        self.harvest_progress = 0
        self.with_mineral = False
        self.mineral_target = None        
        
    def update(self):
        if self.unit.action == ID_HARVEST:
            if self.harvest_progress <= 0:
                self.unit.changeImage("with_mineral")
                self.with_mineral = True
                self.mineral_target.hp -= self.harvest_amount
                self.unit.action = ID_STOP # ID_STOP
            else:
                self.harvest_progress -= self.harvest_speed
        else:
            for target_unit in groups.unitgroup:
                if sprite.collide_rect(self.unit, target_unit):
                    if ID_MINERAL in target_unit.types and self.with_mineral == False:
                        self.harvest(target_unit)
                    elif ID_WAREHOUSE in target_unit.types and target_unit.owner == self.unit.owner and self.with_mineral == True:
                        self.returnCargo(target_unit.owner)
                    #elif self.unit != target_unit:
                    #   self.unit.action = ID_MOVE # ID_STOP

    def harvest(self,mineral):
        self.harvest_progress = 100.0
        self.mineral_target = mineral
        self.unit.action = ID_HARVEST

    def getHarvestingProgress(self):
        return (100.0 - self.harvest_progress) / 100.0

    def returnCargo(self, player):
        player.mineral += self.harvest_amount
        self.with_mineral = False
        self.unit.changeImage("base")
