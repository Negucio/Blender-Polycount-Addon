from . main import \
    VIEW3D_OT_polycount_display, \
    VIEW3D_OT_polycount_other_windows_display, \
    VIEW3D_PT_polycount_main

from . settings import VIEW3D_PT_polycount_settings, \
                       VIEW3D_OT_polycount_save_prefs, \
                       VIEW3D_OT_polycount_reset_prefs

from . misc import VIEW3D_PT_polycount_misc

from . list_Lists import \
    DATA_OT_polycount_lists_list_add, \
    DATA_OT_polycount_lists_list_remove, \
    DATA_OT_polycount_lists_list_to_collection, \
    DATA_UL_polycount_lists_list

from . list_Collections import \
    DATA_OT_polycount_collections_list_refresh, \
    DATA_OT_polycount_collections_list_to_list, \
    DATA_UL_polycount_collections_list

from bpy.utils import register_class, unregister_class

from . import list


def register():
    """
    All interface-related classes are explicitly registered.
    """
    list.register()
    register_class(VIEW3D_OT_polycount_display)
    register_class(VIEW3D_OT_polycount_other_windows_display)

    register_class(DATA_OT_polycount_lists_list_add)
    register_class(DATA_OT_polycount_lists_list_remove)
    register_class(DATA_OT_polycount_lists_list_to_collection)
    register_class(DATA_UL_polycount_lists_list)

    register_class(DATA_OT_polycount_collections_list_refresh)
    register_class(DATA_OT_polycount_collections_list_to_list)
    register_class(DATA_UL_polycount_collections_list)

    register_class(VIEW3D_PT_polycount_main)
    register_class(VIEW3D_OT_polycount_save_prefs)
    register_class(VIEW3D_OT_polycount_reset_prefs)
    register_class(VIEW3D_PT_polycount_settings)
    register_class(VIEW3D_PT_polycount_misc)


def unregister():
    unregister_class(VIEW3D_OT_polycount_display)
    unregister_class(VIEW3D_OT_polycount_other_windows_display)

    unregister_class(VIEW3D_OT_polycount_save_prefs)
    unregister_class(VIEW3D_OT_polycount_reset_prefs)

    unregister_class(DATA_OT_polycount_collections_list_refresh)
    unregister_class(DATA_OT_polycount_collections_list_to_list)
    unregister_class(DATA_UL_polycount_collections_list)

    unregister_class(DATA_OT_polycount_lists_list_add)
    unregister_class(DATA_OT_polycount_lists_list_remove)
    unregister_class(DATA_OT_polycount_lists_list_to_collection)
    unregister_class(DATA_UL_polycount_lists_list)

    list.unregister()
    unregister_class(VIEW3D_PT_polycount_main)
    unregister_class(VIEW3D_PT_polycount_settings)
    unregister_class(VIEW3D_PT_polycount_misc)
