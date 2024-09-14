from ursina import *
from config import *
from ursina.shaders import basic_lighting_shader
from perlin_noise import PerlinNoise


class Block(Button):
    id = 0
    def __init__(self, pos, parent_world, **kwargs):
        super().__init__(
            parent=parent_world,#Батьківський елемент
            model='cube',
            texture=block_texture[Block.id],
            scale=1,
            collider='box',
            position=pos,
            color=color.color(0,0,random.uniform(0.9, 1)),
            highlight_color=color.gray,
            shader = basic_lighting_shader,
            origin_y = 0.5,
            **kwargs)


class WordlEdit(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blocks = {}
        self.noise = PerlinNoise(octaves=3, seed=4522)

    def generate_world(self):
        for x in range(-MAPZISE, MAPZISE):
            for z in range(-MAPZISE, MAPZISE):
                y = floor(self.noise([x / 24, z / 24]) * 6)
                block = Block((x, y, z), self)
                self.blocks[(x,y,z)] = block
    def input(self, key):

        if key == 'right mouse down':
            hit_info = raycast(camera.world_position, camera.forward, distance=5)
            if hit_info.hit:
                block = Block(hit_info.entity.position + hit_info.normal, self)

        if key == 'left mouse down' and mouse.hovered_entity:
            destroy(mouse.hovered_entity)

        if key == 'scroll up':
            Block.id = Block.id + 1

            if Block.id > len(block_texture):
                Block.id = 0
        if key == 'scroll down':
            Block.id = Block.id - 1
            if Block.id < 0:
                Block.id = 0

