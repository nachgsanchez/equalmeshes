import bpy
from base_classes.registrable import Registrable
from operators.selector import Selector

class EqualMeshesPanel(bpy.types.Panel, Registrable):
    bl_idname = 'EM_UI_PANEL'
    bl_label = 'Equal Meshes'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Equal Meshes'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator(Selector.bl_idname)

    @classmethod
    def poll(cls, context):
        return bpy.context.mode == 'OBJECT'