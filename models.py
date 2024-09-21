from ursina import *
from config import *
from ursina.shaders import basic_lighting_shader
from perlin_noise import PerlinNoise
from random import randint
class Tree(Entity):

    def __init__(self, pos, parent_world, **kwargs):
        super().__init__(
            parent=parent_world,#Батьківський елемент
            model='assets/minecraft_tree/scene',
            scale=randint(3, 5),
            collider='box',
            position=pos,
            highlight_color=color.gray,
            shader = basic_lighting_shader,
            origin_y = 0.6,
            **kwargs)



class Block(Button):
    id = 4
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
            origin_y = -0.5,
            **kwargs)


class Chunk(Entity):
    def __init__(self, chunk_pos,  **kwargs):
        super().__init__(model=None, collider=None,shader = basic_lighting_shader, **kwargs)
        self.chunk_pos = chunk_pos
        self.blocks = {}
        self.noise = PerlinNoise(octaves=3, seed=4522)
        self.generate_chunk()
    def generate_chunk(self):
        cx, cz = self.chunk_pos
        for x in range(-CHUNKZISE, CHUNKZISE):
            for z in range(-CHUNKZISE, CHUNKZISE):
                block_x = cx*CHUNKZISE + x
                block_z = cz * CHUNKZISE + z

                y = floor(self.noise([x / 24, z / 24]) * 6)
                block = Block((block_x, y, block_z), self)
                self.blocks[(block_x, y, block_z)] = block

                rand_num = randint(0, 300)

                if rand_num == 52:
                    tree = Tree((block_x, y + 1, block_z), self)


class WordlEdit(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chunks = {}
        self.current_chunk = None

    def generate_world(self):
        for x in range(WORLDSIZE):
            for z in range(WORLDSIZE):
                chunk_pos = (x,z)
                if chunk_pos not in chunk_pos:
                    chunk = Chunk(chunk_pos)
                    self.chunks[chunk_pos] = chunk


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

