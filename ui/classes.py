
class ObjectModeUI():
    def draw(self, context, layout):
        col = layout.column(align=True)
        col.prop(context.scene.Polycount.Draw, "ObjPolycount", text="Obj Mode Count", icon='OBJECT_DATAMODE')
        if context.scene.Polycount.Draw.ObjPolycount:
            box = col.box()
            box.label("Count Display:")
            self.PolygonTypes(context, box)
            self.ModifiersConfig(context, box)
            box.label("Count Mode:")
            self.PolygonContext(context, box)

    def PolygonTypes(self, context, layout):
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(context.scene.Polycount.Draw, "triangles", text="Tris", icon='IMAGE_ALPHA')
        row.prop(context.scene.Polycount.Draw, "faces", text="Faces", icon='SNAP_FACE')
        row = col.row(align=True)
        row.prop(context.scene.Polycount.Draw, "quads", text="Quads", icon='MESH_PLANE')
        row.prop(context.scene.Polycount.Draw, "ngons", text="Ngons", icon='SOLO_OFF')

        # col = box.column()
        # col.alert = True
        # col.prop(context.scene.scene_polycount[0], "value", text="Budget", emboss=False)

    def ModifiersConfig(self, context, layout):
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(context.scene.Polycount.ObjectMode.modifiers, "on", text="Modifiers (Approximate)", icon="MODIFIER")
        row = col.row(align=True)
        row.enabled =context.scene.Polycount.ObjectMode.modifiers.on
        row.prop(context.scene.Polycount.ObjectMode.modifiers, "mirror", text="Mirror", icon='MOD_MIRROR')
        row.prop(context.scene.Polycount.ObjectMode.modifiers, "subsurf", text="Subsurf", icon='MOD_SUBSURF')
        row.prop(context.scene.Polycount.ObjectMode.modifiers, "solidify", text="Solidify", icon='MOD_SOLIDIFY')

    def PolygonContext(self, context, layout):
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(context.scene.Polycount.ObjectMode, "Selected", text="Selection", icon='ZOOM_SELECTED')
        row = layout.row()
        row.prop(context.scene.Polycount.ObjectMode, "Scene", text="Scene", icon='SCENE_DATA')
        row = layout.row()
        self.LayerConfig(context, row)
        row = layout.row()
        self.ListConfig(context, row)

    def LayerConfig(self, context, layout):
        col = layout.column(align=True)
        col.prop(context.scene.Polycount.ObjectMode, "Layer", text="Layer", icon='LAYER_ACTIVE')
        if context.scene.Polycount.ObjectMode.Layer:
            box = col.box()
            box.prop(context.scene.Polycount.MainUI, 'layer_idx')

    def ListConfig(self, context, layout):
        col = layout.column(align=True)
        col.prop(context.scene.Polycount.ObjectMode, "List", text="List", icon='COLLAPSEMENU')
        if context.scene.Polycount.ObjectMode.List:
            box = col.box()
            self.object_list_polycount(context, box)

    def object_list_polycount(self, context, layout):
        row = layout.row()
        row.template_list("DATA_UL_polycount_lists_list", "", context.scene.Polycount.MainUI, "lists_List", context.scene.Polycount.MainUI, "lists_List_Index", rows=2, maxrows=5)
        col = row.column(align=True)
        col.operator("lists_list_add.btn", icon='ZOOMIN', text="")
        col.operator("lists_list_remove.btn", icon='ZOOMOUT', text="")

        if len(context.scene.Polycount.MainUI.lists_List) > 0:
            idx = context.scene.Polycount.MainUI.lists_List_Index
            row = layout.row()
            box = row.box()
            row = box.row()

            split = row.split(percentage=0.6)
            split.label(text=context.scene.Polycount.MainUI.lists_List[idx].list_name + ' contents')
            split = split.split()
            split.prop(context.scene.Polycount.MainUI.lists_List[idx], "obj_list")

            row = box.row()
            row.template_list("DATA_UL_polycount_obj_list", "", context.scene.Polycount.MainUI.lists_List[idx], "obj_list", context.scene.Polycount.MainUI.lists_List[idx], "obj_list_Index")
            row_parent = box.row()
            col = row_parent.column()
            row = col.row(align=True)
            #row.operator("obj_list_add.btn", text="Assign")
            #row.operator("obj_list_remove.btn", text="Remove")
            row.operator("obj_list_add.btn", icon='ZOOMIN', text="")
            row.operator("obj_list_remove.btn", icon='ZOOMOUT', text="")
            row.operator("obj_list_clear.btn", icon='X', text="")
            col = row_parent.column()
            row = col.row(align=True)
            #row.operator("obj_list_select.btn", text="Select").select = True
            #row.operator("obj_list_select.btn", text="Deselect").select = False
            row.operator("obj_list_select.btn", icon='RADIOBUT_ON', text="").select = True
            row.operator("obj_list_select.btn", icon='RADIOBUT_OFF', text="").select = False
            col = row_parent.column()
            row = col.row(align=True)
            row.operator("obj_list_hide.btn", icon='RESTRICT_VIEW_OFF', text="").hide = False
            row.operator("obj_list_hide.btn", icon='RESTRICT_VIEW_ON', text="").hide = True

class EditModeUI():
    def draw(self, context, layout):
        col = layout.column(align=True)
        col.prop(context.scene.Polycount.Draw, "EditModePolycount", text="Edit Mode Count", icon='EDIT')

        if context.scene.Polycount.Draw.EditModePolycount:
            box = col.box()
            self.EditModeContext(context, box)

    def EditModeContext(self, context, layout):
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(context.scene.Polycount.Draw, "selected_tris", text="Tris", icon='MARKER_HLT')
        row.prop(context.scene.Polycount.Draw, "selected_verts", text="Verts", icon='VERTEXSEL')
        row = col.row(align=True)
        row.prop(context.scene.Polycount.Draw, "selected_faces", text="Faces", icon='FACESEL')
        row.prop(context.scene.Polycount.Draw, "selected_edges", text="Edges", icon='EDGESEL')
