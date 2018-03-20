from . main import \
    VIEW3D_OT_polycount_display, \
    VIEW3D_PT_polycount_main

from . settings import VIEW3D_PT_polycount_settings, \
                       VIEW3D_OT_polycount_save_prefs, \
                       VIEW3D_OT_polycount_reset_prefs

from . misc import VIEW3D_PT_polycount_misc

from . list_Lists import \
    DATA_OT_polycount_lists_list_add, \
    DATA_OT_polycount_lists_list_remove, \
    DATA_UL_polycount_lists_list

from . list_Groups import \
    DATA_OT_polycount_groups_list_refresh, \
    DATA_UL_polycount_groups_list

from bpy.utils import register_class, unregister_class

from . import list


def register():
    """
    All interface-related classes are explicitly registered.
    """
    list.register()
    register_class(VIEW3D_OT_polycount_display)

    register_class(DATA_OT_polycount_lists_list_add)
    register_class(DATA_OT_polycount_lists_list_remove)
    register_class(DATA_UL_polycount_lists_list)

    register_class(DATA_OT_polycount_groups_list_refresh)
    register_class(DATA_UL_polycount_groups_list)

    register_class(VIEW3D_PT_polycount_main)
    register_class(VIEW3D_OT_polycount_save_prefs)
    register_class(VIEW3D_OT_polycount_reset_prefs)
    register_class(VIEW3D_PT_polycount_settings)
    register_class(VIEW3D_PT_polycount_misc)


def unregister():
    unregister_class(VIEW3D_OT_polycount_display)

    unregister_class(VIEW3D_OT_polycount_save_prefs)
    unregister_class(VIEW3D_OT_polycount_reset_prefs)

    unregister_class(DATA_OT_polycount_groups_list_refresh)
    unregister_class(DATA_UL_polycount_groups_list)

    unregister_class(DATA_OT_polycount_lists_list_add)
    unregister_class(DATA_OT_polycount_lists_list_remove)
    unregister_class(DATA_UL_polycount_lists_list)

    list.unregister()
    unregister_class(VIEW3D_PT_polycount_main)
    unregister_class(VIEW3D_PT_polycount_settings)
    unregister_class(VIEW3D_PT_polycount_misc)