import bpy
from bpy.props import BoolProperty
from bpy.types import Operator, UIList


class DATA_UL_polycount_obj_list(UIList):
    """
    List to contain objects (only meshes)
    """
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.alignment = 'EXPAND'
        # The name of the object will be displayed when is added to the list
        row = layout.row()
        split = row.split(percentage=0.15)
        split.prop(item.object, "hide", emboss=False, text="")
        split = split.split(percentage=0.15)
        icon_select = 'RADIOBUT_ON' if item.object.select else 'RADIOBUT_OFF'
        split.prop(item.object, "select", text="", emboss=False, icon=icon_select)
        split = split.split()
        split.prop(item.object, "name", text="", emboss=False, icon_value=icon)


class DATA_OT_polycount_obj_list_add(Operator):
    """
    Operator to add objects to the list
    """
    bl_idname = "obj_list_add.btn"
    bl_label = "Add Object"
    bl_description = "Add object to the list"

    def add_obj_to_list(self, idx, context, obj):
        # Add the obj to the list

        item = context.scene.Polycount.MainUI.lists_List[idx].obj_list.add()
        # item.obj stores the obj
        item.object = obj

    @classmethod
    def poll(cls, context):
        # Enabled when, at least, one mesh object is selected
        selected_objs = [obj for obj in context.selected_objects if obj.type == 'MESH']
        return len(selected_objs) > 0

    def execute(self, context):
        # Retrieve the ids of all objects in the list
        idx = context.scene.Polycount.MainUI.lists_List_Index
        objs_in_list = [o.object for o in context.scene.Polycount.MainUI.lists_List[idx].obj_list]
        for obj in [o for o in context.scene.objects if o.select and o.type == 'MESH']:
            # If the object id is already on the list, continue to the next object
            if obj in objs_in_list:
                continue
            # Append the current object id to the ids
            # Ensures not having duplicated ids in the list
            self.add_obj_to_list(idx, context, obj)
        context.scene.Polycount.controller.refresh(context, force=True)
        return {'FINISHED'}


class DATA_OT_polycount_obj_list_remove(Operator):
    """
    Operator to remove objects from the list
    """
    bl_idname = "obj_list_remove.btn"
    bl_label = "Remove Object"
    bl_description = "Remove object from the list"

    @classmethod
    def poll(cls, context):
        # Enabled when the list contains, at least, one item
        idx = context.scene.Polycount.MainUI.lists_List_Index
        return len(context.scene.Polycount.MainUI.lists_List) > 0 and \
            len(context.scene.Polycount.MainUI.lists_List[idx].obj_list) > 0

    def execute(self, context):
        # Index of the selected item in the list
        list_idx = context.scene.Polycount.MainUI.lists_List_Index
        obj_idx = context.scene.Polycount.MainUI.lists_List[list_idx].obj_list_Index
        # The selected item is removed from the list
        bpy.context.scene.Polycount.MainUI.lists_List[list_idx].obj_list.remove(obj_idx)
        context.scene.Polycount.controller.refresh(context, force=True)
        return {'FINISHED'}


class DATA_OT_polycount_obj_list_clear(Operator):
    """
    Operator to remove objects from the list
    """
    bl_idname = "obj_list_clear.btn"
    bl_label = "Clear list"
    bl_description = "Remove all objects from the list"

    @classmethod
    def poll(cls, context):
        # Enabled when the list contains, at least, one item
        idx = context.scene.Polycount.MainUI.lists_List_Index
        return len(context.scene.Polycount.MainUI.lists_List) > 0 and \
            len(context.scene.Polycount.MainUI.lists_List[idx].obj_list) > 0

    def execute(self, context):
        # Index of the selected item in the list
        list_idx = context.scene.Polycount.MainUI.lists_List_Index
        items = len(context.scene.Polycount.MainUI.lists_List[list_idx].obj_list)
        for obj_idx in reversed(range(items)):
            bpy.context.scene.Polycount.MainUI.lists_List[list_idx].obj_list.remove(obj_idx)
        context.scene.Polycount.controller.refresh(context, force=True)
        return {'FINISHED'}


class DATA_OT_polycount_obj_list_select(Operator):
    """
    Operator to remove objects from the list
    """
    bl_idname = "obj_list_select.btn"
    bl_label = "Select/Deselect Objects"
    bl_description = "Select/Deselect all objects in the list"

    select = BoolProperty(default=True)

    @classmethod
    def poll(cls, context):
        # Enabled when the list contains, at least, one item
        idx = context.scene.Polycount.MainUI.lists_List_Index
        return len(context.scene.Polycount.MainUI.lists_List) > 0 and \
            len(context.scene.Polycount.MainUI.lists_List[idx].obj_list) > 0

    def execute(self, context):
        # Index of the selected item in the list of obj_lists
        idx = context.scene.Polycount.MainUI.lists_List_Index
        for obj in context.scene.Polycount.MainUI.lists_List[idx].obj_list:
            if not hasattr(obj, "object") or type(obj.object) != bpy.types.Object:
                continue
            obj.object.select = self.select
        return {'FINISHED'}


class DATA_OT_polycount_obj_list_hide(Operator):
    """
    Operator to remove objects from the list
    """
    bl_idname = "obj_list_hide.btn"
    bl_label = "Show/Hide Objects"
    bl_description = "Show/Hide Objects all object from the list"

    hide = BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        # Enabled when the list contains, at least, one item
        idx = context.scene.Polycount.MainUI.lists_List_Index
        return len(context.scene.Polycount.MainUI.lists_List) > 0 and \
            len(context.scene.Polycount.MainUI.lists_List[idx].obj_list) > 0

    def execute(self, context):
        # Index of the selected item in the list of obj_lists
        idx = context.scene.Polycount.MainUI.lists_List_Index
        for obj in context.scene.Polycount.MainUI.lists_List[idx].obj_list:
            if not hasattr(obj, "object") or type(obj.object) != bpy.types.Object:
                continue
            obj.object.hide = self.hide
        return {'FINISHED'}

