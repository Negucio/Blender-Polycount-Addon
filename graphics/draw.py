import bpy, bgl, blf, collections

class Draw():
    """
    Composes and displays the Polycount information
    """
    def __init__(self):
        self.PostPixelHandle = None # Stores the draw handler
        self.font_id = 0

    def handle_add(self, context, DrawFunction):
        """
        Sets the draw handler which displays the polycount information in the 3DView
        :param context:
        :param DrawFunction: The function which will compose and display the information
        """
        if self.PostPixelHandle is None:
            self.PostPixelHandle = bpy.types.SpaceView3D.draw_handler_add(DrawFunction, (context,), 'WINDOW', 'POST_PIXEL')
            if hasattr(context, "area") and context.area is not None: context.area.tag_redraw()

    def handle_remove(self, context):
        """
        Removes the draw handler
        :param context:
        """
        if self.PostPixelHandle is not None:
            bpy.types.SpaceView3D.draw_handler_remove(self.PostPixelHandle, 'WINDOW')
            if hasattr(context, "area") and context.area is not None: context.area.tag_redraw()
        self.PostPixelHandle = None

    def DrawCell(self, text, position, color, width):
        """
        Draws a cell of the table
        :param text: Text in the cell
        :param position: 2D position of the cell
        """
        if not text.isdigit() or color is None:
            blf.position(0, position[0], position[1], 0)
            bgl.glColor3f(*color)
            blf.draw(self.font_id, text)
            return

        if not hasattr(bpy.context, "scene"): return
        scn = bpy.context.scene
        self.format_digits_2(text, position, scn, width)

        bgl.glColor3f(*color)

    def draw_char(self, position, char, char_sample_width):
        blf.position(0, position[0], position[1], 0)
        text_width, text_height = blf.dimensions(self.font_id, char_sample_width)
        blf.draw(self.font_id, char)
        return position[0] - text_width

    def format_digits_2(self, text, position, scene, width):
        sep = scene.Polycount.Draw.sep_by_char
        color = scene.Polycount.Draw.sep_by_color
        sep_char = scene.Polycount.Draw.sep
        draw_pc = scene.Polycount.Draw

        pos = position[0]+width - (draw_pc.font_size * draw_pc.width * draw_pc.digit_sep * 1.75)

        count = 0
        for char in reversed(text):
            pos = self.draw_char((pos, position[1]), char, char)
            count += 1

            if count % 3 == 0 and count < len(text):
                if sep:
                    pos = self.draw_char((pos, position[1]), ' ' + sep_char, '.')
                if color:
                    if count == 3: bgl.glColor3f(*scene.Polycount.Draw.thousands_color)
                    elif count == 6: bgl.glColor3f(*scene.Polycount.Draw.millions_color)

    def get_cols(self, scn):
        first = 0
        second = 0
        if scn.Polycount.Draw.triangles: first += 1
        if scn.Polycount.Draw.faces: first += 1

        second += first

        if scn.Polycount.Draw.percentage: second += 1

        return first, second

    def DrawLine(self, v1, v2):
        """
        Draws a line between the 2D position v1 and the 2D position v2
        :param v1: First 2D point of the line
        :param v2: Second 2D point of the line
        """
        if v1 and v2:
            bgl.glBegin(bgl.GL_LINES)
            bgl.glVertex2f(*v1)
            bgl.glVertex2f(*v2)
            bgl.glEnd()
        return

    def DrawTable(self, pos, cellSize, content):
        """
        Composes the global Polycount table in the 3DView
        :param pos: Tuple (x,y) of 2D coordinates in pixels inside the 3DView which
                    will set the top-left corner of the table
        :param cellSize:
        :param content: Ordered dictionary with the data of the Object/Global mode
        """
        scn = bpy.context.scene
        row = 0

        # "pos" coordinates set the position of the top-left corner of the table
        initX = pos[0]
        initY = pos[1]

        y = initY

        for key in content:
            if key == 'OBJECT': bgl.glColor3f(*scn.Polycount.Draw.sep_color)
            else: bgl.glColor3f(*(scn.Polycount.Draw.title_color if content[key][1] is None else content[key][1]))
            blf.position(0, initX, y, 0)
            title = key
            max = int(scn.Polycount.Draw.width*10)
            if len(key) > max:
                title = key[0:max-3] + "..."
            blf.draw(self.font_id, title)

            color = scn.Polycount.Draw.title_color if row == 0 else scn.Polycount.Draw.data_color

            bgl.glColor3f(*color)

            col = 1
            if scn.Polycount.Draw.triangles:
                text = 'Total Tris'
                if row > 0: text = str(content[key][0].Triangles)
                self.DrawCell(text, (initX + (cellSize[0] * col), y), color, cellSize[0])
                col = col + 1
            if scn.Polycount.Draw.faces:
                text = 'Faces'
                if row > 0: text = str(content[key][0].Faces)
                self.DrawCell(text, (initX + (cellSize[0] * col), y), color, cellSize[0])
                col = col + 1
            if scn.Polycount.Draw.percentage:
                text = 'Percentage'
                if row > 0:
                    sel_tris = bpy.context.scene.Polycount.ObjectMode.SelectedData.Triangles
                    col_tris = content[key][0].Triangles
                    text = "{0:.2f}%".format(0.0 if col_tris == 0 else (sel_tris/col_tris)*100)
                    if key == 'Selection': text = ""
                self.DrawCell(text, (initX + (cellSize[0] * col), y), color, cellSize[0])
                col = col + 1

            if scn.Polycount.Draw.pure_tris:
                text = 'Triangles'
                if row > 0: text = str(content[key][0].PureTriangles)
                self.DrawCell(text, (initX + (cellSize[0] * col), y), color, cellSize[0])
                col = col + 1
            if scn.Polycount.Draw.quads:
                text = 'Quads'
                if row > 0: text = str(content[key][0].Quads)
                self.DrawCell(text, (initX + (cellSize[0] * col), y), color, cellSize[0])
                col = col + 1
            if scn.Polycount.Draw.ngons:
                text = 'Ngons'
                if row > 0: text = str(content[key][0].Ngons)
                self.DrawCell(text, (initX + (cellSize[0] * col), y), color, cellSize[0])
            row = row + 2

            y = initY - (cellSize[1] * row)

        cols = self.get_cols(scn)

        # Vertical line to separate TotalTris/Faces and Percentage/Tris/Quads/Ngons
        if (scn.Polycount.Draw.triangles or scn.Polycount.Draw.faces) and scn.Polycount.Draw.percentage:
            sepX = initX + (cellSize[0] * cols[0]) + (scn.Polycount.Draw.font_size * (5*scn.Polycount.Draw.width))
            col = scn.Polycount.Draw.sep_color
            bgl.glColor4f(*(col[0], col[1], col[2], 0.25))
            # It's necessary calling this bgl function in order to enable the alpha drawing
            bgl.glEnable(bgl.GL_BLEND)
            self.DrawLine((sepX, initY), (sepX, y + (cellSize[1]*2)))
            bgl.glEnd()
            bgl.glDisable(bgl.GL_BLEND)

        # Vertical line to separate Percentage and Tris/Quads/Ngons
        if (scn.Polycount.Draw.triangles or scn.Polycount.Draw.faces or scn.Polycount.Draw.percentage) and (scn.Polycount.Draw.pure_tris or scn.Polycount.Draw.quads or scn.Polycount.Draw.ngons):
            sepX = initX + (cellSize[0] * cols[1]) + (scn.Polycount.Draw.font_size * (5*scn.Polycount.Draw.width))
            bgl.glColor3f(*scn.Polycount.Draw.sep_color)
            self.DrawLine((sepX, initY), (sepX, y + (cellSize[1]*2)))

        return initX, y


    def DrawEditModeTable(self, pos, cellSize, content):
        scn = bpy.context.scene

        initX = pos[0]
        initY = pos[1]

        y = initY

        row = 0

        for key in content:
            if key == 'EDIT': bgl.glColor3f(*scn.Polycount.Draw.sep_color)
            else: bgl.glColor3f(*scn.Polycount.Draw.title_color)
            blf.position(0, initX, y, 0)
            blf.draw(self.font_id, key)

            color = scn.Polycount.Draw.title_color if row == 0 else scn.Polycount.Draw.data_color

            bgl.glColor3f(*color)

            col = 1
            if scn.Polycount.Draw.selected_tris:
                text = 'Triangles'
                if row > 0: text = str(content[key].Triangles)
                self.DrawCell(text, (initX + (cellSize[0] * col), y), color, cellSize[0])
                col = col + 1
            if scn.Polycount.Draw.selected_verts:
                text = 'Verts'
                if row > 0: text = str(content[key].Verts)
                self.DrawCell(text, (initX + (cellSize[0] * col), y), color, cellSize[0])
                col = col + 1
            if scn.Polycount.Draw.selected_edges:
                text = 'Edges'
                if row > 0: text = str(content[key].Edges)
                self.DrawCell(text, (initX + (cellSize[0] * col), y), color, cellSize[0])
                col = col + 1
            if scn.Polycount.Draw.selected_faces:
                text = 'Faces'
                if row > 0: text = str(content[key].Faces)
                self.DrawCell(text, (initX + (cellSize[0] * col), y), color, cellSize[0])
            row = row + 2

            y = initY - (cellSize[1] * row)

    def get_columns(self, scene):
        # Initializes var to 1 because of the title column
        obj_mode = 1
        if scene.Polycount.Draw.ObjPolycount:
            if scene.Polycount.Draw.triangles:  obj_mode += 1
            if scene.Polycount.Draw.percentage:  obj_mode += 1
            if scene.Polycount.Draw.faces:  obj_mode += 1
            if scene.Polycount.Draw.pure_tris:  obj_mode += 1
            if scene.Polycount.Draw.quads:  obj_mode += 1
            if scene.Polycount.Draw.ngons:  obj_mode += 1

        # Initializes var to 1 because of the title column
        edit_mode = 1
        if scene.Polycount.Draw.EditModePolycount and bpy.context.mode == 'EDIT_MESH':
            if scene.Polycount.Draw.selected_tris:  edit_mode += 1
            if scene.Polycount.Draw.selected_verts:  edit_mode += 1
            if scene.Polycount.Draw.selected_edges:  edit_mode += 1
            if scene.Polycount.Draw.selected_faces:  edit_mode += 1

        return max(obj_mode, edit_mode)

    def get_rows(self, scene):
        # Initializes var to 1 because of the title column
        obj_mode = 1
        if scene.Polycount.Draw.ObjPolycount:
            if scene.Polycount.Draw.Selected:  obj_mode += 1
            if scene.Polycount.Draw.Scene:   obj_mode += 1
            if scene.Polycount.Draw.Layer:   obj_mode += 1
            if scene.Polycount.Draw.List:
                obj_mode += len([l.list_visible for l in bpy.context.scene.Polycount.MainUI.lists_List])

        # Initializes var to 1 because of the title column
        edit_mode = 1
        if scene.Polycount.Draw.EditModePolycount and bpy.context.mode == 'EDIT_MESH': edit_mode += 1

        return obj_mode + edit_mode


    def get_init_pos(self, max, size, perc=1, low_margin=20, high_margin=20, reverse=False):
        # TODO: Check vertical drawing: Table goes outside of the view3d in perc=0 and more than 4 rows
        pos = (max - size) * perc
        if pos < low_margin:
            pos = low_margin
        elif pos > max-high_margin:
            pos = max-high_margin
        return pos if not reverse else max-pos


    def draw_obj_edit_sep_line(self, pos, cellSize, color, cols):
        line_y = pos[1] + cellSize[1]
        bgl.glColor3f(*color)
        line_cols = cols - 0.5
        self.DrawLine((pos[0], line_y), (pos[0] + (line_cols * cellSize[0]), line_y))


    def DrawPolycount(self, context):
        scn = context.scene

        # Sets the text and cell sizes based on the font size
        blf.size(self.font_id, scn.Polycount.Draw.font_size, 72)
        cellRefSize = ((scn.Polycount.Draw.font_size * 6) * scn.Polycount.Draw.width, (scn.Polycount.Draw.font_size * 0.7) * scn.Polycount.Draw.height)

        # Sets the coordinates in pixels of the top-left corner in the 3DView
        cols = self.get_columns(scn)
        initX = self.get_init_pos(bpy.context.region.width, cellRefSize[0]*cols, perc=scn.Polycount.Draw.hor_pos)
        rows = self.get_rows(scn)
        initY = self.get_init_pos(bpy.context.region.height, cellRefSize[1]*rows, perc=scn.Polycount.Draw.vert_pos, reverse=True, high_margin=scn.Polycount.Draw.font_size*10)

        pos = (initX, initY)

        # Recalculates the polycount. Keeps the displayed data up to date.
        context.scene.Polycount.controller.Refresh(context)

        if not scn.Polycount.Draw.Selected and \
                not scn.Polycount.Draw.Scene and \
                not scn.Polycount.Draw.Layer and \
                (not scn.Polycount.Draw.List or \
                 len(bpy.context.scene.Polycount.MainUI.lists_List)==0): return

        # Global Polycount will be displayed if it is on in the ui and if any of its components is on
        objectMode = scn.Polycount.Draw.ObjPolycount and (scn.Polycount.Draw.triangles or scn.Polycount.Draw.percentage or scn.Polycount.Draw.faces or scn.Polycount.Draw.quads or scn.Polycount.Draw.ngons)

        # Object/Global mode: This information will be displayed in real-time in Object and Edit Mode.
        if objectMode:
            # Global mode data is stored in an ordered dictionary
            contentObjMode = collections.OrderedDict()
            # Add the name of each component which will be accounted
            contentObjMode['OBJECT'] = ('Triangles', 'Quads', 'Ngons', 'Faces', "PureTriangles")
            # Data for each Polycount context (selected objects, scene, layer and list) will be stored in the dictionary
            if scn.Polycount.Draw.Selected:   contentObjMode['Selection'] = (scn.Polycount.ObjectMode.SelectedData, None)
            if scn.Polycount.Draw.Scene:      contentObjMode['Scene']    = (scn.Polycount.ObjectMode.SceneData, None)
            if scn.Polycount.Draw.Layer:      contentObjMode['Layer']    = (scn.Polycount.ObjectMode.LayerData, None)
            lists = bpy.context.scene.Polycount.MainUI.lists_List
            if scn.Polycount.Draw.List and len(lists)>0:
                for l in lists:
                    if not l.list_visible: continue
                    contentObjMode[l.list_name] = (l.list_data, l.list_color)

            # Data will be displayed as a table
            pos = self.DrawTable(pos, cellRefSize, contentObjMode)

        # EditMode Polycount will be displayed if it is on in the ui and if any of its components is on
        editMode = scn.Polycount.Draw.EditModePolycount and (scn.Polycount.Draw.selected_tris or scn.Polycount.Draw.selected_verts or scn.Polycount.Draw.selected_edges or scn.Polycount.Draw.selected_faces)

        edit_mode_pos = (pos[0], pos[1]-cellRefSize[1])
        # Edit Mode: This information will be only displayed in Edit Mode
        if bpy.context.mode == 'EDIT_MESH' and editMode:
            if objectMode: self.draw_obj_edit_sep_line(pos, cellRefSize, scn.Polycount.Draw.sep_color, cols)

            # Global mode data is stored in an ordered dictionary
            contentEditMode = collections.OrderedDict()
            # Add the name of each component which will be accounted
            contentEditMode['EDIT'] = ('Triangles', 'Verts', 'Edges', 'Faces')
            # In Edit mode, Polycount only accounts the selected components
            # Data for this context (selected components) will be stored in the dictionary
            contentEditMode['Selected'] = scn.Polycount.EditMode

            # Data will be displayed as a table
            self.DrawEditModeTable(edit_mode_pos, cellRefSize, contentEditMode)

    def DisplayPolycount(self, context):
        """
        Displays the Polycount information in the 3D View
        :param context:
        """
        if self.PostPixelHandle is None: self.HidePolycount(context)
        self.handle_add(context, self.DrawPolycount)

    def HidePolycount(self, context):
        """
        Hides the Polycount information
        :param context:
        """
        if self.PostPixelHandle is not None: self.handle_remove(context)

