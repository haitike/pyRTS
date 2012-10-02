from base_units import *

class Worker(Unit):
    def __init__(self, startx,starty,owner):
        Unit.__init__(self,startx,starty,owner)
        self.image_file = tools.filepath("worker.png")
        self.id = self.ID_WORKER
        self.name = "Worker"
        self.maxHP = 160
        self.speed = 2.5
        self.damage = 8
        self.range = 45
        self.phRes = 0.01

        self.unit_init()

class Ranged(Unit):
    def __init__(self, startx,starty,owner):
        Unit.__init__(self,startx,starty,owner)
        self.image_file = tools.filepath("ranged.png")
        self.id = self.ID_RANGED
        self.name = "Ranged"
        self.AttackAnimation = RangedAttack
        self.maxHP = 90
        self.speed = 2.2
        self.damage = 5
        self.range = 120
        self.atSpeed = 1.2

        self.unit_init()
        

class Tank(Unit):
    def __init__(self, startx,starty,owner):
        Unit.__init__(self,startx,starty,owner)
        self.image_file = tools.filepath("tank.png")
        self.id = self.ID_TANK
        self.name = "Ranged"
        self.AttackAnimation = RangedAttack
        self.maxHP = 175
        self.speed = 1.8
        self.damage = 15
        self.range = 120
        self.atSpeed = 0.6

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
        self.unit_trained = [Worker, Worker, Worker, Ranged, Ranged, Ranged]

        self.unit_init()

class Turret(Building):
    def __init__(self, startx,starty,owner):
        Building.__init__(self,startx,starty,owner)

        self.attack_timer = 30

        self.AttackAnimation = RangedAttack
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
