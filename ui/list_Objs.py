import bpy
from .. polycount.controller import PolycountController

class DATA_UL_polycount_obj_list(bpy.types.UIList):
    """
    List to contain objects (only meshes)
    """
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.alignment = 'EXPAND'
        # The name of the object will be displayed when is added to the list
        layout.label(item.object.name)


class DATA_OT_polycount_obj_list_add(bpy.types.Operator):
    """
    Operator to add objects to the list
    """
    bl_idname = "obj_list_add.btn"
    bl_label = "Add Object"
    bl_description = "Add object to the list"

    pc = PolycountController()

    def add_obj_toList(self, idx, context, object):
        # Add the object to the list

        item = context.scene.Polycount.MainUI.lists_List[idx].obj_list.add()
        # item.object stores the object
        item.object = object

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
            if obj in objs_in_list: continue
            # Append the current object id to the ids
            # Ensures not having duplicated ids in the list
            self.add_obj_toList(idx, context, obj)
        self.pc.Refresh(context, force=True)
        return {'FINISHED'}


class DATA_OT_polycount_obj_list_remove(bpy.types.Operator):
    """
    Operator to remove objects from the list
    """
    bl_idname = "obj_list_remove.btn"
    bl_label = "Remove Object"
    bl_description = "Remove object from the list"

    pc = PolycountController()

    @classmethod
    def poll(cls, context):
        # Enabled when the list contains, at least, one item
        idx = context.scene.Polycount.MainUI.lists_List_Index
        return len(context.scene.Polycount.MainUI.lists_List)>0 and \
               len(context.scene.Polycount.MainUI.lists_List[idx].obj_list)>0

    def execute(self, context):
        # Index of the selected item in the list
        idx = context.scene.Polycount.MainUI.lists_List_Index
        item = context.scene.Polycount.MainUI.lists_List[idx].obj_list_Index
        # The selected item is removed from the list
        bpy.context.scene.Polycount.MainUI.lists_List[idx].obj_list.remove(item)
        self.pc.Refresh(context, force=True)
        return {'FINISHED'}


