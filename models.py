from ursina import *
from config import *
from ursina.shaders import basic_lighting_shader
from perlin_noise import PerlinNoise
from random import randint

import pickle

scene.trees = {}


class Tree(Entity):

    def __init__(self, pos, **kwargs):
        super().__init__(
            parent=scene,#Батьківський елемент
            model='assets/minecraft_tree/scene',
            scale=randint(3, 5),
            collider='box',
            position=pos,
            highlight_color=color.gray,
            shader = basic_lighting_shader,
            origin_y = 0.6,
            **kwargs)
        scene.trees[(self.x , self.y, self.z)] = self


class Block(Button):
    id = 4
    def __init__(self, pos, parent_world, block_id = 4, **kwargs):
        super().__init__(
            parent=parent_world,#Батьківський елемент
            model='cube',
            texture=block_texture[block_id],
            scale=1,
            collider='box',
            position=pos,
            color=color.color(0,0,random.uniform(0.9, 1)),
            highlight_color=color.gray,
            shader = basic_lighting_shader,
            origin_y = -0.5,
            **kwargs)
        parent_world.blocks[(self.x, self.y, self.z)] = self
        self.id = block_id



class Chunk(Entity):
    def __init__(self, chunk_pos,  **kwargs):
        super().__init__(model=None, collider=None,shader = basic_lighting_shader, **kwargs)
        self.chunk_pos = chunk_pos
        self.blocks = {}

        self.noise = PerlinNoise(octaves=2, seed=3504)
        self.is_simplify = False
        self.default_texture = 4
        self.generate_chunk()

    def simplify_chunk(self):
        if self.is_simplify:
            return

        self.model = self.combine()
        self.collder = 'mesh'
        self.texture = block_texture[self.default_texture]

        for block in self.blocks.values():
            destroy(block)
        self.is_simplify = True

    def detail_chunk(self):
        if not self.is_simplify:
            return

        self.model = None
        self.collder = None
        self.texture = None
        for pos, block in self.blocks.items():
            detail_block = Block(pos, self, block_id = block.id)
        self.is_simplify = False


    def generate_chunk(self):
        cx, cz = self.chunk_pos
        for x in range(CHUNKZISE):
            for z in range(CHUNKZISE):
                block_x = cx*CHUNKZISE + x
                block_z = cz * CHUNKZISE + z

                y = floor(self.noise([block_x / 24, block_z / 24]) * 6)
                block = Block((block_x, y, block_z), self)


                rand_num = randint(0, 300)
                if rand_num == 52:
                    tree = Tree((block_x, y + 1, block_z))


class WordlEdit(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(**kwargs)
        self.chunks = {}
        self.current_chunk = None
        self.player = player

    def generate_world(self):
        for x in range(WORLDSIZE):
            for z in range(WORLDSIZE):
                chunk_pos = (x,z)
                if chunk_pos not in chunk_pos:
                    chunk = Chunk(chunk_pos)
                    self.chunks[chunk_pos] = chunk

    def save_game(self):
        game_data = {
            'player_pos': (self.player.x, self.player.y, self.player.z),
            'chunks': [],
            'trees': []
        }
        for chunk_pos, chunk in self.chunks.items():
            blocks_data = []
            for block_pos, block, in chunk.blocks.items():
                blocks_data.append((block_pos, block.id))
            game_data['chunks'].append((chunk_pos, blocks_data))

        for tree_pos, tree in scene.trees.items():
            game_data['trees'].append((tree_pos, tree.scale))

        with open('save.dat ', 'wb') as file:
            pickle.dump(game_data, file)
            print('гру збережено')

    def clear_world(self):
        for chunk in self.chunks.values():
            for block in chunk.blocks.values():
                destroy(block)
            destroy(chunk)
        for tree in scene.trees.values():
            destroy(tree)
        scene.trees.clear()
        self.chunks.clear()

    def load_world(self, chunk_data, tree_data):
        for chunk_pos, blocks in chunk_data:
            chunk = Chunk(chunk_pos)
            for block_pos, block_id in blocks:
                Block(block_pos, chunk, block_id)
            self.chunks[chunk_pos] = chunk
        for tree_pos, tree_scale in tree_data:
            tree = Tree(tree_pos)
            tree.scale = tree_scale

    def load_game(self):
        self.clear_world()
        with open('save.dat', 'rb') as file:
            game_data = pickle.load(file)
            self.clear_world()
            self.load_world(game_data['chunks'], game_data['trees'])
            self.player.x, self.player.y, self.player.z = game_data['player_pos']
            print('гру завантажено')

    def input(self, key):
        if key == 'v':
            self.save_game()

        if key == 'l':
            self.load_game()

        if key == 'right mouse down':
            hit_info = raycast(camera.world_position, camera.forward, distance=5)
            if hit_info.hit:
                block = Block(hit_info.entity.position + hit_info.normal, hit_info.entity.parent, Block.id)

        if key == 'left mouse down' and mouse.hovered_entity:
            if isinstance(mouse.hovered_entity, Block):
                block = mouse.hovered_entity
                chunk = block.parent
                del chunk.blocks[(block.x, block.y, block.z)]
                destroy(mouse.hovered_entity)

            if isinstance(mouse.hovered_entity, Tree):
                tree = mouse.hovered_entity

                del scene.trees[(tree.x, tree.y, tree.z)]
                destroy(tree)

        if key == 'scroll up':
            Block.id = Block.id + 1

            if Block.id >= len(block_texture):
                Block.id = 0
        if key == 'scroll down':
            Block.id = Block.id - 1
            if Block.id <= 0:
                Block.id = 7

    def update(self):
        player_pos = self.player.position
        for chunk_pos, chunk in self.chunks.items():
            chunk_wordl_pos = Vec3(chunk_pos[0] * CHUNKZISE, 0, chunk_pos[1]*CHUNKZISE)
            d = distance(player_pos, chunk_wordl_pos)
            if d < DETAIL_DISTANCE and chunk.is_simplify:
                chunk.detail_chunk()
            elif d >= DETAIL_DISTANCE and not chunk.is_simplify:
                chunk.simplify_chunk()



