import bpy
from . scene_load import polycount_load_post
from . scene_update import polycount_scene_update_post

def register():
    if polycount_scene_update_post not in bpy.app.handlers.scene_update_post:
        bpy.app.handlers.scene_update_post.append(polycount_scene_update_post)

    if polycount_load_post not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(polycount_load_post)


def unregister():
    bpy.app.handlers.scene_update_post.remove(polycount_scene_update_post)
    bpy.app.handlers.load_post.remove(polycount_load_post)
