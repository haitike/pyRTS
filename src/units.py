from base_units import *

class Minion(Unit):
    def __init__(self, startx,starty,owner):
        Unit.__init__(self,startx,starty,owner)
        self.image_file = data.filepath("worker.png")
        self.id = self.ID_WORKER
        self.name = "Worker"
        self.max_hp = 20
        self.speed = 1.5
        self.damage = 4

        self.unit_init()

class Nexus(Building):
    def __init__(self, startx,starty,owner):
        Building.__init__(self,startx,starty,owner)

        self.image_file =  data.filepath("nexus.png")
        self.id = self.ID_CC
        self.name = "Nexus"
        self.hp = 250

        self.unit_init()

class Mineral(NeutralStuff):
    def __init__(self, startx,starty,owner):
        NeutralStuff.__init__(self,startx,starty,owner)

        self.image_file = data.filepath("mineral.png")
        self.id = self.ID_MINERAL
        self.name = "Mineral"

        self.unit_init()
