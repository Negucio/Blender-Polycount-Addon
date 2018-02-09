from bpy.props import StringProperty, CollectionProperty, IntProperty, BoolProperty, PointerProperty
from bpy.types import PropertyGroup, Object

class ObjPropertyGroup(PropertyGroup):
    """
    Stores the properties of a UIList item
    """
    object = PointerProperty(name="object", type=Object)

class ObjListPropertyGroup(PropertyGroup):
    """
    Stores the properties of a UIList item
    """
    obj_list = CollectionProperty(type=ObjPropertyGroup)
    obj_list_index = IntProperty(name="Index", default=0, min=0)
