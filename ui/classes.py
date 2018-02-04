from .. icons import preview_collections

class ObjectModeUI():
    def __init__(self):
        self.icons = preview_collections["main"]

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
        col.prop(context.scene.Polycount.Draw, "triangles", text="Total Tris", icon_value=self.icons["triangles"].icon_id)
        col.prop(context.scene.Polycount.Draw, "percentage", text="%", icon_value=self.icons["percentage"].icon_id)
        col.prop(context.scene.Polycount.Draw, "faces", text="Faces", icon_value=self.icons["faces"].icon_id)

        col = layout.column(align=True)
        col.prop(context.scene.Polycount.Draw, "pure_tris", text="Triangles", icon_value=self.icons["triangles"].icon_id)
        col.prop(context.scene.Polycount.Draw, "quads", text="Quads", icon_value=self.icons["quads"].icon_id)
        col.prop(context.scene.Polycount.Draw, "ngons", text="Ngons", icon_value=self.icons["ngons"].icon_id)
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
        row.prop(context.scene.Polycount.Draw, "Selected", text="Selection", icon='ZOOM_SELECTED')
        row = layout.row()
        row.prop(context.scene.Polycount.Draw, "Scene", text="Scene", icon='SCENE_DATA')
        row = layout.row()
        self.LayerConfig(context, row)
        row = layout.row()
        self.ListConfig(context, row)

    def LayerConfig(self, context, layout):
        col = layout.column(align=True)
        col.prop(context.scene.Polycount.Draw, "Layer", text="Layer", icon='LAYER_ACTIVE')
        if context.scene.Polycount.Draw.Layer:
            box = col.box()
            box.prop(context.scene.Polycount.MainUI, 'layer_idx')

    def ListConfig(self, context, layout):
        col = layout.column(align=True)
        col.prop(context.scene.Polycount.Draw, "List", text="List", icon='COLLAPSEMENU')
        if context.scene.Polycount.Draw.List:
            box = col.box()
            self.object_list_polycount(context, box)

    def object_list_polycount(self, context, layout):
        row = layout.row()
        row.template_list("DATA_UL_polycount_lists_list", "", context.scene.Polycount.MainUI, "lists_List", context.scene.Polycount.MainUI, "lists_List_Index", rows=1, maxrows=5)
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
            row.template_list("DATA_UL_polycount_obj_list", "", context.scene.Polycount.MainUI.lists_List[idx], "obj_list", context.scene.Polycount.MainUI.lists_List[idx], "obj_list_Index", rows=1, maxrows=5)
            col = box.column(align=True)
            row = col.row(align=True)
            row.operator("obj_list_add.btn", text="Assign")
            row.operator("obj_list_remove.btn", text="Remove")

            row = col.row(align=True)
            row.operator("obj_list_select.btn", text="Select All").select = True
            row.operator("obj_list_select.btn", text="Deselect All").select = False

            row = col.row(align=True)
            row.operator("obj_list_hide.btn", text="Show All").hide = False
            row.operator("obj_list_hide.btn", text="Hide All").hide = True

class EditModeUI():
    def __init__(self):
        self.icons = preview_collections["main"]

    def draw(self, context, layout):
        col = layout.column(align=True)
        col.prop(context.scene.Polycount.Draw, "EditModePolycount", text="Edit Mode Count", icon='EDIT')

        if context.scene.Polycount.Draw.EditModePolycount:
            box = col.box()
            self.EditModeContext(context, box)

    def EditModeContext(self, context, layout):
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(context.scene.Polycount.Draw, "selected_tris", text="Tris", icon_value=self.icons["selected_tris"].icon_id)
        row.prop(context.scene.Polycount.Draw, "selected_verts", text="Verts", icon='VERTEXSEL')
        row = col.row(align=True)
        row.prop(context.scene.Polycount.Draw, "selected_faces", text="Faces", icon='FACESEL')
        row.prop(context.scene.Polycount.Draw, "selected_edges", text="Edges", icon='EDGESEL')
