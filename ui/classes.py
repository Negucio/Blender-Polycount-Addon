
from .. icons import preview_collections


class ObjectModeUI:
    def __init__(self):
        self.icons = preview_collections["main"]

    def draw(self, context, layout):
        col = layout.column(align=True)
        draw_pc = context.scene.Polycount.Draw
        col.prop(draw_pc, "ObjPolycount", text="Obj Mode Count", icon='OBJECT_DATAMODE')
        if draw_pc.ObjPolycount:
            box = col.box()
            box.label("Count Display:")
            self.polygon_types(context, box)
            self.modifiers_config(context, box)
            box.label("Count Mode:")
            self.polygon_context(context, box)

    def polygon_types(self, context, layout):
        col = layout.column(align=True)
        draw_pc = context.scene.Polycount.Draw
        col.prop(draw_pc, "triangles", text="Total Tris", icon_value=self.icons["total_tris"].icon_id)
        col.prop(draw_pc, "faces", text="Faces", icon_value=self.icons["faces"].icon_id)

        col = layout.column(align=True)
        col.prop(draw_pc, "pure_tris", text="Triangles", icon_value=self.icons["triangles"].icon_id)
        col.prop(draw_pc, "quads", text="Quads", icon_value=self.icons["quads"].icon_id)
        col.prop(draw_pc, "ngons", text="Ngons", icon_value=self.icons["ngons"].icon_id)
        # col = box.column()
        # col.alert = True
        # col.prop(context.scene.scene_polycount[0], "value", text="Budget", emboss=False)

    def modifiers_config(self, context, layout):
        col = layout.column(align=True)
        draw_pc = context.scene.Polycount.Draw
        row = col.row(align=True)
        row.prop(draw_pc, "modifiers", text="Modifiers (Approximate)", icon="MODIFIER")
        row = col.row(align=True)
        row.enabled = draw_pc.modifiers
        row.prop(draw_pc, "mirror", text="Mirror", icon='MOD_MIRROR')
        row.prop(draw_pc, "subsurf", text="Subsurf", icon='MOD_SUBSURF')
        row.prop(draw_pc, "solidify", text="Solidify", icon='MOD_SOLIDIFY')

    def polygon_context(self, context, layout):
        col = layout.column(align=True)
        draw_pc = context.scene.Polycount.Draw
        row = col.row(align=True)
        row.prop(draw_pc, "Selected", text="Selection", icon='RESTRICT_SELECT_OFF')
        row.prop(draw_pc, "percentage", text="", icon_value=self.icons["percentage"].icon_id)
        row = layout.row()
        row.prop(draw_pc, "Scene", text="Scene", icon='SCENE_DATA')
        row = layout.row()
        self.layer_config(context, row)
        row = layout.row()
        self.list_config(context, row)

    def layer_config(self, context, layout):
        col = layout.column(align=True)
        draw_pc = context.scene.Polycount.Draw
        ui = context.scene.Polycount.MainUI
        col.prop(draw_pc, "Layer", text="Layer", icon='RENDERLAYERS')  # icon='LAYER_ACTIVE')
        if draw_pc.Layer:
            box = col.box()
            box.prop(ui, 'layer_idx')

    def list_config(self, context, layout):
        col = layout.column(align=True)
        draw_pc = context.scene.Polycount.Draw
        col.prop(draw_pc, "List", text="List", icon='COLLAPSEMENU')
        if draw_pc.List:
            box = col.box()
            self.object_list_polycount(context, box)

    def object_list_polycount(self, context, layout):
        row = layout.row()
        ui = context.scene.Polycount.MainUI
        row.template_list("DATA_UL_polycount_lists_list", "",
                          ui, "lists_List",
                          ui, "lists_List_Index",
                          rows=1, maxrows=5)
        col = row.column(align=True)
        col.operator("lists_list_add.btn", icon='ZOOMIN', text="")
        col.operator("lists_list_remove.btn", icon='ZOOMOUT', text="")

        if len(ui.lists_List) > 0:
            idx = ui.lists_List_Index
            row = layout.row()
            box = row.box()
            row = box.row()

            split = row.split(percentage=0.6)
            split.label(text=ui.lists_List[idx].list_name + ' contents')
            split = split.split()
            split.prop(ui.lists_List[idx], "obj_list")

            row = box.row()
            row.template_list("DATA_UL_polycount_obj_list", "",
                              ui.lists_List[idx], "obj_list",
                              ui.lists_List[idx], "obj_list_Index",
                              rows=1, maxrows=5)
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


class EditModeUI:
    def __init__(self):
        self.icons = preview_collections["main"]

    def draw(self, context, layout):
        col = layout.column(align=True)
        draw_pc = context.scene.Polycount.Draw
        col.prop(draw_pc, "EditModePolycount", text="Edit Mode Count", icon='EDIT')

        if draw_pc.EditModePolycount:
            box = col.box()
            self.edit_mode_context(context, box)

    def edit_mode_context(self, context, layout):
        col = layout.column(align=True)
        draw_pc = context.scene.Polycount.Draw
        row = col.row(align=True)
        row.prop(draw_pc, "selected_tris", text="Tris", icon_value=self.icons["selected_tris"].icon_id)
        row.prop(draw_pc, "selected_verts", text="Verts", icon='VERTEXSEL')
        row = col.row(align=True)
        row.prop(draw_pc, "selected_faces", text="Faces", icon='FACESEL')
        row.prop(draw_pc, "selected_edges", text="Edges", icon='EDGESEL')
