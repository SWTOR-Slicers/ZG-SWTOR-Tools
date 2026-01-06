# This code is horrible. it just happens to work. Mostly.
# PEP-8 what's that. Read my Indent Rollercoaster Model manifest!
# So, without further ado…

import bpy
import pathlib
import xml.etree.ElementTree as ET
import addon_utils

from .utils.addon_checks import requirements_checks

checks = requirements_checks()
blender_version = checks["blender_version"]

if blender_version <= 3.6:
    from .shd_additional_swtor_shaders_blen36 import create_AnimatedUV_material, create_EmissiveOnly_material
elif blender_version <= 4.2 :
    from .shd_additional_swtor_shaders_blen40 import create_AnimatedUV_material, create_EmissiveOnly_material
elif blender_version >= 4.3 :
    from .shd_additional_swtor_shaders_blen43 import create_AnimatedUV_material, create_EmissiveOnly_material


# --------------------------------------------------------------
# Basic SWTOR Shader types. First in each list are those we cover.
# The rest are those similar enough to attempt replacing with
# the covered ones, hoping that settings and maps somehow work.
# region
Uber_like = [
    "Uber",
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

Creature_like = [
    "Creature",
    "HighQualityCharacter",
]

Garment_like = [
    "Garment",
    "GarmentScrolling",
]


# All the smart shaders built by Darth Atroxa and their alikes, grouped.
atroxa_shader_types = Uber_like + Creature_like + Garment_like + ["SkinB", "Eye", "HairC"]


# AnimatedUV
AnimatedUV_like = [
    "AnimatedUV",
    "AnimatedUVAlphaBlend",
    "AnimatedVFX",
    "AnimatedVFXAlphaBlend",
    ]


# Shaders that are too basic and need direct support. NOT IN USE AT THE MOMENT
diffuse_only_like = [
    "DiffuseFlat",
    "DiffuseFlatHueable",
    # "Vegetation",
    "Skydome",
    "NoShadeTexFogged",
    ]

# Shaders that either make no sense to do
# or need serious study. NOT IN USE AT THE MOMENT
discardable = [
    "OpacityFade",
    "SimpleParallax"
    ]
# endregion


collider_objects = []



def process_mats(self, mats_list = [], obj = None, already_processed_mats = [], swtor_resources_folderpath = None):

    swtor_shaders_path = swtor_resources_folderpath / "art/shaders/materials"
    
    is_collider = False

    for mat in mats_list:
        
        print("          Material:", mat.name)
        
        
        # Collision Object check at the texturemap level
        if mat.name == "util_collision_hidden":
            is_collider = True


        
        mat_nodes = mat.node_tree.nodes
        swtor_node_in_mat = any("SWTOR" in node.name for node in mat_nodes)



        # Conditions for the material not to be processed:
        
        # It is some sort of Template material.
        if "Template:" in mat.name:
            continue
        
        # It is a PC/NPC wildcard material name.
        if "default" in mat.name:
            continue            


        # If it is called from the 3D Viewer and:
        if not mats_list == []:
            
            # It is not being used in any object.
            if not mat.users:
                continue
            
            # It is already processed.
            if (mat in already_processed_mats):     
                continue
            
            # If there is a SWTOR shader already and overwriting is off.
            if swtor_node_in_mat and not self.use_overwrite_bool:
                continue
            



        # Get SWTOR .mat file and its .xml data
        mat_tree_filepath = swtor_shaders_path / (mat.name + ".mat")
        try:
            matxml_tree = ET.parse(mat_tree_filepath)
        except:
            print("WARNING: THE MATERIAL WASN'T PROCESSED (.mat file not found)\n")
            continue  # disregard and go for the next material
        matxml_root = matxml_tree.getroot()


        # Get SWTOR Shader type ("<Derived>" element)
        matxml_derived = matxml_root.find("Derived").text


        # Save original SWTOR type as a material's custom property for diagnostic purposes.
        mat.swtor_derived = matxml_derived

        # Make some SWTOR shader type simplifications.
        if matxml_derived in Uber_like:
            matxml_derived = "Uber"
        if matxml_derived in Garment_like:
            matxml_derived = "Garment"
        if matxml_derived in Creature_like:
            matxml_derived = "Creature"
        if matxml_derived in AnimatedUV_like:
            matxml_derived = "AnimatedUV"


            
        # Check that the SWTOR shader type is one we cover    
        if  matxml_derived not in (atroxa_shader_types + ["EmissiveOnly", "AnimatedUV"]):
            continue  # Entirely disregard material and go for the next one

        # Delete Principled Shader (and everything else) if needed
        if (
            self.use_overwrite_bool
            or (matxml_derived in atroxa_shader_types and not swtor_node_in_mat)
            or (matxml_derived in ["EmissiveOnly", "AnimatedUV"] and "_d DiffuseMap" not in mat_nodes)
            ):
            
            for node in mat_nodes:
                mat_nodes.remove(node)
                
            # if matxml_derived == "EmissiveOnly":
            #     mat.use_nodes = False
            
        # ----------------------------------------------
        # Basic Blender material's settings

        mat.use_nodes = True  # Redundant?
        mat.use_fake_user = False


        # Read and set some basic material attributes
        mat_AlphaMode = matxml_root.find("AlphaMode").text
        mat_AlphaTestValue = matxml_root.find("AlphaTestValue").text

        # Add Output node to emptied material as long as it's not Emissive Only
        output_node = mat.node_tree.nodes.new('ShaderNodeOutputMaterial')


        # ----------------------------------------------
        # Read material's data
        
        # reset material
        flushtone_value = None
        fleshbrightness = None
        palette1 = None
        palette1specular = None
        palette1metallicspecular = None
        palette2 = None
        palette2specular = None
        palette2metallicspecular = None

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

        # Load material's .xml data
        matxml_inputs = matxml_root.findall("input")
        for matxml_input in matxml_inputs:
            matxml_semantic = matxml_input.find("semantic").text
            matxml_type = matxml_input.find("type").text
            matxml_value = matxml_input.find("value").text


            # # Parsing palette1 data
            # if matxml_semantic == "palette1":
            #     vectval = str(matxml_value).split(',')
            #     palette1_value = [
            #         float(vectval[0]),
            #         float(vectval[1]),
            #         float(vectval[2]),
            #         float(vectval[3]),
            #         ]

            # if matxml_semantic == "palette1Specular":
            #     vectval = str(matxml_value).split(',')
            #     palette1specular_value = [
            #         float(vectval[0]),
            #         float(vectval[1]),
            #         float(vectval[2]),
            #         1.0,
            #         ]

            # if matxml_semantic == "palette1MetallicSpecular":
            #     vectval = str(matxml_value).split(',')
            #     palette1metallicspecular_value = [
            #         float(vectval[0]),
            #         float(vectval[1]),
            #         float(vectval[2]),
            #         1.0,
            #         ]


            # # Parsing palette2 data
            # if matxml_semantic == "palette2":
            #     vectval = str(matxml_value).split(',')
            #     palette2_value = [
            #         float(vectval[0]),
            #         float(vectval[1]),
            #         float(vectval[2]),
            #         float(vectval[3]),
            #         ]

            # if matxml_semantic == "palette2Specular":
            #     vectval = str(matxml_value).split(',')
            #     palette2specular_value = [
            #         float(vectval[0]),
            #         float(vectval[1]),
            #         float(vectval[2]),
            #         1.0,
            #         ]

            # if matxml_semantic == "palette2MetallicSpecular":
            #     vectval = str(matxml_value).split(',')
            #     palette2metallicspecular_value = [
            #         float(vectval[0]),
            #         float(vectval[1]),
            #         float(vectval[2]),
            #         1.0,
            #         ]


            # # Parsing Flushtone and FleshBrightness
            # if matxml_semantic == "FlushTone":
            #     vectval = str(matxml_value).split(',')
            #     flushtone_value = [
            #         float(vectval[0]),
            #         float(vectval[1]),
            #         float(vectval[2]),
            #         ]
                
            # if matxml_semantic == "FleshBrightness":
            #     fleshbrightness = float(str(matxml_value))

            
            # Parsing and loading texture maps
            if matxml_type == "texture":
                matxml_value = matxml_value.replace("\\", "/")
                if matxml_value[0:1] == "/":
                    matxml_value = matxml_value[1:]  # delete possible initial separator
                temp_imagepath = swtor_resources_folderpath / (matxml_value + ".dds")
                try:
                    temp_image = bpy.data.images.load(str(temp_imagepath), check_existing=True)
                    temp_image.colorspace_settings.name = 'Non-Color'
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
                if  obj and "util_collision_hidden" in matxml_value:
                    is_collider = True


        # BASIC SIX ATROXA MATERIALS
        # This uses their .gr2 add-on methods to set their properties
        if matxml_derived in atroxa_shader_types:

            # Add Atroxa Shader
            swtor_nodegroup = mat_nodes.new(type="ShaderNodeHeroEngine")
            swtor_nodegroup.derived = matxml_derived.upper()
            
            # Adjust transparency and shadows
            if blender_version < 4.2:
                if mat_AlphaMode == 'Test':
                    mat.alpha_threshold = float(mat_AlphaTestValue)
                    mat.blend_method = 'CLIP'
                    mat.shadow_method = 'CLIP'
                    swtor_nodegroup.alpha_mode = 'CLIP'
                    try:
                        swtor_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                    except:
                        pass  # Needs to be reimplemented in the .gr2 add-on for 4.2 
                elif mat_AlphaMode == 'Full' or mat_AlphaMode == 'MultipassFull' or mat_AlphaMode == 'Add':
                    mat_AlphaMode = 'Blend'
                    mat.blend_method = 'BLEND'
                    mat.shadow_method = 'HASHED'
                    try:
                        swtor_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                    except:
                        pass  # Needs to be reimplemented in the .gr2 add-on for 4.2 
                else:
                    mat_AlphaMode = 'None'
                    mat.blend_method = 'OPAQUE'
                    mat.shadow_method = 'NONE'
            else:
                # "CLIP" and threshold have to be implemented as nodes
                mat.surface_render_method = 'DITHERED'

            # Set Backface Culling
            swtor_nodegroup.show_transparent_back = False
            
            swtor_nodegroup.location = 0, 0
            swtor_nodegroup.width = 350  # To be able to see the full names of the textures
            swtor_nodegroup.width_hidden = 300

            output_node.location = 400, 0


            # Link the two nodes
            links = mat.node_tree.links
            links.new(output_node.inputs[0],swtor_nodegroup.outputs[0])


            # Set shader's texturemap nodes
            if diffusemap_image:
                swtor_nodegroup.diffuseMap = diffusemap_image

            if glossmap_image:
                swtor_nodegroup.glossMap = glossmap_image

            if rotationmap_image:
                swtor_nodegroup.rotationMap = rotationmap_image

            if palettemap_image:
                swtor_nodegroup.paletteMap = palettemap_image

            if palettemaskmap_image:
                swtor_nodegroup.paletteMaskMap = palettemaskmap_image

            if directionmap_image:
                swtor_nodegroup.directionMap = directionmap_image

            if agemap_image:
                swtor_nodegroup.AgeMap = agemap_image

            if facepaintmap_image:
                swtor_nodegroup.FacepaintMap = facepaintmap_image

            if complexionmap_image:
                swtor_nodegroup.ComplexionMap = complexionmap_image


            # Set values
            if palette1:
                swtor_nodegroup.palette1_hue = palette1[0]
                swtor_nodegroup.palette1_saturation = palette1[1]
                swtor_nodegroup.palette1_brightness = palette1[2]
                swtor_nodegroup.palette1_contrast = palette1[3]

            if palette1specular:
                swtor_nodegroup.palette1_specular = palette1specular
                
            if palette1metallicspecular:
                swtor_nodegroup.palette1_metallic_specular = palette1metallicspecular


            if palette2:
                swtor_nodegroup.palette2_hue = palette2[0]
                swtor_nodegroup.palette2_saturation = palette2[1]
                swtor_nodegroup.palette2_brightness = palette2[2]
                swtor_nodegroup.palette2_contrast = palette2[3]

            if palette2specular:
                swtor_nodegroup.palette2_specular = palette2specular
                
            if palette2metallicspecular:
                swtor_nodegroup.palette2_metallic_specular = palette2metallicspecular

            
            if flushtone_value:
                swtor_nodegroup.flushTone = flushtone_value
                
            if fleshbrightness:
                swtor_nodegroup.fleshBrightness = fleshbrightness


        # OTHER NON-ATROXA MATERIALS
        # They use materials appended from a built-in .blend project in the Add-on
        elif matxml_derived in AnimatedUV_like:
                    
            create_AnimatedUV_material(mat)
            
            # Set some basic material attributes for
            # this style of Holo-like material
            mat.use_backface_culling = False
            mat.use_screen_refraction = False
            mat.show_transparent_back = True

            mat_AlphaMode = matxml_root.find("AlphaMode").text
            mat_AlphaTestValue = matxml_root.find("AlphaTestValue").text

            # Adjust transparency and shadows
            if blender_version < 4.2:
                if mat_AlphaMode == 'Test':
                    mat.alpha_threshold = float(mat_AlphaTestValue)
                    mat.blend_method = 'CLIP'
                    mat.shadow_method = 'CLIP'
                    swtor_nodegroup.alpha_mode = 'CLIP'
                    try:
                        swtor_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                    except:
                        pass  # Needs to be reimplemented in the .gr2 add-on for 4.2 
                elif mat_AlphaMode == 'Full' or mat_AlphaMode == 'MultipassFull' or mat_AlphaMode == 'Add':
                    mat_AlphaMode = 'Blend'
                    mat.blend_method = 'BLEND'
                    mat.shadow_method = 'HASHED'
                    try:
                        swtor_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                    except:
                        pass  # Needs to be reimplemented in the .gr2 add-on for 4.2 
                else:
                    mat_AlphaMode = 'None'
                    mat.blend_method = 'OPAQUE'
                    mat.shadow_method = 'NONE'
            else:
                # "CLIP" and threshold have to be implemented as nodes
                mat.surface_render_method = 'BLENDED'
                
            
            _d = mat_nodes["_d DiffuseMap"]
            _d.image = diffusemap_image
            
            animatedtexture1map = mat_nodes["AnimatedTexture1"]
            animatedtexture1map.image = animatedtexture1map_image
            
            animatedtexture2map = mat_nodes["AnimatedTexture2"]
            animatedtexture2map.image = animatedtexture2map_image

            matxml_inputs = matxml_root.findall("input")
            
            AnimatedUV_node = mat_nodes["SWTOR AnimatedUV Shader"]
            TransformAllUV_node = mat_nodes["SW Aux - TransformAllUV"]

            AnimatedUV_node.inputs["Backface Culling Factor"].default_value = 1.0
            AnimatedUV_node.inputs["Emission Strength"].default_value = 2.5


            for matxml_input in matxml_inputs:
                matxml_semantic = matxml_input.find("semantic").text
                matxml_type = matxml_input.find("type").text
                matxml_value = matxml_input.find("value").text

                # AnimatedUV Nodegroup Settings
                if "animTexTint" in matxml_semantic:
                    if "," not in matxml_value:
                        matxml_value = matxml_value + "," + matxml_value + "," + matxml_value
                    vect_val = matxml_value.split(',')
                    AnimatedUV_node.inputs[matxml_semantic].default_value[0] = float(vect_val[0])
                    AnimatedUV_node.inputs[matxml_semantic].default_value[1] = float(vect_val[1])
                    AnimatedUV_node.inputs[matxml_semantic].default_value[2] = float(vect_val[2])
                                                        
                # -----------------------------------------------------------
                # TransformAllUV Nodegroup settings
                if "animTexUVScrollSpeed" in matxml_semantic:
                    vect_val = matxml_value.split(',')
                    TransformAllUV_node.inputs[matxml_semantic].default_value[0] = float(vect_val[0])
                    TransformAllUV_node.inputs[matxml_semantic].default_value[1] = float(vect_val[1])
                
                if "animTexRotationPivot" in matxml_semantic:
                    vect_val = matxml_value.split(',')
                    TransformAllUV_node.inputs[matxml_semantic].default_value[0] = float(vect_val[0])
                    TransformAllUV_node.inputs[matxml_semantic].default_value[1] = float(vect_val[1])
                
                if "animTexRotationSpeed" in matxml_semantic:
                    TransformAllUV_node.inputs[matxml_semantic].default_value = float(matxml_value)


        elif matxml_derived == "EmissiveOnly":

            # Set some basic material attributes
            mat.use_backface_culling = False

            create_EmissiveOnly_material(mat)


            # Adjust transparency and shadows
            if blender_version < 4.2:
                if mat_AlphaMode == 'Test':
                    mat.alpha_threshold = float(mat_AlphaTestValue)
                    mat.blend_method = 'CLIP'
                    mat.shadow_method = 'CLIP'
                    swtor_nodegroup.alpha_mode = 'CLIP'
                    try:
                        swtor_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                    except:
                        pass  # Needs to be reimplemented in the .gr2 add-on for 4.2 
                elif mat_AlphaMode == 'Full' or mat_AlphaMode == 'MultipassFull' or mat_AlphaMode == 'Add':
                    mat_AlphaMode = 'Blend'
                    mat.blend_method = 'BLEND'
                    mat.shadow_method = 'HASHED'
                    try:
                        swtor_nodegroup.alpha_test_value = float(mat_AlphaTestValue)
                    except:
                        pass  # Needs to be reimplemented in the .gr2 add-on for 4.2 
                else:
                    mat_AlphaMode = 'None'
                    mat.blend_method = 'OPAQUE'
                    mat.shadow_method = 'NONE'
            else:
                # "CLIP" and threshold have to be implemented as nodes
                mat.surface_render_method = 'BLENDED'

            
            _d = mat_nodes["DiffuseMap"]
            _d.image = diffusemap_image
            
            print()
                    
                        
        if mat not in already_processed_mats:
            already_processed_mats.append(mat)

    return is_collider


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
        if object.users_collection and move:
            for current_collections in object.users_collection:
                current_collections.objects.unlink(object)

        # Then link to collection.
        collection.objects.link(object)

    return



class ZGSWTOR_OT_process_named_mats(bpy.types.Operator):

    bl_label = "ZG Process Named Materials"
    bl_idname = "zgswtor.process_named_mats"
    bl_description = "Reads objects' materials names and looks for matching .mat files' information\nto apply the relevant SWTOR shaders and textures. Covers all six basic SWTOR\nshaders plus a few additional ones like AnimatedUV or EmissiveOnly.\nLIMITATION: .mat files lack recoloring palette and PC customization data.\n\n• Requires an enabled SWTOR .gr2 Importer Add-on.\n• Requires setting the path to a 'resources' folder in this addon's Preferences.\n\nFor objects using materials with generic names such as 'default': renaming those\nmaterials to appropriate ones present in 'resources\\art\\shaders\\materials'\nwill make them processable)"
    bl_options = {'REGISTER', 'UNDO'}

    # ------------------------------------------------------------------
    # Check that there are objects in the scene at all (greys-out the UI button otherwise)
    
    @classmethod
    def poll(cls,context):
        if bpy.data.materials:
            return True
        return False


    # Property for the UI buttons to call different actions.
    # See: https://b3d.interplanety.org/en/calling-functions-by-pressing-buttons-in-blender-custom-ui/
    use_selection_only: bpy.props.BoolProperty(
        name="Selection-only",
        description='Applies the material processing to the current selection of objects only',
        default = False,
        options={'HIDDEN'}
        )
    
    convert_this_material:bpy.props.StringProperty(
        name="Material To Convert",
        description="Name of a single material to convert.",
        default = "",
        options={'HIDDEN'}
        )
    
    use_overwrite_bool: bpy.props.BoolProperty(
        name="Overwrite materials",
        description="Reprocesses already processed materials. This allows for updating them if better versions\nof our SWTOR Materials are implemented in new Add-on releases.",
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
    # diagnose issues. These appear in Blender's Material Properties panel
    bpy.types.Material.swtor_derived = bpy.props.StringProperty()


    # ------------------------------------------------------------------
    def execute(self, context):

        bpy.context.window.cursor_set("WAIT")

        # Get the extracted SWTOR assets' "resources" folder from the add-on's preferences. 
        swtor_resources_folderpath = pathlib.Path( bpy.context.preferences.addons["zg_swtor_tools"].preferences.swtor_resources_folderpath )
        swtor_shaders_path = swtor_resources_folderpath / "art/shaders/materials"

        # Check if the SWTOR shaders are available
        if not addon_utils.check("io_scene_gr2")[1]:
            self.report({"WARNING"}, "No version of the 'io_scene_gr2' add-on is enabled.")
            return {"CANCELLED"}

        # Test the existence of the shaders subfolder to validate the SWTOR "resources" folder
        # THIS SHOULDN'T BE NECCESARY WITH THE USE OF requirements_checks
        if not swtor_shaders_path.exists():
            self.report({"WARNING"}, "Unable to find the SWTOR Materials subfolder. Please check this add-on's preferences: either the path to the extracted assets 'resources' folder is incorrect or the resources > art > shaders > materials subfolder is missing.")
            return {"CANCELLED"}



        mats_list = []
        already_processed_mats = []
        collider_objects = []


        # Use from Shader Editor
        if self.convert_this_material != "" and self.convert_this_material in bpy.data.materials:
            
            # Duplicate material to convert data to a new variable and
            # clear the original before processing to avoid issues if processing fails.
            mats_list = [bpy.data.materials[self.convert_this_material]]
            self.convert_this_material = ""
            
            # When in the Shadwr Editor we don't do collider collecting
            # and we always overwrite SWTOR materials.
            bpy.context.scene.use_collect_colliders_bool = False
            self.use_overwrite_bool = True


            print()
            print("PROCESSING OF NAMED SWTOR MATERIALS")
            print()

            process_mats(self, mats_list, None, already_processed_mats, swtor_resources_folderpath)


        # Use from 3D View
        else:
                        
            self.use_collect_colliders_bool = bpy.context.scene.use_collect_colliders_bool
            self.use_overwrite_bool = bpy.context.scene.use_overwrite_bool
            
            if self.use_selection_only:
                selected_objects = bpy.context.selected_objects
            else:
                selected_objects = bpy.data.objects

            if not selected_objects:
                return {"CANCELLED"}

            print()
            print("PROCESSING OF NAMED SWTOR MATERIALS")
            print()


            already_processed_mats = []


            # Main loop            
            amount_to_process = len(selected_objects)
            amount_processed = 0

            for obj in selected_objects:
                is_collider = False
                amount_processed += 1
                if obj.type == "MESH":
                    
                    print("-------------------------------------------")
                    print(f"{amount_processed*100/amount_to_process:6.2f} %    Object: {obj.name}")

                    if len(obj.data.materials) > 0:
                        mats_list = list(obj.data.materials)  # This is more direct than checking material_slots
                        is_collider = process_mats(self, mats_list, obj, already_processed_mats, swtor_resources_folderpath)                        
                    else:
                        print("          OBJECT HAS NO MATERIALS")
                        
                    # Collider object detection and collecting.
                    if self.use_collect_colliders_bool and is_collider is True and obj.name != "Matalogue Dummy Object":
                        collider_objects.append(obj)



            # Adding collider objects to a Collection
            if self.use_collect_colliders_bool and collider_objects:
                if "Collider Objects" not in bpy.context.scene.collection.children:
                    colliders_collection = bpy.data.collections.new("Collider Objects")
                    bpy.context.scene.collection.children.link(colliders_collection)
                else:
                    colliders_collection = bpy.data.collections["Collider Objects"]

                if collider_objects:
                    link_objects_to_collection (collider_objects, colliders_collection, move = True)


            print("\n\nDone!")

        bpy.context.window.cursor_set("DEFAULT")
        return {"FINISHED"}


# UI is set in addon_ui.py


# ------------------------------------------------------------------
# Registrations

def register():
    bpy.types.Scene.use_selection_only = bpy.props.BoolProperty(
        description='Applies the material processing to the current selection of objects only',
        default = False
    )
    
    bpy.types.Scene.use_overwrite_bool = bpy.props.BoolProperty(
        description="Reprocesses already processed materials. This allows for updating them if better versions\nof our SWTOR Materials are implemented in new Add-on releases.",
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
