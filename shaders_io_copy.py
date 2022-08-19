import bpy


class ZGSWTOR_OT_shaders_io_copy(bpy.types.Operator):
    bl_idname = "zgswtor.shaders_io_copy"
    bl_label = "ZG Copy data of Shaders' sockets with the same name"
    bl_description = "Copies data between sockets with matching names\nof a pair of selected Nodes.\n\n• Requires a selection of two nodes.\n• The Active node receives the data.\n• Inputs and outputs set to hidden values\n   or starting with a dash are omitted"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls,context):
        if len(bpy.context.selected_nodes) == 2:
            return True
        else:
            return False


    # Property for the UI buttons to call different actions.
    # See: https://b3d.interplanety.org/en/calling-functions-by-pressing-buttons-in-blender-custom-ui/
    action: bpy.props.EnumProperty(
        name="Copy Type",
        items=[
            ("ng_to_ng", "Nodegroup To Active Nodegroup", "Nodegroup To Active Nodegroup"),
            ("ng_to_st", "Nodegroup To Settings Group", "Nodegroup To Settings Group"),
            ("st_to_ng", "Settings Group To Nodegroup", "Settings Group To Nodegroup"),
            ],
        options={'HIDDEN'}
        )




    def execute(self, context):
        bpy.context.window.cursor_set("WAIT")

        mat_node_tree = bpy.data.materials[context.material.name].node_tree
        mat_nodes = mat_node_tree.nodes
        mat_links = mat_node_tree.links


        destination = context.active_node
        for node in context.selected_nodes:
            if node != destination:
                origin = node
                break

        for output in origin.outputs:
            for input in destination.inputs:
                if (input.name == output.name
                    and input.name[0] != "—"
                    and input.hide_value == False and output.hide_value == False
                ):
                    input.default_value = output.default_value

        bpy.context.window.cursor_set("DEFAULT")
        return {"FINISHED"}


# UI is set in ui.py


# ------------------------------------------------------------------
# Registrations

def register():    
    bpy.utils.register_class(ZGSWTOR_OT_shaders_io_copy)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_shaders_io_copy)

if __name__ == "__main__":
    register()