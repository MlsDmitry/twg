from operator import sub, add
import matplotlib.pyplot as plt
import math

from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain, Vec3, BitMask32, TextureStage, Texture, KeyboardButton, LVector3, ModifierButtons, CollisionTraverser, CollisionHandlerPusher, CollisionNode, CollisionBox, CollisionHandlerQueue, DirectionalLight, AmbientLight, PointLight, OrthographicLens, GeomVertexReader
from panda3d.core import loadPrcFileData, rad2Deg, deg2Rad, Spotlight, Material, SphereLight, AudioSound
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
        self.player_np.setPos(24, 2, 3)
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

        self.player_npc_collision()

        self.music = []
        self.last_music = 0

        self.init_audio()


    def player_npc_collision(self):
        # ball = loader.load_model('egg-models/ball.egg')

        # shape = BulletSphereShape(2)
        # body = BulletRigidBodyNode('player_npc_collider')
        # body.add_shape(shape)
        # np = self.player_np.attach_new_node(body)

        # # ball.reparentTo(self.player_np)
        # # np.node().set_mass(0)
        # np.set_pos(Vec3(0, 0, 2))
        # self.world.attach_rigid_body(np.node())
        pass
        

    def init_light(self):
        render.setShaderAuto()
        
        sphere_light = PointLight('slight')
        sphere_light.attenuation = (0, 0.1, 0)
        self.light = render.attachNewNode(sphere_light)
        self.light.setPos(Vec3(0, 0, 40))
        self.light.lookAt(self.map_np)
        self.light.node().setScene(render)
        self.light.node().setShadowCaster(True)
        self.light.node().showFrustum()
        self.light.node().getLens().setFov(70)
        self.light.node().getLens().setNearFar(10, 100)
        render.setLight(self.light)


        point_light = PointLight('plight')
        point_light.attenuation = (0, 0.15, 0)
        self.pl_light = self.player_np.attachNewNode(point_light)
        self.pl_light.setPos(Vec3(0, 0, 4))
        self.pl_light.node().setScene(render)
        self.pl_light.node().setShadowCaster(True)
        # self.pl_light.node().showFrustum()
        self.pl_light.node().getLens().setFov(180)
        self.pl_light.node().getLens().setNearFar(10, 1000)
        render.setLight(self.pl_light)
        
        self.alight = render.attachNewNode(AmbientLight("Ambient"))
        self.alight.node().setColor((0.04, 0.04, 0.04, 1))
        render.setLight(self.alight)



    def init_camera(self):
        self.cam.setHpr(45, -30, 0)
        
        self.cam.setPos(Vec3(52, -28, 20))
        
        
        
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
        ft = globalClock.getFrameTime()

        self.world.doPhysics(dt)
        
        # move player and camera
        self.handle_move(dt)
        self.handle_cam(dt)
        self.handle_audio()

        for i in range(self.c_handler.getNumEntries()):
            entry = self.c_handler.getEntry(i)
            # print(entry)

        return task.cont

    def init_audio(self):
        for i in range(1, 12):
            voice = loader.loadSfx(f'sound/{i}.mp3')
            self.music.append(voice)

        for i in range(1, 4):
            music = loader.loadSfx(f'sound/music{i}.mp3')
            self.music.append(music)
        
        self.music[-2].play()
        self.last_music = len(self.music) - 2
        
    def handle_audio(self):
        for audio in self.music:
            if audio.status() == audio.PLAYING:
                return
            
        self.last_music += 1
        if self.last_music == len(self.music) - 1:
            self.last_music = len(self.music) - 3
        
        self.music[self.last_music].play()
    
    
    def handle_cam(self, dt):
        # self.cam.setPos(self.player_np.getPos() + Vec3(-15, -15, 10))
        pass


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
            self.player.model.stop()
            pass
           
        self.player_n.setLinearMovement(direction, True)
        self.player_n.setAngularMovement(angle)

        if not self.player.model.getCurrentAnim():
            self.player.model.loop('walk')
            

         
    def create_map(self, width, height):    
        self.map_model = self.model_manager.get('map')
        # self.map_model.setColor((1, 0, 0, 1))
        self.map_np = self.make_collision_from_model(self.map_model, 'floor', 0, self.world, render, Vec3(12.5, 12.5, -2))

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
        np.node().set_mass(mass)
        np.node().set_friction(0.01)
        np.set_pos(target_pos)
        # np.set_scale(5)
        np.set_h(180)
        np.set_p(180)
        np.set_r(180)
        np.set_collide_mask(BitMask32.allOn())

        world.attach_rigid_body(np.node())

        # input_model.setTextureOff(1)
        # input_model.setMaterialOff(1)
        input_model.reparentTo(np)

        return np
