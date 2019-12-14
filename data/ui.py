import bpy
from . object import DataPropertyGroup
from bpy.props import PointerProperty, StringProperty, FloatVectorProperty, BoolProperty,\
    PointerProperty, CollectionProperty, IntProperty, BoolVectorProperty
from bpy.types import PropertyGroup, Collection

from .. ui.list import ObjListPropertyGroup

class ItemCollectionPropertyGroup(PropertyGroup):
    """
    Stores the properties of a UIList item
    """
    # Settings
    list_name: StringProperty(default="")
    list_visible: BoolProperty(default=True)
    list_color: FloatVectorProperty(name="title_color", subtype='COLOR',
                                     default=(1.0, 0.8, 0.1), min=0.0, max=1.0, description="color picker")
    list_data: PointerProperty(options={'HIDDEN'}, type=DataPropertyGroup)
    # Collections
    list: PointerProperty(type=ObjListPropertyGroup)


class CollectionPropertyGroup(PropertyGroup):
    """
    Stores the properties of a Collection item
    """
    # def hide_update_func(self, context):
    #     for obj in self.group.objects:
    #         obj.hide_viewport = self.group_hide

    collection: PointerProperty(name="object", type=Collection)
    collection_visible: BoolProperty(name="visible", default=True)
    collection_hide: BoolProperty(name="hide_viewport", default=False) #, update=hide_update_func)
    collection_data: PointerProperty(options={'HIDDEN'}, type=DataPropertyGroup)
    collection_color: FloatVectorProperty(name="title_color", subtype='COLOR',
                                     default=(1.0, 0.8, 0.1), min=0.0, max=1.0, description="color picker")

class WindowDisplayPropertyGroup(bpy.types.PropertyGroup):
    display: bpy.props.BoolProperty(default=True, description="Display Polycount in this 3DView")

class MainUIPropertyGroup(PropertyGroup):
    """
    Stores the data for the uiLists and the custom layer operator
    """
    # def layer_update_func(self, context):
    #     """
    #     Called on when a layer is selected/deselected
    #     """
    #     context.scene.Polycount.controller.refresh(context, force=True)

    def select_update_func(self, context):
        for obj in bpy.data.objects:
            obj.select_set(False)
        # grp = self.grp_list[self.grp_list_index].group
        # for obj in grp.objects:
        #     obj.select = True

    # UILists
    lists_List_Index: IntProperty(name="Index", default=0, min=0)
    lists_List: CollectionProperty(type=ItemCollectionPropertyGroup)

    # Layer operator
    #layer_idx: BoolVectorProperty(size=20, subtype='LAYER', name='', update=layer_update_func)

    # UIGroups
    col_list: CollectionProperty(type=CollectionPropertyGroup)
    col_list_index: IntProperty(name="Index", default=0, min=0, update=select_update_func)

    window_display: CollectionProperty(type=WindowDisplayPropertyGroup)
    window_display_temp: BoolProperty(default=False, description="Display Polycount in this 3DView")








