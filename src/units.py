from base_units import *

class Worker(Unit):
    name = "Worker"
    supply_cost = 1
    mineral_cost = 50
    building_time = 100.0
    
    def __init__(self, startx,starty,owner):
        Unit.__init__(self,startx,starty,owner)
        self.image_file = tools.filepath("worker.png")
        self.id = ID_WORKER
        self.maxHP = 65
        self.speed = 2.5
        self.damage = 6
        self.range = 45
        self.phRes = 0.01
        
        self.unit_init()

class Ranged(Unit):
    name = "Ranged"
    supply_cost = 1
    mineral_cost = 40
    building_time = 100.0
    
    def __init__(self, startx,starty,owner):
        Unit.__init__(self,startx,starty,owner)
        self.image_file = tools.filepath("ranged.png")
        self.id = ID_RANGED
        self.AttackAnimation = RangedAttack
        self.maxHP = 50
        self.speed = 2.2
        self.damage = 8
        self.range = 120
        self.atSpeed = 1.8

        self.unit_init()
        

class Tank(Unit):
    name = "Tank"
    supply_cost = 2
    mineral_cost = 100
    building_time = 170.0
    
    def __init__(self, startx,starty,owner):
        Unit.__init__(self,startx,starty,owner)
        self.image_file = tools.filepath("tank.png")
        self.id = ID_TANK
        self.AttackAnimation = RangedAttack
        self.maxHP = 125
        self.speed = 1.8
        self.damage = 20
        self.range = 60
        self.atSpeed = 0.6
        self.phRes = 0.1

        self.unit_init()

class Nexus(Building):
    name = "Nexus"
    extra_max_supply = 10
    
    def __init__(self, startx,starty,owner):
        Building.__init__(self,startx,starty,owner)

        self.image_file =  tools.filepath("nexus.png")
        self.size = 5
        self.id = ID_NEXUS
        self.maxHP = 600
        self.phRes = 0.3
        self.training_list = [Worker,  Ranged,  Tank]

        self.unit_init()

class Turret(Building):
    name = "Turret"
    
    def __init__(self, startx,starty,owner):
        Building.__init__(self,startx,starty,owner)

        self.attack_timer = 30

        self.AttackAnimation = RangedAttack
        self.image_file =  tools.filepath("turret.png")
        self.id = ID_TURRET
        self.maxHP = 300
        self.phRes = 0.20
        self.damage = 10
        self.atSpeed = 1.6
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
    name = "Mineral"
    
    def __init__(self, startx,starty,owner):
        NeutralStuff.__init__(self,startx,starty,owner)

        self.image_file = tools.filepath("mineral.png")
        self.id = ID_MINERAL

        self.unit_init()
