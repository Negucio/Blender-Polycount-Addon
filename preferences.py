import bpy
from . common_utils import get_addon_name
from . data.settings import DrawPropertyGroup

class PolycountPreferences(bpy.types.AddonPreferences):
    bl_idname = get_addon_name()

    persistent_settings = bpy.props.PointerProperty(options={'HIDDEN'}, type=DrawPropertyGroup)

    def draw(self, context):
        pass

def register():
    bpy.utils.register_class(PolycountPreferences)

def unregister():
    bpy.utils.unregister_class(PolycountPreferences)
