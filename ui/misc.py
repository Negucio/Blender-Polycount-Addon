import bpy
from bpy.types import Panel


class VIEW3D_PT_polycount_misc(Panel):
    bl_label = "Misc"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Polycount"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        tris = col.operator("mesh.select_face_by_sides", text="Select Tris")
        tris.number = 3
        tris.type = 'EQUAL'
        tris.extend = False
        ngons = col.operator("mesh.select_face_by_sides", text="Select Ngons")
        ngons.number = 4
        ngons.type = 'GREATER'
        ngons.extend = False
