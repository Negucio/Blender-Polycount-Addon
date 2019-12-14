
def has_solidify(obj):
    """
    Checks if the object has a solidify modifier
    :param obj: The object
    :return: True/False
    """
    if not hasattr(obj, "modifiers"):
        return False
    for mod in obj.modifiers:
        if mod.type == 'SOLIDIFY' and mod.show_viewport:
            return True
    return False


def get_levels_subsurf(obj):
    """
    Checks if the object has one or more subsurf modifiers,
    puts all the View levels value together
    and returns the global value
    :param obj: The object
    :return: The levels value for the view in the subsurf(s)
    """
    levels = 0
    if not hasattr(obj, "modifiers"):
        return levels
    for mod in obj.modifiers:
        if mod.type == 'SUBSURF' and mod.show_viewport:
            levels += mod.levels

    return levels


def calculate_subsurf(obj, tris, quads, ngons):
    """
    Calculates the number of polygons of the object
    based on the levels of subsurf modifier
    :param obj: Object to calculate the subsurf modifier polycount
    :param tris: Number of 3-sided polygons in the object
    :param quads: Number of 4-sided polygons in the object
    :param ngons: Number of n-sided polygons in the object
    :return: The number of quads depending on the levels of the assigned subsurf(s)
    """
    levels = get_levels_subsurf(obj)
    if levels == 0:
        return None
    # Subsurf creates as many faces as sides has the source face
    # In the first subsurf level, tris, quads and ngons need to be calculated separately
    # TODO: Ngons are calculated as 5-sided.
    polygons = tris*3 + quads*4 + ngons*5

    # The first level convert all faces in quads so, in the remaining levels,
    # all polygons can be calculated as quads
    polygons *= 4**(levels-1)
    return polygons


def get_mirror_axis(obj):
    """
    Checks if the object has a mirror modifier
    and calculates in how many axis is affecting
    :param obj: The object
    :return: The number of axis the modifier is affecting
    """
    mirror = None
    ret_val = 0
    if not hasattr(obj, "modifiers"):
        return ret_val
    for mod in obj.modifiers:
        if mod.type == 'MIRROR' and mod.show_viewport:
            mirror = mod
            break

    if mirror is None:
        return ret_val

    for axis in mirror.use_axis:
        if axis: ret_val += 1

    return ret_val
