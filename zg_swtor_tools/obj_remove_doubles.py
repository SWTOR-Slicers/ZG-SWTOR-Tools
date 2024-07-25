import bpy
import bmesh

from .utils.addon_checks import requirements_checks

# Main

class ZGSWTOR_OT_remove_doubles(bpy.types.Operator):
    bl_idname = "zgswtor.remove_doubles"
    bl_label = "ZG Remove Doubles"
    bl_description = "Removes objects' double vertices (does a Merge by Distance\n using a threshold of 0.0000001), and applies\nan 'Use Sharp Edge From Normals'.\n\nIt processes each selected object individually.\n\nIf applied to SWTOR objects, this tool will look for the mesh scale\nthey were imported with, to adjust the threshold accordingly"
    bl_options = {'REGISTER', "UNDO"}


    # Check that there is a selection of objects and that we are in Object mode
    # (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        context = bpy.context
        if context.area.type == 'VIEW_3D':
            if context.mode == 'EDIT_MESH':
                return False
            elif context.mode == 'OBJECT':
                for obj in bpy.data.objects:
                    if obj.type == "MESH":
                            return True
        return False
    

    use_selection_only : bpy.props.BoolProperty(
        name="Apply To Selected Objects Only",
        description="Apply to selected objects only.",
        default=True,
        options={'HIDDEN'},
    )

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
        
        
        print("---------------------")
        print("MERGE DOUBLE VERTICES")
        print("---------------------")
        print()

        # After some research, Crunch (AKA UnconventionalError) has changed the code to become
        # bpy.ops-based instead of BMESH based, as that allows for using a type of normals processing
        # that better preserves sharp edges with just an additional parameter.
        vert_count_report = 0

        if self.use_selection_only == True:
            copy_of_selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == "MESH"]
            if not copy_of_selected_objects:
                self.report({"WARNING"}, "No mesh objects were selected.")
                return {"CANCELLED"}
        else:
            copy_of_selected_objects = [obj for obj in bpy.data.objects if obj.type == "MESH"]
                    

        bpy.ops.object.select_all(action='DESELECT')
        for obj in copy_of_selected_objects:
            if obj.type == 'MESH':
                print(obj.name)

                if "gr2_scale" in obj and use_gr2_scale_custom_prop:
                    gr2_scale = obj["gr2_scale"]
                    print("Mesh Scale from 'gr2_scale' property = {gr2_scale}")

                obj_initial_vert_count = len(obj.data.vertices)
                context.view_layer.objects.active = obj
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles(threshold=1e-06 * gr2_scale, use_sharp_edge_from_normals=True)
                bpy.ops.object.editmode_toggle()

                # Calculate the vertex count difference to report how many vertices were merged.
                # Edit mode doesn't update that data until exiting the mode, so,
                # load the object's edit-mode data into the object data
                # via this updating method. See:
                # https://blender.stackexchange.com/questions/8762/vertex-count-appears-incorrect-after-removing-doubles
                # context.object.update_from_editmode()
                # NO LONGER NECESSARY
                
                context.view_layer.objects.active = None
                vert_count_report += len(obj.data.vertices) - obj_initial_vert_count
                print()

        print("\nDONE!")
        
        for obj in copy_of_selected_objects:
           obj.select_set(True)
        
        self.report({'INFO'}, str(-vert_count_report) + " Vertices merged.")

        bpy.context.window.cursor_set("DEFAULT")  # Show normal cursor icon
        return {"FINISHED"}


# UI is set in addon_ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_remove_doubles)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_remove_doubles)

if __name__ == "__main__":
    register()