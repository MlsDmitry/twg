from panda3d.core import Vec3

from core import ModelManager, SmoothDamper

class Player:

    def __init__(self):
        self.model = ModelManager().get('hero')
        self.model.setPos(Vec3(0, -1, 0))
        # self.model.setScale(100)
        self.model.setP(self.model, 90)
        self.model.setH(self.model, 90)

        self.pos = self.model.getPos()
        self.direction = Vec3(0)
        self.velocity = Vec3(1.5, 0, 1.5)
        self.counter = 0

        self.speed = 2.5
        self.max_speed = 2.5
        self.min_speed = 0.15

        self.damper_x = SmoothDamper(10)
        # self.damper_x.velocity = 0.3
        
        self.damper_z = SmoothDamper(10)

        self.damper_pitch = SmoothDamper(10000)
        # self.damper_z.velocity = 0.3
        
        self.damper_x_vals = []
        self.damper_z_vals = []

    def check_backward(self, new_direction):
        if abs(self.direction.x - new_direction.x) != 0:
            self.damper_x.reset()
        if abs(self.direction.z - new_direction.z) != 0:
            self.damper_z.reset()


    def move(self, dt):
        pos = self.player.model.getPos()

        x = self.player.damper_x.smooth_damp(pos.x, pos.x + direction.x, 0.19, dt)
        z = self.player.damper_z.smooth_damp(pos.z, pos.z + direction.z, 0.19, dt)

        self.model.setPos(Vec3(x, -1, z))

    def rotate(self, dt):
        # normalize direction vector
        vec_n = self.direction.normalized()
        # get angle between x and z in radians and convert to degrees
        angle = rad2Deg(math.atan2(vec_n.x, vec_n.z))
        # adjust angle because of the model rotated wrongly
        angle = self.damper_pitch.smooth_damp(self.player.model.getP(), angle + 270, 0.3, dt)
        # rotate player
        self.player.model.setP(angle)



