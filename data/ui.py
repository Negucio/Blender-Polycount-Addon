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
    #Settings
    list_name = bpy.props.StringProperty(default="")
    list_visible = bpy.props.BoolProperty(default=True)
    list_color = bpy.props.FloatVectorProperty(name="title_color", subtype='COLOR', default=(1.0, 0.8, 0.1), min=0.0, max=1.0, description="color picker")
    list_data = bpy.props.PointerProperty(options={'HIDDEN'}, type=DataPropertyGroup)
    #Collections
    obj_list = bpy.props.CollectionProperty(type=ItemListPropertyGroup)
    obj_list_Index = bpy.props.IntProperty(name="Index", default=0, min=0)


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
    layer_idx = bpy.props.BoolVectorProperty(size=20, subtype='LAYER', name='', update=layer_update_func)
