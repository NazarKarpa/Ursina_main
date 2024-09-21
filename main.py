
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


app = Ursina()
from config import *
from models import Block, WordlEdit


player = FirstPersonController()
sky = Sky(texture='sky_sunset')
player.x = CHUNKZISE/2
player.z = CHUNKZISE/2
player.y = 20
player.gravity = 0.5

# sworod = Entity(model='assets/scene', scale=0.1, collider='box')
# ground = Entity(model='quad', texture='grass',
#                 scale=63, rotation=90, collider='box',
#                 position=(-2,0,0), texture_scale=(4,4))
camera.clip_plane_far = 12
light = DirectionalLight(shadows=True)
light.look_at(Vec3(-1, -1, -1))
world = WordlEdit()
world.generate_world()


app.run()