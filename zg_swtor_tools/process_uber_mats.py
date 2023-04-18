# This code is horrible. it just happens to work. Mostly.
# PEP-8 what's that. Read my Indent Rollercoaster Model manifest!
# So, without further ado…

import bpy
import pathlib
import xml.etree.ElementTree as ET
import addon_utils


class ZGSWTOR_OT_process_uber_mats(bpy.types.Operator):

    bl_label = "ZG Process Uber Materials"
    bl_idname = "zgswtor.process_uber_mats"
    bl_description = "Scans for Uber materials in selected objects and places in them\nUber shaders and their associated textures.\n\n• Requires a selection of objects.\n• Requires an enabled SWTOR .gr2 Importer Add-on."
    bl_options = {'REGISTER', 'UNDO'}

    # ------------------------------------------------------------------
    # Check that there is a selection of objects (greys-out the UI button otherwise)
    
    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects:
            return True
        else:
            return False

    # ------------------------------------------------------------------
    # Define some checkbox-type properties
    # (they'll interact with scene-level properties
    # used in the UI panel)
    
    use_overwrite_bool: bpy.props.BoolProperty(
        name="Overwrite Uber materials",
        description='Processes the selected objects Uber materials even if they have an Uber shader already, effectively "regenerating" those ones',
        default = False,
        options={'HIDDEN'}
        )

    use_collect_colliders_bool: bpy.props.BoolProperty(
        name="Collect Collider objects",
        description='Collects all objects with an "util_collision_hidden" material in a Collection named "Collider Objects"',
        default = True,
        options={'HIDDEN'}
        )



    # Register some properties in the Material class for helping
    # diagnose issues
    bpy.types.Material.swtor_derived = bpy.props.StringProperty()


    # ------------------------------------------------------------------
    def execute(self, context):

        bpy.context.window.cursor_set("WAIT")
        
        # Make operator properties equal to UI properties
        self.use_collect_colliders_bool = bpy.context.scene.use_collect_colliders_bool
        
        self.use_overwrite_bool = bpy.context.scene.use_overwrite_bool


        selected_objects = bpy.context.selected_objects
        if not selected_objects:
            return {"CANCELLED"}

        # Create nodegroup InanimatedUV for provisional Holo material
        create_InanimatedUV_nodegroup()


        # --------------------------------------------------------------
        # Get the extracted SWTOR assets' "resources" folder from the add-on's preferences. 
        swtor_resources_path = bpy.context.preferences.addons[__package__].preferences.swtor_resources_path
        
        swtor_shaders_path = swtor_resources_path + "/art/shaders/materials"

        # Test the existence of the shaders subfolder to validate the SWTOR "resources" folder
        if pathlib.Path(swtor_shaders_path).exists() == False:
            self.report({"WARNING"}, "Unable to find the SWTOR Materials subfolder. Please check this add-on's preferences: either the path to the extracted assets 'resources' folder is incorrect or the resources > art > shaders > materials subfolder is missing.")
            return {"CANCELLED"}

        # --------------------------------------------------------------
        # Check which version of the SWTOR shaders are available
        if addon_utils.check("io_scene_gr2_legacy")[1]:
            if "Uber Shader" in bpy.data.node_groups:
                gr2_addon_legacy = True
            else:
                self.report({"WARNING"}, "Although the Legacy version of the 'io_scene_gr2' add-on is enabled, no Uber Shader exists yet. Please import any arbitrary .gr2 object to produce an Uber Shader template.")
                return {"CANCELLED"}
        elif addon_utils.check("io_scene_gr2")[1]:
            gr2_addon_legacy = False
        else:
            self.report({"WARNING"}, "No version of the 'io_scene_gr2' add-on is enabled.")
            return {"CANCELLED"}

        print()
        print("PROCESSING OF MATERIALS STARTS HERE")
        print()

        # Main loop

        already_processed_mats = []
        collider_objects = []
        
        items_to_process = len(selected_objects)
        items_processed = 0

        for ob in selected_objects:
            if ob.type == "MESH":

                items_processed += 1

                print("-------------------------------------------")
                print(f"{items_processed*100/items_to_process:6.2f} %    Object: {ob.name}")

                is_collision_object = False

                for mat_slot in ob.material_slots:

                    mat = mat_slot.material
                    print("          Material: ", mat.name)

                    if mat.name == "util_collision_hidden":
                        is_collision_object = True
                        collider_objects.append(ob)

                    if (
                        (r"Template: " not in mat.name)
                        and (r"default" not in mat.name)
                        and mat.users
                        and mat.name not in already_processed_mats
                    ):

                        # By looking for the material in the shaders folder we'll inherently
                        # filter out recolorable materials such as skin, eyes or armor already,
                        # finding only the Uber and a few Creature ones.
                        mat_tree_filepath = swtor_shaders_path + "/" + mat.name + ".mat"
                        try:
                            matxml_tree = ET.parse(mat_tree_filepath)
                        except:
                            continue  # disregard and go for the next material
                        matxml_root = matxml_tree.getroot()

                        matxml_derived = matxml_root.find("Derived").text

                        mat.swtor_derived = matxml_derived

                        if matxml_derived == "Glass":
                            matxml_derived = "Uber"
                            transparent_uber = True
                        else:
                            transparent_uber = False

                        if  matxml_derived in ["Uber", "EmissiveOnly", "AnimatedUV", "Glass"]:

                            mat_nodes = mat.node_tree.nodes

                            # Delete Principled Shader if needed
                            if (
                                self.use_overwrite_bool == True
                                or (matxml_derived == "Uber" and not ("Uber Shader" in mat_nodes or "SWTOR" in mat_nodes))
                                or ((matxml_derived == "EmissiveOnly" or matxml_derived == "Glass") and not "_d DiffuseMap" in mat_nodes)
                                or (matxml_derived == "AnimatedUV" and not "_d DiffuseMap" in mat_nodes)
                            ):
                                for node in mat_nodes:
                                    mat_nodes.remove(node)
                            else:
                                continue  # Entirely disregard material and go for the next one

                            # ----------------------------------------------
                            # Basic material settings

                            mat.use_nodes = True  # Redundant?
                            mat.use_fake_user = False


                            # Read and set some basic material attributes
                            mat_AlphaMode = matxml_root.find("AlphaMode").text
                            mat_AlphaTestValue = matxml_root.find("AlphaTestValue").text

                            # Add Output node to emptied material as long as it's not Emissive Only
                            output_node = mat.node_tree.nodes.new('ShaderNodeOutputMaterial')


                            # ----------------------------------------------
                            # Gather texture maps

                            diffusemap_image = None
                            rotationmap_image = None
                            glossmap_image = None

                            temp_image = None
                            temp_imagepath = None

                            matxml_inputs = matxml_root.findall("input")
                            for matxml_input in matxml_inputs:
                                matxml_semantic = matxml_input.find("semantic").text
                                matxml_type = matxml_input.find("type").text
                                matxml_value = matxml_input.find("value").text

                                # Parsing and loading texture maps

                                if matxml_type == "texture":
                                    matxml_value = matxml_value.replace("\\", "/")
                                    temp_imagepath = swtor_resources_path + "/" + matxml_value + ".dds"
                                    try:
                                        temp_image = bpy.data.images.load(temp_imagepath, check_existing=True)
                                        temp_image.colorspace_settings.name = 'Raw'
                                    except:
                                        pass
                                    if matxml_semantic == "DiffuseMap":
                                        diffusemap_image = temp_image
                                    elif matxml_semantic == "RotationMap1":
                                        rotationmap_image = temp_image
                                    elif matxml_semantic == "GlossMap":
                                        glossmap_image = temp_image

                                    # Collision Object check at the texturemap level
                                    if  "util_collision_hidden" in matxml_value and is_collision_object == False:
                                        is_collision_object = True
                                        collider_objects.append(ob)



                            # ----------------------------------------------
                            # Add Uber Shader and connect texturemaps

                            
                            # ----------------------------------------------
                            #   For Legacy version of the shader

                            if gr2_addon_legacy and matxml_derived == "Uber":

                                # Adjust transparency and shadows
                                mat.alpha_threshold = float(mat_AlphaTestValue)

                                if mat_AlphaMode == 'Test':
                                    mat.blend_method = 'CLIP'
                                    mat.shadow_method = 'CLIP'
                                elif mat_AlphaMode == 'Full' or mat_AlphaMode == 'MultipassFull' or mat_AlphaMode == 'Add':
                                    mat_AlphaMode == 'Blend'
                                    mat.blend_method = 'BLEND'
                                    mat.shadow_method = 'HASHED'
                                else:
                                    mat_AlphaMode == 'None'
                                    mat.blend_method = 'OPAQUE'
                                    mat.shadow_method = 'NONE'

                                # Set Backface Culling
                                mat.use_backface_culling = False


                                # Add Uber Shader and link it to Output node
                                uber_nodegroup = mat_nodes.new(type="ShaderNodeGroup")
                                uber_nodegroup.node_tree = bpy.data.node_groups["Uber Shader"]
                                
                                uber_nodegroup.location = 0, 0
                                uber_nodegroup.width = 300
                                uber_nodegroup.width_hidden = 300
                                uber_nodegroup.name = "Uber Shader"
                                uber_nodegroup.label = "Uber Shader"

                                output_node.location = 400, 0

                                links = mat.node_tree.links

                                links.new(output_node.inputs[0],uber_nodegroup.outputs[0])


                                # Add Diffuse node and link it to Uber shader
                                if not "_d DiffuseMap" in mat_nodes:
                                    _d = mat_nodes.new(type='ShaderNodeTexImage')
                                    _d.name = _d.label = "_d DiffuseMap"
                                else:
                                    _d = mat_nodes["_d DiffuseMap"]
                                _d.location = (-464, 300)
                                _d.width = _d.width_hidden = 300
                                links.new(uber_nodegroup.inputs[0],_d.outputs[0])
                                _d.image = diffusemap_image


                                # Add Rotation node and link it to Uber shader
                                if matxml_derived != "EmissiveOnly":
                                    if not "_n RotationMap" in mat_nodes:
                                        _n = mat_nodes.new(type='ShaderNodeTexImage')
                                        _n.name = _n.label = "_n RotationMap"
                                    else:
                                        _n = mat_nodes["_n RotationMap"]
                                    _n.location = (-464, 0)
                                    _n.width = _n.width_hidden = 300
                                    links.new(uber_nodegroup.inputs[1],_n.outputs[0])
                                    links.new(uber_nodegroup.inputs[2],_n.outputs[1])
                                    _n.image = rotationmap_image
                                else:
                                    uber_nodegroup.inputs[1] = [0, 0.5, 0, 1]
                                    uber_nodegroup.inputs[2] = 0.5


                                # Add Gloss node and link it to Uber shader
                                if not "_s GlossMap" in mat_nodes:
                                    _s = mat_nodes.new(type='ShaderNodeTexImage')
                                    _s.name = _s.label = "_s GlossMap"
                                else:
                                    _s = mat_nodes["_s GlossMap"]
                                _s.location = (-464, -300)
                                _s.width = _s.width_hidden = 300
                                links.new(uber_nodegroup.inputs[3],_s.outputs[0])
                                links.new(uber_nodegroup.inputs[4],_s.outputs[1])
                                _s.image = glossmap_image

                            # ----------------------------------------------
                            #   For modern version of the shader
                            elif not gr2_addon_legacy and matxml_derived == "Uber":

                                # Add Uber Shader
                                uber_nodegroup = mat_nodes.new(type="ShaderNodeHeroEngine")
                                uber_nodegroup.derived = 'UBER'
                                
                                # Adjust transparency and shadows
                                mat.alpha_threshold = float(mat_AlphaTestValue)
                                
                                if mat_AlphaMode == 'Test':
                                    mat.blend_method = 'CLIP'
                                    mat.shadow_method = 'CLIP'
                                    uber_nodegroup.alpha_mode = 'CLIP'
                                    try:
                                        uber_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                                    except:
                                        pass
                                elif mat_AlphaMode == 'Full' or mat_AlphaMode == 'MultipassFull' or mat_AlphaMode == 'Add':
                                    mat_AlphaMode == 'Blend'
                                    mat.blend_method = 'BLEND'
                                    mat.shadow_method = 'HASHED'
                                    try:
                                        uber_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                                    except:
                                        pass
                                else:
                                    mat_AlphaMode == 'None'
                                    mat.blend_method = 'OPAQUE'
                                    mat.shadow_method = 'NONE'



                                # Set Backface Culling
                                uber_nodegroup.show_transparent_back = False
                                
                                uber_nodegroup.location = 0, 0
                                uber_nodegroup.width = 350  # I like to be able to see the names of the textures
                                uber_nodegroup.width_hidden = 300

                                output_node.location = 400, 0

                                # Link the two nodes
                                links = mat.node_tree.links
                                links.new(output_node.inputs[0],uber_nodegroup.outputs[0])

                                # Set shader's texturemap nodes
                                uber_nodegroup.diffuseMap = diffusemap_image
                                uber_nodegroup.glossMap = glossmap_image
                                uber_nodegroup.rotationMap = rotationmap_image

                            # ----------------------------------------------
                            # For EmissiveOnly-type material,
                            # a provisional glass material.
                            # Some ideas taken from here:
                            # https://blenderbasecamp.com/how-to-make-glass-transparent-in-eevee/
                            
                            elif matxml_derived == "EmissiveOnly":

                                # Set some Eevee settings for this style of glass
                                bpy.data.scenes["Scene"].eevee.use_ssr_refraction = True

                                # Set some basic material attributes for
                                # this style of glass-like material
                                mat.blend_method = 'OPAQUE'
                                mat.shadow_method = 'NONE'
                                mat.use_backface_culling = False
                                mat.use_screen_refraction = True
                                mat.refraction_depth = 0.001

                                # Add Principled BSDF Shader
                                if not "Principled BSDF" in mat_nodes:
                                    principled = mat.node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")
                                else:
                                    principled = mat_nodes["Principled BSDF"]
                                
                                # Add Diffuse node
                                if not "_d DiffuseMap" in mat_nodes:
                                    _d = mat_nodes.new(type='ShaderNodeTexImage')
                                    _d.name = _d.label = "_d DiffuseMap"
                                else:
                                    _d = mat_nodes["_d DiffuseMap"]
                                _d.image = diffusemap_image

                                principled.location = (-300, 0)
                                output_node.location = (0, 0)
                                _d.location = (-800, -200)
                                _d.width = _d.width_hidden = 300

                                # Linking nodes and setting some Principled shader values
                                links = mat.node_tree.links

                                links.new(output_node.inputs[0], principled.outputs[0])
                                
                                # Blender 2.8x
                                if bpy.app.version < (2, 90, 0):
                                    principled.inputs[5].default_value   = 0.5      # Specular
                                    principled.inputs[7].default_value   = 0.0      # Roughness
                                    principled.inputs[14].default_value  = 1.050    # IOR
                                    principled.inputs[15].default_value  = 0.950    # Transmission
                                    
                                    links.new(principled.inputs[17],_d.outputs[0])  # Emission
                                # Blender 2.9x
                                elif bpy.app.version < (3, 0, 0):
                                    principled.inputs[5].default_value   = 0.5      # Specular
                                    principled.inputs[7].default_value   = 0.0      # Roughness
                                    principled.inputs[14].default_value  = 1.050    # IOR
                                    principled.inputs[15].default_value  = 0.950    # Transmission
                                    
                                    links.new(principled.inputs[17],_d.outputs[0])  # Emission
                                # Blender 3.x
                                else:
                                    principled.inputs[7].default_value   = 0.5      # Specular
                                    principled.inputs[9].default_value   = 0.0      # Roughness
                                    principled.inputs[16].default_value  = 1.050    # IOR
                                    principled.inputs[17].default_value  = 0.950    # Transmission
                                    
                                    links.new(principled.inputs[19],_d.outputs[0])  # Emission

                            elif matxml_derived == "AnimatedUV":

                                # Set some basic material attributes for
                                # this style of Holo-like material
                                mat.blend_method = 'BLEND'
                                mat.shadow_method = 'NONE'
                                mat.use_backface_culling = False
                                mat.use_screen_refraction = False
                                mat.show_transparent_back = True

                                # Add provisional InanimatedUV :P Shader
                                if not "InanimatedUV" in mat_nodes:
                                    inanimated_uv = mat.node_tree.nodes.new(type="ShaderNodeGroup")
                                    inanimated_uv.node_tree = bpy.data.node_groups["InanimatedUV"]

                                    inanimated_uv.label = "InanimatedUV"
                                    inanimated_uv.name  = "InanimatedUV"
                                else:
                                    inanimated_uv = mat_nodes["InanimatedUV"]
                                
                                # Add Diffuse node
                                if not "_d DiffuseMap" in mat_nodes:
                                    _d = mat_nodes.new(type='ShaderNodeTexImage')
                                    _d.name = _d.label = "_d DiffuseMap"
                                else:
                                    _d = mat_nodes["_d DiffuseMap"]
                                _d.image = diffusemap_image

                                inanimated_uv.location = (-300, 0)
                                output_node.location = (0, 0)
                                _d.location = (-800, -200)
                                _d.width = _d.width_hidden = 300

                                # Linking nodes and setting some Principled shader values
                                links = mat.node_tree.links
                                links.new(output_node.inputs[0], inanimated_uv.outputs[0])
                                links.new(inanimated_uv.inputs[0],_d.outputs[0])  # Diffuse
                                inanimated_uv.inputs[1].default_value = 1.5         # Emissiveness
                                
                            
                        already_processed_mats.append(mat.name)


        # Adding collider objects to a Collection
        if self.use_collect_colliders_bool and collider_objects:
            if not "Collider Objects" in bpy.context.scene.collection.children:
                colliders_collection = bpy.data.collections.new("Collider Objects")
                bpy.context.scene.collection.children.link(colliders_collection)
            else:
                colliders_collection = bpy.data.collections["Collider Objects"]

            if collider_objects:
                link_objects_to_collection (collider_objects, colliders_collection, move = True)


        print("\n\nDone!")

        bpy.context.window.cursor_set("DEFAULT")
        return {"FINISHED"}


# UI is set in ui.py


# ------------------------------------------------------------------
# Registrations

def register():
    bpy.types.Scene.use_overwrite_bool = bpy.props.BoolProperty(
        description="Rewrites already existing Uber and EmissiveOnly materials.\nThis allows for converting Legacy Uber materials\nto modern ones and viceversa.",
        default=False
    )
    bpy.types.Scene.use_collect_colliders_bool = bpy.props.BoolProperty(
        description='Creates or uses a "Collider Objects" Collection and adds to it\nany object with an "util_collision_hidden" type of material\nto facilitate its management and / or deletion',
        default=True
    )
    bpy.utils.register_class(ZGSWTOR_OT_process_uber_mats)

def unregister():
    del bpy.types.Scene.use_overwrite_bool
    del bpy.types.Scene.use_collect_colliders_bool
    
    bpy.utils.unregister_class(ZGSWTOR_OT_process_uber_mats)

if __name__ == "__main__":
    register()




def create_InanimatedUV_nodegroup():
    import bpy

    inanimatedUV_node_tree = bpy.data.node_groups.get('InanimatedUV')
    if not inanimatedUV_node_tree:
        inanimatedUV_node_tree = bpy.data.node_groups.new('InanimatedUV', 'ShaderNodeTree')
        for node in inanimatedUV_node_tree.nodes:
            inanimatedUV_node_tree.nodes.remove(node)

        # INPUTS
        input = inanimatedUV_node_tree.inputs.new('NodeSocketColor', '_d DIffuseMap - Color')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = (1.0, 1.0, 1.0, 1.0)
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'name'):
            input.name = '_d DIffuseColor'
        input = inanimatedUV_node_tree.inputs.new('NodeSocketFloat', 'Emissive Strength')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = 4.0
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 1000000.0
        if hasattr(input, 'min_value'):
            input.min_value = 1.0
        if hasattr(input, 'name'):
            input.name = 'Emissive Strength'

        # OUTPUTS
        output = inanimatedUV_node_tree.outputs.new('NodeSocketShader', 'Shader')
        if hasattr(output, 'attribute_domain'):
            output.attribute_domain = 'POINT'
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Shader'

        # NODES
        transparent_bsdf_1 = inanimatedUV_node_tree.nodes.new('ShaderNodeBsdfTransparent')
        if hasattr(transparent_bsdf_1, 'color'):
            transparent_bsdf_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(transparent_bsdf_1, 'hide'):
            transparent_bsdf_1.hide = False
        if hasattr(transparent_bsdf_1, 'location'):
            transparent_bsdf_1.location = (-107.830322265625, -66.45764923095703)
        if hasattr(transparent_bsdf_1, 'mute'):
            transparent_bsdf_1.mute = False
        if hasattr(transparent_bsdf_1, 'name'):
            transparent_bsdf_1.name = 'Transparent BSDF'
        if hasattr(transparent_bsdf_1, 'use_custom_color'):
            transparent_bsdf_1.use_custom_color = False
        if hasattr(transparent_bsdf_1, 'width'):
            transparent_bsdf_1.width = 140.0
        input_ = next((input_ for input_ in transparent_bsdf_1.inputs if input_.identifier=='Color'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (1.0, 1.0, 1.0, 1.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Color'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in transparent_bsdf_1.inputs if input_.identifier=='Weight'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Weight'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False

        add_shader_1 = inanimatedUV_node_tree.nodes.new('ShaderNodeAddShader')
        if hasattr(add_shader_1, 'color'):
            add_shader_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(add_shader_1, 'hide'):
            add_shader_1.hide = False
        if hasattr(add_shader_1, 'location'):
            add_shader_1.location = (107.830322265625, 8.104637145996094)
        if hasattr(add_shader_1, 'mute'):
            add_shader_1.mute = False
        if hasattr(add_shader_1, 'name'):
            add_shader_1.name = 'Add Shader'
        if hasattr(add_shader_1, 'use_custom_color'):
            add_shader_1.use_custom_color = False
        if hasattr(add_shader_1, 'width'):
            add_shader_1.width = 140.0

        group_output_1 = inanimatedUV_node_tree.nodes.new('NodeGroupOutput')
        if hasattr(group_output_1, 'color'):
            group_output_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(group_output_1, 'hide'):
            group_output_1.hide = False
        if hasattr(group_output_1, 'is_active_output'):
            group_output_1.is_active_output = True
        if hasattr(group_output_1, 'location'):
            group_output_1.location = (297.830322265625, -0.0)
        if hasattr(group_output_1, 'mute'):
            group_output_1.mute = False
        if hasattr(group_output_1, 'name'):
            group_output_1.name = 'Group Output'
        if hasattr(group_output_1, 'use_custom_color'):
            group_output_1.use_custom_color = False
        if hasattr(group_output_1, 'width'):
            group_output_1.width = 140.0

        emission_1 = inanimatedUV_node_tree.nodes.new('ShaderNodeEmission')
        if hasattr(emission_1, 'color'):
            emission_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(emission_1, 'hide'):
            emission_1.hide = False
        if hasattr(emission_1, 'location'):
            emission_1.location = (-107.83030700683594, 66.45764923095703)
        if hasattr(emission_1, 'mute'):
            emission_1.mute = False
        if hasattr(emission_1, 'name'):
            emission_1.name = 'Emission'
        if hasattr(emission_1, 'use_custom_color'):
            emission_1.use_custom_color = False
        if hasattr(emission_1, 'width'):
            emission_1.width = 140.0
        input_ = next((input_ for input_ in emission_1.inputs if input_.identifier=='Color'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (1.0, 1.0, 1.0, 1.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Color'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in emission_1.inputs if input_.identifier=='Strength'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 4.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Strength'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in emission_1.inputs if input_.identifier=='Weight'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Weight'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False

        group_input_1 = inanimatedUV_node_tree.nodes.new('NodeGroupInput')
        if hasattr(group_input_1, 'color'):
            group_input_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(group_input_1, 'hide'):
            group_input_1.hide = False
        if hasattr(group_input_1, 'location'):
            group_input_1.location = (-307.830322265625, -0.0)
        if hasattr(group_input_1, 'mute'):
            group_input_1.mute = False
        if hasattr(group_input_1, 'name'):
            group_input_1.name = 'Group Input'
        if hasattr(group_input_1, 'use_custom_color'):
            group_input_1.use_custom_color = False
        if hasattr(group_input_1, 'width'):
            group_input_1.width = 140.0
        if hasattr(group_input_1.outputs[0], 'default_value'):
            group_input_1.outputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
        if hasattr(group_input_1.outputs[0], 'display_shape'):
            group_input_1.outputs[0].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[0], 'enabled'):
            group_input_1.outputs[0].enabled = True
        if hasattr(group_input_1.outputs[0], 'hide'):
            group_input_1.outputs[0].hide = False
        if hasattr(group_input_1.outputs[0], 'hide_value'):
            group_input_1.outputs[0].hide_value = False
        if hasattr(group_input_1.outputs[0], 'name'):
            group_input_1.outputs[0].name = '_d DIffuseColor'
        if hasattr(group_input_1.outputs[0], 'show_expanded'):
            group_input_1.outputs[0].show_expanded = False
        if hasattr(group_input_1.outputs[1], 'default_value'):
            group_input_1.outputs[1].default_value = 4.0
        if hasattr(group_input_1.outputs[1], 'display_shape'):
            group_input_1.outputs[1].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[1], 'enabled'):
            group_input_1.outputs[1].enabled = True
        if hasattr(group_input_1.outputs[1], 'hide'):
            group_input_1.outputs[1].hide = False
        if hasattr(group_input_1.outputs[1], 'hide_value'):
            group_input_1.outputs[1].hide_value = False
        if hasattr(group_input_1.outputs[1], 'name'):
            group_input_1.outputs[1].name = 'Emissive Strength'
        if hasattr(group_input_1.outputs[1], 'show_expanded'):
            group_input_1.outputs[1].show_expanded = False

        # LINKS
        inanimatedUV_node_tree.links.new(group_input_1.outputs[0], emission_1.inputs[0])
        inanimatedUV_node_tree.links.new(add_shader_1.outputs[0], group_output_1.inputs[0])
        inanimatedUV_node_tree.links.new(emission_1.outputs[0], add_shader_1.inputs[0])
        inanimatedUV_node_tree.links.new(transparent_bsdf_1.outputs[0], add_shader_1.inputs[1])
        inanimatedUV_node_tree.links.new(group_input_1.outputs[1], emission_1.inputs[1])

    return

def link_objects_to_collection (objects, collection, move = False):
    """
    Links objects to a Collection. If move == True,
    it unlinks the objects from their current Collections first.
    Accepts a single object or a list of objects. 
    """

    # Make sure objects works as a list for the loop.
    if not isinstance(objects, list):
        objects = [objects]

    for object in objects:
        # First, unlink from any collections it is in.
        if object.users_collection and move == True:
            for current_collections in object.users_collection:
                current_collections.objects.unlink(object)

        # Then link to collection.
        collection.objects.link(object)

    return