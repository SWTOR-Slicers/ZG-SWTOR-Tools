import bpy

# Deselect all objects
bpy.ops.object.select_all(action='DESELECT')

# Store the current active object
current_active_object = bpy.context.active_object

# Iterate through all view layers in the scene
for view_layer in bpy.context.scene.view_layers:
    bpy.context.window.view_layer = view_layer  # Set the view layer temporarily
    
    # Check if there are any non-camera objects in the view layer
    non_camera_objects = [obj for obj in bpy.context.window.view_layer.objects if obj.type != 'CAMERA']
    
    if non_camera_objects:
        # Loop through all objects in the view layer
        for obj in non_camera_objects:
            # Select the object
            obj.select_set(True)

        # Make the objects single user
        bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True, material=False, animation=False)

        # Clear parent relationships while preserving transformations
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

        # Deselect all objects again
        bpy.ops.object.select_all(action='DESELECT')

# Restore the original active object
if current_active_object:
    current_active_object.select_set(True)
    bpy.context.view_layer.objects.active = current_active_object
    
    
    
# ---------------------------------------------------------------------------


import bpy

def make_single_user(context, selected_objects=True, obdata=True, material=False, animation=False):
    for obj in context.selected_objects:
        if selected_objects:
            obj.data = obj.data.copy() if obdata else obj.data
            if material:
                obj.material_slots[0].material = obj.material_slots[0].material.copy()

        if animation:
            for fcurve in obj.animation_data.action.fcurves:
                fcurve.keyframe_points.insert(fcurve.keyframe_points[-1].co[0] + 1, fcurve.keyframe_points[-1].co[1])

    return