from operator import sub, add

from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain, Vec3, BitMask32, TextureStage, Texture
from panda3d.core import loadPrcFileData


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

        # self.hero = loader.loadModel("egg-models/anime-girl.egg")
        self.hero = loader.loadModel("egg-models/human.egg")
        self.hero.reparentTo(render)
        self.hero.setPos(0, -1, 0)
        # self.hero.setScale(0.1)
        self.hero.setP(self.hero, 90)
        self.hero.setH(self.hero, 180)

        min_v, max_v = self.hero.getTightBounds()
        print(max_v - min_v)

        # load the 3D models
        # self.plane = self.loader.loadModel("egg-models/plane")
        self.tex = self.loader.loadTexture("textures/LPC_Terrain/block_#.png", multiview=True)
        # self.tex.setWrapU(Texture.WM_repeat)
        # self.tex.setWrapV(Texture.WM_repeat)
        # self.plane.setTexture(self.tex1)

        self.box = self.loader.loadModel("egg-models/box.egg")
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
        self.accept("w", self.move, ["up"])
        # self.accept("w-up", self.endWalk)
        self.accept("s", self.move, ["down"])
        # self.accept("s-up", self.endReverse)
        self.accept("a", self.move, ["left"])
        # self.accept("a-up", self.endTurnLeft)
        self.accept("d", self.move, ["right"])
        # self.accept("d-up", self.endTurnRight)


    def get_cam_cords(self):
        return self.cam.getX(), self.cam.getY(), self.cam.getZ()

    def move(self, direction):
        pos = self.hero.getPos()
        if direction == "left":
            self.hero.setPos(pos + Vec3(-1, 0, 0))
        elif direction == "right":
            self.hero.setPos(pos + Vec3(1, 0, 0))
        elif direction == "up":
            self.hero.setPos(pos + Vec3(0, 0, 1))
        elif direction == "down":
            self.hero.setPos(pos + Vec3(0, 0, -1))
                    
        
    # def move_forward(self):
    #     x, y, z = tuple(map(add, self.get_cam_cords(), (0, 1, 0)))
    #     self.cam.setPos(x, y, z)


    # def move_backward(self):
    #     x, y, z = tuple(map(sub, self.get_cam_cords(), (0, 1, 0)))
    #     self.cam.setPos(x, y, z)
                

    # def move_left(self):
    #     x, y, z = tuple(map(sub, self.get_cam_cords(), (1, 0, 0)))
    #     self.cam.setPos(x, y, z)


    # def move_right(self):
    #     x, y, z = tuple(map(add, self.get_cam_cords(), (1, 0, 0)))
    #     self.cam.setPos(x, y, z)
    

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
                self.box.instanceTo(tile)
                counter += 1
                
