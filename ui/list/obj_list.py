import bpy
from bpy.props import BoolProperty, StringProperty
from bpy.types import Operator, UIList
from . utils import get_property, PREFIX

class_ids = {'add': PREFIX + "obj_list_add.btn",
           'remove': PREFIX + "obj_list_remove.btn",
           'clear': PREFIX + "obj_list_clear.btn",
           'select': PREFIX + "obj_list_select.btn",
           'hide': PREFIX + "obj_list_hide.btn",
           'list': PREFIX + "DATA_UL_obj_list"
           }

class ListOperator():
    def updata_data_path(self, context):
        ListOperator.data_path_cls = self.data_path

    data_path = StringProperty(name="data_path", default='', update=updata_data_path)
    data_path_cls = ''

    @staticmethod
    def get_prop(context, data_path):
        return get_property(context, data_path)

    @classmethod
    def has_objects(cls, context):
        prop = cls.get_prop(context, cls.data_path_cls)
        if prop is None:
            return False
        # Enabled when the list contains, at least, one item
        return len(prop.obj_list) > 0


class ObjQuantityOperator(ListOperator):
    @classmethod
    def check_selected_objs(cls, context):
        # Enabled when, at least, one mesh object is selected
        selected_objs = [obj for obj in context.selected_objects if obj.type == 'MESH']
        return len(selected_objs) > 0

    def add_obj_to_list(self, prop, obj):
        # Add the obj to the list
        item = prop.obj_list.add()
        # item.obj stores the obj
        item.object = obj

    def add_objs(self, context):
        prop = self.get_prop(context, self.data_path)
        # Retrieve the ids of all objects in the list
        objs_in_list = [o.object for o in prop.obj_list]
        for obj in [o for o in context.scene.objects if o.select and o.type == 'MESH']:
            # If the object id is already on the list, continue to the next object
            if obj in objs_in_list:
                continue
            # Append the current object id to the ids
            # Ensures not having duplicated ids in the list
            self.add_obj_to_list(prop, obj)

    def remove_obj(self, context):
        prop = self.get_prop(context, self.data_path)
        # Index of the selected item in the list
        obj_idx = prop.obj_list_index
        # The selected item is removed from the list
        prop.obj_list.remove(obj_idx)

    def clear_objs(self, context):
        prop = self.get_prop(context, self.data_path)
        items = len(prop.obj_list)
        for obj_idx in reversed(range(items)):
            prop.obj_list.remove(obj_idx)


class ObjSelectionOperator(ListOperator):
    def select_objs(self, context, select):
        prop = self.get_prop(context, self.data_path)
        for obj in prop.obj_list:
            if not hasattr(obj, "object") or type(obj.object) != bpy.types.Object:
                continue
            obj.object.select = select

class ObjVisibilityOperator(ListOperator):
    def hide_objs(self, context, hide):
        prop = self.get_prop(context, self.data_path)
        for obj in prop.obj_list:
            if not hasattr(obj, "object") or type(obj.object) != bpy.types.Object:
                continue
            obj.object.hide = hide

class DATA_UL_obj_list(UIList):
    """
    List to contain objects (only meshes)
    """
    bl_idname = class_ids['list']

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


class DATA_OT_obj_list_add(ObjQuantityOperator, Operator):
    """
    Operator to add objects to the list
    """
    bl_idname = class_ids['add']
    bl_label = "Add Object(s)"
    bl_description = "Add selected object(s) to the list"


    @classmethod
    def poll(cls, context):
        return cls.check_selected_objs(context)

    def execute(self, context):
        self.add_objs(context)
        return {'FINISHED'}


class DATA_OT_obj_list_remove(ObjQuantityOperator, Operator):
    """
    Operator to remove objects from the list
    """
    bl_idname = class_ids['remove']
    bl_label = "Remove Object"
    bl_description = "Remove object from the list"

    @classmethod
    def poll(cls, context):
        return cls.has_objects(context)

    def execute(self, context):
        self.remove_obj(context)
        return {'FINISHED'}


class DATA_OT_obj_list_clear(ObjQuantityOperator, Operator):
    """
    Operator to remove all the objects from the list
    """
    bl_idname = class_ids['clear']
    bl_label = "Clear list"
    bl_description = "Remove all objects from the list"

    @classmethod
    def poll(cls, context):
        return cls.has_objects(context)

    def execute(self, context):
        self.clear_objs(context)
        return {'FINISHED'}


class DATA_OT_obj_list_select(ObjSelectionOperator, Operator):
    """
    Operator to select/deselect objects from the list
    """
    bl_idname = class_ids['select']
    bl_label = "Select/Deselect Objects"
    bl_description = "Select/Deselect all objects in the list"

    select = BoolProperty(default=True)

    @classmethod
    def poll(cls, context):
        return cls.has_objects(context)

    def execute(self, context):
        self.select_objs(context, self.select)
        return {'FINISHED'}


class DATA_OT_obj_list_hide(ObjVisibilityOperator, Operator):
    """
    Operator to show/hide objects from the list
    """
    bl_idname = class_ids['hide']
    bl_label = "Show/Hide Objects"
    bl_description = "Show/Hide Objects all object from the list"

    hide = BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        return cls.has_objects(context)

    def execute(self, context):
        self.hide_objs(context, self.hide)
        return {'FINISHED'}

