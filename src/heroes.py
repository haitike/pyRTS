from base_units import *

class Tank(Hero):
    initialAtributes = (14,12,9,16,8) # Vitality, Energy, Strength, Dextery, Inteligence
    InitialSpeed = 3.2
    InitialRange = 170
    isMelee = False
    attackType = Unit.ID_FIRE

    def __init__(self, startx,starty,owner):
        Hero.__init__(self,startx,starty,owner)
        
        self.image_file = tools.filepath("tank.png")
        self.AttackAnimation = RangedMinionAttack
        self.id = self.ID_TANK
        self.name = "Tank"
        
        self.unit_init()
