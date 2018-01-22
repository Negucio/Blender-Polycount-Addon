import bpy

class DataPropertyGroup(bpy.types.PropertyGroup):
    """
    Stores the count of polygons of an object or a scene
    """
    Triangles   = bpy.props.IntProperty(name="Triangles",   default=0)
    PureTriangles   = bpy.props.IntProperty(name="PureTriangles",   default=0)
    Quads       = bpy.props.IntProperty(name="Quads",       default=0)
    Ngons       = bpy.props.IntProperty(name="Ngons",       default=0)
    Faces       = bpy.props.IntProperty(name="Faces",       default=0)

class ObjPolycountPropertyGroup(bpy.types.PropertyGroup):
    """
    Stores the data which Polycount needs for any object in the scene.
    Under "object.Polycount"
    """
    Updated     = bpy.props.BoolProperty(default = False)   # If False the polycount for the object will be recalculated
    MirrorAxis  = bpy.props.IntProperty(default = 0, min=0, max=3)
    HasSolidify = bpy.props.BoolProperty(default=False)
    Data        = bpy.props.PointerProperty(options={'HIDDEN'}, type=DataPropertyGroup)