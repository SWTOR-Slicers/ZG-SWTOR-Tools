import bpy


class ZGSWTOR_OT_swtor_smart_materials_dumbifier(bpy.types.Operator):

    bl_label = "SWTOR Tools"
    bl_idname = "zgswtor.swtor_smart_materials_dumbifier"
    bl_description = 'Converts Darth Atroxa\'s smart modern SWTOR shaders to "dumb",\ntextures outside-type ones for easier customization.\nRequires the modern .gr2 add-on to be active\nduring the conversion'
    bl_options = {'REGISTER', 'UNDO'}

    # ------------------------------------------------------------------
    # Check that there is a selection of objects (greys-out the UI button otherwise)
    
    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects:
            return True
        else:
            return False


    # SWTOR shader TYPES to new shader names
    
    shader_renames = {
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
    swtor_txtr_maps_names = [
        "diffuseMap",
        "rotationMap",
        "glossMap",
        "paletteMap",
        "paletteMaskMap",
        "ageMap",
        "complexionMap",
        "facepaintMap",
        "directionMap",
        ]

    # Simple factors or RGB values
    swtor_shdr_params_names = [
        "palette1_hue",
        "palette1_saturation",
        "palette1_brightness",
        "palette1_contrast",
        "palette1_specular",
        "palette1_metallic_specular",
        "palette2_hue",
        "palette2_saturation",
        "palette2_brightness",
        "palette2_contrast",
        "palette2_specular",
        "palette2_metallic_specular",
        "flesh_brightness",
        "flush_tone"
    ]


    print("\n\n\n\n\n\n\n\n\n\n")
 
    def execute(self, context):
        bpy.context.window.cursor_set("DEFAULT")

        zgswtor_shaders_path = "/Volumes/RECURSOS/3D SWTOR/SWTOR SHADERS/New SWTOR Custom Shaders.blend"

        # I'm reading the selected objects here because for some reason
        # if I execute the external shaders linker the selection is lost.
        # Maybe because it works in a different context?
        selected_objs = bpy.context.selected_objects


        if "SWTOR - Creature Shader" not in bpy.data.node_groups:
            try:
                bpy.ops.zgswtor.external_shaders_linker()
            except:
                self.report({"WARNING"}, "External Shaders Linker not found")
                return {"CANCELLED"}

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

                        # Safety check
                        if derived not in self.shader_renames.keys():
                            continue


                        # Add SWTOR Nodegroup
                        new_node = mat_nodes.new(type="ShaderNodeGroup")
                        new_node.node_tree = bpy.data.node_groups[self.shader_renames[derived]]

                        new_node.location = 0, 0
                        new_node.width = 250
                        new_node.name = new_node.label = self.shader_renames[derived]

                        # Link it to Material Output Node
                        mat_links.new(output_node.inputs[0],new_node.outputs[0])

                        # Create a dict of the new shader' inputs' names and positions
                        new_node_input_names = {}
                        for pos in range(len(new_node.inputs)):
                            input_names = new_node.inputs[pos].name
                            new_node_input_names[input_names] = pos
                                                
                        #### Cycle through Standard SWTOR input names to read and copy their values.
                        # It tests which inputs the new Nodegroup has and copies Atroxa's
                        # inputs' values obtained thorugh its methods. As Atroxa's Nodegroup
                        # doesn't vary the number of properties and methods per Derived type,
                        # I use the new Nodegroup's inputs as reference. That's why the input
                        # names' massaging to facilitate looking them up, which maybe it's a
                        # bit too smart and a correspondence table would be simpler if slower.
                        #
                        # EDIT: I just discovered node inputs/outputs CAN be selected by name.
                        # So, all this will be simplified later on.

                        for swtor_shdr_param_name in self.swtor_shdr_params_names:
                            new_node_name = swtor_shdr_param_name.title().replace('_', ' ')
                            new_node_input_position = new_node_input_names.get(new_node_name)
                            if new_node_input_position != None:
                                new_value = atroxa_node[swtor_shdr_param_name] 
                                print(new_node_name, new_value, "\n")
                                new_node.inputs[new_node_input_position].default_value = atroxa_node[swtor_shdr_param_name]

                        #### Cycle through standard SWTOR texturemap names to add them and link them.
                        # It tests which inputs the new Nodegroup has and copies Atroxa's
                        # inputs' values obtained thorugh its methods. As Atroxa's Nodegroup
                        # doesn't vary the number of properties and methods per Derived type,
                        # I use the new Nodegroup's inputs as reference. I couldn't make the
                        # lookup smart enough, so, I loop through
                        #
                        # EDIT: I just discovered node inputs/outputs CAN be selected by name.
                        # So, all this will be simplified later on.
                        
                        for swtor_txtr_map_name in self.swtor_txtr_maps_names:
                            for name in new_node_input_names:
                                if (swtor_txtr_map_name.lower() + " color") in name.lower():
                                    txtr_node_name = name.replace(" Color","")
                                    new_node_input_position = new_node_input_names[name]
                                    print(name, new_node_input_position, "\n")
                                    
                                    if new_node_input_position != None:
                                        # Create texture node if it doesn't previously exist
                                        if not txtr_node_name in mat_nodes:
                                            txtr_node = mat_nodes.new(type='ShaderNodeTexImage')
                                            txtr_node.name = txtr_node.label = txtr_node_name
                                        else:
                                            txtr_node = mat_nodes[txtr_node_name]

                                        # Adjust position, size and other details
                                        txtr_node.location = (-350 - new_node_input_position * 16, -150 - new_node_input_position * 20)
                                        txtr_node.width = txtr_node.width_hidden = 300
                                        txtr_node.hide = True

                                        #link it to the SWTOR nodegroup (Color and Alpha)
                                        mat_links.new(txtr_node.outputs[0], new_node.inputs[new_node_input_position])
                                        mat_links.new(txtr_node.outputs[1], new_node.inputs[new_node_input_position+1])

                                        # If the texturemap node has no assigned image, mute it
                                        if atroxa_node[swtor_txtr_map_name]:
                                            txtr_node.image = atroxa_node[swtor_txtr_map_name]
                                        else:
                                            txtr_node.mute = True

                                        # Create the links for feeding a DirectionMap with
                                        # the Specular Lookup calculated inside the Nodegroup
                                        if name == "DirectionMap Color":
                                            
                                            rerouter_1 = mat_nodes.new(type="NodeReroute")
                                            rerouter_1.location = 350, -250
                                            rerouter_2 = mat_nodes.new(type="NodeReroute")
                                            rerouter_2.location = 350, -50 - len(new_node.inputs)*30
                                            rerouter_3 = mat_nodes.new(type="NodeReroute")
                                            rerouter_3.location = -650, -50 - len(new_node.inputs)*30
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
    bpy.utils.register_class(ZGSWTOR_OT_swtor_smart_materials_dumbifier)

def unregister():    
    bpy.utils.unregister_class(ZGSWTOR_OT_swtor_smart_materials_dumbifier)

if __name__ == "__main__":
    register()