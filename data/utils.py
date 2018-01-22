

def reset_data_property(dataProperty):
    """
    Resets the content of the DataPropertyGroup instance which is receive as a parameter
    :param dataProperty: Receives a blender python DataPropertyGroup instance
    :return:
    """
    # If the dataProperty has not these attributes, it is not a DataPropertyGroup instance
    if not hasattr(dataProperty, "Triangles") or \
            not hasattr(dataProperty, "PureTriangles") or \
            not hasattr(dataProperty, "Quads") or \
            not hasattr(dataProperty, "Ngons") or \
            not hasattr(dataProperty, "Faces"): return

    dataProperty.Triangles = 0
    dataProperty.PureTriangles = 0
    dataProperty.Quads = 0
    dataProperty.Ngons = 0
    dataProperty.Faces = 0