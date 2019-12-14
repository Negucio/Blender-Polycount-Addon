import bpy
from . settings import DrawPropertyGroup
from . object import DataPropertyGroup, ObjPolycountPropertyGroup
from . scene import EditModePropertyGroup, ObjectModePropertyGroup, ScnTempPropertyGroup, ScnPolycountPropertyGroup
from . ui import ItemCollectionPropertyGroup, MainUIPropertyGroup, WindowDisplayPropertyGroup, CollectionPropertyGroup
from bpy.utils import register_class, unregister_class
from bpy.props import PointerProperty
from bpy.types import Object, Scene


def register():
    """
    All Polycount blender classes are explicitly registered.
    Object and Scene Polycount variables are declared
    """
    register_class(WindowDisplayPropertyGroup)
    register_class(DataPropertyGroup)
    register_class(DrawPropertyGroup)
    register_class(ItemCollectionPropertyGroup)
    register_class(ObjPolycountPropertyGroup)
    register_class(EditModePropertyGroup)
    register_class(ObjectModePropertyGroup)
    register_class(CollectionPropertyGroup)
    register_class(MainUIPropertyGroup)
    register_class(ScnTempPropertyGroup)
    register_class(ScnPolycountPropertyGroup)

    # Every object-related variable which Polycount uses will be under Object.Polycount
    Object.Polycount = PointerProperty(options={'HIDDEN'}, type=ObjPolycountPropertyGroup)

    # Every scene-related variable which Polycount uses will be under Scene.Polycount
    Scene.Polycount = PointerProperty(options={'HIDDEN'}, type=ScnPolycountPropertyGroup)


def unregister():
    del bpy.types.Object.Polycount
    del bpy.types.Scene.Polycount

    unregister_class(WindowDisplayPropertyGroup)
    unregister_class(DataPropertyGroup)
    unregister_class(DrawPropertyGroup)
    unregister_class(ItemCollectionPropertyGroup)
    unregister_class(ObjPolycountPropertyGroup)
    unregister_class(EditModePropertyGroup)
    unregister_class(ObjectModePropertyGroup)
    unregister_class(MainUIPropertyGroup)
    unregister_class(CollectionPropertyGroup)
    unregister_class(ScnTempPropertyGroup)
    unregister_class(ScnPolycountPropertyGroup)

