from base_units import *

class Minion(Unit):
    def __init__(self, startx,starty,owner):
        Unit.__init__(self,startx,starty,owner)
        self.image_file = tools.filepath("minion.png")
        self.id = self.ID_MINION
        self.name = "Minion"
        self.maxHP = 160
        self.speed = 2.5
        self.damage = 8
        self.range = 45
        self.phRes = 0.01

        self.unit_init()

class RangedMinion(Unit):
    def __init__(self, startx,starty,owner):
        Unit.__init__(self,startx,starty,owner)
        self.image_file = tools.filepath("ranged_minion.png")
        self.id = self.ID_RANGEDMINION
        self.name = "Ranged Minion"
        self.AttackAnimation = RangedMinionAttack
        self.maxHP = 100
        self.speed = 2.1
        self.damage = 5
        self.range = 120
        self.atSpeed = 1.2

        self.unit_init()

class Nexus(Building):
    def __init__(self, startx,starty,owner,creation_point,target_point):
        Building.__init__(self,startx,starty,owner, creation_point, target_point)

        self.image_file =  tools.filepath("nexus.png")
        self.size = 5
        self.id = self.ID_NEXUS
        self.name = "Nexus"
        self.maxHP = 1500
        self.phRes = 0.3
        self.unit_trained = [Minion, Minion, Minion, RangedMinion, RangedMinion, RangedMinion]

        self.unit_init()

class Turret(Building):
    def __init__(self, startx,starty,owner):
        Building.__init__(self,startx,starty,owner)

        self.attack_timer = 30

        self.AttackAnimation = RangedMinionAttack
        self.image_file =  tools.filepath("turret.png")
        self.id = self.ID_TURRET
        self.name = "Turret"
        self.maxHP = 1200
        self.phRes = 0.20
        self.damage = 30
        self.atSpeed = 2
        self.vision = self.range = 200

        self.unit_init()

    def update(self, seconds):
        BaseObject.update(self,seconds)
        if self.attack_timer <= 30: self.attack_timer += self.atSpeed
        self.target_enemy = self.getNewEnemy()
        if self.target_enemy != None:
            if self.attack_timer > 30:
                self.AttackAnimation(self, self.target_enemy ,self.damage, self.range )
                self.attack_timer = 0


class Mineral(NeutralStuff):
    def __init__(self, startx,starty,owner):
        NeutralStuff.__init__(self,startx,starty,owner)

        self.image_file = tools.filepath("mineral.png")
        self.id = self.ID_MINERAL
        self.name = "Mineral"

        self.unit_init()
