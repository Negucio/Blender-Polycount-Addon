import bpy
import bmesh
from . utils import get_mirror_axis, calculate_subsurf, has_solidify, get_levels_subsurf
from .. data.utils import reset_data_property
from ..ui.utils import redraw

class PolycountController:

    def object_mode(self, obj, polygons, bm=False):
        """

        :param obj:
        :param polygons:
        :param bm: bmesh
        :return:
        """
        if obj is None or not hasattr(obj, 'type') or obj.type != 'MESH':
            return None
        if not hasattr(obj, 'Polycount'):
            return None
        pure_tris = 0
        face_tris = 0
        quads = 0
        ngons = 0

        if bm:
            polygons.ensure_lookup_table()

        for poly in polygons:
            v = len(poly.verts) if bm else len(poly.vertices)

            if v == 3:
                pure_tris += 1
            elif v == 4:
                quads += 1
                face_tris += 2
            else:
                ngons += 1
                face_tris += (v - 2)

        tris = pure_tris + face_tris
        faces = pure_tris + quads + ngons

        obj.Polycount.Data.PureTriangles = pure_tris
        obj.Polycount.Data.Triangles = tris
        obj.Polycount.Data.Quads = quads
        obj.Polycount.Data.Ngons = ngons
        obj.Polycount.Data.Faces = faces
        obj.Polycount.MirrorAxis = get_mirror_axis(obj)
        obj.Polycount.HasSolidify = has_solidify(obj)
        obj.Polycount.Updated = True

    def edit_mode(self, obj, bm):
        if obj is None or not hasattr(obj, 'type') or obj.type != 'MESH':
            return None
        if not hasattr(obj, 'Polycount'):
            return None

        scn = bpy.context.scene

        verts = [v for v in bm.verts if v.select]
        edges = [e for e in bm.edges if e.select]
        faces = [f for f in bm.faces if f.select]

        tris = 0
        for face in faces:
            v = len(face.verts)
            if v == 3:
                tris += 1
            elif v == 4:
                tris += 2
            else:
                tris += (v - 2)

        scn.Polycount.EditMode.Triangles = tris
        scn.Polycount.EditMode.Verts = len(verts)
        scn.Polycount.EditMode.Edges = len(edges)
        scn.Polycount.EditMode.Faces = len(faces)

    def calculate_polycount(self, obj):
        if bpy.context.mode == 'EDIT_MESH' and bpy.context.active_object == obj:
            bm = bmesh.from_edit_mesh(obj.data)
            self.object_mode(obj, bm.faces, bm=True)
            self.edit_mode(obj, bm)
        else:
            self.object_mode(obj, obj.data.polygons, bm=False)

    def set_data(self, objects, data_property):
        if objects is None:
            return
        reset_data_property(data_property)
        for obj in objects:
            if obj.type != 'MESH':
                continue
            if not obj.Polycount.Updated:
                self.calculate_polycount(obj)

            tris = obj.Polycount.Data.Triangles
            pure_tris = obj.Polycount.Data.PureTriangles
            quads = obj.Polycount.Data.Quads
            ngons = obj.Polycount.Data.Ngons
            faces = obj.Polycount.Data.Faces

            mirror_mult = 1
            solidify_mult = 1

            draw = bpy.context.scene.Polycount.Draw
            levels = get_levels_subsurf(obj)
            if draw.modifiers:
                if draw.subsurf and levels > 0:
                    data = obj.Polycount.Data
                    quads = calculate_subsurf(obj, data.PureTriangles, data.Quads, data.Ngons)
                    tris = quads * 2
                    faces = quads
                    ngons = 0
                    pure_tris = 0

                # TODO: Approximate. Merge and clipping should be taking into account
                if draw.mirror:
                    mirror_mult = 2 ** obj.Polycount.MirrorAxis

                # TODO: Approximate. Should be calculated counting how many edges are border and adding to the account
                if draw.solidify and obj.Polycount.HasSolidify:
                    solidify_mult = 2

            data_property.Triangles += tris * mirror_mult * solidify_mult
            data_property.PureTriangles += pure_tris * mirror_mult * solidify_mult
            data_property.Quads += quads * mirror_mult * solidify_mult
            data_property.Ngons += ngons * mirror_mult * solidify_mult
            data_property.Faces += faces * mirror_mult * solidify_mult

    def scene_polycount(self):
        self.set_data(bpy.context.scene.objects, bpy.context.scene.Polycount.ObjectMode.SceneData)

    # def layer_polycount(self):
    #     objs = []
    #     for layer in range(len(bpy.context.scene.Polycount.MainUI.layer_idx)):
    #         if bpy.context.scene.Polycount.MainUI.layer_idx[layer]:
    #             objs += [ob for ob in bpy.context.scene.objects if ob.layers[layer] and ob not in objs]
    #
    #     self.set_data(objs, bpy.context.scene.Polycount.ObjectMode.LayerData)

    def list_polycount(self, context):
        if len(context.scene.Polycount.MainUI.lists_List) == 0:
            return
        for l in context.scene.Polycount.MainUI.lists_List:
            objs = [o.object for o in l.list.obj_list
                    if o.object is not None and
                    o.object.name in context.scene.objects]
            self.set_data(objs, l.list_data)

    def collection_polycount(self, context):
        if len(context.scene.Polycount.MainUI.col_list) == 0:
            return
        for item in context.scene.Polycount.MainUI.col_list:
            objs = [o for o in item.collection.all_objects]
            self.set_data(objs, item.collection_data)

    def refresh(self, context, force=False):
        # start_time = time.time()
        scene = context.scene

        if not scene.Polycount.polycounted:
            scene.Polycount.polycounted = True

        # It is necessary to calculate_polycount the selection polycount if the percentage column is enabled
        if force or scene.Polycount.Draw.Selected or scene.Polycount.Draw.percentage:
            self.set_data(context.selected_objects, scene.Polycount.ObjectMode.SelectedData)

        if force or scene.Polycount.Draw.Scene:
            self.scene_polycount()

        # if force or scene.Polycount.Draw.Layer:
        #     self.layer_polycount()

        if force or scene.Polycount.Draw.List:
            self.list_polycount(context)

        if force or scene.Polycount.Draw.Collection:
            self.collection_polycount(context)

        redraw()
        # print("--- %s seconds ---" % (time.time() - start_time))
