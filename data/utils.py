
def reset_data_property(data_property):
    """
    Resets the content of the DataPropertyGroup instance which is receive as a parameter
    :param data_property: Receives a blender python DataPropertyGroup instance
    :return:
    """
    # If the data_property has not these attributes, it is not a DataPropertyGroup instance
    tris = hasattr(data_property, "Triangles")
    ptris = hasattr(data_property, "PureTriangles")
    quads = hasattr(data_property, "Quads")
    ngons = hasattr(data_property, "Ngons")
    faces = hasattr(data_property, "Faces")

    if tris and ptris and quads and ngons and faces:
        data_property.Triangles = 0
        data_property.PureTriangles = 0
        data_property.Quads = 0
        data_property.Ngons = 0
        data_property.Faces = 0
