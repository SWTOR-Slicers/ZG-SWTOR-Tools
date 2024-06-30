import bpy
import statistics

class ZGSWTOR_OT_reset_group_transforms(bpy.types.Operator):
    bl_idname = "zgswtor.reset_group_transforms"
    bl_label = "ZG Reset Group's Transforms"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Allows for resetting a selection of objects' transforms as a group instead of individually.\nUseful when copypasting a selection of items which in their original scene were too far away\nfrom the scene's origin, typical when collecting items from an imported SWTOR Area for reuse."

    # Check that there is a selection of objects (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects:
            return True
        else:
            return False


    # PROPERTIES

    # Property for the UI buttons to call different actions.
    # See: https://b3d.interplanety.org/en/calling-functions-by-pressing-buttons-in-blender-custom-ui/
    
    action: bpy.props.EnumProperty(
        name="Scaling Type",
        items=[
            ("POSITION", "Position", "Position"),
            ("ROTATION", "Rotation", "Rotation"),
            ("SCALE", "Scale", "Scale"),
            ("UNPARENT", "Clear Parenting Preserving Transforms", "Clear Parenting Preserving Transforms"),
            ],
        options={'HIDDEN'}
        )

    
    def execute(self, context):

        # Select only objects that aren't parented to avoid double-scaling.
        # Scales both sizes and positions in respect to the origin so that
        # the whole scene's object spacing is correctly preserved.

        bpy.context.window.cursor_set("WAIT")

        non_parented_objects = [obj for obj in bpy.context.selected_objects if not obj.parent]
        
        if len(non_parented_objects) == 1 or len(context.selected_objects) == 1:
            x_median = non_parented_objects[0].location[0]
            y_median = non_parented_objects[0].location[1]
            z_median = non_parented_objects[0].location[2]
        else:
            x_median = statistics.mean( [obj.location[0] for obj in non_parented_objects] )
            y_median = statistics.mean( [obj.location[1] for obj in non_parented_objects] )
            z_median = statistics.mean( [obj.location[2] for obj in non_parented_objects] )

        if self.action == "POSITION":
            for obj in non_parented_objects:
                obj.location = [
                    obj.location[0] - x_median,
                    obj.location[1] - y_median,
                    obj.location[2] - z_median,
                ]
        elif self.action == "ROTATION":
            pass
        elif self.action == "UNPARENT":
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

        bpy.context.window.cursor_set("DEFAULT")
        return {"FINISHED"}


# UI is set in ui.py

# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_reset_group_transforms)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_reset_group_transforms)


if __name__ == "__main__":
    register()