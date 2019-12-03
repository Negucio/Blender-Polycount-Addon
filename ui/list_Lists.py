import bpy
from bpy.props import StringProperty
from bpy.types import UIList, Operator
from .. common_utils import redraw


class DATA_UL_polycount_lists_list(UIList):
    """
    List to contain lists of objects
    """
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.alignment = 'EXPAND'
        row = layout.row()
        split = row.split(percentage=0.2)
        icon_visible = 'OUTLINER_OB_LAMP' if item.list_visible else 'LAMP'
        split.prop(item, "list_visible", text="", emboss=False, icon=icon_visible)
        split = split.split(percentage=0.7)
        split.prop(item, "list_name", text="", emboss=False, icon_value=icon)
        split = split.split()
        split.prop(item, "list_color", text="", icon_value=icon)


class DATA_OT_polycount_lists_list_add(Operator):
    """
    Operator to add objects to the list
    """
    bl_idname = "lists_list_add.btn"
    bl_label = "New List"
    bl_description = "Add list to the list"

    name: StringProperty(name="name", default='List')

    def resolve_name_collision(self, name, context):
        names_in_list = [l.list_name for l in context.scene.Polycount.MainUI.lists_List]
        ret_name = name
        count = 1
        # While the name is already in the list...
        while ret_name in names_in_list:
            # ...a new name will be created based on the original name
            ret_name = "{0}.{1:0>3}".format(name, count)
            count = count+1
        return ret_name

    def add_to_list(self, name, context):
        # Add the new list to the list
        item = context.scene.Polycount.MainUI.lists_List.add()
        items = len(context.scene.Polycount.MainUI.lists_List)
        # Sets the focus/index on the new list
        context.scene.Polycount.MainUI.lists_List_Index = items-1

        item.list_name = self.resolve_name_collision(name, context)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.add_to_list(self.name, context)
        redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        # A dialog asking for the list name will be displayed
        return wm.invoke_props_dialog(self)


class DATA_OT_polycount_lists_list_remove(Operator):
    """
    Operator to remove the selected object list from the list
    """
    bl_idname = "lists_list_remove.btn"
    bl_label = "Remove List"
    bl_description = "Remove list from the list"

    @classmethod
    def poll(cls, context):
        # Enabled when the list contains, at least, one item
        return len(bpy.context.scene.Polycount.MainUI.lists_List) > 0

    def execute(self, context):
        # Index of the selected item in the list
        index = bpy.context.scene.Polycount.MainUI.lists_List_Index
        # At removing a list, the first item is set
        bpy.context.scene.Polycount.MainUI.lists_List_Index = 0
        # The selected item is remove from the list
        bpy.context.scene.Polycount.MainUI.lists_List.remove(index)
        redraw()
        return {'FINISHED'}


class DATA_OT_polycount_lists_list_to_group(Operator):
    bl_idname = "lists_list_to_group.btn"
    bl_label = "Convert list to group"
    bl_description = "Convert list to group"

    @classmethod
    def poll(cls, context):
        # Enabled when the list contains, at least, one item
        return len(bpy.context.scene.Polycount.MainUI.lists_List) > 0

    def execute(self, context):
        # Index of the selected item in the list
        index = context.scene.Polycount.MainUI.lists_List_Index
        list = context.scene.Polycount.MainUI.lists_List[index]
        grp = bpy.data.groups.new(list.list_name)
        for obj in list.list.obj_list:
            grp.objects.link(obj.object)

        redraw()
        return {'FINISHED'}
