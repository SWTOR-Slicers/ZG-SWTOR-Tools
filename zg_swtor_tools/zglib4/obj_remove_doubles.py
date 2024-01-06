import bpy
import bmesh


# Main

class ZGSWTOR_OT_remove_doubles(bpy.types.Operator):
    bl_idname = "zgswtor.remove_doubles"
    bl_label = "ZG Remove Doubles"
    bl_description = "Removes double vertices (does a Merge by Distance\nin selected objects using a threshold of 0.0000001),\nand applies a Normals > Average > Face Area.\n\n• Requires a selection of objects.\n• Processes each selected object individually."
    bl_options = {'REGISTER', "UNDO"}

    # Check that there is a selection of objects and that we are in Object mode
    # (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects and bpy.context.mode == "OBJECT":
            there_are_meshes = False
            for obj in bpy.context.selected_objects:
                if obj.type == "MESH":
                    there_are_meshes = True
                    break
            return there_are_meshes
        else:
            return False


    def execute(self, context):

        context.window.cursor_set("WAIT")  # Show wait cursor icon

        print("---------------------")
        print("MERGE DOUBLE VERTICES")
        print("---------------------")
        print()

        # After some research, Crunch (AKA UnconventionalError) has changed the code to become
        # bpy.ops-based instead of BMESH based, as that allows for using a type of normals processing
        # that better preserves sharp edges with just an additional parameter.
        vert_count_report = 0
        copy_of_selected_objects = list(context.selected_objects)
        bpy.ops.object.select_all(action='DESELECT')
        for obj in copy_of_selected_objects:
            if obj.type == 'MESH':
                print(obj.name)
                obj_initial_vert_count = len(obj.data.vertices)
                context.view_layer.objects.active = obj
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles(threshold=1e-06, use_sharp_edge_from_normals=True)
                bpy.ops.object.editmode_toggle()

                # Calculate the vertex count difference to report how many
                # vertices were merged.
                # Edit mode doesn't update that data until exiting the mode, so,
                # load the object's edit-mode data into the object data
                # via this updating method. See:
                # https://blender.stackexchange.com/questions/8762/vertex-count-appears-incorrect-after-removing-doubles
                # context.object.update_from_editmode()
                context.view_layer.objects.active = None
                vert_count_report += len(obj.data.vertices) - obj_initial_vert_count
                print()

        print("\nDONE!")
        
        for obj in copy_of_selected_objects:
           obj.select_set(True)
        
        self.report({'INFO'}, str(-vert_count_report) + " Vertices merged.")

        bpy.context.window.cursor_set("DEFAULT")  # Show normal cursor icon
        return {"FINISHED"}


# UI is set in ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_remove_doubles)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_remove_doubles)

if __name__ == "__main__":
    register()