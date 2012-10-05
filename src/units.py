from passives import *
from base_units import *

class Worker(Unit):
    name = "Worker"
    supply_cost = 1
    mineral_cost = 50
    building_time = 100.0
    
    def __init__(self, startx,starty,owner):
        Unit.__init__(self,startx,starty,owner)
        self.image_files = {"base" : "worker.png",  
                                          "with_mineral" : "worker_with_mineral.png"}
        self.id = ID_WORKER
        self.maxHP = 65
        self.speed = 2.5
        self.damage = 6
        self.range = 45
        
        self.types = (ID_UNIT,  ID_HARVESTER)
        self.passives.append(pasHarvestMineral(self))
        self.unit_init()

class Ranged(Unit):
    name = "Ranged"
    supply_cost = 1
    mineral_cost = 40
    building_time = 100.0
    
    def __init__(self, startx,starty,owner):
        Unit.__init__(self,startx,starty,owner)
        self.image_files = {"base" : "ranged.png"}
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
        self.image_files = {"base" : "tank.png"}
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
        self.image_files = {"base" : "nexus.png"}
        self.size = 5
        self.id = ID_NEXUS
        self.maxHP = 600
        self.phRes = 0.3
        
        self.types = (ID_BUILDING,  ID_WAREHOUSE)        
        self.training_list = [Worker,  Ranged,  Tank]
        
        self.unit_init()

class Turret(Building):
    name = "Turret"
    
    def __init__(self, startx,starty,owner):
        Building.__init__(self,startx,starty,owner)
        self.image_files = {"base" : "turret.png"}
        self.id = ID_TURRET
        self.maxHP = 300
        self.phRes = 0.20
        self.vision = 200
        
        self.passives.append(pasTurretAttack(self, RangedAttack,  12,  1.8))
        self.unit_init()

class MineralPatch(NeutralStuff):
    name = "Mineral"
    
    def __init__(self, startx,starty,owner):
        NeutralStuff.__init__(self,startx,starty,owner)
        self.image_files = {"base" : "mineral.png"}
        self.id = ID_MINERAL_PATCH
        self.maxHP= 150
        self.types = (ID_NEUTRALSTUFF,  ID_MINERAL)
        self.unit_init()
