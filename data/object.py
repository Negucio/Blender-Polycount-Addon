import bpy
from bpy.props import IntProperty, BoolProperty, PointerProperty
from bpy.types import PropertyGroup


class DataPropertyGroup(PropertyGroup):
    """
    Stores the count of polygons of an object or a scene
    """
    Triangles = IntProperty(name="Triangles",   default=0)
    PureTriangles = IntProperty(name="PureTriangles",   default=0)
    Quads = IntProperty(name="Quads",       default=0)
    Ngons = IntProperty(name="Ngons",       default=0)
    Faces = IntProperty(name="Faces",       default=0)


class ObjPolycountPropertyGroup(PropertyGroup):
    """
    Stores the data which Polycount needs for any object in the scene.
    Under "object.Polycount"
    """
    Updated = BoolProperty(default=False)   # If False the polycount for the object will be recalculated
    MirrorAxis = IntProperty(default=0, min=0, max=3)
    HasSolidify = BoolProperty(default=False)
    Data = PointerProperty(options={'HIDDEN'}, type=DataPropertyGroup)
