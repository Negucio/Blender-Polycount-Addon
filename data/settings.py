import bpy

class DrawPropertyGroup(bpy.types.PropertyGroup):
    """
    Customizes how the data is displayed
    """
    props = [
        'ObjPolycount',
        'triangles',
        'percentage',
        'pure_tris',
        'quads',
        'ngons',
        'faces',
        'modifiers',
        'mirror',
        'subsurf',
        'solidify',
        'Selected',
        'Scene',
        'Layer',
        'List',
        'EditModePolycount',
        'selected_tris',
        'selected_verts',
        'selected_edges',
        'selected_faces',
        'width',
        'height',
        'hor_pos',
        'vert_pos',
        'digit_sep',
        'title_sep',
        'font_size',
        'title_color',
        'data_color',
        'sep_color',
        'perc_color',
        'sep_by_color',
        'thousands_color',
        'millions_color',
        'sep_by_char',
        'sep'
    ]

    # Scene data
    ObjPolycount = bpy.props.BoolProperty(default=True, description='Object Polycount')
    triangles = bpy.props.BoolProperty(default=True, description='Triangles*1 + Quads*2 + Ngons*(vertices - 2)')
    percentage = bpy.props.BoolProperty(default=False, description='Percentage of selected triangles in relation to the row')
    pure_tris = bpy.props.BoolProperty(default=False, description='3-sided polygons')
    quads = bpy.props.BoolProperty(default=False, description='4-sided polygons')
    ngons = bpy.props.BoolProperty(default=False, description='N-sided polygons')
    faces = bpy.props.BoolProperty(default=False, description='Triangles + Quads + Ngons')

    # Which modifiers will be took into consideration in the polycount
    modifiers   = bpy.props.BoolProperty(default=True, description="Modifiers affects Polycount")
    mirror      = bpy.props.BoolProperty(default=True, description="Mirror modifier affects Polycount")
    subsurf     = bpy.props.BoolProperty(default=True, description="Subsurf modifier affects Polycount")
    solidify    = bpy.props.BoolProperty(default=True, description="Solidify modifier affects Polycount")

    # Which data will be displayed
    Selected = bpy.props.BoolProperty(default=True, description="Selected Object(s) Polycount")
    Scene = bpy.props.BoolProperty(default=True, description="Scene Polycount")
    Layer = bpy.props.BoolProperty(default=False, description="Layer(s) Polycount")
    List = bpy.props.BoolProperty(default=False, description="List Polycount")

    # Edit Mode data
    EditModePolycount = bpy.props.BoolProperty(default=True, description='Edit Mode Polycount')
    selected_tris = bpy.props.BoolProperty(default=True, description="Triangles*1 + Quads*2 + Ngons*(vertices - 2)")
    selected_verts = bpy.props.BoolProperty(default=False, description="Selected Vertices Polycount")
    selected_edges = bpy.props.BoolProperty(default=False, description="Selected Edges Polycount")
    selected_faces = bpy.props.BoolProperty(default=False, description="Selected Faces Polycount")

    # Drawing settings
    width = bpy.props.FloatProperty(name="width", default=1.2, min=1, max=1.5)
    height = bpy.props.FloatProperty(name="height", default=1, min=1, max=1.5)

    hor_pos = bpy.props.FloatProperty(name="hor_pos", default=1, max=1, min=0)
    vert_pos = bpy.props.FloatProperty(name="vert_pos", default=0, max=1, min=0)
    digit_sep = bpy.props.FloatProperty(name="digit_sep", default=1, max=1.5, min=1)
    title_sep = bpy.props.FloatProperty(name="title_sep", default=0.5, max=1, min=0)
    font_size = bpy.props.IntProperty(name="FontSize", default=14, max=20, min=12)
    title_color = bpy.props.FloatVectorProperty(name="title_color", subtype='COLOR', default=(1.0, 0.8, 0.1), min=0.0, max=1.0, description="color picker")
    data_color = bpy.props.FloatVectorProperty(name="data_color", subtype='COLOR', default=(1.0, 1.0, 1.0), min=0.0, max=1.0, description="color picker")
    sep_color = bpy.props.FloatVectorProperty(name="sep_color", subtype='COLOR', default=(0.5, 1.0, 0.5), min=0.0, max=1.0, description="color picker")
    perc_color = bpy.props.FloatVectorProperty(name="perc_color", subtype='COLOR', default=(0.5, 0.75, 1.0), min=0.0, max=1.0, description="color picker")

    # Large numbers visualization settings
    sep_by_color = bpy.props.BoolProperty(default=True, description="Separate large numbers with colors")
    thousands_color = bpy.props.FloatVectorProperty(name="thousands_color", subtype='COLOR', default=(1.0, 0.75, 0.75), min=0.0, max=1.0, description="color picker")
    millions_color = bpy.props.FloatVectorProperty(name="millions_color", subtype='COLOR', default=(0.75, 0.75, 1.0), min=0.0, max=1.0, description="color picker")

    sep_by_char = bpy.props.BoolProperty(default=True, description="Separate large numbers with char")

    sep = bpy.props.EnumProperty(name='sep', default=' ',
        items=[
            (' ', 'Space', 'Space'),
            ('.', 'Dot', 'Dot'),
            (',', 'Comma', 'Comma')
        ])

    def reset(self):
        for prop in self.props:
            self.property_unset(prop)

    def clone(self, draw_property_group):
        for prop in self.props:
            if not hasattr(draw_property_group, prop): return

        for prop in self.props:
            source = getattr(draw_property_group, prop)
            setattr(self, prop, source)

