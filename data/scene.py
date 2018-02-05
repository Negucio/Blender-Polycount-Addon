import bpy
from . import DataPropertyGroup
from . graphics import DrawPropertyGroup
from . ui import ObjListPropertyGroup

from .. polycount.controller import PolycountController

class ObjectModePropertyGroup(bpy.types.PropertyGroup):
    """
    Stores the global Polycount options
    """
    # The data itself
    SelectedData   = bpy.props.PointerProperty(options={'HIDDEN'}, type=DataPropertyGroup)
    SceneData      = bpy.props.PointerProperty(options={'HIDDEN'}, type=DataPropertyGroup)
    LayerData      = bpy.props.PointerProperty(options={'HIDDEN'}, type=DataPropertyGroup)

class EditModePropertyGroup(bpy.types.PropertyGroup):
    """
    Stores the data which can be displayed in Edit Mode
    """
    Triangles = bpy.props.IntProperty(name="Triangles", default=0)
    Verts = bpy.props.IntProperty(name="Verts", default=0)
    Edges = bpy.props.IntProperty(name="Edges", default=0)
    Faces = bpy.props.IntProperty(name="Faces", default=0)

class ScnTempPropertyGroup(bpy.types.PropertyGroup):
    """
    Stores the temp data which needs to be global to the whole scene
    """
    selected_verts = bpy.props.IntProperty(default=0)
    mesh_objs = bpy.props.IntProperty(default=0)

class ScnPolycountPropertyGroup(bpy.types.PropertyGroup):
    def display_polycount(self, context):
        bpy.ops.display_polycount.btn('EXEC_DEFAULT')

    controller = PolycountController()

    Display     = bpy.props.BoolProperty(default=False, description="Display Polycount", update=display_polycount)
    EditMode    = bpy.props.PointerProperty(options={'HIDDEN'}, type=EditModePropertyGroup)
    ObjectMode  = bpy.props.PointerProperty(options={'HIDDEN'}, type=ObjectModePropertyGroup)
    Draw        = bpy.props.PointerProperty(options={'HIDDEN'}, type=DrawPropertyGroup)
    MainUI      = bpy.props.PointerProperty(options={'HIDDEN'}, type=ObjListPropertyGroup)
    polycounted = bpy.props.BoolProperty(default=False)
    temp        = bpy.props.PointerProperty(options={'HIDDEN'}, type=ScnTempPropertyGroup)
