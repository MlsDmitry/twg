from operator import sub, add
import matplotlib.pyplot as plt
import math

from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain, Vec3, BitMask32, TextureStage, Texture, KeyboardButton, LVector3, ModifierButtons, CollisionTraverser, CollisionHandlerPusher, CollisionNode, CollisionBox, CollisionHandlerQueue, DirectionalLight, AmbientLight, PointLight, OrthographicLens, GeomVertexReader
from panda3d.core import loadPrcFileData, rad2Deg, deg2Rad, Spotlight
from panda3d.bullet import *

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

        # self.init_light()

        # initialize camera
        self.init_camera()
        
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
        print(self.player.model.findAllMaterials())
        
        # self.player.model.reparentTo(render)
        # self.player.initialize_collision()
        # self.c_trav.addCollider(self.player.collider, self.c_handler)

        # load texture for cubes
        self.tex = self.loader.loadTexture("textures/waves5/000.png")

        taskMgr.add(self.game_loop, 'game loop')
        
        # self.map_model.setHpr(180, 90, 0)
        # print(self.map_model.getPos())
        # self.map_model.setPos(0, 0, -1


        # physics

        # debug stuff
        self.debugNP = render.attachNewNode(BulletDebugNode('Debug'))
        self.debugNP.node().showWireframe(True)
        self.debugNP.node().showConstraints(True)
        self.debugNP.node().showBoundingBoxes(True)
        self.debugNP.node().showNormals(True)
        # self.debugNP.show()

        # world
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.setDebugNode(self.debugNP.node())

        shape = BulletBoxShape(Vec3(30, 30, 30))
        node = BulletRigidBodyNode('World')
        node.addShape(shape)

        self.world_np = render.attachNewNode(node)

        # Plane

        # shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        # node = BulletRigidBodyNode('Ground')
        # node.addShape(shape)
        # np = render.attachNewNode(node)
        # np.setPos(0, 0, -2)
        # self.world.attachRigidBody(node)

        # Boxes
        model = loader.loadModel('models/box.egg')
        model.setPos(-0.5, -0.5, -0.5)
        model.flattenLight()
        
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        node = BulletRigidBodyNode('Box')
        node.setMass(50)
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setPos(-0.5, -0.5, 10)
        self.world.attachRigidBody(node)
        model.copyTo(np)
        
        # player
        height = 4.7
        radius = 0.4
        shape = BulletCapsuleShape(radius, height - 2 * radius, ZUp)

        self.player_n = BulletCharacterControllerNode(shape, 0.4, 'player')
        self.player_np = self.world_np.attachNewNode(self.player_n)
        self.player_np.setPos(24, 2, 1)
        # self.player_np.setP(180)
        self.player_np.setCollideMask(BitMask32.allOn())

        self.world.attachCharacter(self.player_np.node())
        # 
        # print(model.copyTo(self.player_np))
        self.player.model.reparentTo(self.player_np)
        self.player.model.setPos(0, 0, -2)
        

        # Create map
        self.create_map(25, 25)

        self.init_light()

        self.accept('c', self.handle_light)
        self.accept('v', self.handle_light)
        self.accept('b', self.handle_light)

        
        

    def init_light(self):
        # plight = PointLight('plight')
        # plight.setColor((0.756, 0.266, 0.054, 1))
        # plight.setShadowCaster(True, 512, 512)
        # render.setShaderAuto()
        # plight.setColor((1, 0.956, 0.898, 1))
        
        # plnp = self.player_np.attachNewNode(plight)

        # plight.attenuation = (0, 0.1, 0)
        # plnp.setPos(12.5, 12.5, 15)

        # dlight = DirectionalLight('dlight')
        # dlight.setColor((1, 0.956, 0.898, 1))
        # dlight.setDirection(Vec3(0, -1, 0))
        
        # dlnp = render.attachNewNode(dlight)
        # dlnp.setPos(2, 0, 40)

        # alight = AmbientLight('alight')
        # alight.setColor((1, 0.956, 0.898, 1))
        # alight = AmbientLight("alight")
        # alight.setColor((0.04, 0.04, 0.04, 1))
        # alnp = render.attachNewNode(alight)

        # self.map_model.setLight(plnp)
        # self.map_model.setLight(alnp)

        # alnp = render.attachNewNode(alight)
        
        # render.clearLight()
        # render.setLight(alnp)
        # render.setLight(alnp)
        # render.setLight(plnp)
        # self.map_model.setLight(plnp)
        # self.player_np.attachNewNode(plnp)

        self.light_model = loader.loadModel('box')
        self.light_model.setScale(0.2, 0.2, 0.2)
        self.light_model.setPos(4, 4, -40)

        # plight = PointLight("plight")
        # plight.setShadowCaster(True, 2048, 2048)
        render.setShaderAuto()
        # self.map_np.setShaderAuto()

        # plight.setColor((1, 1, 1, 1))
        # plnp = self.player_np.attachNewNode(plight)
        # render.setLight(plnp)
        # plnp.setPos(Vec3(0, 0, 5))
        # self.player_np.setLight(plnp)
        # plight.setAttenuation((1, 0, 0)) # constant, linear, and quadratic.
        # self.map_model.setLight(plnp)
        # self.player_np.setLight(plnp)

        # alight = AmbientLight("alight")
        # alight.setColor((0.08, 0.08, 0.08, 1))
        # alnp = self.player_np.attachNewNode(alight)
        # self.player_np.setLight(alnp)
        
        # render.setLight(alnp)
        # render.setLight(plnp)
        # self.render.setLight(plnp)
        # self.map_np.setLight(plnp)
        # self.map_np.setLight(alnp)
        # self.map_np.setLight(plnp)
        # self.render.setLight(alnp)
#        self.trees.setLight(alnp)
#        self.floor.setLight(alnp)

        # light = render.attachNewNode(Spotlight("Spot"))
        # light.node().setScene(render)
        # light.node().setShadowCaster(True, 1024, 1024)
        # light.node().getLens().setFov(35)
        # #light.node().showFrustum()
        # light.node().getLens().setNearFar(10, 30)
        # render.setLight(light)
        # plight = PointLight('plight')
        # plnp = self.player_np.attachNewNode(plight)
        # self.player_np.setLight(plnp)

        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.04, .04, .04, 1))
        ambient_light = render.attachNewNode(ambientLight)
        render.setLight(ambient_light)

        self.directionalLight = DirectionalLight("directionalLight")
        # directionalLight.setDirection(Vec3(1, 0, 0))
        # directionalLight.setColor((0.6, 0.6, 0.6, 1))
        self.directionalLight.setShadowCaster(True, 1024, 1024)
        light = render.attachNewNode(self.directionalLight)
        render.setLight(light)

        self.light_model.reparentTo(light)
        light.setPos(self.player_np.getPos())

        print(light.node())
        # light.setPos(8, 8, 40)
        # self.direct_light.append(light)
        # render.setLight(light)

        pass

    def init_camera(self):
        # self.cam.setH(45)  # set cam global Roll rotation
        # self.cam.setR(30)
        self.cam.setHpr(45, -30, 0)
        # self.cam.setP(self.cam, 65)  # set cam local Pitch rotation
        # lens = OrthographicLens()
        # lens.setFilmSize(30, 25)
        # # lens.setNearFar(-50, 50)
        # self.cam.node().setLens(lens)
        self.cam.setPos(Vec3(33, -8, 10))
        pass
        
        
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
            
    def game_loop(self, task):
        dt = globalClock.getDt()

        self.world.doPhysics(dt)
        
        # move player and camera
        self.handle_move(dt)
        self.handle_cam(dt)

        for i in range(self.c_handler.getNumEntries()):
            entry = self.c_handler.getEntry(i)
            # print(entry)

        return task.cont

    
    def handle_cam(self, dt):
        # self.cam.setPos(self.player_np.getPos() + Vec3(-15, -15, 10))
        pass

    def handle_light(self):
        direction = self.directionalLight.getDirection()
        add_dir = Vec3(0, 0, 0)
        if self.mouseWatcherNode.isButtonDown(KeyboardButton.asciiKey('c')):
            if (direction.x + 1) == 2:
                add_dir.x = -2
            else:
                add_dir.x = 1
            self.directionalLight.setDirection(direction + add_dir)
        elif self.mouseWatcherNode.isButtonDown(KeyboardButton.asciiKey('v')):
            if (direction.y + 1) == 2:
                add_dir.y = -2
            else:
                add_dir.y = 1
            self.directionalLight.setDirection(direction + add_dir)

        print(self.directionalLight.getDirection())
        
    def handle_move(self, dt):
        SPEED = 30
        direction = Vec3(0)
        angle = 0

        if self.mouseWatcherNode.isButtonDown(KeyboardButton.asciiKey('w')):
            direction.y += SPEED
        if self.mouseWatcherNode.isButtonDown(KeyboardButton.asciiKey('s')):
            direction.y -= SPEED
        if self.mouseWatcherNode.isButtonDown(KeyboardButton.asciiKey('a')):
            direction.x -= SPEED
            angle = 180
        if self.mouseWatcherNode.isButtonDown(KeyboardButton.asciiKey('d')):
            direction.x += SPEED
            angle = -180

        # check if we are moving
        if direction == Vec3(0):
            # self.player.model.stop()
            pass
           
        self.player_n.setLinearMovement(direction, True)
        self.player_n.setAngularMovement(angle)

        # if not self.player.model.getCurrentAnim():
        #     self.player.model.loop('walk')
            

         
    def create_map(self, width, height):
        """ Creates a 2D grid of of tiles. """
        # counter = 0
        # box = loader.loadModel('box')
        # for y in range(height):
        #     for x in range(width):
        #         tile = self.render.attachNewNode(f'tile-{counter}')
        #         tile.setPos(-x, y, 0)
        #         tile.setTexture(self.tex, 1)
        #         box.instanceTo(tile)
        #         counter += 1

        # self.cam.lookAt(tile)
        # tile = loader.loadModel('models/box')
        # tile.setPos(1, -2, 1)
        # tile.setScale(3)
        # # tile.setColor((1, 0, 1, 1))
        # tile.reparentTo(render)
        # tile.find('**/box').node().setIntoCollideMask(BitMask32.bit(1))
        
        self.map_model = self.model_manager.get('map')
        # self.map_model.setColor((1, 0, 0, 1))
        self.map_np = self.make_collision_from_model(self.map_model, 'floor', 1.0, self.world, render, Vec3(12.5, 12.5, -2))
        print(self.map_model.getBounds())


    def make_collision_from_model(self, input_model, rigid_body_name, mass, world, render, target_pos):
        # tristrip generation from static models
        # generic tri-strip collision generator begins
        # 1. Prepare model
        input_model.clear_model_nodes()
        input_model.flatten_strong()
              
        geom_nodes = input_model.find_all_matches('**/+GeomNode')

        mesh = BulletTriangleMesh()
        for geom_np in geom_nodes:
            geom_n = geom_np.node()
            ts = geom_np.getTransform(input_model)
            for geom in geom_n.getGeoms():
                mesh.addGeom(geom, ts)
        
        print(geom_nodes)

        shape = BulletTriangleMeshShape(mesh, dynamic=False)
        body = BulletRigidBodyNode(rigid_body_name)
        body.add_shape(shape)
        np = render.attach_new_node(body)
        # np.node().set_mass(mass)
        # np.node().set_friction(0.01)
        np.set_pos(target_pos)
        # np.set_scale(5)
        np.set_h(180)
        np.set_p(180)
        np.set_r(180)
        np.set_collide_mask(BitMask32.allOn())

        world.attach_rigid_body(np.node())

        input_model.setTextureOff(1)
        input_model.setMaterialOff(1)
        input_model.reparentTo(np)

        return np
