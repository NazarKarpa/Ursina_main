from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
sky = Sky(texture='sky_sunset')



cube = Entity(model='assest/scene', scale=30, collider='box')
ground = Entity(model='quad', texture='grass',
                scale=63, rotation=90, collider='box',
                position=(-2,0,0), texture_scale=(4,4))
cube.position = (0,-1002,3)

# EditorCamera()
EditorCamera()
def input(key):
        if key == 'w':
            cube.position = (0, 0, 0)

app.run()