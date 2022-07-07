from panda3d.core import Vec3

from core import ModelManager

class Player:

    def __init__(self):
        self.model = ModelManager().get('hero')
        self.model.setPos(Vec3(0, -1, 0))
        # self.model.setScale(100)
        self.model.setP(self.model, 90)
        self.model.setH(self.model, 180)

        self.pos = self.model.getPos()
        self.vel = Vec3(0)
        self.counter = 0

        self.speed = 5
        self.current_speed = 0
        self.x_vals = []
        self.z_vals = []
        
    def smooth_step(self, dt):
        # return (self.speed * self.velocity
        pass
