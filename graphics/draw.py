import bpy, bgl, blf, collections
from .. polycount.controller import PolycountController

class Draw():
    """
    Composes and displays the Polycount information
    """
    def __init__(self):
        self.PostPixelHandle = None # Stores the draw handler
        self.font_id = 0
        self.pc = PolycountController()

    def handle_add(self, context, DrawFunction):
        """
        Sets the draw handler which displays the polycount information in the 3DView
        :param context:
        :param DrawFunction: The function which will compose and display the information
        """
        if self.PostPixelHandle is None:
            self.PostPixelHandle = bpy.types.SpaceView3D.draw_handler_add(DrawFunction, (), 'WINDOW', 'POST_PIXEL')
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

    def DrawCell(self, text, position):
        """
        Draws a cell of the table
        :param text: Text in the cell
        :param position: 2D position of the cell
        """
        blf.position(0, position[0], position[1], 0)
        blf.draw(self.font_id, text)

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

        for key in content:
            y = initY - (cellSize[1] * row)

            if key == 'OBJECT': bgl.glColor3f(*scn.Polycount.Draw.sep_color)
            else: bgl.glColor3f(*scn.Polycount.Draw.title_color)
            blf.position(0, initX, y, 0)
            blf.draw(self.font_id, key)

            if row == 0: bgl.glColor3f(*scn.Polycount.Draw.title_color)
            else: bgl.glColor3f(*scn.Polycount.Draw.data_color)

            col = 1
            if scn.Polycount.Draw.triangles:
                text = 'Tris'
                if row > 0: text = str(content[key].Triangles)
                self.DrawCell(text, (initX + (cellSize[0] * col), y))
                col = col + 1
            if scn.Polycount.Draw.faces:
                text = 'Faces'
                if row > 0: text = str(content[key].Faces)
                self.DrawCell(text, (initX + (cellSize[0] * col), y))
                col = col + 1
            if scn.Polycount.Draw.quads:
                text = 'Quads'
                if row > 0: text = str(content[key].Quads)
                self.DrawCell(text, (initX + (cellSize[0] * col), y))
                col = col + 1
            if scn.Polycount.Draw.ngons:
                text = 'Ngons'
                if row > 0: text = str(content[key].Ngons)
                self.DrawCell(text, (initX + (cellSize[0] * col), y))
            row = row + 2

        if (scn.Polycount.Draw.triangles or scn.Polycount.Draw.faces) and (scn.Polycount.Draw.quads or scn.Polycount.Draw.ngons):
            triOrFac = 2 if scn.Polycount.Draw.triangles and scn.Polycount.Draw.faces else 1
            sepX = initX + (cellSize[0] * triOrFac) + (scn.Polycount.Draw.font_size * 5)
            bgl.glColor3f(*scn.Polycount.Draw.sep_color)
            self.DrawLine((sepX, initY), (sepX, y))
        return (initX + (cellSize[0] * col) , y)

    def DrawEditModeTable(self, pos, cellSize, content, objectMode):
        scn = bpy.context.scene

        initX = bpy.context.region.width - 400 + scn.Polycount.Draw.hor_Offset
        initY = pos[1]

        if objectMode:
            initY = initY - cellSize[1]
            bgl.glColor3f(*scn.Polycount.Draw.sep_color)
            self.DrawLine((initX, initY), (pos[0]+(cellSize[0]/2), initY))
            initY = initY - cellSize[1]*2
        row = 0

        for key in content:
            y = initY - (cellSize[1] * row)

            if key == 'EDIT': bgl.glColor3f(*scn.Polycount.Draw.sep_color)
            else: bgl.glColor3f(*scn.Polycount.Draw.title_color)
            blf.position(0, initX, y, 0)
            blf.draw(self.font_id, key)

            if row == 0: bgl.glColor3f(*scn.Polycount.Draw.title_color)
            else: bgl.glColor3f(*scn.Polycount.Draw.data_color)

            col = 1
            if scn.Polycount.Draw.selected_tris:
                text = 'Tris'
                if row > 0: text = str(content[key].Triangles)
                self.DrawCell(text, (initX + (cellSize[0] * col), y))
                col = col + 1
            if scn.Polycount.Draw.selected_verts:
                text = 'Verts'
                if row > 0: text = str(content[key].Verts)
                self.DrawCell(text, (initX + (cellSize[0] * col), y))
                col = col + 1
            if scn.Polycount.Draw.selected_edges:
                text = 'Edges'
                if row > 0: text = str(content[key].Edges)
                self.DrawCell(text, (initX + (cellSize[0] * col), y))
                col = col + 1
            if scn.Polycount.Draw.selected_faces:
                text = 'Faces'
                if row > 0: text = str(content[key].Faces)
                self.DrawCell(text, (initX + (cellSize[0] * col), y))
            row = row + 2

    def DrawPolycount(self):
        ctx = bpy.context
        scn = ctx.scene

        # TODO: Constants should not be used in order to set the initial position.
        # TODO: Should be dependant on the region limits, allowing to customize only the offsets
        # TODO: and keeping the limits to avoid drawing outside the 3dView.
        # Sets the coordinates in pixels of the top-left corner in the 3DView
        initX = bpy.context.region.width - 400 + scn.Polycount.Draw.hor_Offset
        initY = bpy.context.region.height - 22 + scn.Polycount.Draw.vert_Offset
        pos = (initX, initY)

        # Sets the text and cell sizes based on the font size
        blf.size(self.font_id, scn.Polycount.Draw.font_size, 72)
        cellRefSize = (scn.Polycount.Draw.font_size * 6, scn.Polycount.Draw.font_size - 4)

        # Recalculates the polycount. Keeps the displayed data up to date.
        self.pc.Refresh(ctx)

        # Global Polycount will be displayed if it is on in the ui and if any of its components is on
        objectMode = scn.Polycount.Draw.ObjPolycount and (scn.Polycount.Draw.triangles or scn.Polycount.Draw.faces or scn.Polycount.Draw.quads or scn.Polycount.Draw.ngons)

        # Object/Global mode: This information will be displayed in real-time in Object and Edit Mode.
        if objectMode:
            # Global mode data is stored in an ordered dictionary
            content = collections.OrderedDict()
            # Add the name of each component which will be accounted
            content['OBJECT'] = ('Triangles', 'Quads', 'Ngons', 'Faces')

            # Data for each Polycount context (selected objects, scene, layer and list) will be stored in the dictionary
            if scn.Polycount.ObjectMode.Selected:   content['Selected'] = scn.Polycount.ObjectMode.SelectedData
            if scn.Polycount.ObjectMode.Scene:      content['Scene']    = scn.Polycount.ObjectMode.SceneData
            if scn.Polycount.ObjectMode.Layer:      content['Layer']    = scn.Polycount.ObjectMode.LayerData
            lists = bpy.context.scene.Polycount.MainUI.lists_List
            if scn.Polycount.ObjectMode.List and len(lists)>0:
                for l in lists:
                    content[l.list_name] =  l.list_data

            # Data will be displayed as a table
            pos = self.DrawTable(pos, cellRefSize, content)

        # EditMode Polycount will be displayed if it is on in the ui and if any of its components is on
        editMode = scn.Polycount.Draw.EditModePolycount and (scn.Polycount.Draw.selected_tris or scn.Polycount.Draw.selected_verts or scn.Polycount.Draw.selected_edges or scn.Polycount.Draw.selected_faces)
        # Edit Mode: This information will be only displayed in Edit Mode
        if bpy.context.mode == 'EDIT_MESH' and editMode:
            # Global mode data is stored in an ordered dictionary
            contentEditMode = collections.OrderedDict()
            # Add the name of each component which will be accounted
            contentEditMode['EDIT'] = ('Tris', 'Verts', 'Edges', 'Faces')
            # In Edit mode, Polycount only accounts the selected components
            # Data for this context (selected components) will be stored in the dictionary
            contentEditMode['Selected'] = scn.Polycount.EditMode

            # Data will be displayed as a table
            self.DrawEditModeTable(pos, cellRefSize, contentEditMode, objectMode)

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

