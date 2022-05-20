import bpy
import os
from pathlib import Path
from bpy.app.handlers import persistent

@persistent
def handler_new_scene(scene):
    # Check that we aren't editing the custom shaders template file
    # to prevent from appending/linking the shaders to itself
    # and set a prop to control the UI's related widgets
    
    new_shaders_filepath = bpy.context.preferences.addons[__package__].preferences.swtor_custom_shaders_blendfile_path
    
    open_blend_file = bpy.data.filepath
    
    bpy.types.Scene.blendfile_is_template_bool = new_shaders_filepath != open_blend_file

    print("-----------")
    print(bpy.types.Scene.blendfile_is_template_bool)
    print("-----------")    


class ZGSWTOR_OT_customize_swtor_shaders(bpy.types.Operator):

    bl_label = "SWTOR Tools"
    bl_idname = "zgswtor.customize_swtor_shaders"
    bl_description = 'Converts Darth Atroxa\'s smart modern SWTOR shaders to "dumb",\ntextures outside-type ones for easier customization.\n\n• Requires the modern .gr2 add-on to be enabled during the conversion'
    bl_options = {'REGISTER', 'UNDO'}

    # ------------------------------------------------------------------
    # Check that there is a selection of objects (greys-out the UI button otherwise)
    
    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects:
            return True
        else:
            return False


    # Properties

    # preserve_atroxa_bool: bpy.props.BoolProperty(
    #     name="Preserve original shaders",
    #     description='Keep the original SWTOR shader, unconnected',
    #     default = True,
    #     options={'HIDDEN'}
    #     )


    # Some lists and dicts:
    
    # SWTOR shader types to new shader names
    atroxa_shaders_to_new = {
        "CREATURE": "SWTOR - Creature Shader",
        "EYE"     : "SWTOR - Eye Shader",
        "GARMENT" : "SWTOR - Garment Shader",
        "HAIRC"   : "SWTOR - HairC Shader",
        "SKINB"   : "SWTOR - SkinB Shader",
        "UBER"    : "SWTOR - Uber Shader",
    }

    # All possible shader parameters in all of Atroxa's shaders
    # that also are accesible as methods. By checking that those
    # methods exist in each material's Atroxa shader, the parameters
    # can be copied in an "if it exists then" manner instead of
    # custom-coding each shader case separately.
    # The downside is that it requires Atroxa's .gr2 add-on to be
    # enabled for that to work, but the complexity of this code
    # would shoot up otherwise.

    # Common material settings
    mat_types = [
        "derived",
        "alpha_mode",
        "alpha_test_value",
        ]

    # Texture maps
    new_txmaps_to_atroxa = {
        "_d DiffuseMap"     : "diffuseMap",
        "_n RotationMap"    : "rotationMap",
        "_s GlossMap"       : "glossMap",
        "_h PaletteMap"     : "paletteMap",
        "_m PaletteMaskMap" : "paletteMaskMap",
        "AgeMap"            : "ageMap",
        "ComplexionMap"     : "complexionMap",
        "FacepaintMap"      : "facepaintMap",
        "DirectionMap"      : "directionMap",
        }


    # Simple factors or RGB values
    new_params_to_atroxa = {
        "Palette1 Hue"               : "palette1_hue",
        "Palette1 Saturation"        : "palette1_saturation",
        "Palette1 Brightness"        : "palette1_brightness",
        "Palette1 Contrast"          : "palette1_contrast",
        "Palette1 Specular"          : "palette1_specular",
        "Palette1 Metallic Specular" : "palette1_metallic_specular",
        "Palette2 Hue"               : "palette2_hue",
        "Palette2 Saturation"        : "palette2_saturation",
        "Palette2 Brightness"        : "palette2_brightness",
        "Palette2 Contrast"          : "palette2_contrast",
        "Palette2 Specular"          : "palette2_specular",
        "Palette2 Metallic Specular" : "palette2_metallic_specular",
        "Flesh Brightness"           : "flesh_brightness",
        "Flush Tone"                 : "flush_tone"
        }

    print("\n\n\n\n\n\n\n\n\n\n")
 
    def execute(self, context):
        print(bpy.types.Scene.blendfile_is_template_bool)
        bpy.context.window.cursor_set("DEFAULT")

        # I'm reading the selected objects here because for some reason
        # if I execute the external shaders linker the selection is lost.
        selected_objs = bpy.context.selected_objects

        # Check that we aren't editing the custom shaders template file
        # to prevent from appending/linking the shaders to itself
        new_shaders_filepath = bpy.context.preferences.addons[__package__].preferences.swtor_custom_shaders_blendfile_path

        open_blend_file = bpy.data.filepath
        
        bpy.types.Scene.blendfile_is_template_bool = new_shaders_filepath != open_blend_file





        # ----------------------------------------------------
        
        for obj in selected_objs:
            if obj.type == "MESH":

                print("-------------------------------")
                print("Object:", obj.name)

                for mat_slot in obj.material_slots:
                    mat = mat_slot.material
                    mat_nodes = mat.node_tree.nodes
                    mat_links = mat.node_tree.links
                    
                    output_node = mat_nodes["Material Output"]
                    output_node.location = 400, 0


                    if "SWTOR" in mat_nodes:
                        atroxa_node = mat_nodes["SWTOR"]
                        atroxa_node.location = 600, 0

                        # Start working on the material

                        derived = atroxa_node.derived
                        print(derived)

                        # Check for new shader existence to avoid duplicates 
                        if self.atroxa_shaders_to_new[derived] in mat_nodes:
                            continue


                        # Add SWTOR Nodegroup
                        new_node = mat_nodes.new(type="ShaderNodeGroup")
                        new_node.node_tree = bpy.data.node_groups[self.atroxa_shaders_to_new[derived]]

                        new_node.location = 0, 0
                        new_node.width = 250
                        new_node.name = new_node.label = self.atroxa_shaders_to_new[derived]
                        txtr_nodes_y_offset = -len(new_node.inputs) * 16 - 46

                        # Link it to Material Output Node
                        mat_links.new(output_node.inputs[0],new_node.outputs[0])

                                                
                        # Copy Atroxa node values to new node,
                        # creating texturemap nodes as needed

                        new_node_inputs_enum = enumerate(new_node.inputs)
                        for new_node_input_index, new_node_input in new_node_inputs_enum:
                            
                            new_node_input_name = new_node_input.name
                            if new_node_input_name in self.new_params_to_atroxa:  # Non-texturemap data
                                new_node_input.default_value= getattr(atroxa_node, self.new_params_to_atroxa[new_node_input.name])
                            else:
                                new_node_input_name = new_node_input_name.replace(" Color", "")  # texturemap data 
                                if new_node_input_name in self.new_txmaps_to_atroxa:

                                    # Create texture node if it doesn't previously exist
                                    # Adjust position, size and other details
                                    if not new_node_input_name in mat_nodes:
                                        txtr_node = mat_nodes.new(type='ShaderNodeTexImage')
                                        txtr_node.name = txtr_node.label = new_node_input_name
                                    else:
                                        txtr_node = mat_nodes[new_node_input_name]

                                    
                                    txtr_node.location = (-350 - new_node_input_index * 16, txtr_nodes_y_offset - new_node_input_index * 21)
                                    txtr_node.width = txtr_node.width_hidden = 300
                                    txtr_node.hide = True

                                    #link it to the SWTOR nodegroup (Color and Alpha)
                                    mat_links.new(txtr_node.outputs[0], new_node.inputs[new_node_input_index])
                                    mat_links.new(txtr_node.outputs[1], new_node.inputs[new_node_input_index+1])

                                    # Assign image to the texturemap node.
                                    # If it has no assigned image, mute the node.
                                    if atroxa_node[self.new_txmaps_to_atroxa[new_node_input_name] ]:
                                        txtr_node.image = atroxa_node[self.new_txmaps_to_atroxa[new_node_input_name] ]
                                    else:
                                        txtr_node.mute = True

                                    # Create the links for feeding a DirectionMap with
                                    # the Specular Lookup calculated inside the Nodegroup
                                    if new_node_input_name == "DirectionMap Color":

                                        bottom_y = txtr_nodes_y_offset - len(new_node.inputs)*21 - 50
                                        
                                        rerouter_1 = mat_nodes.new(type="NodeReroute")
                                        rerouter_1.location = 350, -250
                                        rerouter_2 = mat_nodes.new(type="NodeReroute")
                                        rerouter_2.location = 350, bottom_y
                                        rerouter_3 = mat_nodes.new(type="NodeReroute")
                                        rerouter_3.location = -650, bottom_y
                                        rerouter_4 = mat_nodes.new(type="NodeReroute")
                                        rerouter_4.location = -650, txtr_node.location[1]-10
                                        
                                        mat_links.new(new_node.outputs["Specular Lookup AUX"], rerouter_1.inputs[0])
                                        mat_links.new(rerouter_1.outputs[0], rerouter_2.inputs[0])
                                        mat_links.new(rerouter_2.outputs[0], rerouter_3.inputs[0])
                                        mat_links.new(rerouter_3.outputs[0], rerouter_4.inputs[0])
                                        mat_links.new(rerouter_4.outputs[0], txtr_node.inputs[0])

        return {"FINISHED"}


# UI is set in ui.py


# ------------------------------------------------------------------
# Registrations

def register():
    bpy.app.handlers.load_pre.append(handler_new_scene)
    
    bpy.types.Scene.preserve_atroxa_bool = bpy.props.BoolProperty(
        name="Preserve original shaders",
        description='Keep the original SWTOR shader, unconnected',
        default = True,
    )
    
    bpy.utils.register_class(ZGSWTOR_OT_customize_swtor_shaders)

def unregister():
    del bpy.types.Scene.preserve_atroxa_bool
    
    bpy.utils.unregister_class(ZGSWTOR_OT_customize_swtor_shaders)

if __name__ == "__main__":
    register()