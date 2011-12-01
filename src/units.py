from base_units import *

class Minion(Unit):
    def __init__(self, startx,starty,owner):
        Unit.__init__(self,startx,starty,owner)
        self.image_file = tools.filepath("minion.png")
        self.id = self.ID_MINION
        self.name = "Minion"
        self.max_hp = 20
        self.speed = 2.5
        self.damage = 5
        self.range = 45

        self.unit_init()

class RangedMinion(Unit):
    def __init__(self, startx,starty,owner):
        Unit.__init__(self,startx,starty,owner)
        self.image_file = tools.filepath("ranged_minion.png")
        self.id = self.ID_RANGEDMINION
        self.name = "Ranged Minion"
        self.AttackAnimation = RangedMinionAttack
        self.max_hp = 16
        self.speed = 2
        self.damage = 3
        self.range = 150
        self.attack_speed = 1.2

        self.unit_init()

class Nexus(Building):
    def __init__(self, startx,starty,owner,creation_point,target_point):
        Building.__init__(self,startx,starty,owner,creation_point,target_point)

        self.image_file =  tools.filepath("nexus.png")
        self.id = self.ID_NEXUS
        self.name = "Nexus"
        self.max_hp = 250
        self.armor = 0.2
        self.unit_trained = RangedMinion

        self.unit_init()

class Turret(Building):
    def __init__(self, startx,starty,owner,creation_point,target_point):
        Building.__init__(self,startx,starty,owner,creation_point,target_point)

        self.attack_timer = 30

        self.AttackAnimation = RangedMinionAttack
        self.image_file =  tools.filepath("turret.png")
        self.id = self.ID_TURRET
        self.name = "Turret"
        self.max_hp = 150
        self.armor = 0.25
        self.damage = 20
        self.vision = self.range = 200

        self.unit_init()

    def update(self, players):
        BaseObject.update(self,players)
        if self.attack_timer <= 30: self.attack_timer += self.attack_speed
        self.target_enemy = self.getNewEnemy(players)
        if self.target_enemy != None:
            if self.attack_timer > 30:
                players[self.owner].animations.add(self.AttackAnimation(self, self.target_enemy ,self.damage, self.range ))
                self.attack_timer = 0


class Mineral(NeutralStuff):
    def __init__(self, startx,starty,owner):
        NeutralStuff.__init__(self,startx,starty,owner)

        self.image_file = tools.filepath("mineral.png")
        self.id = self.ID_MINERAL
        self.name = "Mineral"

        self.unit_init()
