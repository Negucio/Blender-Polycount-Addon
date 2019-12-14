import bpy
from bpy.props import StringProperty
from bpy.types import UIList, Operator
from .utils import redraw


class DATA_UL_polycount_collections_list(UIList):
    """
    List to contain lists of collections
    """
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.alignment = 'EXPAND'
        row = layout.row()
        split = row.split(factor=0.15)
        icon_visible = 'HIDE_OFF' if item.collection_visible else 'HIDE_ON'
        split.prop(item, "collection_visible", emboss=False, text="", icon=icon_visible)
        split = split.split(factor=0.15)
        split.prop(item.collection, "hide_viewport", text="", emboss=False)
        split = split.split(factor=0.65)
        split.prop(item.collection, "name", text="", emboss=False, icon_value=icon)
        split = split.split()
        split.prop(item, "collection_color", text="", icon_value=icon)


class DATA_OT_polycount_collections_list_refresh(Operator):
    """
    Operator to refresh the collections from the scene in the list
    """
    bl_idname = "collections_list_refresh.btn"
    bl_label = "Refresh List"
    bl_description = "Refresh list"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.scene.Polycount.MainUI.col_list.clear()
        for col in bpy.data.collections:
            # Add the new group to the list
            item = context.scene.Polycount.MainUI.col_list.add()
            item.collection = col

        redraw()
        return {'FINISHED'}


class DATA_OT_polycount_collections_list_to_list(Operator):
    """
    Operator to create a list with the objects in the selected collection
    """
    bl_idname = "collections_list_to_list.btn"
    bl_label = "CollectionToList"
    bl_description = "Creates a list from the collection"

    @classmethod
    def poll(cls, context):
        return len(context.scene.Polycount.MainUI.col_list) > 0

    def execute(self, context):
        mainUI = context.scene.Polycount.MainUI
        col = mainUI.col_list[mainUI.col_list_index]
        bpy.ops.lists_list_add.btn('EXEC_DEFAULT', name=col.collection.name)
        new_list = mainUI.lists_List[len(mainUI.lists_List)-1]

        for obj in [o for o in col.collection.all_objects if o.type == 'MESH']:
            item = new_list.list.obj_list.add()
            item.object = obj

        redraw()
        return {'FINISHED'}
