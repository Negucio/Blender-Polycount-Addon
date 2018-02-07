import bpy
from . import DataPropertyGroup
from . settings import DrawPropertyGroup
from . ui import ObjListPropertyGroup

from .. polycount.controller import PolycountController

from bpy.types import PropertyGroup
from bpy.props import PointerProperty, IntProperty, BoolProperty


class ObjectModePropertyGroup(PropertyGroup):
    """
    Stores the global Polycount options
    """
    # The data itself
    SelectedData = PointerProperty(options={'HIDDEN'}, type=DataPropertyGroup)
    SceneData = PointerProperty(options={'HIDDEN'}, type=DataPropertyGroup)
    LayerData = PointerProperty(options={'HIDDEN'}, type=DataPropertyGroup)


class EditModePropertyGroup(PropertyGroup):
    """
    Stores the data which can be displayed in Edit Mode
    """
    Triangles = IntProperty(name="Triangles", default=0)
    Verts = IntProperty(name="Verts", default=0)
    Edges = IntProperty(name="Edges", default=0)
    Faces = IntProperty(name="Faces", default=0)


class ScnTempPropertyGroup(PropertyGroup):
    """
    Stores the temp data which needs to be global to the whole scene
    """
    selected_verts = IntProperty(default=0)
    mesh_objs = IntProperty(default=0)


class ScnPolycountPropertyGroup(PropertyGroup):
    def display_polycount(self, context):
        bpy.ops.display_polycount.btn('EXEC_DEFAULT')

    controller = PolycountController()

    Display = BoolProperty(default=False, description="Display Polycount", update=display_polycount)
    EditMode = PointerProperty(options={'HIDDEN'}, type=EditModePropertyGroup)
    ObjectMode = PointerProperty(options={'HIDDEN'}, type=ObjectModePropertyGroup)
    Draw = PointerProperty(options={'HIDDEN'}, type=DrawPropertyGroup)
    MainUI = PointerProperty(options={'HIDDEN'}, type=ObjListPropertyGroup)
    polycounted = BoolProperty(default=False)
    temp = PointerProperty(options={'HIDDEN'}, type=ScnTempPropertyGroup)
