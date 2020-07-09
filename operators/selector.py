import bpy
from base_classes.registrable import Registrable
from core.solver import Solver
from core.simple_solver import SimpleSolver

import math
import mathutils

#The menu draw function for the class
def menu_draw(self, context):
    self.layout.operator(Selector.bl_idname)

class Selector(bpy.types.Operator, Registrable):
    bl_idname = "select.select_equal"
    bl_label = "Select Equal Meshes"
    bl_description = "Selects all meshes equal to the active selected geometry"
    bl_options = {'REGISTER', 'UNDO'}

    #Treshold is hardcoded for now
    treshold = 0.001

    def execute(self, context):
        if (bpy.context.mode != 'OBJECT'):
            return {'FINISHED'}
            
        active_obj = bpy.context.view_layer.objects.active
        
        #We check that the scene status is valid 
        if active_obj is None or not active_obj.select_get():
            self.report({'WARNING'}, 'There is no (active) selected object in the scene.')
            return {'FINISHED'}
        if active_obj.type != 'MESH':
            self.report({'WARNING'}, 'Active object is not a mesh object.')
            return {'FINISHED'}
        if len(active_obj.data.vertices) < 3:
            self.report({'WARNING'}, 'Active object must have 3 or more vertices.')
            return {'FINISHED'}

        obj_count = len(bpy.context.view_layer.objects)
        wm = bpy.context.window_manager
        wm.progress_begin(0, 99)
        for idx, obj in enumerate(bpy.context.view_layer.objects):
            if obj.type != 'MESH' or obj == active_obj:
                continue
            if len(obj.data.vertices) == len(active_obj.data.vertices):
                s_solver = SimpleSolver(obj, active_obj, Selector.treshold)
                equal = s_solver.Solve()
                if equal:
                    obj.select_set(True)
            wm.progress_update(math.ceil(100 * (idx / obj_count)))
        wm.progress_end()
        return {'FINISHED'}
    
    @classmethod
    def register(cls):
        bpy.types.VIEW3D_MT_select_object.append(menu_draw)

    @classmethod
    def unregister(cls):
        bpy.types.VIEW3D_MT_select_object.remove(menu_draw)
    