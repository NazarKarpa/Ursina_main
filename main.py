import random

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
from perlin_noise import PerlinNoise


app = Ursina()
MAPZISE = 10
class Block(Button):
    def __init__(self, pos, **kwargs):
        super().__init__(
            parent=scene,#Батьківський елемент
            model='cube',
            texture='assest/cube_grass/send.png',
            scale=1,
            collider='box',
            position=pos,
            color=color.color(0,0,random.uniform(0.9, 1)),
            origin_y = 0.5,
            **kwargs)

player = FirstPersonController()
sky = Sky(texture='sky_sunset')


# sworod = Entity(model='assest/scene', scale=0.1, collider='box')
# ground = Entity(model='quad', texture='grass',
#                 scale=63, rotation=90, collider='box',
#                 position=(-2,0,0), texture_scale=(4,4))
noise = PerlinNoise(octaves=3, seed=4522)


for x in range(-MAPZISE, MAPZISE):
    for z in range(-MAPZISE, MAPZISE):
        y = floor(noise([x/24, z/24])*6)
        block = Block((x, y, z))

app.run()