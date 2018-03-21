import bpy
import os


def get_addon_name():
    return os.path.basename(os.path.dirname(os.path.abspath(__file__)))


def get_preferences():
    addon_name = get_addon_name()
    return bpy.context.user_preferences.addons[addon_name].preferences

def redraw():
    for area in bpy.context.screen.areas:
        if area.type in ['VIEW_3D']:
            area.tag_redraw()
