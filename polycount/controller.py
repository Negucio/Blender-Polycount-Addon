import bpy, bmesh
from . utils import get_mirror_axis, calculate_subsurf, has_solidify, get_levels_subsurf
from .. data.utils import reset_data_property

class PolycountController():
    def PolycountObjectMode(self, object, polygons, bmesh=False):
        if object == None or not hasattr(object, 'type') or object.type != 'MESH': return None
        if not hasattr(object, 'Polycount'): return None
        pure_tris = 0
        face_tris = 0
        quads = 0
        ngons = 0
        if bmesh: polygons.ensure_lookup_table()
        for poly in polygons:
            v = len(poly.verts) if bmesh else len(poly.vertices)

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

        object.Polycount.Data.PureTriangles = pure_tris
        object.Polycount.Data.Triangles = tris
        object.Polycount.Data.Quads = quads
        object.Polycount.Data.Ngons = ngons
        object.Polycount.Data.Faces = faces
        object.Polycount.MirrorAxis = get_mirror_axis(object)
        object.Polycount.HasSolidify = has_solidify(object)
        object.Polycount.Updated = True

    def PolycountEditMode(self, object, bm):
        if object == None or not hasattr(object, 'type') or object.type != 'MESH': return None
        if not hasattr(object, 'Polycount'): return None

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


    def CalculatePolycount(self, obj):
        if (bpy.context.mode == 'EDIT_MESH' and bpy.context.active_object == obj):
            bm = bmesh.from_edit_mesh(obj.data)
            self.PolycountObjectMode(obj, bm.faces, bmesh=True)
            self.PolycountEditMode(obj, bm)
        else:
            self.PolycountObjectMode(obj, obj.data.polygons, bmesh=False)


    def SetPolycount(self, objects, dataProperty):
        if (objects == None): return
        reset_data_property(dataProperty)
        for obj in objects:
            if obj.type != 'MESH': continue
            if not obj.Polycount.Updated: self.CalculatePolycount(obj)

            tris = obj.Polycount.Data.Triangles
            quads = obj.Polycount.Data.Quads
            ngons = obj.Polycount.Data.Ngons
            faces = obj.Polycount.Data.Faces

            mirrorMult = 1
            solidifyMult = 1

            mods = bpy.context.scene.Polycount.ObjectMode.modifiers
            levels = get_levels_subsurf(obj)
            if mods.on:
                if mods.subsurf and levels > 0:
                    quads = calculate_subsurf(obj, obj.Polycount.Data.PureTriangles, obj.Polycount.Data.Quads, obj.Polycount.Data.Ngons)
                    tris = quads * 2
                    faces = quads
                    ngons = 0

                # TODO: The result is approximate. Merge and clipping should be taking into account
                if mods.mirror: mirrorMult = 2 ** obj.Polycount.MirrorAxis

                # TODO: The result is approximate. Should be calculated counting how many edges are border and adding to the account
                if mods.solidify and obj.Polycount.HasSolidify: solidifyMult = 2

            dataProperty.Triangles  += tris  * mirrorMult * solidifyMult
            dataProperty.Quads      += quads * mirrorMult * solidifyMult
            dataProperty.Ngons      += ngons * mirrorMult * solidifyMult
            dataProperty.Faces      += faces * mirrorMult * solidifyMult


    def ScenePolycount(self):
        self.SetPolycount(bpy.context.scene.objects, bpy.context.scene.Polycount.ObjectMode.SceneData)

    def LayerPolycount(self):
        objs = []
        for layer in range(len(bpy.context.scene.Polycount.MainUI.layer_idx)):
            if bpy.context.scene.Polycount.MainUI.layer_idx[layer]:
                objs += [ob for ob in bpy.context.scene.objects if ob.layers[layer] and ob not in objs]
                self.SetPolycount(objs, bpy.context.scene.Polycount.ObjectMode.LayerData)

    def ListPolycount(self, context):
        if len(context.scene.Polycount.MainUI.lists_List) == 0: return
        for l in context.scene.Polycount.MainUI.lists_List:
            objs = [o.object for o in l.obj_list]
            self.SetPolycount(objs, l.list_data)


    def Refresh(self, context, force=False):
        # start_time = time.time()
        scene = context.scene
        if force or scene.Polycount.ObjectMode.Selected:
            self.SetPolycount(context.selected_objects, scene.Polycount.ObjectMode.SelectedData)

        if force or scene.Polycount.ObjectMode.Scene:
            self.ScenePolycount()

        if force or scene.Polycount.ObjectMode.Layer:
            self.LayerPolycount()

        if force or scene.Polycount.ObjectMode.List:
            self.ListPolycount(context)

        if hasattr(context, "area") and context.area != None: context.area.tag_redraw()
        # print("--- %s seconds ---" % (time.time() - start_time))


