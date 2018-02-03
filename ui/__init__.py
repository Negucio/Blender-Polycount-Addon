import bpy
from . main import \
    VIEW3D_OT_polycount_display, \
    VIEW3D_PT_polycount_main

from . settings import VIEW3D_PT_polycount_settings

from . misc import VIEW3D_PT_polycount_misc

from . list_Objs import \
    DATA_OT_polycount_obj_list_add, \
    DATA_OT_polycount_obj_list_remove, \
    DATA_UL_polycount_obj_list, \
    DATA_OT_polycount_obj_list_select, \
    DATA_OT_polycount_obj_list_hide, \
    DATA_OT_polycount_obj_list_clear

from . list_Lists import \
    DATA_OT_polycount_lists_list_add, \
    DATA_OT_polycount_lists_list_remove, \
    DATA_UL_polycount_lists_list


def register():
    """
    All interface-related classes are explicitly registered.
    """
    bpy.utils.register_class(VIEW3D_OT_polycount_display)

    bpy.utils.register_class(DATA_OT_polycount_obj_list_add)
    bpy.utils.register_class(DATA_OT_polycount_obj_list_remove)
    bpy.utils.register_class(DATA_OT_polycount_obj_list_select)
    bpy.utils.register_class(DATA_OT_polycount_obj_list_hide)
    bpy.utils.register_class(DATA_OT_polycount_obj_list_clear)
    bpy.utils.register_class(DATA_UL_polycount_obj_list)

    bpy.utils.register_class(DATA_OT_polycount_lists_list_add)
    bpy.utils.register_class(DATA_OT_polycount_lists_list_remove)
    bpy.utils.register_class(DATA_UL_polycount_lists_list)


    bpy.utils.register_class(VIEW3D_PT_polycount_main)
    bpy.utils.register_class(VIEW3D_PT_polycount_settings)
    bpy.utils.register_class(VIEW3D_PT_polycount_misc)


def unregister():
    bpy.utils.unregister_class(VIEW3D_OT_polycount_display)

    bpy.utils.unregister_class(VIEW3D_PT_polycount_main)
    bpy.utils.unregister_class(VIEW3D_PT_polycount_settings)
    bpy.utils.unregister_class(VIEW3D_PT_polycount_misc)

    bpy.utils.unregister_class(DATA_OT_polycount_obj_list_add)
    bpy.utils.unregister_class(DATA_OT_polycount_obj_list_remove)
    bpy.utils.unregister_class(DATA_OT_polycount_obj_list_select)
    bpy.utils.unregister_class(DATA_OT_polycount_obj_list_hide)
    bpy.utils.unregister_class(DATA_OT_polycount_obj_list_clear)
    bpy.utils.unregister_class(DATA_UL_polycount_obj_list)

    bpy.utils.unregister_class(DATA_OT_polycount_lists_list_add)
    bpy.utils.unregister_class(DATA_OT_polycount_lists_list_remove)
    bpy.utils.unregister_class(DATA_UL_polycount_lists_list)