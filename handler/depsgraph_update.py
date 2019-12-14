import bpy
import bmesh
from bpy.app.handlers import persistent
from .. common_utils import redraw

# scene_update_post
def edit_mode_count(act_obj):
    """
    In Edit Mode, the polycount for the active object will be updated
    when the number of selected vertices changes
    :param act_obj: The active object
    """
    # If it is not in Edit Mode goes out
    if bpy.context.mode != 'EDIT_MESH' or act_obj.mode != 'EDIT':
        return
    bm = bmesh.from_edit_mesh(act_obj.data)
    if bm is not None:
        if hasattr(bm.verts, "ensure_lookup_table"):
            bm.verts.ensure_lookup_table()
        verts_sel = [v for v in bm.verts if v.select]
        if bpy.context.scene.Polycount.temp.selected_verts != len(verts_sel):
            # If the number of selected vertices of the active object has changed,
            # the polycount will be updated in this object
            bpy.context.scene.Polycount.temp.selected_verts = len(verts_sel)
            act_obj.Polycount.Updated = False


def check_removed_objs(scene):
    """
    Checks if any mesh object is deleted from the current scene.
    If it is, the function seeks for those deleted objects in all the polycount lists in the scene
    and it removes the deleted objects from them
    :param scene: Current scene
    """
    meshes = len([o for o in scene.objects if o.type == "MESH"])
    if meshes == scene.Polycount.temp.mesh_objs:
        return

    if meshes < scene.Polycount.temp.mesh_objs:
        for l in scene.Polycount.MainUI.lists_List:
            if len(l.list.obj_list) == [o for o in l.list.obj_list
                                        if o.object is not None and o.object.name in scene.objects]:
                continue

            not_in_scene = []
            for i in range(len(l.list.obj_list)):
                obj = l.list.obj_list[i].object
                if obj is None or (obj is not None and obj.name not in scene.objects):
                    not_in_scene.append(i)

            for ob in reversed(not_in_scene):
                l.list.obj_list.remove(ob)

        redraw()

    scene.Polycount.temp.mesh_objs = meshes

@persistent
def polycount_depsgraph_update_post(scene):
    """
    Called on after updating scene data
    :param scene: At appending this function to the scene_update_post, it receives the scene as a parameter.
    """
    check_removed_objs(scene)

    obj = bpy.context.active_object
    if obj is None or not hasattr(obj, 'Polycount') or not hasattr(obj.Polycount, 'Updated'):
        return

    if scene.Polycount.temp.collections != len(bpy.data.collections):
        bpy.context.scene.Polycount.temp.collections = len(bpy.data.collections)
        bpy.ops.collections_list_refresh.btn('EXEC_DEFAULT')

    depsgraph = bpy.context.evaluated_depsgraph_get()
    for update in depsgraph.updates:
        if update.id.original == obj and update.is_updated_geometry:
            obj.Polycount.Updated = False
            if obj.mode != 'EDIT' and scene.Polycount.temp.selected_verts != 0:
                # When the active object is not in Edit mode selected_verts should be 0
                scene.Polycount.temp.selected_verts = 0

    # In Edit Mode
    if scene.Polycount.Draw.EditModePolycount:
        edit_mode_count(obj)
