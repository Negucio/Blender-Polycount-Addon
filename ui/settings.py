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
        col.prop(context.scene.Polycount.Draw, "hor_pos", text="X")
        col.prop(context.scene.Polycount.Draw, "vert_pos", text="Y")
        col.prop(context.scene.Polycount.Draw, "font_size", text="Font Size")
        col.prop(context.scene.Polycount.Draw, "width", text="Width")
        col.prop(context.scene.Polycount.Draw, "height", text="Height")

        row = layout.row()
        col = row.column(align=True)
        col.prop(context.scene.Polycount.Draw, "title_color", text="Title")
        col = row.column(align=True)
        col.prop(context.scene.Polycount.Draw, "data_color", text="Data")
        col = row.column(align=True)
        col.prop(context.scene.Polycount.Draw, "sep_color", text="Sep")

        col = layout.column()
        col.label("Separate large numbers:")
        row = col.row(align=True)
        row.prop(context.scene.Polycount.Draw, "sep_by_color", text="By color", toggle=True)
        row.prop(context.scene.Polycount.Draw, "sep_by_dot", text="By dot", toggle=True)
        col.separator()
        row = col.row()
        col = row.column(align=True)
        col.prop(context.scene.Polycount.Draw, "thousands_color", text="Thousands")
        col = row.column(align=True)
        col.prop(context.scene.Polycount.Draw, "millions_color", text="Millions")





