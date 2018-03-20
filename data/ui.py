import bpy
from . object import DataPropertyGroup
from bpy.props import PointerProperty, StringProperty, FloatVectorProperty, BoolProperty,\
    PointerProperty, CollectionProperty, IntProperty, BoolVectorProperty
from bpy.types import PropertyGroup, Group

from .. ui.list import ObjListPropertyGroup

class ItemCollectionPropertyGroup(PropertyGroup):
    """
    Stores the properties of a UIList item
    """
    # Settings
    list_name = StringProperty(default="")
    list_visible = BoolProperty(default=True)
    list_color = FloatVectorProperty(name="title_color", subtype='COLOR',
                                     default=(1.0, 0.8, 0.1), min=0.0, max=1.0, description="color picker")
    list_data = PointerProperty(options={'HIDDEN'}, type=DataPropertyGroup)
    # Collections
    list = PointerProperty(type=ObjListPropertyGroup)


class GrpPropertyGroup(PropertyGroup):
    """
    Stores the properties of a UIGroup item
    """
    group = PointerProperty(name="object", type=Group)
    visible = BoolProperty(name="visible", default=True)
    select = BoolProperty(name="select", default=False)

class MainUIPropertyGroup(PropertyGroup):
    """
    Stores the data for the uiLists and the custom layer operator
    """
    def layer_update_func(self, context):
        """
        Called on when a layer is selected/deselected
        """
        context.scene.Polycount.controller.refresh(context, force=True)

    # UILists
    lists_List_Index = IntProperty(name="Index", default=0, min=0)
    lists_List = CollectionProperty(type=ItemCollectionPropertyGroup)

    # Layer operator
    layer_idx = BoolVectorProperty(size=20, subtype='LAYER', name='', update=layer_update_func)

    # UIGroups
    grp_list = CollectionProperty(type=GrpPropertyGroup)
    grp_list_index = IntProperty(name="Index", default=0, min=0)




