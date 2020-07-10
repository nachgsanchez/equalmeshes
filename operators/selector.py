#Util imports
import math

#Blender imports
import bpy
import mathutils

#Project imports
from em.base_classes.registrable import Registrable
from em.core.solver import Solver
from em.core.simple_solver import SimpleSolver

#The menu draw function for the class
def menu_draw(self, context):
    self.layout.operator(Selector.bl_idname)

class Selector(bpy.types.Operator, Registrable):
    bl_idname = "select.select_equal"
    bl_label = "Select Equal Meshes"
    bl_description = "Selects all meshes equal to the active selected geometry"
    bl_options = {'REGISTER', 'UNDO'}

    #Will be used to store keyboard shortcuts
    keymaps = None

    #Treshold is hardcoded for now
    treshold = 0.001

    def execute(self, context):
        if (bpy.context.mode != 'OBJECT'):
            return {'FINISHED'}
            
        active_obj = bpy.context.view_layer.objects.active
        
        #We check that the scene status is valid 
        #If there is no active object, or the active object is not selected (can happen and it's confusing)
        if active_obj is None or not active_obj.select_get():
            self.report({'WARNING'}, 'There is no (active) selected object in the scene.')
            return {'FINISHED'}

        #If it's something other than a mesh
        if active_obj.type != 'MESH':
            self.report({'WARNING'}, 'Active object is not a mesh object.')
            return {'FINISHED'}

        #If it has less than three vertices
        #TODO checking for double vertices 
        if len(active_obj.data.vertices) < 3:
            self.report({'WARNING'}, 'Active object must have 3 or more vertices.')
            return {'FINISHED'}

        wm = bpy.context.window_manager
        
        #Object count in view layer, used to give a rough estimation of progress
        obj_count = len(bpy.context.view_layer.objects)
        
        #We begin the progress cursor
        wm.progress_begin(0, 99)

        for idx, obj in enumerate(bpy.context.view_layer.objects):
            #We do not compare against out active object, and we skip all objects that
            #are not meshes
            if obj.type != 'MESH' or obj == active_obj:
                continue
            
            if len(obj.data.vertices) == len(active_obj.data.vertices):
                s_solver = SimpleSolver(obj, active_obj, Selector.treshold)
                equal = s_solver.Solve()
                
                if equal:
                    obj.select_set(True)
            
            #Update progress
            wm.progress_update(math.ceil(100 * (idx / obj_count)))
        
        wm.progress_end()
        return {'FINISHED'}
    
    @classmethod
    def register(cls):
        bpy.types.VIEW3D_MT_select_object.append(menu_draw)

        #We register shortcuts
        cls.keymaps = []
        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(cls.bl_idname, type='E', value='PRESS', shift=True)
        cls.keymaps.append((km, kmi))

    @classmethod
    def unregister(cls):
        bpy.types.VIEW3D_MT_select_object.remove(menu_draw)

        #We remove shortcuts
        for km, i in keymaps:
            km.keymap_items.remove(i)
    