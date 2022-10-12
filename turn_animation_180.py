import bpy

class ZGSWTOR_OT_turn_animation_180(bpy.types.Operator):
    bl_idname = "zgswtor.turn_animation_180"
    bl_label = "ZG Turn Animation 180°"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Turns imported SWTOR animations 180° so that the animated\ncharacters look forward or backwards in the viewport.\n\n• Requires a selection that includes characters' skeletons.\n• The action is reversible by re-applying it"

    # Check that there is a selection of objects (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects:
            if any([obj.type == "ARMATURE" for obj in bpy.context.selected_objects]):
                return True
            else:
                return False
        else:
            return False

    

    def execute(self, context):
        bpy.context.window.cursor_set("WAIT")

        # armatures = [obj for obj in context.selected_objects if obj.type == "ARMATURE"]
    
        # for armature in armatures:
        #     if armature.animation_data:
        #        armature.pose.bones["Bip01"].rotation_quaternion[2] = 0
        

        bpy.context.window.cursor_set("DEFAULT")
        return {"FINISHED"}

        # else:
        #     bpy.context.window.cursor_set("DEFAULT")
        #     self.report({"WARNING"}, "No modifiable objects were selected.")
        #     return {"CANCELLED"}






# UI is set in ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_turn_animation_180)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_turn_animation_180)

if __name__ == "__main__":
    register()