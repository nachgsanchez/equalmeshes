import bpy
from base_classes.registrable import Registrable

class Selector(bpy.types.Operator, Registrable):
    bl_idname = "em_select.equal"
    bl_label = "Select Equal Meshes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = bpy.context.view_layer.objects.selected.items()
        if (len(selected_objects) == 0):
            self.report({'WARNING'}, 'There is currently no selected object.')
        if (len(selected_objects) > 1):
            self.report({'WARNING'}, 'Multiple selections are currently not supported.')
        
        active_obj = bpy.context.view_layer.objects.active
        return {'FINISHED'} 