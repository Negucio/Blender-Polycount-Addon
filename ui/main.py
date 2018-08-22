import bpy
from .. graphics.draw import Draw
from bpy.types import Operator, Panel
from ..common_utils import redraw, get_region
from . utils import manage_window_visualization


class VIEW3D_OT_polycount_display(Operator):
    bl_idname = "display_polycount.btn"
    bl_label = "Display"
    bl_description = "Display polycount"

    drawing = Draw()

    def execute(self, context):
        if context.scene.Polycount.Display:
            context.scene.Polycount.controller.refresh(context)
            self.drawing.display_polycount(context)
        else:
            self.drawing.hide_polycount(context)

        redraw()
        return {'FINISHED'}

class VIEW3D_OT_polycount_other_windows_display(Operator):
    bl_idname = "display_other_windows_display.btn"
    bl_label = "Display"
    bl_description = "Display polycount in the other 3DViews"

    show = bpy.props.BoolProperty(default=True)

    def execute(self, context):
        region = get_region(context)
        manage_window_visualization(context, region.id, self.show)
        redraw()
        return {'FINISHED'}

class VIEW3D_PT_polycount_main(Panel):
    bl_label = "Polycount"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Polycount"
    # bl_options = {'HIDE_HEADER'}

    @classmethod
    def register(cls):
        # The import needs to be here so that ObjectModeUI and EditModeUI
        # load in the register of this class and not before
        from . classes import ObjectModeUI, EditModeUI
        cls.object_mode = ObjectModeUI()
        cls.edit_mode = EditModeUI()

    @classmethod
    def poll(cls, context):
        return True

    def window_display_button(self, context, layout, region):
        wd = context.scene.Polycount.MainUI.window_display
        if len(wd)==0 or not context.scene.Polycount.Display:
            col = layout.column(align=True)
            col.enabled=False
            col.prop(context.scene.Polycount.MainUI, "window_display_temp", text="", icon="VISIBLE_IPO_OFF")
        else:
            icon = "VISIBLE_IPO_ON" if wd[region.id].display else "VISIBLE_IPO_OFF"
            layout.prop(wd[region.id], "display", text="", icon=icon)

    def other_windows_display_buttons(self, layout):
        box = layout.box()
        col = box.column(align=True)
        row = col.row()
        row.label("Other 3D Views")
        row = col.row(align=True)
        row.operator("display_other_windows_display.btn", text="Show").show = True
        row.operator("display_other_windows_display.btn", text="Hide").show = False

    def draw(self, context):
        region = get_region(context)
        layout = self.layout

        col = layout.column(align=True)
        icon = 'OUTLINER_OB_LAMP' if context.scene.Polycount.Display else 'LAMP'
        row = col.row(align=True)
        row.prop(context.scene.Polycount, "Display", text="Polycount", icon=icon)
        self.window_display_button(context, row, region)

        row = col.row(align=True)
        row.enabled = context.scene.Polycount.Display
        self.other_windows_display_buttons(row)

        layout.separator()
        self.object_mode.draw(context, self.layout)
        layout.separator()
        self.edit_mode.draw(context, self.layout)
