import bpy
from os import path
from bpy.utils import previews

"""
Based on https://blender.stackexchange.com/questions/41565/loading-icons-into-custom-addon/58830#58830
Thanks batFINGER

"""

icon_dir = path.dirname(__file__)
preview_collections = {}


def register():
    pcoll = previews.new()

    icons = {
            "faces": "Faces.png",
            "ngons": "Ngons.png",
            "percentage": "Percentage.png",
            "quads": "Quads.png",
            "selected_tris": "Triangle_Selection_Edit_Mode.png",
            "triangles": "Triangles.png",
            "total_tris": "Total_Tris.png",
            }

    for key, f in icons.items():
        pcoll.load(key, path.join(icon_dir, f), 'IMAGE')

    preview_collections["main"] = pcoll


def unregister():
    for pcoll in preview_collections.values():
        previews.remove(pcoll)
    preview_collections.clear()
