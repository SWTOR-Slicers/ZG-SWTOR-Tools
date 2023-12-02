import bpy

def create_AnimatedUV_nodegroup(context, material_datablock, matxml_tree):
    '''
    '''
    
    swtor_resources_folderpath = bpy.context.preferences.addons[__package__].preferences.swtor_resources_folderpath

    matxml_root = matxml_tree.getroot()


    # Check for the existence of the requisite Nodegroups
    # or import them from the template .blend file
    
    if not ("SW Aux - TransformAllUV" in bpy.data.node_groups and
            "SWTOR - AnimatedUV Shader" in bpy.data.node_groups):
        
        basic_swtor_shaders_blend_filepath = os.path.join(os.path.dirname(__file__), "Basic SWTOR Shaders.blend")

        if Path(basic_swtor_shaders_blend_filepath).exists() == False:
            self.report({"WARNING"}, "Unable to find the Basic SWTOR shaders.blend file inside this Add-on's directory.")
            return {"CANCELLED"}

        legacy_materials_path = bpy.path.native_pathsep(basic_swtor_shaders_blend_filepath + "/Material")









    return material_datablock