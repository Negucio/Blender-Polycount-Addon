import re
from ... common_utils import get_addon_name

PATTERN = r"([a-zA-Z0-9_\-]*)(\[([0-9]+)\])"
PREFIX_LOWER = get_addon_name().lower() + '_'
PREFIX_UPPER = get_addon_name().upper() + '_'

def get_property(context, data_path):
    prop = context
    for attr in data_path.split("."):
        match = re.search(PATTERN, attr)
        if match:
            prop = getattr(prop, match.group(1))
            if len(prop) == 0:
                return None
            prop = prop[int(match.group(3))]
        else:
            prop = getattr(prop, attr)
    return prop


def draw_list(context, data_path, layout, title, tuple_buttons=(True, True, True, True)):
    prop = get_property(context, data_path)
    row = layout.row()
    box = row.box()
    row = box.row()

    split = row.split(factor=0.6)
    split.label(text=title + ' contents')
    split = split.split()
    split.prop(prop, "obj_list")

    row = box.row()
    row.template_list(PREFIX_UPPER+"DATA_UL_obj_list", "",
                      prop, 'obj_list',
                      prop, 'obj_list_index',
                      rows=1, maxrows=5)

    col = box.column(align=True)
    row = col.row(align=True)
    if tuple_buttons[0]:
        row.operator(PREFIX_LOWER+"obj_list_add.btn", text="Assign").data_path = data_path
        row.operator(PREFIX_LOWER+"obj_list_remove.btn", text="Remove").data_path = data_path

    if tuple_buttons[1]:
        row = col.row(align=True)
        row.operator(PREFIX_LOWER+"obj_list_clear.btn", text="Clear").data_path = data_path

    if tuple_buttons[2]:
        row = col.row(align=True)
        op = row.operator(PREFIX_LOWER+"obj_list_select.btn", text="Select All")
        op.select = True
        op.data_path = data_path

        op = row.operator(PREFIX_LOWER+"obj_list_select.btn", text="Deselect All")
        op.select = False
        op.data_path = data_path

    if tuple_buttons[3]:
        row = col.row(align=True)
        op = row.operator(PREFIX_LOWER+"obj_list_hide.btn", text="Show All")
        op.hide = False
        op.data_path = data_path

        op = row.operator(PREFIX_LOWER+"obj_list_hide.btn", text="Hide All")
        op.hide = True
        op.data_path = data_path




