import bpy
from . object import DataPropertyGroup
from .. polycount.controller import PolycountController

class ItemListPropertyGroup(bpy.types.PropertyGroup):
    """
    Stores the properties of a UIList item
    """
    object = bpy.props.PointerProperty(name="object", type=bpy.types.Object)

class ItemCollectionPropertyGroup(bpy.types.PropertyGroup):
    """
    Stores the properties of a UIList item
    """
    list_name = bpy.props.StringProperty(default="")
    obj_list = bpy.props.CollectionProperty(type=ItemListPropertyGroup)
    obj_list_Index = bpy.props.IntProperty(name="Index", default=0, min=0)
    list_data = bpy.props.PointerProperty(options={'HIDDEN'}, type=DataPropertyGroup)


class ObjListPropertyGroup(bpy.types.PropertyGroup):
    """
    Stores the data for the uiLists and the custom layer operator
    """
    pc = PolycountController()

    def layer_update_func(self, context):
        """
        Called on when a layer is selected/deselected
        """
        self.pc.Refresh(context, force=True)

    # UILists
    lists_List_Index = bpy.props.IntProperty(name="Index", default=0, min=0)
    lists_List = bpy.props.CollectionProperty(type=ItemCollectionPropertyGroup)

    # Layer operator
    layer_idx = bpy.props.BoolVectorProperty(size=20, subtype='LAYER', name='Select layer', update=layer_update_func)
