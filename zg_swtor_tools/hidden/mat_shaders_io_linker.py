import bpy


class ZGSWTOR_OT_shaders_io_linker(bpy.types.Operator):
    bl_idname = "zgswtor.shaders_io_linker"
    bl_label = "ZG Link Shaders' sockets with the same name"
    bl_description = "Links sockets with matching names\nof a pair of selected Nodes.\n\n• Requires a selection of two nodes.\n• The Active node receives the links.\n• Inputs and outputs set to hidden values\n   or starting with a dash are omitted"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls,context):
        if len(bpy.context.selected_nodes) == 2:
            return True
        else:
            return False


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
                    mat_links.new(output,input)

        bpy.context.window.cursor_set("DEFAULT")
        return {"FINISHED"}


# UI is set in ui.py


# ------------------------------------------------------------------
# Registrations

def register():    
    bpy.utils.register_class(ZGSWTOR_OT_shaders_io_linker)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_shaders_io_linker)

if __name__ == "__main__":
    register()