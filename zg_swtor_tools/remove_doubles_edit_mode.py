import bpy
import bmesh


# Main

class ZGSWTOR_OT_remove_doubles_edit_mode(bpy.types.Operator):
    bl_idname = "zgswtor.remove_doubles_edit_mode"
    bl_label = "ZG Remove Doubles in Edit Mode"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Removes selected double vertices (does a Merge by Distance\nin selected vertices using a coarser threshold of 0.00001),\nand applies a Normals > Average > Face Area to the whole object.\n\n• Requires a selection of faces/edges/vertices."

    # Check that we are in Edit mode
    # and that we are editing a single object
    @classmethod
    def poll(cls,context):
        if (
            len(bpy.context.selected_objects) == 1
            and bpy.context.mode == "EDIT_MESH"
            ):
            return True
        else:
            return False


    def execute(self, context):

        context.window.cursor_set("WAIT")  # Show wait cursor icon

        obj=context.selected_objects[0]
        obj_initial_vert_count = len(obj.data.vertices)

        # For this case we aren't using bmesh, as bpy.ops is fast enough
        # and makes things simpler.

        # Convert selection mode to vertices just in case.
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')

        # We are using a lower threshold than in the object-level merger
        # which is appropriate for neck and limb seams but would be
        # trouble in facial features (fused lips and other horror stories).
        bpy.ops.mesh.remove_doubles(threshold = 1e-04)

        # Calculate the vertex count difference to report how many
        # vertices were merged.
        # Edit mode doesn't update that data until exiting the mode, so,
        # load the objects edit-mode data into the object data
        # via this updating method. See:
        # https://blender.stackexchange.com/questions/8762/vertex-count-appears-incorrect-after-removing-doubles
        bpy.context.object.update_from_editmode()
        obj_final_vert_count = len(obj.data.vertices)
        vert_count_report = obj_initial_vert_count - obj_final_vert_count

        # Use Autosmooth just in case
        bpy.data.objects[obj.name].data.use_auto_smooth = True

        # Just in case, we do only the Normals averaging if some vertex
        # was merged (I don't know if this calculation can accumulate
        # imprecisions if executed to often, so…)
        if vert_count_report > 0:
            # We select the full mesh for the Normals averaging pass. 
            bpy.ops.mesh.select_all(action="SELECT")

            # Normals averaging for correct looks. Merits some discussion.
            bpy.ops.mesh.average_normals(average_type='FACE_AREA')
            bpy.ops.mesh.select_all(action="DESELECT")

            self.report({'INFO'}, str(vert_count_report) + " Vertices merged. All affected objects were Auto-Smoothed and their Normals averaged by face area.")
        else:
            self.report({'INFO'}, "0 Vertices merged")


        context.window.cursor_set("DEFAULT")  # Show normal cursor icon
        return {"FINISHED"}




# UI is set in ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_remove_doubles_edit_mode)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_remove_doubles_edit_mode)

if __name__ == "__main__":
    register()