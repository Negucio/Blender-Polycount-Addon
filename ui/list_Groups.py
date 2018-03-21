import bpy
from bpy.props import StringProperty
from bpy.types import UIList, Operator


class DATA_UL_polycount_groups_list(UIList):
    """
    List to contain lists of groups
    """
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.alignment = 'EXPAND'
        row = layout.row()
        split = row.split(percentage=0.15)
        icon_visible = 'OUTLINER_OB_LAMP' if item.group_visible else 'LAMP'
        split.prop(item, "group_visible", emboss=False, text="", icon=icon_visible)
        split = split.split(percentage=0.15)
        icon_select = 'VISIBLE_IPO_OFF' if item.group_hide else 'VISIBLE_IPO_ON'
        split.prop(item, "group_hide", text="", emboss=False, icon=icon_select)
        split = split.split()
        split.prop(item.group, "name", text="", emboss=False, icon_value=icon)


class DATA_OT_polycount_groups_list_refresh(Operator):
    """
    Operator to refresh the groups in the scene in the list
    """
    bl_idname = "groups_list_refresh.btn"
    bl_label = "Refresh List"
    bl_description = "Refresh list"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.scene.Polycount.MainUI.grp_list.clear()
        for grp in bpy.data.groups:
            # Add the new group to the list
            item = context.scene.Polycount.MainUI.grp_list.add()
            item.group = grp

        # TODO: Substitute all other tag_redraws in the code for this approach
        for area in bpy.context.screen.areas:
            if area.type in ['VIEW_3D']:
                area.tag_redraw()
        return {'FINISHED'}
