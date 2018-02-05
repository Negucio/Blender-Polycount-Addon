import bpy
from . graphics import DrawPropertyGroup
from . object import DataPropertyGroup, ObjPolycountPropertyGroup
from . scene import EditModePropertyGroup, ObjectModePropertyGroup, ScnTempPropertyGroup, ScnPolycountPropertyGroup
from . ui import ItemListPropertyGroup, ItemCollectionPropertyGroup, ObjListPropertyGroup

def register():
    """
    All Polycount blender classes are explicitly registered.
    Object and Scene Polycount variables are declared
    """
    bpy.utils.register_class(DataPropertyGroup)
    bpy.utils.register_class(DrawPropertyGroup)
    bpy.utils.register_class(ItemListPropertyGroup)
    bpy.utils.register_class(ItemCollectionPropertyGroup)
    bpy.utils.register_class(ObjPolycountPropertyGroup)
    bpy.utils.register_class(EditModePropertyGroup)
    bpy.utils.register_class(ObjectModePropertyGroup)
    bpy.utils.register_class(ObjListPropertyGroup)
    bpy.utils.register_class(ScnTempPropertyGroup)
    bpy.utils.register_class(ScnPolycountPropertyGroup)

    # Every object-related variable which Polycount uses will be under Object.Polycount
    bpy.types.Object.Polycount = bpy.props.PointerProperty(options={'HIDDEN'}, type=ObjPolycountPropertyGroup)

    # Every scene-related variable which Polycount uses will be under Scene.Polycount
    bpy.types.Scene.Polycount = bpy.props.PointerProperty(options={'HIDDEN'}, type=ScnPolycountPropertyGroup)

def unregister():
    del bpy.types.Object.Polycount
    del bpy.types.Scene.Polycount

    bpy.utils.unregister_class(DataPropertyGroup)
    bpy.utils.unregister_class(DrawPropertyGroup)
    bpy.utils.unregister_class(ItemListPropertyGroup)
    bpy.utils.unregister_class(ItemCollectionPropertyGroup)
    bpy.utils.unregister_class(ObjPolycountPropertyGroup)
    bpy.utils.unregister_class(EditModePropertyGroup)
    bpy.utils.unregister_class(ObjectModePropertyGroup)
    bpy.utils.unregister_class(ObjListPropertyGroup)
    bpy.utils.unregister_class(ScnTempPropertyGroup)
    bpy.utils.unregister_class(ScnPolycountPropertyGroup)

