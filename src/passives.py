import math

class passTurretAttack():
    def __init__(self, unit,   animation,  range,  damage,  atSpeed):
        self.attack_timer = 30
        self.AttackAnimation = animation
        self.range = range
        self.damage = damage
        self.atSpeed = atSpeed
        self.unit = unit
        
    def update(self):
        if self.attack_timer <= 30: self.attack_timer += self.atSpeed
        target_enemy = self.getNewEnemy()
        if target_enemy != None:
            if self.attack_timer > 30:
                self.AttackAnimation(self.unit, target_enemy ,self.damage, self.range )
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
