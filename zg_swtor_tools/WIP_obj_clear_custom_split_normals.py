import bpy
import bmesh


# Main

class ZGSWTOR_OT_clear_custom_split_normals(bpy.types.Operator):
    bl_idname = "zgswtor.clear_custom_split_normals"
    bl_label = "ZG clear_custom_split_normals"
    bl_description = "Applies the 'clear_custom_split_normals' operator to the selected objects or to all objects."
    bl_options = {'REGISTER', "UNDO"}


    @classmethod
    def poll(cls,context):
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

        print("--------------------------")
        print("CLEAR CUSTOM SPLIT NORMALS")
        print("--------------------------")
        print()

        processed_objects_count = 0

        if self.use_selection_only == True:
            copy_of_selected_objects = context.selected_objects
        else:
            copy_of_selected_objects = [obj for obj in bpy.data.objects if obj.type == "MESH"]
            if not copy_of_selected_objects:
                bpy.context.window.cursor_set("DEFAULT")  # Show normal cursor icon
                self.report({"WARNING"}, "There are no mesh objects to process in this .blend project.")
                return {"CANCELLED"}

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
                processed_objects_count += len(obj.data.vertices) - obj_initial_vert_count
                print()

        print("\nDONE!")
        
        for obj in copy_of_selected_objects:
           obj.select_set(True)
        
        self.report({'INFO'}, str(-processed_objects_count) + " Vertices merged.")

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