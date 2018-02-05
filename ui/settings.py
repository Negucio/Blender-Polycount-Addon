import bpy
from .. common_utils import get_preferences


class SettingsConfirmDialogOp(bpy.types.Operator):
    bl_label = "Are you sure?. This action will save global User Settings"

    def invoke(self, context, event):
        wm = context.window_manager
        # A dialog asking for confirmation will be displayed
        return wm.invoke_confirm(self, event)


class VIEW3D_OT_polycount_save_prefs(SettingsConfirmDialogOp):
    bl_idname = "save_prefs_polycount.btn"
    bl_description = "Make current configuration persistant"

    def execute(self, context):
        prefs = get_preferences()
        prefs.persistent_settings.clone(context.scene.Polycount.Draw)
        bpy.ops.wm.save_userpref()
        return {'FINISHED'}


class VIEW3D_OT_polycount_reset_prefs(SettingsConfirmDialogOp):
    bl_idname = "reset_prefs_polycount.btn"
    bl_description = "Reset configuration to default"

    def execute(self, context):
        prefs = get_preferences()
        context.scene.Polycount.Draw.reset()
        prefs.persistent_settings.reset()
        if hasattr(context, "area") and context.area is not None: context.area.tag_redraw()
        bpy.ops.wm.save_userpref()
        return {'FINISHED'}

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
        col_display = layout.column(align=True)
        col_display.label("Data display:")
        col_display.prop(context.scene.Polycount.Draw, "hor_pos", text="X")
        col_display.prop(context.scene.Polycount.Draw, "vert_pos", text="Y")
        col_display.prop(context.scene.Polycount.Draw, "font_size", text="Font Size")
        col_display.prop(context.scene.Polycount.Draw, "width", text="Width")
        col_display.prop(context.scene.Polycount.Draw, "height", text="Height")
        col_display.prop(context.scene.Polycount.Draw, "digit_sep", text="Digit Separation")

        row = col_display.row(align=True)
        col_display = row.column(align=True)
        col_display.prop(context.scene.Polycount.Draw, "title_color", text="Title")
        col_display = row.column(align=True)
        col_display.prop(context.scene.Polycount.Draw, "data_color", text="Data")
        col_display = row.column(align=True)
        col_display.prop(context.scene.Polycount.Draw, "sep_color", text="Sep")

        col_large_numbers = layout.column(align=True)
        col_large_numbers.label("Separate large numbers:")

        box = col_large_numbers.box()
        col_color = box.column(align=True)
        row = col_color.row()
        row.prop(context.scene.Polycount.Draw, "sep_by_color", text="By color", toggle=True)
        row = col_color.row(align=True)
        col = row.column(align=True)
        col.prop(context.scene.Polycount.Draw, "thousands_color", text="Thousands")
        col = row.column(align=True)
        col.prop(context.scene.Polycount.Draw, "millions_color", text="Millions")

        box = col_large_numbers.box()
        col_sep = box.column()
        row = col_sep.row()
        row.prop(context.scene.Polycount.Draw, "sep_by_char", text="By char", toggle=True)
        row = col_sep.row(align=True)
        row.prop(context.scene.Polycount.Draw, "sep", expand=True)

        col_config = layout.column(align=True)
        col_config.label("Configuration:")
        row = col_config.row()
        row.operator("save_prefs_polycount.btn", text="Save current configuration")
        row = col_config.row(align=True)
        row.operator("reset_prefs_polycount.btn", text="Reset config to default")


