from operator import sub, add

from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain, Vec3, BitMask32, TextureStage, Texture, KeyboardButton, LVector3, ModifierButtons
from panda3d.core import loadPrcFileData

from core import ModelManager, Player
import core.config


config = """
win-size 1280 720
show-frame-rate-meter 1
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
        # self.model_manager.loader = loader
        self.load_scene()
        # self.player = loader.loadModel("egg-models/anime-girl.egg")
        # self.player = loader.loadModel("egg-models/human.egg")
        self.player = Player()
        self.player.model.reparentTo(render)
        # self.player.setPos(0, -1, 0)
        # self.player.setScale(0.1)
        # self.player.setP(self.player, 90)
        # self.player.setH(self.player, 180)
        
        # min_v, max_v = self.player.getTightBounds()
        # print(max_v - min_v)
        # load the 3D models
        # self.plane = self.loader.loadModel("egg-models/plane")
        self.tex = self.loader.loadTexture("textures/LPC_Terrain/block_#.png", multiview=True)
        # self.tex.setWrapU(Texture.WM_repeat)
        # self.tex.setWrapV(Texture.WM_repeat)
        # self.plane.setTexture(self.tex1)

        # self.box = self.loader.loadModel("egg-models/box.egg")
        # self.box.reparentTo(self.render)
# create an empty node path
        # self.my_map = self.render.attachNewNode("iso-map")
        # fill the empty node path with grid tiles
        self.create_map(10, 10)

        # self.cam.setPos(0, -100, 0)

        # self.terrain = GeoMipTerrain("waves")
        # self.terrain.setHeightfield("textures/waves5/199.png")
        # self.terrain.setColorMap("textures/seamlessTextures/100_1374_seamless.JPG")
        # self.terrain.getRoot().setSz(35)
        # self.terrain.getRoot().reparentTo(render)
        # self.terrain.generate()

        # z = self.terrain.getElevation(256, 256) * 40
        # self.cam.setPos(0, 0, z)

        # self.terrain.setFocalPoint(self.cam)
        # self.taskMgr.add(self.updateTerrain, "update terrain")

        self.accept("escape", exit)
        # self.accept("w", self.move, ["up"])
        # # self.accept("w-up", self.endWalk)
        # self.accept("s", self.move, ["down"])
        # # self.accept("s-up", self.endReverse)
        # self.accept("a", self.move, ["left"])
        # # self.accept("a-up", self.endTurnLeft)
        # self.accept("d", self.move, ["right"])
        # self.accept("d-up", self.endTurnRight)
        taskMgr.add(self.game_loop, 'game_loop')


    def get_cam_cords(self):
        return self.cam.getX(), self.cam.getY(), self.cam.getZ()

    def load_scene(self):
        # change state of gui to Loading scene
        for model_name, file_path in core.config.models.items():
            model = self.model_manager.load(model_name, file_path) 

    def game_loop(self, task):
        dt = self.clock.dt
        self.handle_move(dt)
        
        return task.cont

    
    def handle_move(self, dt):
        SPEED = 1 #constant
        direction = Vec3(0)

        if self.mouseWatcherNode.isButtonDown(KeyboardButton.up()):
            direction.z += SPEED
        if self.mouseWatcherNode.isButtonDown(KeyboardButton.down()):
            direction.z -= SPEED
        if self.mouseWatcherNode.isButtonDown(KeyboardButton.left()):
            direction.x -= SPEED
        if self.mouseWatcherNode.isButtonDown(KeyboardButton.right()):
            direction.x += SPEED

        if abs(self.player.direction.x - direction.x) != 0:
            self.player.velocity.x = 1.5 
        if abs(self.player.direction.z - direction.z) != 0:
            self.player.velocity.z = 1.5 
        
        # print(self..mouseWatcherNode.isButtonDown(KeyboardButton.
        if direction.x != 0 or direction.z != 0:
            self.player.direction = direction

            pos = self.player.model.getPos()

            x = self.player.smooth_damp(pos.x, pos.x + direction.x, self.player.velocity.x, 0.3, 2.5, dt)
            z = self.player.smooth_damp(pos.z, pos.z + direction.z, self.player.velocity.z, 0.3, 2.5, dt)
            print(self.player.model.getPos() - Vec3(x, 0, z), self.player.velocity)
            self.player.model.setPos(Vec3(x * direction.x, -1, z * direction.z))
            # next_pos = self.player.smooth_damp(self.player.model.getPos(), self.player.model.getPos() + direction, self.player.velocity, 0.3, self.player.max_speed, dt)
            # print(next_pos)
            
            # x = self.player.smooth_step(self.player.velocity.x * dt * 1.5)
            # z = self.player.smooth_step(self.player.velocity.z * dt * 1.5)
            # print(self.player.velocity, x, z)
            
            # self.player.velocity = self.player.velocity + Vec3(x, 0, z)

            # print(self.player.velocity, self.player.velocity.length())

            # if self.player.velocity.length() > self.player.speed:
            #     self.player.velocity = Vec3(self.player.speed ** 0.5, 0, self.player.speed ** 0.5)
            # print('============')
            # print('Smooth step:', Vec3(self.player.velocity.x * direction.x, 0, self.player.velocity.z * direction.z))
            # print('Simple:', Vec3(direction * dt * self.player.speed))
            # print('============')
            
            # self.player.model.setPos(self.player.model.getPos() + Vec3(self.player.velocity.x * direction.x, 0, self.player.velocity.z * direction.z))
            # self.cam.lookAt(self.player.model.getPos())


    def updateTerrain(self, task):
        self.terrain.update()
        return task.cont

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
                
