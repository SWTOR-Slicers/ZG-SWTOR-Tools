import bpy
import os
from pathlib import Path


def merge_material_nodes(source_material_name, destination_material_name):
    # Get the source and destination materials
    source_material = bpy.data.materials.get(source_material_name)
    destination_material = bpy.data.materials.get(destination_material_name)

    # Check if both materials exist
    if not source_material or not destination_material:
        print("Error: One or both materials do not exist.")
        return

    # Get the node trees of the materials
    source_node_tree = source_material.node_tree
    destination_node_tree = destination_material.node_tree

    # Create a mapping between source and destination nodes
    node_mapping = {}

    # Add nodes to the destination node tree
    for source_node in source_node_tree.nodes:
        new_node = destination_node_tree.nodes.new(type=source_node.bl_idname)
        new_node.name = source_node.name
        new_node.label = source_node.label
        new_node.location = source_node.location
        new_node.hide = source_node.hide
        new_node.use_custom_color = source_node.use_custom_color
        new_node.color = source_node.color


        # Add the mapping between source and destination nodes
        node_mapping[source_node] = new_node

    # Add links to the destination node tree
    for source_link in source_node_tree.links:
        source_socket = node_mapping.get(source_link.from_node).outputs[source_link.from_socket.name]
        destination_socket = node_mapping.get(source_link.to_node).inputs[source_link.to_socket.name]
        destination_node_tree.links.new(source_socket, destination_socket)



# -------------------------------------------------------------
class SWTOR_OT_koda(bpy.types.Operator):
    bl_idname = "swtor.koda"
    bl_label = "Magical Boy Sailor Koda"
    bl_description = "Kodafly"
    bl_options = {'REGISTER', 'UNDO'}


    # Check that there is a selection of objects either
    # in the 3D Viewer or in any Outliner in order to
    # enable the operator.
    @classmethod
    def poll(cls,context):
        true_or_false = False
        if bpy.context.selected_objects and bpy.context.mode == "OBJECT":
            true_or_false = True
        else:
            for window in context.window_manager.windows:
                screen = window.screen
                for area in screen.areas:
                    if area.type == 'OUTLINER':
                        with context.temp_override(window=window, area=area):
                            if context.selected_ids:
                                true_or_false = True
                                break
        return true_or_false


    # Property for the UI buttons to call different actions.
    # See: https://b3d.interplanety.org/en/calling-functions-by-pressing-buttons-in-blender-custom-ui/
    use_selection_only: bpy.props.BoolProperty(
        name="Selection-only",
        description='Applies the material processing to the current selection of objects only',
        default = False,
        options={'HIDDEN'}
        )


    # SWTOR shader types to new shader names
    atroxa_shaders_to_new = {
        "CREATURE": "SWTOR - Creature Shader",
        "EYE"     : "SWTOR - Eye Shader",
        "GARMENT" : "SWTOR - Garment Shader",
        "HAIRC"   : "SWTOR - HairC Shader",
        "SKINB"   : "SWTOR - SkinB Shader",
        "UBER"    : "SWTOR - Uber Shader",
    }




    def execute(self, context):



        # I'm reading the selected objects here because for some reason
        # if I execute the external shaders linker the selection is lost.
        selected_objs = bpy.context.selected_objects

        for obj in selected_objs:
            if obj.type == "MESH":

                print("-------------------------------")
                print("Object:", obj.name)

                for mat_slot in obj.material_slots:
                    mat = mat_slot.material
                    mat_nodes = mat.node_tree.nodes
                    mat_links = mat.node_tree.links

                    if "Material Output" in mat_nodes:
                        output_node = mat_nodes["Material Output"]
                    else:
                        output_node = mat_nodes.new(type="ShaderNodeOutputMaterial")

                    output_node.location = 400, 0


                    if "SWTOR" in mat_nodes:

                        atroxa_node = mat_nodes["SWTOR"]

            
        # Append the baked material template from the auxiliary .blend file inside the Add-on 
        
        # aux_blendfile_name = "CaptnKoda ShadersPacked no samples.blend"
        
        # legacy_materials_blend_filepath = os.path.join(os.path.dirname(__file__), aux_blendfile_name)

        # if Path(legacy_materials_blend_filepath).exists() == False:
        #     self.report({"WARNING"}, "Unable to find the custom SWTOR shaders .blend file inside this Addon's directory.")
        #     return {"CANCELLED"}

        # legacy_materials_path = bpy.path.native_pathsep(legacy_materials_blend_filepath + "/Material")
        
        legacy_materials_path = r"D:\3D SWTOR\SWTOR ASSETS\CaptnKoda ShadersPacked no samples.blend"

        baked_mat_template_name = "BAKED MATERIAL TEMPLATE"
        if baked_mat_template_name not in bpy.data.materials:
            try:
                bpy.ops.wm.append(
                filename=baked_mat_template_name,
                directory=legacy_materials_path,
                do_reuse_local_id=True,  # This seems to be failing, hence the checking
                set_fake=True,
                link=False,
                )
            except:
                self.report({"WARNING"}, "Unable to find the " + baked_mat_template_name + " in the .blend file holding the Legacy SWTOR Materials in this Addon's directory.")
                return {"CANCELLED"}
            
        
        # Append the baked material template node tree's nodes
        # to the existing Legacy SWTOR materials in the project
        
        merge_material_nodes(baked_mat_template_name, mat.name)
        
                
        
        self.report({'INFO'}, "Conversion finished")
        return {"FINISHED"}
                   
                   

# -------------------------------------------------------------
# Registrations

def register():
    bpy.utils.register_class(SWTOR_OT_koda)



def unregister():
    bpy.utils.unregister_class(SWTOR_OT_koda)

if __name__ == "__main__":
    register()