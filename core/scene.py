from operator import sub, add
import matplotlib.pyplot as plt
import math

from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain, Vec3, BitMask32, TextureStage, Texture, KeyboardButton, LVector3, ModifierButtons, CollisionTraverser, CollisionHandlerPusher, CollisionNode, CollisionBox, CollisionHandlerQueue, DirectionalLight, AmbientLight, PointLight, OrthographicLens, GeomVertexReader


from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import TransformState
from panda3d.core import BitMask32
from panda3d.core import Filename
from panda3d.core import PNMImage
from panda3d.core import GeoMipTerrain

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletHeightfieldShape
from panda3d.bullet import ZUp

from panda3d.core import loadPrcFileData

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

        self.set_background_color(1, 1, 1, 1)
        
        # set the camera to the correct position to create an isometric view
        # self.cam.setPos(0, 0, 0)  # set cam global position
        self.cam.setR(45)  # set cam global Roll rotation
        self.cam.setP(self.cam, 65)  # set cam local Pitch rotation
        # self.cam.setPos(self.cam, self.cam.getPos() + Vec3(-4, -4, -4))  # set cam local position
        self.cam.setPos(Vec3(-3200, 0, 50))

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

        # map model
        
        self.map_model.setColor((1, 0, 0, 1))
        self.map_model.reparentTo(render)
        self.map_model.setHpr(180, 0, 90)
        self.cam.setHpr(260, 0, 0)

        print(self.map_model.getTightBounds())
        # self.map_model.setHpr(180, 90, 0)
        # self.map_model.setPos(0, 0, -100)
        # print(self.map_model.getTightBounds())

        # self.worldNP = render.attachNewNode('World')

        # # World
        # self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
        # # self.debugNP.show()
        # # self.debugNP.node().showNormals(True)
        
        # self.world = BulletWorld()
        # self.world.setGravity(Vec3(0, 0, -9.81))
        # self.world.setDebugNode(self.debugNP.node())

        
        height = 8.0
        
        img = PNMImage(Filename('egg-models/heightmap.png'))
        terrainTexture = self.loader.loadTexture("textures/waves5/000.png")

        # self.map_model.setTexture(TextureStage.getDefault(), terrainTexture)
        # self.map_model.setTexScale(TextureStage.getDefault(), 100)
        # shape = BulletHeightfieldShape(img, height, ZUp)
        # shape.setUseDiamondSubdivision(True)

        # np = self.worldNP.attachNewNode(BulletRigidBodyNode('Heightfield'))
        # np.node().addShape(shape)
        # np.setPosheight(0, 0, 0)
        # np.setCollideMask(BitMask32.allOn())

        # self.world.attachRigidBody(np.node())

        # self.hf = np.node() # To enable/disable debug visualisation

        # self.terrain = GeoMipTerrain('terrain')
        # self.terrain.setHeightfield(img)
 
        # self.terrain.setBlockSize(32)
        # self.terrain.setNear(20)
        # self.terrain.setFar(100)
        # self.terrain.setFocalPoint(base.camera)
 
        # root = self.terrain.getRoot()
        # root.setTexture(TextureStage.getDefault(), terrainTexture)
        # root.setTexScale(TextureStage.getDefault(), 100)
        # root.reparentTo(render)
        # root.setSz(400)
        # root.setPos(-100, 0, -100)
        # self.cam.setPos(-50, -500, 0)
        # print(root.getHpr())
        # root.setHpr(0, 90, 0)
        # print(root.getHpr())
        
        # self.terrain.generate()

        
        self.init_light()

    def init_light(self):
        plight = PointLight('plight')
        plight.setColor((0.756, 0.266, 0.054, 1))
        
        plnp = render.attachNewNode(plight)
        plight.attenuation = (1, 0, 0)
        plnp.setPos(500, 200, 4)

        dlight = DirectionalLight('my dlight')
        dlight.setColor((0.756, 0.266, 0.054, 1))
        
        dlnp = render.attachNewNode(dlight)
        dlnp.setPos(500, 200, 4)
        
        render.setLight(plnp)
        
        # self.terrain.getRoot().setLight(dlnp)
        self.map_model.setLight(dlnp)
        

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

        # angle = 10 * dt
        # self.map_model.setP(self.map_model.getP() + angle) 

        # self.world.doPhysics(dt, 10, 0.008)
        # self.terrain.update()
        
        # for i in range(self.c_handler.getNumEntries()):
        #     entry = self.c_handler.getEntry(i)
        #     print(entry)

        return task.cont


    def handle_cam(self, dt):
        self.cam.setPos(self.player.model.getPos() + Vec3(-15, -10, -15))
        pass

        
    def handle_move(self, dt):
        SPEED = 1
        direction = Vec3(0)
        rotation = Vec3(0)

        if self.mouseWatcherNode.isButtonDown(KeyboardButton.asciiKey('w')):
            direction.z += SPEED
        if self.mouseWatcherNode.isButtonDown(KeyboardButton.asciiKey('s')):
            direction.z -= SPEED
        if self.mouseWatcherNode.isButtonDown(KeyboardButton.asciiKey('a')):
            direction.x -= SPEED
        if self.mouseWatcherNode.isButtonDown(KeyboardButton.asciiKey('d')):
            direction.x += SPEED

        if self.mouseWatcherNode.isButtonDown(KeyboardButton.up()):
            rotation.y += SPEED
        if self.mouseWatcherNode.isButtonDown(KeyboardButton.down()):
            rotation.y -= SPEED
        if self.mouseWatcherNode.isButtonDown(KeyboardButton.right()):
            rotation.x -= SPEED
        if self.mouseWatcherNode.isButtonDown(KeyboardButton.left()):
            rotation.x += SPEED

        if rotation != Vec3(0):
            h_angle = 50 * dt * rotation.x
            p_angle = 50 * dt * rotation.y
        
            # self.cam.setHpr(self.cam.getH() + h_angle, self.cam.getP() + p_angle, 0)
            # print(self.cam.getHpr())
            
            
        # check if we are moving
        if direction == Vec3(0):
            self.player.model.stop()
            return

        # x = 500 * dt * direction.x
        # y = 500 * dt * direction.y
         
        # self.cam.setPos(self.cam.getPos() + Vec3(x, y, 0))
        # print(self.cam.getPos())
        # check if we are moving backward, if true, then reset velocity.
        self.player.check_backward(direction)

        # assign new direction
        self.player.direction = direction

        # move player towards direction
        self.player.move(dt)
        
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
        self.map_model = self.model_manager.get('mars_map_00')
        
