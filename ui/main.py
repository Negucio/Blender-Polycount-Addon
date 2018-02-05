import bpy
from .. graphics.draw import Draw

class VIEW3D_OT_polycount_display(bpy.types.Operator):
    bl_idname = "display_polycount.btn"
    bl_label = "Display"
    bl_description = "Display polycount"

    drawing = Draw()

    def execute(self, context):
        if context.scene.Polycount.Display:
            context.scene.Polycount.controller.Refresh(context)
            self.drawing.DisplayPolycount(context)
        else:
            self.drawing.HidePolycount(context)

        if hasattr(context, "area") and context.area is not None: context.area.tag_redraw()
        return {'FINISHED'}


class VIEW3D_PT_polycount_main(bpy.types.Panel):
    bl_label = "Polycount"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Polycount"
    # bl_options = {'HIDE_HEADER'}

    def __init__(self):
        # The import needs to be here so that ObjectModeUI and EditModeUI
        # load in the register of this class and not before
        from .classes import ObjectModeUI, EditModeUI
        self.object_mode = ObjectModeUI()
        self.edit_mode = EditModeUI()

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        icon = 'OUTLINER_OB_LAMP' if context.scene.Polycount.Display else 'LAMP'
        row = layout.row()
        row.prop(context.scene.Polycount, "Display", text="Polycount", icon=icon)

        layout.separator()
        self.object_mode.draw(context, self.layout)
        layout.separator()
        self.edit_mode.draw(context, self.layout)
