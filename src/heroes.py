from base_units import *

class Tank(Hero):
    def __init__(self, startx,starty,owner):
        Hero.__init__(self,startx,starty,owner)
        self.image_file = tools.filepath("tank.png")
        self.AttackAnimation = RangedMinionAttack
        self.id = self.ID_TANK
        self.name = "Tank"
        self.max_hp = 100
        self.hp_regeneration = 0.008
        self.speed = 3
        self.damage = 15
        self.range = 200
        self.attack_speed = 1.5
        self.armor = 0.05
        self.unit_init()