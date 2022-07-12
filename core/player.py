import math

from panda3d.core import Vec3, rad2Deg, BitMask32, Point3, CollisionNode, CollisionBox
from direct.actor.Actor import Actor

from core import ModelManager, SmoothDamper, shortest_arc, config

class Player:

    def __init__(self):
        # self.model = ModelManager().get('ball')
        self.model = Actor('egg-models/masha-anim.egg')
        self.model.setPos(Vec3(0, 0, 0))
        self.model.setTwoSided(True)
        self.model.setScale(2)
        # self.model.setColor(0, 0, 0, 1)
        
        self.model.setP(self.model, 90)
        self.model.setH(self.model, 180)

        self.pos = self.model.getPos()
        self.direction = Vec3(0)

        self.damper_x = SmoothDamper(10)
        self.damper_z = SmoothDamper(10)
        self.damper_pitch = SmoothDamper(10000)

        self.collider = None

        
    def check_backward(self, new_direction):
        if abs(self.direction.x - new_direction.x) != 0:
            self.damper_x.reset()
        if abs(self.direction.z - new_direction.z) != 0:
            self.damper_z.reset()


    def move(self, dt):
        pos = self.model.getPos()

        x = self.damper_x.smooth_damp(pos.x, pos.x + self.direction.x, 0.25, dt)
        z = self.damper_z.smooth_damp(pos.z, pos.z + self.direction.z, 0.25, dt)

        self.model.setPos(Vec3(x, 0, z))

    def rotate(self, dt):
        # normalize direction vector
        vec_n = self.direction.normalized()
        # get angle between x and z in radians and convert to degrees
        angle = math.atan2(vec_n.z, vec_n.x)
        angle = rad2Deg(angle)
        # print(self.model.getP(), angle, shortest_arc(self.model.getP(), angle))
        # if angle < 0:
        #     angle = 360 + angle
        # print(angle)
        # adjust angle because of the model rotated wrongly
        angle = self.damper_pitch.smooth_damp(self.model.getP(), angle + 180, 0.3, dt)
        # rotate player
        self.model.setP(angle)

    def initialize_collision(self):
        collide_node = self.model.find('**/Cylinder')
        collide_node.node().setFromCollideMask(BitMask32.bit(1))
        collide_node.node().setIntoCollideMask(BitMask32.allOff())
        collide_node.show()

        self.collider = collide_node
        
