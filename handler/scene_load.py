import bpy
from bpy.app.handlers import persistent
from .. common_utils import get_preferences


@persistent
def polycount_load_post(param):
    """
    Called on after loading a .blend file
    :param param: In order to append this function to the load_post handler, this has to receive a parameter. Always None.
    """
    scn = bpy.context.scene

    if not scn.Polycount.polycounted:
        prefs = get_preferences()
        if prefs is not None: scn.Polycount.Draw.clone(prefs.persistent_settings)

    # At loading the .blend file, scene var "selected_verts" should be 0
    bpy.context.scene.Polycount.temp.selected_verts = 0

    # Assigning the var to itself forces the calling of its update function
    # This activates the Polycount at loading a scene
    scn.Polycount.Display = scn.Polycount.Display

    # TODO: Could be in preferences. Let the user the choice
    # If the list of lists is empty, empty list named "Default" will be added
    if len(bpy.context.scene.Polycount.MainUI.lists_List)==0:
        item = bpy.context.scene.Polycount.MainUI.lists_List.add()
        item.list_name = "Default"