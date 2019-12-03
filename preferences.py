import bpy
from . common_utils import get_addon_name
from . data.settings import DrawPropertyGroup
from bpy.props import PointerProperty
from bpy.utils import register_class, unregister_class


class PolycountPreferences(bpy.types.AddonPreferences):
    bl_idname = get_addon_name()

    persistent_settings: PointerProperty(options={'HIDDEN'}, type=DrawPropertyGroup)

    def draw(self, context):
        pass


def register():
    register_class(PolycountPreferences)


def unregister():
    unregister_class(PolycountPreferences)
