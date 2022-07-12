from operator import sub, add
import matplotlib.pyplot as plt
import math

from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain, Vec3, BitMask32, TextureStage, Texture, KeyboardButton, LVector3, ModifierButtons, CollisionTraverser, CollisionHandlerPusher, CollisionNode, CollisionBox, CollisionHandlerQueue, DirectionalLight, AmbientLight, PointLight, OrthographicLens, GeomVertexReader
from panda3d.core import loadPrcFileData, rad2Deg, deg2Rad

from core import ModelManager, Player, SmoothDamper
import core.config


config = """
win-size 1280 720
show-frame-rate-meter 1
sync-video 0
load-file-type p3assimp
"""
# threading-model Cull/Draw
# """

loadPrcFileData("", config)

class GameScene(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.set_background_color(0, 0, 0, 1)
        
        # set the camera to the correct position to create an isometric view
        self.cam.setPos(0, 6, 0)  # set cam global position
        self.cam.setR(45)  # set cam global Roll rotation
        self.cam.setP(self.cam, 65)  # set cam local Pitch rotation
        self.cam.setPos(self.cam, self.cam.getPos() + Vec3(-4, -4, -4))  # set cam local position

        # model manager
        self.model_manager = ModelManager(loader=loader)
        # load models
        self.load_scene()

        # collision code start
        
        # prevents nominated solid objects from intersecting other solid objects.
        self.pusher = CollisionHandlerPusher()
        self.c_handler = CollisionHandlerQueue()
        self.c_trav = CollisionTraverser()
        base.cTrav = self.c_trav
        # collision code end
        
        self.player = Player()
        self.player.model.setTwoSided(True)
        # self.player.model.setColor(0, 1, 1, 1)
        self.player.model.reparentTo(render)
        # print(self.player.collider)
        self.player.initialize_collision()
        # self.c_trav.addCollider(self.player.collider, self.c_handler)

        # axis indication
        # self.axis = loader.loadModel('zup-axis')
        # self.axis.reparentTo(self.render)
        # self.axis.setPos(-1, -1, 0)
        # self.axis.setScale(0.2)

        # load texture for cubes
        self.tex = self.loader.loadTexture("textures/waves5/000.png")

        # creat map
        self.create_map(10, 30)
    
        # self.pusher.addCollider(self.player.collider, self.player.model)
        # self.c_trav.addCollider(self.player.collider, base.pusher)
        # self.c_trav.showCollisions(render)

        self.accept("escape", exit)

        taskMgr.add(self.game_loop, 'game loop')
        taskMgr.add(self.mouse_task, 'mouse task')

        # self.dlnp.lookAt(self.map_model)
        # self.map_model.setLightOff()
        # self.map_model.setLight(self.dlnp)
        # lens = OrthographicLens()
        # lens.setFilmSize(16, 9)
        # lens.setNearFar(-50, 50)
        # self.cam.node().setLens(lens)
        self.map_model.setColor((1, 0, 0, 1))
        self.map_model.reparentTo(render)
        self.map_model.setHpr(180, 90, 0)
        self.map_model.setPos(0, 0, 0)
        print(self.map_model.getTightBounds())
        self.init_light()

    def init_light(self):
        plight = PointLight('plight')
        plight.setColor((0.756, 0.266, 0.054, 1))
        plnp = render.attachNewNode(plight)
        plight.attenuation = (0, 0.1, 0)
        plnp.setPos(2, -10, 2)
        render.setLight(plnp)
        # self.map_model.setLight(plnp)
        

    def record(self):
        self.movie(namePrefix='frame', duration=15, fps=30, format='png')

    def mouse_task(self, task):
        # self.axis.setHpr(self.cam.getHpr())
        return task.cont

    def get_cam_cords(self):
        return self.cam.getX(), self.cam.getY(), self.cam.getZ()

    def load_scene(self):
        # change state of gui to Loading scene
        for model_name, file_path in core.config.models.items():
            model = self.model_manager.load(model_name, file_path) 

    def handle_light(self, dt):
        pass
            
    def game_loop(self, task):
        dt = self.clock.dt

        # move player and camera
        self.handle_move(dt)
        self.handle_cam(dt)
        self.handle_light(dt)

        for i in range(self.c_handler.getNumEntries()):
            entry = self.c_handler.getEntry(i)
            print(entry)

        return task.cont


    def handle_cam(self, dt):
        self.cam.setPos(self.player.model.getPos() + Vec3(-15, -10, -15))
        pass

        
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
            self.player.model.stop()
            return
        
        
        # check if we are moving backward, if true, then reset velocity.
        self.player.check_backward(direction)

        # assign new direction
        self.player.direction = direction

        # move player towards direction
        self.player.move(dt)
        print(self.player.model.get_pos(self.map_model))
        
        # rotate player towards direction 
        self.player.rotate(dt)

        if not self.player.model.getCurrentAnim():
            self.player.model.loop('walk')
        # print(self.player.model.getCurrentAnim())

         
    def create_map(self, width, height):
        """ Creates a 2D grid of of tiles. """
        # counter = 0
        # for z in range(height):
        #     for x in range(width):
        #         tile = self.render.attachNewNode(f'tile-{counter}')
        #         tile.setPos(x, 0, z)
        #         tile.setTexture(self.tex)
        #         self.model_manager.get('box').instanceTo(tile)
        #         tile.find('**/Cube').node().setIntoCollideMask(BitMask32.allOff())
        #         counter += 1
                
        # tile = loader.loadModel('models/box')
        # tile.setPos(1, -2, 1)
        # tile.setColor((1, 0, 1, 1))
        # tile.reparentTo(render)
        # tile.find('**/box').node().setIntoCollideMask(BitMask32.bit(1))
        self.map_model = self.model_manager.get('map')
