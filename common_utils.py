import bpy
from . import bl_info

def get_addon_name():
    return bl_info["name"]

def get_preferences():
    addon_name = get_addon_name()
    return bpy.context.preferences.addons[addon_name].preferences


