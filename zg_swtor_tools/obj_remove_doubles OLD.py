import bpy
import bmesh


# Main

class ZGSWTOR_OT_remove_doubles(bpy.types.Operator):
    bl_idname = "zgswtor.remove_doubles"
    bl_label = "ZG Remove Doubles"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Removes double vertices (does a Merge by Distance\nin selected objects using a threshold of 0.0000001),\nand applies a Normals > Average > Face Area.\n\n• Requires a selection of objects.\n• Processes each selected object individually."

    # Check that there is a selection of objects and that we are in Object mode
    # (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects and bpy.context.mode == "OBJECT":
            return True
        else:
            return False


    def execute(self, context):

        bpy.context.window.cursor_set("WAIT")  # Show wait cursor icon

        if bpy.context.object:

            selected_objects = [obj for obj in bpy.context.selected_editable_objects if obj.type == "MESH" and not "skeleton" in obj.name]

            if selected_objects:
                temp_mesh = bmesh.new()

                vert_count_report = 0  

                for obj in selected_objects:

                    print("------------------")
                    print(obj.name)

                    # We are doing the remove doubles through bmesh
                    # because it's twice faster than through ops.
                    temp_mesh.from_mesh(obj.data)
                    obj_initial_vert_count = len(temp_mesh.verts)  # For reporting
                    bmesh.ops.remove_doubles(temp_mesh, verts= temp_mesh.verts, dist= 1e-06)
                    temp_mesh.to_mesh(obj.data)
                    obj.data.update()
                    obj_final_vert_count = len(temp_mesh.verts)  # For reporting
                    temp_mesh.clear()

                    obj_merged_vertices = obj_initial_vert_count - obj_final_vert_count
                    print("Merged vertices = " + str(obj_merged_vertices))
                    vert_count_report += obj_merged_vertices

                    # The following ops aren't supported by bmesh, so,
                    # we have to do them through bpy.ops, turning each
                    # object in the loop into an Active one.

                    # current way to force an object to be Active:
                    # it's based on the current View Layer. See:
                    # https://docs.blender.org/manual/en/latest/scene_layout/view_layers/introduction.html#outliner
                    # for possible undesired implications.

                    # Use Autosmooth just in case
                    bpy.data.objects[obj.name].data.use_auto_smooth = True

                    # Just in case, we do only the Normals averaging if some vertex
                    # was merged (I don't know if this calculation can accumulate
                    # imprecisions if executed too often, so…)
                    if obj_merged_vertices > 0:
                        bpy.context.view_layer.objects.active = obj

                        bpy.ops.object.mode_set(mode = "EDIT")
                        bpy.ops.mesh.select_all(action="SELECT")

                        # Normals averaging for correct looks. Merits some discussion.
                        result = bpy.ops.mesh.average_normals(average_type='FACE_AREA')
                        print("Average face area's normals " + str(result))
                        result = bpy.ops.object.mode_set(mode = "OBJECT")
                        print("Set to Object Mode " + str(result))
                        self.report({'INFO'}, str(vert_count_report) + " Vertices merged. All affected objects were Auto-Smoothed and their Normals averaged by face area.")
                    else:
                        self.report({'INFO'}, "0 Vertices merged")

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