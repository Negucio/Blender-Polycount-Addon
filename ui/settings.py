import bpy

class VIEW3D_PT_polycount_settings(bpy.types.Panel):
    """
    Configures the drawing of the data in the 3DView
    """
    bl_label = "Settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Polycount"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.prop(context.scene.Polycount.Draw, "hor_Offset", text="Offset X")
        col.prop(context.scene.Polycount.Draw, "vert_Offset", text="Offset Y")
        col.prop(context.scene.Polycount.Draw, "font_size", text="Font Size")

        row = layout.row()
        col = row.column(align=True)
        col.prop(context.scene.Polycount.Draw, "title_color", text="Title")
        col = row.column(align=True)
        col.prop(context.scene.Polycount.Draw, "data_color", text="Data")
        col = row.column(align=True)
        col.prop(context.scene.Polycount.Draw, "sep_color", text="Sep")



