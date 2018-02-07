import bpy
from . scene_load import polycount_load_post
from . scene_update import polycount_scene_update_post
from bpy.app.handlers import scene_update_post, load_post


def register():
    if polycount_scene_update_post not in scene_update_post:
        scene_update_post.append(polycount_scene_update_post)

    if polycount_load_post not in load_post:
        load_post.append(polycount_load_post)


def unregister():
    scene_update_post.remove(polycount_scene_update_post)
    load_post.remove(polycount_load_post)
