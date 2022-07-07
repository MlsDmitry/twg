from operator import sub, add
import matplotlib.pyplot as plt
import math

from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain, Vec3, BitMask32, TextureStage, Texture, KeyboardButton, LVector3, ModifierButtons
from panda3d.core import loadPrcFileData, rad2Deg, deg2Rad

from core import ModelManager, Player
import core.config


config = """
win-size 1280 720
show-frame-rate-meter 1
sync-video 0
"""
# threading-model Cull/Draw
# """

loadPrcFileData("", config)

class GameScene(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.set_background_color(0, 0, 0, 1)
        
        # set the camera to the correct position to create an isometric view
        self.cam.setPos(0, -6, 0)  # set cam global position
        self.cam.setR(45)  # set cam global Roll rotation
        self.cam.setP(self.cam, 65)  # set cam local Pitch rotation
        self.cam.setPos(self.cam, self.cam.getPos() + Vec3(0, 0, -4))  # set cam local position

        # model manager
        self.model_manager = ModelManager(loader=loader)
        # load models
        self.load_scene()

        self.player = Player()
        self.player.model.reparentTo(render)

        # load texture for cubes
        self.tex = self.loader.loadTexture("textures/LPC_Terrain/block_#.png", multiview=True)

        self.create_map(10, 10)

        self.accept("escape", exit)

        taskMgr.add(self.game_loop, 'game_loop')


    def get_cam_cords(self):
        return self.cam.getX(), self.cam.getY(), self.cam.getZ()

    def load_scene(self):
        # change state of gui to Loading scene
        for model_name, file_path in core.config.models.items():
            model = self.model_manager.load(model_name, file_path) 

    def game_loop(self, task):
        dt = self.clock.dt

        # move player and camera
        self.handle_move(dt)
        self.handle_cam(dt)
        
        
        return task.cont

    def handle_cam(self, dt):
        self.cam.setPos(self.player.model.getPos() + Vec3(-6, -6, -6))
        vec_n = self.player.direction.normalized()
        angle = math.atan2(math.cos(vec_n.x), math.sin(vec_n.z)) + deg2Rad(90)
        # self.cam.setR(rad2Deg(angle))
        # self.cam.setR(45)  # set cam global Roll rotation
        # self.cam.setP(self.cam, 65) 
    
    def handle_move(self, dt):
        SPEED = 1
        direction = Vec3(0)

        if self.mouseWatcherNode.isButtonDown(KeyboardButton.up()):
            direction.z += SPEED
        if self.mouseWatcherNode.isButtonDown(KeyboardButton.down()):
            direction.z -= SPEED
        if self.mouseWatcherNode.isButtonDown(KeyboardButton.left()):
            direction.x -= SPEED
        if self.mouseWatcherNode.isButtonDown(KeyboardButton.right()):
            direction.x += SPEED

        # check if we are moving
        if direction == Vec3(0):
            return

        # check if we are moving backward, if true, then reset velocity.
        self.player.check_backward(direction)

        # assign new direction
        self.player.direction = direction

        # move player towards direction
        self.player.move(dt)
        
        # rotate player towards direction 
        self.player.rotate(dt)

         
    def create_map(self, width, height):
        """ Creates a 2D grid of of tiles. """
        counter = 0
        for z in range(height):
            for x in range(width):
                tile = self.render.attachNewNode(f'tile-{counter}')
                tile.setPos(x, 0, z)
                tile.setTexture(self.tex, 1)
                # tile.setTexScale(TextureStage.getDefault(), 1, 1)
                self.model_manager.get('box').instanceTo(tile)
                counter += 1
                
