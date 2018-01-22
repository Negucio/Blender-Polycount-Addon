import bpy

class DATA_UL_polycount_lists_list(bpy.types.UIList):
    """
    List to contain lists of objects
    """
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.alignment = 'EXPAND'
        row = layout.row()
        row.prop(item, "list_name", text="", emboss=False, icon_value=icon)

class DATA_OT_polycount_lists_list_add(bpy.types.Operator):
    """
    Operator to add objects to the list
    """
    bl_idname = "lists_list_add.btn"
    bl_label = "New List"
    bl_description = "Add list to the list"

    name = bpy.props.StringProperty(name="name", default='List')

    def resolve_name_collision(self, name):
        names_in_list = [l.list_name for l in bpy.context.scene.Polycount.MainUI.lists_List]
        ret_name = name
        count = 1
        # While the name is already in the list...
        while ret_name in names_in_list:
            # ...a new name will be created based on the original name
            ret_name = "{0}.{1:0>3}".format(name, count)
            count = count+1
        return ret_name

    def add_toList(self, name):
        # Add the new list to the list
        item = bpy.context.scene.Polycount.MainUI.lists_List.add()
        items = len(bpy.context.scene.Polycount.MainUI.lists_List)
        # Sets the focus/index on the new list
        bpy.context.scene.Polycount.MainUI.lists_List_Index = items-1

        item.list_name = self.resolve_name_collision(name)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.add_toList(self.name)
        if hasattr(context, "area") and context.area != None: context.area.tag_redraw()

        # # If any object(s) in the scene is/are selected at creating the new list, it/they will be added to it
        # if len(context.selected_objects)>0: bpy.ops.obj_list_add.btn('EXEC_DEFAULT')

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        # A dialog asking for the list name will be displayed
        return wm.invoke_props_dialog(self)

class DATA_OT_polycount_lists_list_remove(bpy.types.Operator):
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
        if hasattr(context, "area") and context.area != None: context.area.tag_redraw()
        return {'FINISHED'}
