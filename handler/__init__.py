import bpy
from . scene_load import polycount_load_post
from . depsgraph_update import polycount_depsgraph_update_post
from bpy.app.handlers import depsgraph_update_post, load_post


def register():
    if polycount_depsgraph_update_post not in depsgraph_update_post:
        depsgraph_update_post.append(polycount_depsgraph_update_post)

    if polycount_load_post not in load_post:
        load_post.append(polycount_load_post)


def unregister():
    depsgraph_update_post.remove(polycount_depsgraph_update_post)
    load_post.remove(polycount_load_post)
