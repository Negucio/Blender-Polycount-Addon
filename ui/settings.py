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
        col.prop(context.scene.Polycount.Draw, "digit_sep", text="Digit Separation")

        row = layout.row()
        col = row.column(align=True)
        col.prop(context.scene.Polycount.Draw, "title_color", text="Title")
        col = row.column(align=True)
        col.prop(context.scene.Polycount.Draw, "data_color", text="Data")
        col = row.column(align=True)
        col.prop(context.scene.Polycount.Draw, "sep_color", text="Sep")

        colMain = layout.column()
        colMain.label("Separate large numbers:")
        box = colMain.box()
        row = box.row()
        row.prop(context.scene.Polycount.Draw, "sep_by_color", text="By color", toggle=True)
        row = box.row()
        col = row.column(align=True)
        col.prop(context.scene.Polycount.Draw, "thousands_color", text="Thousands")
        col = row.column(align=True)
        col.prop(context.scene.Polycount.Draw, "millions_color", text="Millions")

        box = colMain.box()
        row = box.row()
        row.prop(context.scene.Polycount.Draw, "sep_by_char", text="By char", toggle=True)
        row = box.row(align=True)
        row.prop(context.scene.Polycount.Draw, "sep", expand=True)
