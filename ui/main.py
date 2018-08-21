import bpy
from .. graphics.draw import Draw
from bpy.types import Operator, Panel
from ..common_utils import redraw, get_region


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

    def draw(self, context):
        region = get_region(context)
        layout = self.layout
        #self.displayPC.PolycountDisplay = context.scene.Polycount.Display and context.region is not None and context.region.id is 4
        icon = 'OUTLINER_OB_LAMP' if context.scene.Polycount.Display else 'LAMP'
        row = layout.row(align=True)
        row.prop(context.scene.Polycount, "Display", text="Polycount", icon=icon)
        if len(context.scene.Polycount.MainUI.window_display)>0:
            icon = "VISIBLE_IPO_ON" if context.scene.Polycount.MainUI.window_display[region.id].display else "VISIBLE_IPO_OFF"
            row.prop(context.scene.Polycount.MainUI.window_display[region.id], "display", text="", icon=icon)

        layout.separator()
        self.object_mode.draw(context, self.layout)
        layout.separator()
        self.edit_mode.draw(context, self.layout)
