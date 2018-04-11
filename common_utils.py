import bpy
from . import bl_info

def get_addon_name():
    return bl_info["name"]

def get_preferences():
    addon_name = get_addon_name()
    return bpy.context.user_preferences.addons[addon_name].preferences

def redraw():
    for area in bpy.context.screen.areas:
        if area.type in ['VIEW_3D']:
            area.tag_redraw()
