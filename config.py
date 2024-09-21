from ursina import load_texture
import os

CHUNKZISE = 10
WORLDSIZE = 2

BASE_DIR = os.getcwd()
IMG_DIR = os.path.join(BASE_DIR, 'assets/cube_grass')
block_texture = []
file_list = os.listdir(IMG_DIR)
for image in file_list:
    texture = load_texture('assets/cube_grass' + os.sep + image)
    block_texture.append(texture)
