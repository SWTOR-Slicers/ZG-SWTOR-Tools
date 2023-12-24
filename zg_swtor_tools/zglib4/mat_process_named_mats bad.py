# This code is horrible. it just happens to work. Mostly.
# PEP-8 what's that. Read my Indent Rollercoaster Model manifest!
# So, without further ado…

import bpy
import pathlib
import xml.etree.ElementTree as ET
import addon_utils


from .shd_EmissiveOnly import create_EmissiveOnly_nodegroup

from .shd_AnimatedUV import create_AnimatedUV_nodegroup


class ZGSWTOR_OT_process_named_mats(bpy.types.Operator):

    bl_label = "ZG Process Uber Materials"
    bl_idname = "zgswtor.process_named_mats"
    bl_description = "Reads objects' materials names and looks for matching .mat files' information\nto apply the relevant SWTOR shaders and textures. Covers all six basic SWTOR\nshaders plus a few additional ones like AnimatedUV or EmissiveOnly.\nLIMITATION: .mat files lack recoloring palette and PC customization data.\n\n• Requires an enabled SWTOR .gr2 Importer Add-on.\n• Requires setting the path to a 'resources' folder in this addon's Preferences.\n\nFor objects using materials with generic names such as 'default': renaming those\nmaterials to appropriate ones present in 'resources\\art\\shaders\\materials'\nwill make them processable)"
    bl_options = {'REGISTER', 'UNDO'}

    # ------------------------------------------------------------------
    # Check that there are objects in the scene at all (greys-out the UI button otherwise)
    
    @classmethod
    def poll(cls,context):
        if bpy.data.objects:
            return True
        else:
            return False


    # Property for the UI buttons to call different actions.
    # See: https://b3d.interplanety.org/en/calling-functions-by-pressing-buttons-in-blender-custom-ui/
    use_selection_only: bpy.props.BoolProperty(
        name="Selection-only",
        description='Applies the material processing to the current selection of objects only',
        default = False,
        options={'HIDDEN'}
        )

    # ------------------------------------------------------------------
    # Define some checkbox-type properties
    # (they'll interact with scene-level properties
    # used in the UI panel)
    
    use_overwrite_bool: bpy.props.BoolProperty(
        name="Overwrite Uber materials",
        description="Rewrites already existing processed materials.\nThis allows for updating them if improved ones\nare introduced in this Add-on's updates.",
        default = False,
        options={'HIDDEN'}
        )

    use_collect_colliders_bool: bpy.props.BoolProperty(
        name="Collect Collider objects",
        description='Collects all objects with an "util_collision_hidden" material in a Collection named "Collider Objects"',
        default = True,
        options={'HIDDEN'}
        )



    # Register some custom properties in the Material class for helping
    # diagnose issues
    bpy.types.Material.swtor_derived = bpy.props.StringProperty()


    # ------------------------------------------------------------------
    def execute(self, context):

        bpy.context.window.cursor_set("WAIT")
        
        # Make operator properties' values match UI properties' ones
        self.use_collect_colliders_bool = bpy.context.scene.use_collect_colliders_bool
        
        self.use_overwrite_bool = bpy.context.scene.use_overwrite_bool

        if self.use_selection_only == True:
            selected_objects = bpy.context.selected_objects
        else:
            selected_objects = bpy.data.objects

        if not selected_objects:
            return {"CANCELLED"}

        # Create nodegroup EmissiveOnly for provisional Holo material
        create_EmissiveOnly_nodegroup()


        # --------------------------------------------------------------
        # Get the extracted SWTOR assets' "resources" folder from the add-on's preferences. 
        swtor_resources_folderpath = bpy.context.preferences.addons["zg_swtor_tools"].preferences.swtor_resources_folderpath
        
        swtor_shaders_path = swtor_resources_folderpath + "/art/shaders/materials"

        # Test the existence of the shaders subfolder to validate the SWTOR "resources" folder
        if pathlib.Path(swtor_shaders_path).exists() == False:
            self.report({"WARNING"}, "Unable to find the SWTOR Materials subfolder. Please check this add-on's preferences: either the path to the extracted assets 'resources' folder is incorrect or the resources > art > shaders > materials subfolder is missing.")
            return {"CANCELLED"}

        # --------------------------------------------------------------
        # Check which version of the SWTOR shaders are available
        if addon_utils.check("io_scene_gr2_legacy")[1]:
            self.report({"WARNING"}, "This tool is no longer compatible with the Legacy version of the SWTOR .gr2 Importer Add-on")
            return {"CANCELLED"}
        elif addon_utils.check("io_scene_gr2")[1]:
            pass
        else:
            self.report({"WARNING"}, "No version of the 'io_scene_gr2' add-on is enabled.")
            return {"CANCELLED"}


        # --------------------------------------------------------------
        # Some provisional shader substitution lists
        
        Uber_like = [
            "UberHueable",
            "VegetationHighQuality",
            "Grass",
            "UberEnvBlend",
            "Glass",
            "Ice",
            "UberScrolling",
            "Cloud",
            "Waterfall",
            "Vegetation",
            ]
        
        diffuse_only_like = [
            "DiffuseFlat",
            "DiffuseFlatHueable",
            # "Vegetation",
            "Skydome",
            "NoShadeTexFogged",
            ]
        
        AnimatedUV_like = [
            "AnimatedUVAlphaBlend",
            "AnimatedVFX",
            "AnimatedVFXAlphaBlend",
            ]
        
        discardable = [
            "OpacityFade",
            "SimpleParallax"
            ]
        
        
        print()
        print("PROCESSING OF MATERIALS STARTS HERE")
        print()

        # Loop through list of objects

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


                # Loop through list of object's materials
                for mat_slot in ob.material_slots:

                    # MATERIAL PROCESSING STARTS HERE -------------------------------------

                    mat = mat_slot.material
                    print("          Material: ", mat.name)


                    if mat.name == "util_collision_hidden":
                        is_collision_object = True
                        collider_objects.append(ob)

                    # Check that we want to process the material:
                    # it's not a template nor a recolorable material,
                    # it's in use by objects, but still unprocessed
                    # (multiple objects can share same materials).
                    if (
                        (r"Template: " not in mat.name)
                        and (r"default" not in mat.name)
                        and mat.users
                        and mat.name not in already_processed_mats
                        ):

                        # Read .mat material file as .xml.
                        # If it fails, disregard and go for
                        # the next material in the loop.
                        mat_tree_filepath = swtor_shaders_path + "/" + mat.name + ".mat"
                        try:
                            matxml_tree = ET.parse(mat_tree_filepath)
                        except:
                            continue
                        matxml_root = matxml_tree.getroot()


                        matxml_derived = matxml_root.find("Derived").text

                        mat.swtor_derived = matxml_derived
                        # print("            Shader: ", matxml_derived)


                        if matxml_derived in Uber_like:
                            matxml_derived = "Uber"

                        if matxml_derived in AnimatedUV_like:
                            matxml_derived = "AnimatedUV"
                            
                        if  matxml_derived in ["Uber", "Creature", "HighQualityCharacter", "Eye", "HairC", "SkinB", "Garment", "EmissiveOnly", "AnimatedUV", "Glass"]:

                            mat_nodes = mat.node_tree.nodes

                            # Delete Principled Shader if needed
                            if (self.use_overwrite_bool == True
                                or (matxml_derived == "Uber" and not ("Uber Shader" in mat_nodes or "SWTOR" in mat_nodes))
                                or (matxml_derived == "Creature" and not ("Creature Shader" in mat_nodes or "SWTOR" in mat_nodes))
                                or (matxml_derived == "HighQualityCharacter" and not ("HighQualityCharacter" in mat_nodes or "SWTOR" in mat_nodes))
                                or (matxml_derived == "Eye" and not ("Eye Shader" in mat_nodes or "SWTOR" in mat_nodes))
                                or (matxml_derived == "HairC" and not ("Hair Shader" in mat_nodes or "SWTOR" in mat_nodes))
                                or (matxml_derived == "SkinB" and not ("Skin Shader" in mat_nodes or "SWTOR" in mat_nodes))
                                or (matxml_derived == "Garment" and not ("Garment Shader" in mat_nodes or "SWTOR" in mat_nodes))
                                or ((matxml_derived == "EmissiveOnly" or matxml_derived == "Glass") and not "_d DiffuseMap" in mat_nodes)
                                or (matxml_derived == "AnimatedUV" and not "_d DiffuseMap" in mat_nodes)
                                ):
                                for node in mat_nodes:
                                    mat_nodes.remove(node)
                                if matxml_derived == "EmissiveOnly":
                                    mat.use_nodes = False
                                
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
                            # Gather shader values and texture emaps
                            
                            # Initializing shader values
                            flushtone_value = None
                            fleshbrightness = None
                            palette1 = None
                            palette1specular = None
                            palette1metallicspecular = None
                            palette2 = None
                            palette2specular = None
                            palette2metallicspecular = None
                            
                            # Initializing texturemaps
                            diffusemap_image = None
                            rotationmap_image = None
                            glossmap_image = None
                            palettemap_image = None
                            palettemaskmap_image = None
                            directionmap_image = None
                            agemap_image = None
                            complexionmap_image = None
                            facepaintmap_image = None
                            animatedtexture1map_image = None
                            animatedtexture2map_image = None


                            temp_image = None
                            temp_imagepath = None

                            matxml_inputs = matxml_root.findall("input")
                            for matxml_input in matxml_inputs:
                                matxml_semantic = matxml_input.find("semantic").text
                                matxml_type = matxml_input.find("type").text
                                matxml_value = matxml_input.find("value").text


                                # Parsing and loading values

                                if matxml_semantic == "palette1":
                                    vectval = str(matxml_value).split(',')
                                    palette1_value = [
                                        float(vectval[0]),
                                        float(vectval[1]),
                                        float(vectval[2]),
                                        float(vectval[3]),
                                        ]

                                if matxml_semantic == "palette1Specular":
                                    vectval = str(matxml_value).split(',')
                                    palette1specular_value = [
                                        float(vectval[0]),
                                        float(vectval[1]),
                                        float(vectval[2]),
                                        1.0,
                                        ]

                                if matxml_semantic == "palette1MetallicSpecular":
                                    vectval = str(matxml_value).split(',')
                                    palette1metallicspecular_value = [
                                        float(vectval[0]),
                                        float(vectval[1]),
                                        float(vectval[2]),
                                        1.0,
                                        ]



                                if matxml_semantic == "palette2":
                                    vectval = str(matxml_value).split(',')
                                    palette2_value = [
                                        float(vectval[0]),
                                        float(vectval[1]),
                                        float(vectval[2]),
                                        float(vectval[3]),
                                        ]

                                if matxml_semantic == "palette2Specular":
                                    vectval = str(matxml_value).split(',')
                                    palette2specular_value = [
                                        float(vectval[0]),
                                        float(vectval[1]),
                                        float(vectval[2]),
                                        1.0,
                                        ]

                                if matxml_semantic == "palette2MetallicSpecular":
                                    vectval = str(matxml_value).split(',')
                                    palette2metallicspecular_value = [
                                        float(vectval[0]),
                                        float(vectval[1]),
                                        float(vectval[2]),
                                        1.0,
                                        ]



                                if matxml_semantic == "FlushTone":
                                    vectval = str(matxml_value).split(',')
                                    flushtone_value = [
                                        float(vectval[0]),
                                        float(vectval[1]),
                                        float(vectval[2]),
                                        ]
                                    
                                if matxml_semantic == "FleshBrightness":
                                    fleshbrigtness_value = float(str(matxml_value))

                                
                                # Parsing and loading texturemaps

                                if matxml_type == "texture":
                                    matxml_value = matxml_value.replace("\\", "/")
                                    temp_imagepath = swtor_resources_folderpath + "/" + matxml_value + ".dds"
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
                                    elif matxml_semantic == "PaletteMap":
                                        palettemap_image = temp_image
                                    elif matxml_semantic == "PaletteMaskMap":
                                        palettemaskmap_image = temp_image
                                    elif matxml_semantic == "AgeMap":
                                        agemap_image = temp_image
                                    elif matxml_semantic == "ComplexionMap":
                                        complexionmap_image = temp_image
                                    elif matxml_semantic == "FacepaintMap":
                                        facepaintmap_image = temp_image
                                    elif matxml_semantic == "DirectionMap":
                                        directionmap_image = temp_image
                                    elif matxml_semantic == "AnimatedTexture1":
                                        animatedtexture1map_image = temp_image
                                    elif matxml_semantic == "AnimatedTexture2":
                                        animatedtexture2map_image = temp_image

                                    # Collision Object check at the texturemap level
                                    if  "util_collision_hidden" in matxml_value and is_collision_object == False:
                                        is_collision_object = True
                                        collider_objects.append(ob)



                            # DARTH ATROXA'S .GR2 IMPORTER'S SWTOR SHADERS -------------------------------------


                            # ----------------------------------------------
                            # Add Uber Shader and connect texturemaps


                            if matxml_derived == "Uber":

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
                                if diffusemap_image:
                                    uber_nodegroup.diffuseMap = diffusemap_image
    
                                if glossmap_image:
                                    uber_nodegroup.glossMap = glossmap_image
    
                                if rotationmap_image:
                                    uber_nodegroup.rotationMap = rotationmap_image


                            # ----------------------------------------------
                            # Add Creature Shader and connect texturemaps

                            elif (matxml_derived == "Creature" or matxml_derived == "HighQualityCharacter"):


                                # Add Creature Shader
                                creature_nodegroup = mat_nodes.new(type="ShaderNodeHeroEngine")
                                creature_nodegroup.derived = 'CREATURE'
                                
                                # Adjust transparency and shadows
                                mat.alpha_threshold = float(mat_AlphaTestValue)
                                
                                if mat_AlphaMode == 'Test':
                                    mat.blend_method = 'CLIP'
                                    mat.shadow_method = 'CLIP'
                                    creature_nodegroup.alpha_mode = 'CLIP'
                                    try:
                                        creature_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                                    except:
                                        pass
                                elif mat_AlphaMode == 'Full' or mat_AlphaMode == 'MultipassFull' or mat_AlphaMode == 'Add':
                                    mat_AlphaMode == 'Blend'
                                    mat.blend_method = 'BLEND'
                                    mat.shadow_method = 'HASHED'
                                    try:
                                        creature_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                                    except:
                                        pass
                                else:
                                    mat_AlphaMode == 'None'
                                    mat.blend_method = 'OPAQUE'
                                    mat.shadow_method = 'NONE'



                                # Set Backface Culling
                                creature_nodegroup.show_transparent_back = False
                                
                                creature_nodegroup.location = 0, 0
                                creature_nodegroup.width = 350  # I like to be able to see the names of the textures
                                creature_nodegroup.width_hidden = 300

                                output_node.location = 400, 0

                                # Link the two nodes
                                links = mat.node_tree.links
                                links.new(output_node.inputs[0],creature_nodegroup.outputs[0])

                                # Set shader's texturemap nodes
                                if diffusemap_image:
                                    creature_nodegroup.diffuseMap = diffusemap_image
    
                                if glossmap_image:
                                    creature_nodegroup.glossMap = glossmap_image
    
                                if rotationmap_image:
                                    creature_nodegroup.rotationMap = rotationmap_image

                                if palettemaskmap_image:
                                    creature_nodegroup.paletteMaskMap = palettemaskmap_image

                                if directionmap_image:
                                    creature_nodegroup.directionMap = directionmap_image

                                # Set some values
                                
                                if flushtone_value:
                                    creature_nodegroup.flushTone = flushtone_value
                                    
                                if fleshbrightness:
                                    creature_nodegroup.fleshBrightness = fleshbrightness


                            # ----------------------------------------------
                            # Add Eye Shader and connect texturemaps
                            
                            elif matxml_derived == "Eye":


                                # Add Eye Shader
                                eye_nodegroup = mat_nodes.new(type="ShaderNodeHeroEngine")
                                eye_nodegroup.derived = 'EYE'
                                
                                # Adjust transparency and shadows
                                mat.alpha_threshold = float(mat_AlphaTestValue)
                                
                                if mat_AlphaMode == 'Test':
                                    mat.blend_method = 'CLIP'
                                    mat.shadow_method = 'CLIP'
                                    eye_nodegroup.alpha_mode = 'CLIP'
                                    try:
                                        eye_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                                    except:
                                        pass
                                elif mat_AlphaMode == 'Full' or mat_AlphaMode == 'MultipassFull' or mat_AlphaMode == 'Add':
                                    mat_AlphaMode == 'Blend'
                                    mat.blend_method = 'BLEND'
                                    mat.shadow_method = 'HASHED'
                                    try:
                                        eye_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                                    except:
                                        pass
                                else:
                                    mat_AlphaMode == 'None'
                                    mat.blend_method = 'OPAQUE'
                                    mat.shadow_method = 'NONE'



                                # Set Backface Culling
                                eye_nodegroup.show_transparent_back = False
                                
                                eye_nodegroup.location = 0, 0
                                eye_nodegroup.width = 350  # I like to be able to see the names of the textures
                                eye_nodegroup.width_hidden = 300

                                output_node.location = 400, 0

                                # Link the two nodes
                                links = mat.node_tree.links
                                links.new(output_node.inputs[0],eye_nodegroup.outputs[0])

                                # Set shader's texturemap nodes
                                if diffusemap_image:
                                    eye_nodegroup.diffuseMap = diffusemap_image
    
                                if glossmap_image:
                                    eye_nodegroup.glossMap = glossmap_image
    
                                if rotationmap_image:
                                    eye_nodegroup.rotationMap = rotationmap_image

                                if palettemaskmap_image:
                                    eye_nodegroup.paletteMaskMap = palettemaskmap_image

                                if directionmap_image:
                                    eye_nodegroup.directionMap = directionmap_image

                                # Set some values
                                
                                if palette1:
                                    eye_nodegroup.palette1_hue = palette1[0]
                                    eye_nodegroup.palette1_saturation = palette1[1]
                                    eye_nodegroup.palette1_brightness = palette1[2]
                                    eye_nodegroup.palette1_contrast = palette1[3]

                                if palette1specular:
                                    eye_nodegroup.palette1_specular = palette1specular
                                    
                                if palette1metallicspecular:
                                    eye_nodegroup.palette1_metallic_specular = palette1metallicspecular


                            # ----------------------------------------------
                            # Add HairC Shader and connect texturemaps

                            elif matxml_derived == "HairC":


                                # Add HairC Shader
                                hairc_nodegroup = mat_nodes.new(type="ShaderNodeHeroEngine")
                                hairc_nodegroup.derived = 'HAIRC'
                                
                                # Adjust transparency and shadows
                                mat.alpha_threshold = float(mat_AlphaTestValue)
                                
                                if mat_AlphaMode == 'Test':
                                    mat.blend_method = 'CLIP'
                                    mat.shadow_method = 'CLIP'
                                    hairc_nodegroup.alpha_mode = 'CLIP'
                                    try:
                                        hairc_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                                    except:
                                        pass
                                elif mat_AlphaMode == 'Full' or mat_AlphaMode == 'MultipassFull' or mat_AlphaMode == 'Add':
                                    mat_AlphaMode == 'Blend'
                                    mat.blend_method = 'BLEND'
                                    mat.shadow_method = 'HASHED'
                                    try:
                                        hairc_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                                    except:
                                        pass
                                else:
                                    mat_AlphaMode == 'None'
                                    mat.blend_method = 'OPAQUE'
                                    mat.shadow_method = 'NONE'



                                # Set Backface Culling
                                hairc_nodegroup.show_transparent_back = False
                                
                                hairc_nodegroup.location = 0, 0
                                hairc_nodegroup.width = 350  # I like to be able to see the names of the textures
                                hairc_nodegroup.width_hidden = 300

                                output_node.location = 400, 0

                                # Link the two nodes
                                links = mat.node_tree.links
                                links.new(output_node.inputs[0],hairc_nodegroup.outputs[0])

                                # Set shader's texturemap nodes
                                if diffusemap_image:
                                    hairc_nodegroup.diffuseMap = diffusemap_image
    
                                if glossmap_image:
                                    hairc_nodegroup.glossMap = glossmap_image
    
                                if rotationmap_image:
                                    hairc_nodegroup.rotationMap = rotationmap_image

                                if palettemap_image:
                                    hairc_nodegroup.paletteMap = palettemap_image

                                if palettemaskmap_image:
                                    hairc_nodegroup.paletteMaskMap = palettemaskmap_image

                                if directionmap_image:
                                    hairc_nodegroup.directionMap = directionmap_image

                                # Set some values
                                
                                if palette1:
                                    hairc_nodegroup.palette1_hue = palette1[0]
                                    hairc_nodegroup.palette1_saturation = palette1[1]
                                    hairc_nodegroup.palette1_brightness = palette1[2]
                                    hairc_nodegroup.palette1_contrast = palette1[3]

                                if palette1specular:
                                    hairc_nodegroup.palette1_specular = palette1specular
                                    
                                if palette1metallicspecular:
                                    hairc_nodegroup.palette1_metallic_specular = palette1metallicspecular


                            # ----------------------------------------------
                            # Add Garment Shader and connect texturemaps
                            
                            elif matxml_derived == "Garment":

                                # Add Garment Shader
                                garment_nodegroup = mat_nodes.new(type="ShaderNodeHeroEngine")
                                garment_nodegroup.derived = 'GARMENT'
                                
                                # Adjust transparency and shadows
                                mat.alpha_threshold = float(mat_AlphaTestValue)
                                
                                if mat_AlphaMode == 'Test':
                                    mat.blend_method = 'CLIP'
                                    mat.shadow_method = 'CLIP'
                                    garment_nodegroup.alpha_mode = 'CLIP'
                                    try:
                                        garment_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                                    except:
                                        pass
                                elif mat_AlphaMode == 'Full' or mat_AlphaMode == 'MultipassFull' or mat_AlphaMode == 'Add':
                                    mat_AlphaMode == 'Blend'
                                    mat.blend_method = 'BLEND'
                                    mat.shadow_method = 'HASHED'
                                    try:
                                        garment_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                                    except:
                                        pass
                                else:
                                    mat_AlphaMode == 'None'
                                    mat.blend_method = 'OPAQUE'
                                    mat.shadow_method = 'NONE'



                                # Set Backface Culling
                                garment_nodegroup.show_transparent_back = False
                                
                                garment_nodegroup.location = 0, 0
                                garment_nodegroup.width = 350  # I like to be able to see the names of the textures
                                garment_nodegroup.width_hidden = 300

                                output_node.location = 400, 0

                                # Link the two nodes
                                links = mat.node_tree.links
                                links.new(output_node.inputs[0],garment_nodegroup.outputs[0])

                                # Set shader's texturemap nodes
                                if diffusemap_image:
                                    garment_nodegroup.diffuseMap = diffusemap_image
    
                                if glossmap_image:
                                    garment_nodegroup.glossMap = glossmap_image
    
                                if rotationmap_image:
                                    garment_nodegroup.rotationMap = rotationmap_image

                                if palettemap_image:
                                    garment_nodegroup.paletteMap = palettemap_image

                                if palettemaskmap_image:
                                    garment_nodegroup.paletteMaskMap = palettemaskmap_image


                                # Set some values
                                
                                if palette1:
                                    garment_nodegroup.palette1_hue = palette1[0]
                                    garment_nodegroup.palette1_saturation = palette1[1]
                                    garment_nodegroup.palette1_brightness = palette1[2]
                                    garment_nodegroup.palette1_contrast = palette1[3]

                                if palette1specular:
                                    garment_nodegroup.palette1_specular = palette1specular
                                    
                                if palette1metallicspecular:
                                    garment_nodegroup.palette1_metallic_specular = palette1metallicspecular


                                if palette2:
                                    garment_nodegroup.palette2_hue = palette2[0]
                                    garment_nodegroup.palette2_saturation = palette2[1]
                                    garment_nodegroup.palette2_brightness = palette2[2]
                                    garment_nodegroup.palette2_contrast = palette2[3]

                                if palette2specular:
                                    garment_nodegroup.palette2_specular = palette2specular
                                    
                                if palette2metallicspecular:
                                    garment_nodegroup.palette2_metallic_specular = palette2metallicspecular


                            # ----------------------------------------------
                            # Add SkinB Shader and connect texturemaps

                            elif matxml_derived == "SkinB":


                                # Add SkinB Shader
                                skinb_nodegroup = mat_nodes.new(type="ShaderNodeHeroEngine")
                                skinb_nodegroup.derived = 'SKINB'
                                
                                # Adjust transparency and shadows
                                mat.alpha_threshold = float(mat_AlphaTestValue)
                                
                                if mat_AlphaMode == 'Test':
                                    mat.blend_method = 'CLIP'
                                    mat.shadow_method = 'CLIP'
                                    skinb_nodegroup.alpha_mode = 'CLIP'
                                    try:
                                        skinb_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                                    except:
                                        pass
                                elif mat_AlphaMode == 'Full' or mat_AlphaMode == 'MultipassFull' or mat_AlphaMode == 'Add':
                                    mat_AlphaMode == 'Blend'
                                    mat.blend_method = 'BLEND'
                                    mat.shadow_method = 'HASHED'
                                    try:
                                        skinb_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                                    except:
                                        pass
                                else:
                                    mat_AlphaMode == 'None'
                                    mat.blend_method = 'OPAQUE'
                                    mat.shadow_method = 'NONE'



                                # Set Backface Culling
                                skinb_nodegroup.show_transparent_back = False
                                
                                skinb_nodegroup.location = 0, 0
                                skinb_nodegroup.width = 350  # I like to be able to see the names of the textures
                                skinb_nodegroup.width_hidden = 300

                                output_node.location = 400, 0

                                # Link the two nodes
                                links = mat.node_tree.links
                                links.new(output_node.inputs[0],skinb_nodegroup.outputs[0])

                                # Set shader's texturemap nodes
                                if diffusemap_image:
                                    skinb_nodegroup.diffuseMap = diffusemap_image
    
                                if glossmap_image:
                                    skinb_nodegroup.glossMap = glossmap_image
    
                                if rotationmap_image:
                                    skinb_nodegroup.rotationMap = rotationmap_image

                                if palettemap_image:
                                    skinb_nodegroup.paletteMap = palettemap_image

                                if palettemaskmap_image:
                                    skinb_nodegroup.paletteMaskMap = palettemaskmap_image

                                if agemap_image:
                                    skinb_nodegroup.AgeMap = agemap_image

                                if facepaintmap_image:
                                    skinb_nodegroup.FacepaintMap = facepaintmap_image

                                if complexionmap_image:
                                    skinb_nodegroup.ComplexionMap = complexionmap_image

                                # Set some values
                                
                                if palette1:
                                    skinb_nodegroup.palette1_hue = palette1[0]
                                    skinb_nodegroup.palette1_saturation = palette1[1]
                                    skinb_nodegroup.palette1_brightness = palette1[2]
                                    skinb_nodegroup.palette1_contrast = palette1[3]

                                if palette1specular:
                                    skinb_nodegroup.palette1_specular = palette1specular
                                    
                                if palette1metallicspecular:
                                    skinb_nodegroup.palette1_metallic_specular = palette1metallicspecular


                                
                                if flushtone_value:
                                    skinb_nodegroup.flushTone = flushtone_value
                                    
                                if fleshbrightness:
                                    skinb_nodegroup.fleshBrightness = fleshbrightness



                            # NON-ATROXA SWTOR SHADERS ---------------------------------------------------------

                            # Add EmissiveOnly Shader and connect texturemaps:
                            # it's a provisional glass material with some refraction.
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


                                # Add Gamma correction Shader
                                if not "Gamma" in mat_nodes:
                                    gamma = mat.node_tree.nodes.new(type="ShaderNodeGamma")
                                else:
                                    gamma = mat_nodes["Gamma"]
                                gamma.inputs["Gamma"].default_value = 2.2


                                # Add Diffuse node
                                if not "_d DiffuseMap" in mat_nodes:
                                    _d = mat_nodes.new(type='ShaderNodeTexImage')
                                    _d.name = _d.label = "_d DiffuseMap"
                                else:
                                    _d = mat_nodes["_d DiffuseMap"]
                                _d.image = diffusemap_image

                                principled.location = (-300, 0)
                                gamma.location = (-550, -310)
                                output_node.location = (0, 0)
                                _d.location = (-1000, -200)
                                _d.width = _d.width_hidden = 300

                                # Linking nodes and setting some Principled shader values
                                links = mat.node_tree.links

                                #   Output to Principled
                                links.new(output_node.inputs[0], principled.outputs[0])
                                
                                #   Principled to Gamma
                                # Blender 2.8x
                                if bpy.app.version < (2, 90, 0):
                                    principled.inputs[5].default_value   = 0.5      # Specular
                                    principled.inputs[7].default_value   = 0.0      # Roughness
                                    principled.inputs[14].default_value  = 1.050    # IOR
                                    principled.inputs[15].default_value  = 0.950    # Transmission
                                    
                                    links.new(principled.inputs[17],gamma.outputs[0])  # Emission
                                # Blender 2.9x
                                elif bpy.app.version < (3, 0, 0):
                                    principled.inputs[5].default_value   = 0.5      # Specular
                                    principled.inputs[7].default_value   = 0.0      # Roughness
                                    principled.inputs[14].default_value  = 1.050    # IOR
                                    principled.inputs[15].default_value  = 0.950    # Transmission
                                    
                                    links.new(principled.inputs[17],gamma.outputs[0])  # Emission
                                # Blender 3.x
                                else:
                                    principled.inputs[7].default_value   = 0.5      # Specular
                                    principled.inputs[9].default_value   = 0.0      # Roughness
                                    principled.inputs[16].default_value  = 1.050    # IOR
                                    principled.inputs[17].default_value  = 0.950    # Transmission
                                    
                                    links.new(principled.inputs[19],gamma.outputs[0])  # Emission

                                # Gamma to _d
                                links.new(_d.outputs[0],gamma.inputs[0])  # Emission
                                
                                
                            # ----------------------------------------------
                            # Add AnimatedUV Shader and connect texturemaps

                            elif matxml_derived == "AnimatedUV":
                                    
                                create_AnimatedUV_nodegroup(mat)
                                
                                # Set some basic material attributes for
                                # this style of Holo-like material
                                mat.blend_method = 'BLEND'
                                mat.shadow_method = 'NONE'
                                mat.use_backface_culling = False
                                mat.use_screen_refraction = False
                                mat.show_transparent_back = True


                                # mat_AlphaMode = matxml_root.find("AlphaMode").text
                                # mat_AlphaTestValue = matxml_root.find("AlphaTestValue").text
                                
                                _d = mat_nodes["_d DiffuseMap"]
                                _d.image = diffusemap_image
                                
                                animatedtexture1map = mat_nodes["AnimatedTexture1"]
                                animatedtexture1map.image = animatedtexture1map_image
                                
                                animatedtexture2map = mat_nodes["AnimatedTexture2"]
                                animatedtexture2map.image = animatedtexture2map_image

                                matxml_inputs = matxml_root.findall("input")
                                
                                AnimatedUV_node = mat_nodes["SWTOR - AnimatedUV Shader"]
                                TransformAllUV_node = mat_nodes["SW Aux - TransformAllUV"]

                                AnimatedUV_node.inputs["Backface Culling Factor"].default_value = 1.0
                                AnimatedUV_node.inputs["Emission Strength"].default_value = 2.5


                                for matxml_input in matxml_inputs:
                                    matxml_semantic = matxml_input.find("semantic").text
                                    matxml_type = matxml_input.find("type").text
                                    matxml_value = matxml_input.find("value").text

                                    # AnimatedUV Nodegroup Settings
                                    # (in the .mat files this can be vector or float)
                                    if (matxml_semantic == "animTexTint0" or
                                        matxml_semantic == "animTexTint1" or
                                        matxml_semantic == "animTexTint2"):
                                        
                                        if matxml_type == "vector4":
                                            vect_val = matxml_value.split(',')
                                            AnimatedUV_node.inputs[matxml_semantic].default_value[0] = float(vect_val[0])
                                            AnimatedUV_node.inputs[matxml_semantic].default_value[1] = float(vect_val[1])
                                            AnimatedUV_node.inputs[matxml_semantic].default_value[2] = float(vect_val[2])
                                        else:
                                            AnimatedUV_node.inputs[matxml_semantic].default_value[0] = matxml_value
                                            AnimatedUV_node.inputs[matxml_semantic].default_value[1] = matxml_value
                                            AnimatedUV_node.inputs[matxml_semantic].default_value[2] = matxml_value
                                    
                                    # -----------------------------------------------------------
                                    # TransformAllUV Nodegroup settings
                                    if matxml_semantic == "animTexUVScrollSpeed0":
                                        vect_val = matxml_value.split(',')
                                        TransformAllUV_node.inputs[matxml_semantic].default_value[0] = float(vect_val[0])
                                        TransformAllUV_node.inputs[matxml_semantic].default_value[1] = float(vect_val[1])
                                        # TransformAllUV_node.inputs[matxml_semantic].default_value[2] = float(vect_val[2])
                                    
                                    if matxml_semantic == "animTexRotationPivot0":
                                        vect_val = matxml_value.split(',')
                                        TransformAllUV_node.inputs[matxml_semantic].default_value[0] = float(vect_val[0])
                                        TransformAllUV_node.inputs[matxml_semantic].default_value[1] = float(vect_val[1])
                                        # TransformAllUV_node.inputs[matxml_semantic].default_value[2] = float(vect_val[2])
                                    
                                    if matxml_semantic == "animTexRotationSpeed0":
                                        TransformAllUV_node.inputs[matxml_semantic].default_value = float(matxml_value)
                                    
                                    if matxml_semantic == "animTexUVScrollSpeed1":
                                        vect_val = matxml_value.split(',')
                                        TransformAllUV_node.inputs[matxml_semantic].default_value[0] = float(vect_val[0])
                                        TransformAllUV_node.inputs[matxml_semantic].default_value[1] = float(vect_val[1])
                                        # TransformAllUV_node.inputs[matxml_semantic].default_value[2] = float(vect_val[2])
                                    
                                    if matxml_semantic == "animTexRotationPivot1":
                                        vect_val = matxml_value.split(',')
                                        TransformAllUV_node.inputs[matxml_semantic].default_value[0] = float(vect_val[0])
                                        TransformAllUV_node.inputs[matxml_semantic].default_value[1] = float(vect_val[1])
                                        # TransformAllUV_node.inputs[matxml_semantic].default_value[2] = float(vect_val[2])
                                    
                                    if matxml_semantic == "animTexRotationSpeed1":
                                        TransformAllUV_node.inputs[matxml_semantic].default_value = float(matxml_value)
                                    
                                    if matxml_semantic == "animTexUVScrollSpeed2":
                                        vect_val = matxml_value.split(',')
                                        TransformAllUV_node.inputs[matxml_semantic].default_value[0] = float(vect_val[0])
                                        TransformAllUV_node.inputs[matxml_semantic].default_value[1] = float(vect_val[1])
                                        # TransformAllUV_node.inputs[matxml_semantic].default_value[2] = float(vect_val[2])
                                    
                                    if matxml_semantic == "animTexRotationPivot2":
                                        vect_val = matxml_value.split(',')
                                        TransformAllUV_node.inputs[matxml_semantic].default_value[0] = float(vect_val[0])
                                        TransformAllUV_node.inputs[matxml_semantic].default_value[1] = float(vect_val[1])
                                        # TransformAllUV_node.inputs[matxml_semantic].default_value[2] = float(vect_val[2])
                                    
                                    if matxml_semantic == "animTexRotationSpeed2":
                                        TransformAllUV_node.inputs[matxml_semantic].default_value = float(matxml_value)
                                    


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
    bpy.types.Scene.use_selection_only = bpy.props.BoolProperty(
        description='Applies the material processing to the current selection of objects only',
        default = False
    )
    bpy.types.Scene.use_overwrite_bool = bpy.props.BoolProperty(
        description="Rewrites already existing processed materials.\nThis allows for updating them if improved ones\nare introduced in this Add-on's updates.",
        default=False
    )
    bpy.types.Scene.use_collect_colliders_bool = bpy.props.BoolProperty(
        description='Creates or uses a "Collider Objects" Collection and adds to it\nany object with an "util_collision_hidden" type of material\nto facilitate its management and / or deletion',
        default=True
    )
    bpy.utils.register_class(ZGSWTOR_OT_process_named_mats)

def unregister():
    del bpy.types.Scene.use_selection_only
    del bpy.types.Scene.use_overwrite_bool
    del bpy.types.Scene.use_collect_colliders_bool
    
    bpy.utils.unregister_class(ZGSWTOR_OT_process_named_mats)

if __name__ == "__main__":
    register()


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
