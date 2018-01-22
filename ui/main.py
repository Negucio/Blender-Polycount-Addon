import bpy
from .. graphics.draw import Draw
from .. polycount.controller import PolycountController

class VIEW3D_OT_polycount_display(bpy.types.Operator):
    bl_idname = "display_polycount.btn"
    bl_label = "Display"
    bl_description = "Display polycount"

    drawing = Draw()
    pc = PolycountController()

    def execute(self, context):
        if context.scene.Polycount.Display:
            self.pc.Refresh(context)
            self.drawing.DisplayPolycount(context)
        else:
            self.drawing.HidePolycount(context)

        if hasattr(context, "area") and context.area is not None: context.area.tag_redraw()

        return {'FINISHED'}


class VIEW3D_PT_polycount_main(bpy.types.Panel):
    bl_label = "Polycount"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Polycount"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        icon = 'OUTLINER_OB_LAMP' if context.scene.Polycount.Display else 'LAMP'
        row = layout.row()
        row.prop(context.scene.Polycount, "Display", text="Polycount", icon=icon)


class VIEW3D_PT_polycount_object(bpy.types.Panel):
    bl_label = "Object Polycount"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Polycount"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.prop(context.scene.Polycount.Draw, "ObjPolycount", text="Obj Mode Polycount", icon='OBJECT_DATAMODE')
        if context.scene.Polycount.Draw.ObjPolycount:
            box = col.box()
            self.PolygonTypes(context, box)
            self.PolygonContext(context, box)
            self.ModifiersConfig(context, box)
            self.ContextConfig(context, box)

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

    def PolygonContext(self, context, layout):
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(context.scene.Polycount.ObjectMode, "Selected", text="Selected", icon='ZOOM_SELECTED')
        row.prop(context.scene.Polycount.ObjectMode, "Scene", text="Scene", icon='SCENE_DATA')
        row = col.row(align=True)
        row.prop(context.scene.Polycount.ObjectMode, "Layer", text="Layer", icon='LAYER_ACTIVE')
        row.prop(context.scene.Polycount.ObjectMode, "List", text="List", icon='COLLAPSEMENU')

    def ModifiersConfig(self, context, layout):
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(context.scene.Polycount.ObjectMode.modifiers, "on", text="Modifiers (Approximate)", icon="MODIFIER")
        row = col.row(align=True)
        row.enabled =context.scene.Polycount.ObjectMode.modifiers.on
        row.prop(context.scene.Polycount.ObjectMode.modifiers, "mirror", text="Mirr", icon='MOD_MIRROR')
        row.prop(context.scene.Polycount.ObjectMode.modifiers, "subsurf", text="Subs", icon='MOD_SUBSURF')
        row.prop(context.scene.Polycount.ObjectMode.modifiers, "solidify", text="Sldf", icon='MOD_SOLIDIFY')

    def ContextConfig(self, context, layout):
        layout.prop(context.scene.Polycount.MainUI, 'layer_idx')
        self.object_list_polycount(context, layout)

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
            row.label(text=context.scene.Polycount.MainUI.lists_List[idx].list_name)
            row.prop(context.scene.Polycount.MainUI.lists_List[idx], "obj_list")
            row = box.row()
            row.template_list("DATA_UL_polycount_obj_list", "", context.scene.Polycount.MainUI.lists_List[idx], "obj_list", context.scene.Polycount.MainUI.lists_List[idx], "obj_list_Index")
            row = box.row(align=False)
            row.operator("obj_list_add.btn", icon='ZOOMIN', text="")
            row.operator("obj_list_remove.btn", icon='ZOOMOUT', text="")


class VIEW3D_PT_polycount_edit_mode(bpy.types.Panel):
    bl_label = "Edit Mode Polycount"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Polycount"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.prop(context.scene.Polycount.Draw, "EditModePolycount", text="Edit Mode Polycount", icon='EDIT')

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