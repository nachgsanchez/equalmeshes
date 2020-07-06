bl_info = {
    'name': 'Equal Meshes',
    'author': 'Nacho Sanchez',
    'version': (0, 1, 0, 0),
    'blender': (2, 80, 0),
    'category': 'Mesh'
}

import sys
from os.path import dirname, realpath

dir_path = dirname(realpath(__file__))
sys.path.append(dir_path)

import reloader
from registrator import register_all_classes, unregister_all_classes
def register():
    reloader.reload_all_modules()
    register_all_classes()

def unregister():
    unregister_all_classes()

if __name__ == '__main__':
    register()