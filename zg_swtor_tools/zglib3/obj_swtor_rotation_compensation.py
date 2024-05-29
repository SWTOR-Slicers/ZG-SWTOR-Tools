import bpy
from math import radians
from mathutils import Matrix

class ZGSWTOR_OT_quickscale(bpy.types.Operator):
    bl_idname = "zgswtor.quickscale"
    bl_label = "ZG Quickscale"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Quickscaler:\nResizes objects preserving their relative distances to facilitate\noperations that require real life-like sizes (e.g., auto-weight painting).\n\n• Requires a selection of objects.\n• Affects unparented objects only to avoid double-scaling"

    # Check that there is a selection of objects (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects:
            return True
        else:
            return False



    



    
    def execute(self, context):

        # Select only objects that aren't parented to avoid double-scaling.
        # Scales both sizes and positions in respect to the origin so that
        # the whole scene's object spacing is correctly preserved.

        bpy.context.window.cursor_set("WAIT")

        scale = bpy.context.scene.zgswtor_quickscale_factor

        selected_objects = [obj for obj in bpy.context.selected_objects if not obj.parent]

        if selected_objects:
            if self.action == "UPSCALE":
                for obj in selected_objects:
                    obj.scale *= scale
                    obj.location *= scale
            elif self.action == "DOWNSCALE":
                for obj in selected_objects:
                    obj.scale /= scale
                    obj.location /= scale

        bpy.context.window.cursor_set("DEFAULT")
        return {"FINISHED"}





# Check if there is an active object
def recursive_rotator(obj):
    # imported .gr2's exact 90º rotation in radians
    rotation_angle_radians = 1.570796251296997  

    # Create a 4x4 rotation matrix
    rotation_matrix = Matrix.Rotation(rotation_angle_radians, 4, 'X')

    # Apply the rotation to the object's data
    bpy.context.active_object.data.transform(rotation_matrix)

    # Update the scene to reflect the changes
    bpy.context.view_layer.update()
    
    # Rotate the object as such object -90º to get it back to its original apparent state
    bpy.context.active_object.rotation_euler[0] -= rotation_angle_radians






# UI is set in ui.py

# Registrations

    bpy.utils.register_class(ZGSWTOR_OT_quickscale)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_quickscale)


if __name__ == "__main__":
    register()