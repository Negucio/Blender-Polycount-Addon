import bpy

class DrawPropertyGroup(bpy.types.PropertyGroup):
    """
    Customizes how the data is displayed
    """
    # Scene data
    ObjPolycount = bpy.props.BoolProperty(default = True, description = 'Object Polycount')
    triangles = bpy.props.BoolProperty(default = True, description = 'Triangles*1 + Quads*2 + Ngons*(vertices - 2)')
    percentage = bpy.props.BoolProperty(default = True, description = 'Percentage of triangles in relation to the scene')
    quads     = bpy.props.BoolProperty(default = True, description = '4-sided polygons')
    ngons     = bpy.props.BoolProperty(default = True, description = 'N-sided polygons')
    faces     = bpy.props.BoolProperty(default = True, description = 'Triangles + Quads + Ngons')

    # Edit Mode data
    EditModePolycount = bpy.props.BoolProperty(default = True, description = 'Edit Mode Polycount')
    selected_tris = bpy.props.BoolProperty(default = True, description="Triangles*1 + Quads*2 + Ngons*(vertices - 2)")
    selected_verts = bpy.props.BoolProperty(default = True, description="Selected Vertices Polycount")
    selected_edges = bpy.props.BoolProperty(default = True, description="Selected Edges Polycount")
    selected_faces = bpy.props.BoolProperty(default = True, description="Selected Faces Polycount")

    # Drawing settings
    width = bpy.props.FloatProperty(name = "width", default = 1.2, min=1, max=1.5)
    height = bpy.props.FloatProperty(name = "height", default = 1, min=1, max=1.5)

    hor_pos = bpy.props.FloatProperty(name = "hor_pos", default = 1, max=1, min=0)
    vert_pos = bpy.props.FloatProperty(name = "vert_pos", default = 0, max=1, min=0)
    font_size = bpy.props.IntProperty(name = "FontSize", default = 14, max= 20, min=12)
    title_color = bpy.props.FloatVectorProperty(name="title_color", subtype='COLOR', default=(1.0, 0.8, 0.1), min=0.0, max=1.0, description="color picker")
    data_color = bpy.props.FloatVectorProperty(name="data_color", subtype='COLOR', default=(1.0, 1.0, 1.0), min=0.0, max=1.0, description="color picker")
    sep_color = bpy.props.FloatVectorProperty(name="sep_color", subtype='COLOR', default=(0.5, 1.0, 0.5), min=0.0, max=1.0, description="color picker")

    # Large numbers visualization settings
    sep_by_color = bpy.props.BoolProperty(default = True, description="Separate large numbers with colors")
    sep_by_dot = bpy.props.BoolProperty(default = True, description="Separate large numbers with dots")
    thousands_color = bpy.props.FloatVectorProperty(name="thousands_color", subtype='COLOR', default=(1.0, 0.75, 0.75), min=0.0, max=1.0, description="color picker")
    millions_color = bpy.props.FloatVectorProperty(name="millions_color", subtype='COLOR', default=(0.75, 0.75, 1.0), min=0.0, max=1.0, description="color picker")