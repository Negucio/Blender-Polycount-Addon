import bpy
import bgl
import blf
import collections as python_collections
from ..common_utils import redraw, get_region


class Draw:
    """
    Composes and displays the Polycount information
    """
    def __init__(self):
        self.PostPixelHandle = None     # Stores the draw handler
        self.font_id = 0

    def handle_add(self, context, draw_func):
        """
        Sets the draw handler which displays the polycount information in the 3DView
        :param context:
        :param draw_func: The function which will compose and display the information
        """
        if self.PostPixelHandle is None:
            self.PostPixelHandle = bpy.types.SpaceView3D.draw_handler_add(draw_func, (context,), 'WINDOW', 'POST_PIXEL')
            redraw()

    def handle_remove(self, context):
        """
        Removes the draw handler
        :param context:
        """
        if self.PostPixelHandle is not None:
            bpy.types.SpaceView3D.draw_handler_remove(self.PostPixelHandle, 'WINDOW')
            redraw()
        self.PostPixelHandle = None

    def draw_cell(self, text, position, color, width):
        """
        Draws a cell of the table
        :param text: Text in the cell
        :param position: 2D position of the cell
        :param color: Color of the text in the cell
        :param width: Width of the cell
        """
        if not text.isdigit() or color is None:
            blf.position(self.font_id, position[0], position[1], 0)
            blf.color(self.font_id, color[0], color[1], color[2], 1.0)
            blf.draw(self.font_id, text)
            return

        if not hasattr(bpy.context, "scene"):
            return
        scn = bpy.context.scene
        self.format_digits_2(text, position, scn, width)

        blf.color(self.font_id, color[0], color[1], color[2], 1.0)

    def draw_char(self, position, char, char_sample_width):
        blf.position(self.font_id, position[0], position[1], 0)
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
                    if count == 3:
                        tc = scene.Polycount.Draw.thousands_color
                        blf.color(self.font_id, tc[0], tc[1], tc[2], 1.0)
                    elif count == 6:
                        mc = scene.Polycount.Draw.millions_color
                        blf.color(self.font_id, mc[0], mc[1], mc[2], 1.0)

    # def draw_line(self, v1, v2):
    #     """
    #     Draws a line between the 2D position v1 and the 2D position v2
    #     :param v1: First 2D point of the line
    #     :param v2: Second 2D point of the line
    #     """
    #     if v1 and v2:
    #         bgl.glBegin(bgl.GL_LINES)
    #         bgl.glVertex2f(*v1)
    #         bgl.glVertex2f(*v2)
    #         bgl.glEnd()
    #     return

    def draw_table(self, pos, cell_size, content):
        """
        Composes the global Polycount table in the 3DView
        :param pos: Tuple (x,y) of 2D coordinates in pixels inside the 3DView which
                    will set the top-left corner of the table
        :param cell_size:
        :param content: Ordered dictionary with the data of the Object/Global mode
        """
        scn = bpy.context.scene
        draw_pc = scn.Polycount.Draw
        row = 0

        # "pos" coordinates set the position of the top-left corner of the table
        init_x = pos[0]
        init_y = pos[1]

        x = init_x + (40 * draw_pc.title_sep)
        y = init_y

        for key in content:
            content_color = draw_pc.title_color if content[key][1] is None else content[key][1]
            title_color = draw_pc.sep_color if key == 'OBJECT' else content_color
            blf.color(self.font_id, title_color[0], title_color[1], title_color[2], 1.0)

            title = key
            max_chars = int(draw_pc.width * (9 + (5*draw_pc.title_sep)))

            perc = ''
            if draw_pc.percentage and row > 0 and key != 'Selection':
                sel_tris = bpy.context.scene.Polycount.ObjectMode.SelectedData.Triangles
                col_tris = content[key][0].Triangles
                perc = " {0}%".format(int(0 if col_tris == 0 else (sel_tris / col_tris) * 100))
                max_chars -= len(perc)

            if len(key) > max_chars:
                title = key[0:max_chars-2] + "..."

            blf.position(self.font_id, init_x, y, 0)
            blf.draw(self.font_id, title)

            if perc:
                title_width, title_height = blf.dimensions(self.font_id, title)
                pc = draw_pc.perc_color
                blf.color(self.font_id, pc[0], pc[1], pc[2], 1.0)
                blf.position(self.font_id, init_x+title_width, y, 0)
                blf.draw(self.font_id, perc)

            color = draw_pc.title_color if row == 0 else draw_pc.data_color
            blf.color(self.font_id, color[0], color[1], color[2], 1.0)

            col = 1
            if draw_pc.triangles:
                text = 'Total Tris'
                if row > 0:
                    text = str(content[key][0].Triangles)
                self.draw_cell(text, (x + (cell_size[0] * col), y), color, cell_size[0])
                col = col + 1
            if draw_pc.faces:
                text = 'Faces'
                if row > 0:
                    text = str(content[key][0].Faces)
                self.draw_cell(text, (x + (cell_size[0] * col), y), color, cell_size[0])
                col = col + 1

            if draw_pc.pure_tris:
                text = 'Triangles'
                if row > 0:
                    text = str(content[key][0].PureTriangles)
                self.draw_cell(text, (x + (cell_size[0] * col), y), color, cell_size[0])
                col = col + 1
            if draw_pc.quads:
                text = 'Quads'
                if row > 0:
                    text = str(content[key][0].Quads)
                self.draw_cell(text, (x + (cell_size[0] * col), y), color, cell_size[0])
                col = col + 1
            if draw_pc.ngons:
                text = 'Ngons'
                if row > 0:
                    text = str(content[key][0].Ngons)
                self.draw_cell(text, (x + (cell_size[0] * col), y), color, cell_size[0])
            row = row + 2

            y = init_y - (cell_size[1] * row)

        # Vertical line to separate Percentage and Tris/Quads/Ngons
        if (draw_pc.triangles or draw_pc.faces) and (draw_pc.pure_tris or draw_pc.quads or draw_pc.ngons):
            cols = 2 if draw_pc.triangles and draw_pc.faces else 1
            sep_x = x + (cell_size[0] * cols) + (draw_pc.font_size * (5 * draw_pc.width))
            sc = draw_pc.sep_color
            blf.color(self.font_id, sc[0], sc[1], sc[2], 1.0)
            #self.draw_line((sep_x, init_y), (sep_x, y + (cell_size[1] * 2)))

        return x, y

    def draw_edit_mode_table(self, pos, cell_size, content):
        scn = bpy.context.scene
        draw_pc = scn.Polycount.Draw

        init_x = pos[0]
        init_y = pos[1]

        y = init_y

        row = 0

        for key in content:
            if key == 'EDIT':
                sp = draw_pc.sep_color
                blf.color(self.font_id, sp[0], sp[1], sp[2], 1.0)
            else:
                tc = draw_pc.title_color
                blf.color(self.font_id, tc[0], tc[1], tc[2], 1.0)
            blf.position(self.font_id, init_x, y, 0)
            blf.draw(self.font_id, key)

            color = draw_pc.title_color if row == 0 else draw_pc.data_color
            blf.color(self.font_id, color[0], color[1], color[2], 1.0)

            col = 1
            if draw_pc.selected_tris:
                text = 'Triangles'
                if row > 0:
                    text = str(content[key].Triangles)
                self.draw_cell(text, (init_x + (cell_size[0] * col), y), color, cell_size[0])
                col = col + 1
            if draw_pc.selected_verts:
                text = 'Verts'
                if row > 0:
                    text = str(content[key].Verts)
                self.draw_cell(text, (init_x + (cell_size[0] * col), y), color, cell_size[0])
                col = col + 1
            if draw_pc.selected_edges:
                text = 'Edges'
                if row > 0:
                    text = str(content[key].Edges)
                self.draw_cell(text, (init_x + (cell_size[0] * col), y), color, cell_size[0])
                col = col + 1
            if draw_pc.selected_faces:
                text = 'Faces'
                if row > 0:
                    text = str(content[key].Faces)
                self.draw_cell(text, (init_x + (cell_size[0] * col), y), color, cell_size[0])
            row = row + 2

            y = init_y - (cell_size[1] * row)

    def get_columns(self, scene):
        # Initializes var to 1 because of the title column
        obj_mode = 1
        if scene.Polycount.Draw.ObjPolycount:
            if scene.Polycount.Draw.triangles:
                obj_mode += 1
            if scene.Polycount.Draw.faces:
                obj_mode += 1
            if scene.Polycount.Draw.pure_tris:
                obj_mode += 1
            if scene.Polycount.Draw.quads:
                obj_mode += 1
            if scene.Polycount.Draw.ngons:
                obj_mode += 1

        # Initializes var to 1 because of the title column
        edit_mode = 1
        if scene.Polycount.Draw.EditModePolycount and bpy.context.mode == 'EDIT_MESH':
            if scene.Polycount.Draw.selected_tris:
                edit_mode += 1
            if scene.Polycount.Draw.selected_verts:
                edit_mode += 1
            if scene.Polycount.Draw.selected_edges:
                edit_mode += 1
            if scene.Polycount.Draw.selected_faces:
                edit_mode += 1

        return max(obj_mode, edit_mode)

    def get_rows(self, scene):
        # Initializes var to 1 because of the title column
        obj_mode = 1
        if scene.Polycount.Draw.ObjPolycount:
            if scene.Polycount.Draw.Selected:
                obj_mode += 1
            if scene.Polycount.Draw.Scene:
                obj_mode += 1
            # if scene.Polycount.Draw.Layer:
            #     obj_mode += 1
            if scene.Polycount.Draw.List:
                obj_mode += len([l.list_visible for l in bpy.context.scene.Polycount.MainUI.lists_List])

        # Initializes var to 1 because of the title column
        edit_mode = 1
        if scene.Polycount.Draw.EditModePolycount and bpy.context.mode == 'EDIT_MESH':
            edit_mode += 1

        return obj_mode + edit_mode

    def get_init_pos(self, max_value, size, perc=1, low_margin=20, high_margin=20, reverse=False):
        # TODO: Check vertical drawing: Table goes outside of the view3d in perc=0 and more than 4 rows
        pos = (max_value - size) * perc
        if pos < low_margin:
            pos = low_margin
        elif pos > max_value-high_margin:
            pos = max_value - high_margin
        return pos if not reverse else max_value - pos

    def draw_obj_edit_sep_line(self, pos, cell_size, color, cols):
        line_y = pos[1] + cell_size[1]
        blf.color(self.font_id, color[0], color[1], color[2], 1.0)
        line_cols = cols - 0.5
        #self.draw_line((pos[0], line_y), (pos[0] + (line_cols * cell_size[0]), line_y))

    def manage_windows(self, region, scene):
        if region is None:
            return

        windows = len(scene.Polycount.MainUI.window_display)
        if windows > region.id:
            return
        count = 0
        while windows <= region.id + 1 or count > 100:
            item = scene.Polycount.MainUI.window_display.add()
            windows = len(scene.Polycount.MainUI.window_display)
            if count == region.id:
                item.display = True
            count = count + 1

    def draw_polycount(self, context):
        scn = context.scene

        # region = get_region(context)
        # self.manage_windows(region, scn)
        # if not context.scene.Polycount.MainUI.window_display[region.id].display:
        #     return

        draw_pc = scn.Polycount.Draw

        # Sets the text and cell sizes based on the font size
        blf.size(self.font_id, draw_pc.font_size, 72)
        cell_ref_size = ((draw_pc.font_size * 6) * draw_pc.width, (draw_pc.font_size * 0.7) * draw_pc.height)

        # Sets the coordinates in pixels of the top-left corner in the 3DView
        cols = self.get_columns(scn)
        init_x = self.get_init_pos(bpy.context.region.width, cell_ref_size[0]*cols+(40*draw_pc.title_sep),
                                   perc=draw_pc.hor_pos)
        rows = self.get_rows(scn)
        init_y = self.get_init_pos(bpy.context.region.height, cell_ref_size[1]*rows,
                                   perc=draw_pc.vert_pos, reverse=True, high_margin=draw_pc.font_size*10)

        pos = (init_x, init_y)

        # Recalculates the polycount. Keeps the displayed data up to date.
        context.scene.Polycount.controller.refresh(context)

        if not draw_pc.Selected and \
                not draw_pc.Scene and \
                (not draw_pc.List or len(bpy.context.scene.Polycount.MainUI.lists_List) == 0):
            return

        # Global Polycount will be displayed if it is on in the ui and if any of its components is on
        any_selected = draw_pc.triangles or draw_pc.percentage or draw_pc.faces or draw_pc.quads or draw_pc.ngons or draw_pc.pure_tris
        object_mode = draw_pc.ObjPolycount and any_selected

        # Object/Global mode: This information will be displayed in real-time in Object and Edit Mode.
        if object_mode:
            # Global mode data is stored in an ordered dictionary
            content_obj_mode = python_collections.OrderedDict()
            # Add the name of each component which will be accounted
            content_obj_mode['OBJECT'] = ('Triangles', 'Quads', 'Ngons', 'Faces', "PureTriangles")
            # Data for each Polycount context (selected objects, scene, layer and list) will be stored in the dictionary
            if draw_pc.Selected:
                content_obj_mode['Selection'] = (scn.Polycount.ObjectMode.SelectedData, None)
            if draw_pc.Scene:
                content_obj_mode['Scene'] = (scn.Polycount.ObjectMode.SceneData, None)
            # if draw_pc.Layer:
            #     content_obj_mode['Layer'] = (scn.Polycount.ObjectMode.LayerData, None)
            lists = bpy.context.scene.Polycount.MainUI.lists_List
            if draw_pc.List and len(lists) > 0:
                for l in lists:
                    if not l.list_visible:
                        continue
                    content_obj_mode["L_" + l.list_name] = (l.list_data, l.list_color)

            collections = bpy.context.scene.Polycount.MainUI.col_list
            if draw_pc.Collection and len(collections) > 0:
                for col in collections:
                    if not col.collection_visible:
                        continue
                    content_obj_mode["C_" + col.collection.name] = (col.collection_data, col.collection_color)

            # Data will be displayed as a table
            pos = self.draw_table(pos, cell_ref_size, content_obj_mode)

        # EditMode Polycount will be displayed if it is on in the ui and if any of its components is on
        any_selected = draw_pc.selected_tris or draw_pc.selected_verts or \
            draw_pc.selected_edges or draw_pc.selected_faces
        edit_mode = draw_pc.EditModePolycount and any_selected

        edit_mode_pos = (pos[0], pos[1]-cell_ref_size[1])
        # Edit Mode: This information will be only displayed in Edit Mode
        if bpy.context.mode == 'EDIT_MESH' and edit_mode:
            if object_mode:
                self.draw_obj_edit_sep_line(pos, cell_ref_size, draw_pc.sep_color, cols)

            # Global mode data is stored in an ordered dictionary
            content_edit_mode = python_collections.OrderedDict()
            # Add the name of each component which will be accounted
            content_edit_mode['EDIT'] = ('Triangles', 'Verts', 'Edges', 'Faces')
            # In Edit mode, Polycount only accounts the selected components
            # Data for this context (selected components) will be stored in the dictionary
            content_edit_mode['Selected'] = scn.Polycount.EditMode

            # Data will be displayed as a table
            self.draw_edit_mode_table(edit_mode_pos, cell_ref_size, content_edit_mode)

    def display_polycount(self, context):
        """
        Displays the Polycount information in the 3D View
        :param context:
        """
        if self.PostPixelHandle is None:
            self.hide_polycount(context)
        self.handle_add(context, self.draw_polycount)

    def hide_polycount(self, context):
        """
        Hides the Polycount information
        :param context:
        """
        if self.PostPixelHandle is not None:
            self.handle_remove(context)

