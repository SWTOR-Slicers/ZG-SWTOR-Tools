import bpy

from .utils.addon_checks import requirements_checks

checks = requirements_checks()
blender_version = checks["blender_version"]


def selected_outliner_items(context):
    '''
    Returns selected outliner items
    as a list of RNA objects (in the
    Python sense) including Collections
    '''

    items_in_selection = []

    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'OUTLINER':
                with context.temp_override(window=window, area=area):
                    for item in context.selected_ids:
                        items_in_selection.append(item)
                                
    return items_in_selection



class ZGSWTOR_OT_customize_swtor_shaders(bpy.types.Operator):

    bl_label = "ZG Customize SWTOR Shaders"
    bl_idname = "zgswtor.customize_swtor_shaders"
    bl_description = 'Converts the .gr2 Add-on\'s smart modern SWTOR shaders to "dumb",\ntextures outside-type ones for easier customization.\n\n• Requires the modern .gr2 add-on to be enabled during the conversion\n• Requires setting a path to an appropriate .blend file holding\n   customizable SWTOR shaders in this Addon\'s Preferences'
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls,context):
        checks = requirements_checks()
        if bpy.data.materials and bpy.data.objects and checks['gr2']:
            return True
        return False


    # Properties

    preserve_atroxa_bool: bpy.props.BoolProperty(
        name="Preserve original shaders",
        description='Keep the original SWTOR shaders, disconnected from the Output Node,\nso that comparing or reverting to them is possible',
        default = True,
        options={'HIDDEN'}
        )

    # Property for the UI buttons to call different actions.
    # See: https://b3d.interplanety.org/en/calling-functions-by-pressing-buttons-in-blender-custom-ui/
    use_selection_only: bpy.props.BoolProperty(
        name="Selection-only",
        description='Applies the shaders conversion to the current selection of objects only',
        default = False,
        options={'HIDDEN'}
        )

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

 
    def execute(self, context):
        bpy.context.window.cursor_set("DEFAULT")


        checks = requirements_checks()
        blender_version = checks["blender_version"]


        # I'm reading the selected objects here because for some reason
        # if I execute the external shaders linker the selection is lost.
        if self.use_selection_only:
            selected_objs = context.selected_objects
        else:
            selected_objs = bpy.data.objects

        # Call external shaders linker/appender operator
        shaders_lib_filepath = bpy.context.preferences.addons["zg_swtor_tools"].preferences.swtor_custom_shaders_blendfile_path
        
        open_blend_filepath = bpy.data.filepath

        if open_blend_filepath != shaders_lib_filepath:
            bpy.ops.zgswtor.add_custom_external_swtor_shaders(link = context.scene.use_linking_bool)

        # ----------------------------------------------------
        
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

                        # Set material's alpha, shadow and backface culling settings.
                        # Blend Mode to CLIP as a minimum for the extra
                        # transparency setting to work.
                        
                        if blender_version < 4.2:
                            mat.blend_method = "CLIP"
                            mat.alpha_threshold = atroxa_node.alpha_test_value
                            if mat.blend_method == 'HASHED':
                                mat.shadow_method = 'HASHED'
                            else:
                                mat.shadow_method = 'CLIP'
                        else:
                            # "CLIP" and threshold have to be implemented as nodes
                            mat.surface_render_method = 'DITHERED'
                        mat.use_backface_culling = False


                        # Start conversion to new shader
                        derived = atroxa_node.derived

                        # Check for new shader existence to avoid duplicates 
                        if self.atroxa_shaders_to_new[derived] in mat_nodes:
                            continue

                        # Add SWTOR Nodegroup
                        new_node = mat_nodes.new(type="ShaderNodeGroup")
                        new_node.node_tree = bpy.data.node_groups[self.atroxa_shaders_to_new[derived]]

                        new_node.location = 0, 0
                        new_node.width = 320
                        new_node.name = new_node.label = self.atroxa_shaders_to_new[derived]
                        nodes_io_y_incrmt = 21
                        nodes_io_y_offset = -len(new_node.outputs) * nodes_io_y_incrmt - 76


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
                                    if new_node_input_name not in mat_nodes:
                                        txtr_node = mat_nodes.new(type='ShaderNodeTexImage')
                                        txtr_node.name = txtr_node.label = new_node_input_name
                                    else:
                                        txtr_node = mat_nodes[new_node_input_name]

                                    
                                    txtr_node.location = (-350 - new_node_input_index * 16,
                                                          nodes_io_y_offset - new_node_input_index * nodes_io_y_incrmt)
                                    # RotationMap's repositioning to accomodate feeding DirectionMaps' normals
                                    if derived in ['CREATURE', 'SKINB', 'HAIRC'] and "rotation" in txtr_node.name.lower():
                                        txtr_node.location[0] = txtr_node.location[0] - 360
                                        rotMap_node = txtr_node
                                    
                                    txtr_node.width = 300.0
                                    if blender_version < 4:
                                        txtr_node.width_hidden = 300.0
                                    txtr_node.hide = True

                                    #link it to the SWTOR nodegroup (Color and Alpha)
                                    mat_links.new(txtr_node.outputs[0], new_node.inputs[new_node_input_index])
                                    mat_links.new(txtr_node.outputs[1], new_node.inputs[new_node_input_index+1])

                                    # Assign image to the texturemap node.
                                    # If it has no assigned image, mute the node.
                                    texture_image = getattr(atroxa_node, self.new_txmaps_to_atroxa[new_node_input_name], None)
                                    if texture_image:
                                        txtr_node.image = texture_image
                                    else:
                                        txtr_node.mute = True

                                    # If the texture node was a DirectionMap, add a normals converter node
                                    # and related links to RotationMap and DirectionMap.
                                    if new_node_input_name == "DirectionMap":
                                        dirMap_node = txtr_node
                                        # Add SWTOR Nodegroup
                                        normals_convert_node = mat_nodes.new(type='ShaderNodeGroup')
                                        normals_convert_node.node_tree = bpy.data.node_groups["SW Aux - GetSpecularLookupFromSwizzledTexture"]

                                        normals_convert_node.width = 150.0
                                        normals_convert_node.name = "SW Aux - GetSpecularFromSwizzledTexture"
                                        normals_convert_node.location = txtr_node.location[0] - 180.0, txtr_node.location[1]
                                        normals_convert_node.hide = True
                                        normals_convert_node.use_custom_color = True
                                        normals_convert_node.color = (0.0, 0.0, 0.0)

                                        mat_links.new(rotMap_node.outputs[0], normals_convert_node.inputs[0])
                                        mat_links.new(rotMap_node.outputs[1], normals_convert_node.inputs[1])

                                        mat_links.new(normals_convert_node.outputs[0], dirMap_node.inputs[0])
                                        
                                        
                        if context.scene.preserve_atroxa_bool:
                            # Reposition smart shader out of the way
                            atroxa_node.location = 600, 0
                        else:
                            mat_nodes = mat_nodes.remove(atroxa_node)
    
        return {"FINISHED"}


# UI is set in addon_ui.py


# ------------------------------------------------------------------
# Registrations

def register():
    
    bpy.types.Scene.preserve_atroxa_bool = bpy.props.BoolProperty(
        name="Preserve original shaders",
        description='Keep the original SWTOR shaders, disconnected from the Output Node,\nso that comparing or reverting to them is possible',
        default = True,
    )
    # bpy.types.Scene.css_use_selection_only = bpy.props.BoolProperty(
    #     description='Applies the shaders conversion to the current selection of objects only',
    #     default = False
    # )
    bpy.utils.register_class(ZGSWTOR_OT_customize_swtor_shaders)

def unregister():
    del bpy.types.Scene.preserve_atroxa_bool
    # del bpy.types.Scene.css_use_selection_only

    
    bpy.utils.unregister_class(ZGSWTOR_OT_customize_swtor_shaders)

if __name__ == "__main__":
    register()