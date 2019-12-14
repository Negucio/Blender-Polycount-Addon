import bpy

def redraw():
    for w in bpy.context.window_manager.windows:
        for area in w.screen.areas:
            if area.type in ['VIEW_3D']:
                area.tag_redraw()
    for w in context.scene.Polycount.MainUI.window_display:
        if count == current_region_id:
            count = count + 1
            continue
        w.display = show
        count = count + 1