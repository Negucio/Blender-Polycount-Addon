# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Polycount",
    "author": "Roberto Noya <negucio@gmail.com>, Oliver Villar <oliver@blendtuts.com>",
    "description": "Display triangle, quad, ngon and face count, in Object and Edit Mode",
    "version": (1, 0, 4),
    "blender": (2, 7, 9),
    "location": "View3D > Tools",
    "warning": "",
    "wiki_url": "",
    "category": "3D View"}


import bpy
from . import icons

from . import preferences

# Import blender classes to register
from . import data

# Import handler functions to register
from . import handler

# Import Panels, Operators and Lists which compose the interface
from . import ui

def register():
    icons.register()
    ui.register()
    data.register()
    preferences.register()
    handler.register()


def unregister():
    handler.unregister()
    preferences.register()
    data.unregister()
    ui.unregister()
    icons.unregister()

    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

