import bpy
import bmesh

from .utils.addon_checks import requirements_checks


# Main

class ZGSWTOR_OT_remove_doubles_edit_mode(bpy.types.Operator):
    bl_idname = "zgswtor.remove_doubles_edit_mode"
    bl_label = "ZG Remove Doubles in Edit Mode"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Removes selected double vertices (does a Merge by Distance\nin selected vertices using a coarser threshold of 0.00001),\nand applies a Normals > Average > Face Area to the whole object.\n\nIf a SWTOR object, this tool will look for the mesh scale it was\nimported with, to adjust the threshold accordingly.\n\n• Requires switching to Edit Mode.\n• Requires a selection of faces/edges/vertices."

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


        # Checking if we must handle SWTOR objects' custom properties about their meshes' scales
        use_gr2_scale_custom_prop = context.preferences.addons["zg_swtor_tools"].preferences.use_gr2_scale_custom_prop

        # Checking if we are dealing with a .gr2 Add-on with scaling parameters
        checks = requirements_checks()
        if checks["gr2HasParams"]:
            if context.preferences.addons["io_scene_gr2"].preferences.gr2_scale_object:
                gr2_scale = context.preferences.addons["io_scene_gr2"].preferences.gr2_scale_factor
            else:
                gr2_scale = 1.0
        else:
            gr2_scale = 1.0

        print(f"Global Scale for threshold calculation = {gr2_scale}")
        if use_gr2_scale_custom_prop:
            print("SWTOR objects with custom 'gr_scale' properties will use their own.")
        
        obj=context.selected_objects[0]

        if "gr2_scale" in obj and use_gr2_scale_custom_prop:
            gr2_scale = obj["gr2_scale"]

        obj_initial_vert_count = len(obj.data.vertices)

        # For this case we aren't using bmesh, as bpy.ops is fast enough
        # and makes things simpler.

        # Convert selection mode to vertices just in case.
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')

        # We are using a lower threshold than in the object-level merger
        # which is appropriate for neck and limb seams but would be
        # trouble in facial features (fused lips and other horror stories).
        # We are also preserving sharp edges, as in the object mode remove
        # doubles tool, although the use case suggests we wouldn't want
        # that here, but for now we'll keep consistency and see how it goes.
        bpy.ops.mesh.remove_doubles(threshold = 1e-04 * gr2_scale, use_sharp_edge_from_normals=True)

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

        if vert_count_report > 0:
            # # Just in case, we do only the Normals averaging if some vertex
            # # was merged (I don't know if this calculation can accumulate
            # # imprecisions if executed to often, so…)

            # # We select the full mesh for the Normals averaging pass. 
            # bpy.ops.mesh.select_all(action="SELECT")

            # # Normals averaging for correct looks. Merits some discussion.
            # bpy.ops.mesh.average_normals(average_type='FACE_AREA')
            # bpy.ops.mesh.select_all(action="DESELECT")

            self.report({'INFO'}, str(vert_count_report) + " Vertices merged. All affected objects were Auto-Smoothed and their Normals averaged by face area.")
        else:
            self.report({'INFO'}, "0 Vertices merged")


        context.window.cursor_set("DEFAULT")  # Show normal cursor icon
        return {"FINISHED"}




# UI is set in addon_ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_remove_doubles_edit_mode)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_remove_doubles_edit_mode)

if __name__ == "__main__":
    register()