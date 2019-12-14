import bpy

def redraw():
    for w in bpy.context.window_manager.windows:
        for area in w.screen.areas:
            if area.type in ['VIEW_3D']:
                area.tag_redraw()

def manage_window_visualization(context, current_area, show):
    for w in context.scene.Polycount.MainUI.window_display:
        if w.area == current_area:
            continue
        w.display = show
    redraw()

def get_area(id):
    try:
        wm = bpy.data.window_managers[id[0]].windows[id[1]].screeen.areas[id[2]]
    except:
        return None

    return wm

def get_area_display(id):
    for a in bpy.context.scene.Polycount.MainUI.window_display:
        if a.area != id:
            continue
        else:
            return a
    return None

def get_area_id(area):
    if area.type != 'VIEW_3D':
        return None

    wm_count = 0
    for wm in bpy.data.window_managers:
        w_count = 0
        for w in wm.windows:
            a_count = 0
            for a in w.screen.areas:
                if a == area:
                    return str(wm_count) + str(w_count) + str(a_count)
                a_count = a_count + 1
            w_count = w_count + 1
        wm_count = wm_count + 1

    return None