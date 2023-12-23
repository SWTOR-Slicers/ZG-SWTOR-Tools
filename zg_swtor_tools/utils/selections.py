import bpy

def selected_objects_in_3d_view(context):
    if bpy.context.mode == "OBJECT" and bpy.context.selected_objects:
        enable_operator = True
    else:
        enable_operator = False
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'OUTLINER':
                    with context.temp_override(window=window, area=area):
                        if context.selected_ids:
                            for item in context.selected_ids:
                                if item.type == "MESH":
                                    enable_operator = True
                                    break
    return enable_operator


def selected_objects_in_outliner(context):
    enable_operator = False
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'OUTLINER':
                with context.temp_override(window=window, area=area):
                    if context.selected_ids:
                        for item in context.selected_ids:
                            if item.type == "MESH":
                                enable_operator = True
                                break
    return enable_operator


def selected_objects_in_outliner(context):
    enable_operator = False
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'OUTLINER':
                with context.temp_override(window=window, area=area):
                    if context.selected_ids:
                        for item in context.selected_ids:
                            if item.type == "MESH":
                                enable_operator = True
                                break
    return enable_operator
