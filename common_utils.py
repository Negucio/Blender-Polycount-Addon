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

def get_region(context):
    if context.area.type != 'VIEW_3D':
        return None
    for r in context.area.regions:
        if r.type == 'WINDOW':
            return r

    return None

def manage_windows(region, scene):
    if region is None:
        return

    windows = len(scene.Polycount.MainUI.window_display)
    if windows > region.id:
        return
    count = 0
    while windows<=region.id+1 or count>100:
        item = scene.Polycount.MainUI.window_display.add()
        windows = len(scene.Polycount.MainUI.window_display)
        if count == region.id:
            item.display = True
        count=count+1