
def manage_window_visualization(context, current_region_id, show):
    count = 0
    for w in context.scene.Polycount.MainUI.window_display:
        if count == current_region_id:
            count = count + 1
            continue
        w.display = show
        count = count + 1