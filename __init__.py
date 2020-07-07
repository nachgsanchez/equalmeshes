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

import bpy

import reloader
from registrator import register_all_classes, unregister_all_classes
from operators.selector import Selector

keymaps = []

def register():
    reloader.reload_all_modules()
    register_all_classes()

    #We register shortcuts here (for now)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new(Selector.bl_idname, type='E', value='PRESS', shift=True)
    keymaps.append((km, kmi))

def unregister():
    unregister_all_classes()
    for km, i in keymaps:
        km.keymap_items.remove(i)
    keymaps.clear()

if __name__ == '__main__':
    register()