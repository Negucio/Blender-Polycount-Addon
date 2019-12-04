import bpy
from . data import ObjPropertyGroup, ObjListPropertyGroup
from bpy.utils import register_class, unregister_class

from . obj_list import \
    DATA_OT_obj_list_add, \
    DATA_OT_obj_list_remove, \
    DATA_UL_obj_list, \
    DATA_OT_obj_list_select, \
    DATA_OT_obj_list_hide, \
    DATA_OT_obj_list_clear

def register():
    bpy.types.Object.select = bpy.props.BoolProperty(
        set=lambda o, val: o.select_set(val),
        get=lambda o: o.select_get())

    register_class(ObjPropertyGroup)
    register_class(ObjListPropertyGroup)

    register_class(DATA_OT_obj_list_add)
    register_class(DATA_OT_obj_list_remove)
    register_class(DATA_OT_obj_list_select)
    register_class(DATA_OT_obj_list_hide)
    register_class(DATA_OT_obj_list_clear)
    register_class(DATA_UL_obj_list)


def unregister():
    unregister_class(DATA_OT_obj_list_add)
    unregister_class(DATA_OT_obj_list_remove)
    unregister_class(DATA_OT_obj_list_select)
    unregister_class(DATA_OT_obj_list_hide)
    unregister_class(DATA_OT_obj_list_clear)
    unregister_class(DATA_UL_obj_list)

    unregister_class(ObjListPropertyGroup)
    unregister_class(ObjPropertyGroup)
