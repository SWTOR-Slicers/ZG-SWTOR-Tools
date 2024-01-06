import bpy
import addon_utils
from pathlib import Path
import os



ADDON_ROOT = __file__.rsplit(__name__.rsplit(".")[0])[0] + __name__.rsplit(".")[0]



def requirements_checks():
    '''Returns a dict with both boolean and string reports on the existence
    and validity of some resources necessary for certain tools to work'''
    
    checks = {}




    # -----------------------------
    # .gr2 Add-on checks
    
    checks["gr2"] = addon_utils.check("io_scene_gr2")[1]

    if "io_scene_gr2" not in addon_utils.addons_fake_modules:
        checks["gr2_status"] = "NOT INSTALLED"
        checks["gr2_status_verbose"] = "NOT INSTALLED. No .gr2 Importer Add-on is currently installed."

    if addon_utils.check("io_scene_gr2")[1]:
        checks["gr2_status"] = "ENABLED"
        checks["gr2_status_verbose"] = "ENABLED. A .gr2 Importer Add-on is installed and enabled."
    else:
        checks["gr2_status"] = "DISABLED"
        checks["gr2_status_verbose"] = "DISABLED. A .gr2 Importer Add-on is installed, but still needs to be enabled."




    # -----------------------------
    # 'resources' folder checks

    swtor_resources_folderpath = getattr(bpy.context.preferences.addons["zg_swtor_tools"].preferences, "swtor_resources_folderpath", "")
    is_badly_written = os.sep not in swtor_resources_folderpath
    is_unfilled = swtor_resources_folderpath == "Choose or type the folder's path"
    is_a_folder = Path(swtor_resources_folderpath).exists()
    is_a_resources_folder = ( Path(swtor_resources_folderpath) / "art/shaders/materials").exists()

    checks["resources"] = is_a_resources_folder
    
    if is_unfilled:
        checks["resources_status"] = "NOT SET"
        checks["resources_status_verbose"] = "NOT SET."
    else:
        if is_badly_written:
            checks["resources_status"] = "NOT VALID"
            checks["resources_status_verbose"] = "NOT VALID. This is not a folder path."
        else:
            if is_a_resources_folder:
                checks["resources_status"] = "SET"
                checks["resources_status_verbose"] = "SET. This is a valid 'resources' folder."
            else:
                if is_a_folder:
                    checks["resources_status"] = "NOT VALID"
                    checks["resources_status_verbose"] = "NOT VALID. This folder isn't a valid 'resources' directory root."
                else:
                    checks["resources_status"] = "NOT FOUND"
                    checks["resources_status_verbose"] = "NOT FOUND. No folder can't be found at the specified path."




    # -----------------------------
    # custom shaders checks

    # Default one
    default_custom_shaders_blend_filepath = os.path.join(ADDON_ROOT, "rsrc", "Custom SWTOR Shaders.blend")

    # Current one
    custom_shaders_blend_filepath = getattr(bpy.context.preferences.addons["zg_swtor_tools"].preferences, "swtor_custom_shaders_blendfile_path", "")
        
    blend_file_badly_written = (".blend" not in custom_shaders_blend_filepath or os.sep not in custom_shaders_blend_filepath)
    blend_file_exists = Path(custom_shaders_blend_filepath).is_file()
    blend_file_is_internal = (custom_shaders_blend_filepath == default_custom_shaders_blend_filepath)

    # Check .blend file's insides for a custom Garment shader to validate it:
    # (see https://devtalk.blender.org/t/traverse-blend-file-to-get-list-of-collections/10348/14 
    # the '_' avoids actually loading anything )
    if blend_file_exists:
        with bpy.data.libraries.load(str(custom_shaders_blend_filepath)) as (data_from, _):
            blend_file_is_valid = "SWTOR - Garment Shader" in data_from.node_groups
    else:
        blend_file_is_valid = False

    checks["custom_shaders"] = blend_file_exists

    if blend_file_exists:
        if blend_file_is_valid:
            checks["custom_shaders"] = True
            if blend_file_is_internal:
                checks["custom_shaders_status"] = "INTERNAL"
                checks["custom_shaders_status_verbose"] = "INTERNAL. Uses the Custom SWTOR Shaders .blend file inside the Add-on."
            else:
                checks["custom_shaders_status"] = "EXTERNAL"
                checks["custom_shaders_status_verbose"] = "EXTERNAL. Uses a Custom SWTOR Shaders .blend file outside the Add-on."
        else:
            checks["custom_shaders"] = False
            checks["custom_shaders_status"] = "NOT VALID"
            checks["custom_shaders_status_verbose"] = "NOT VALID. This .blend file doesn't contain valid Custom SWTOR Shaders."
    else:
        if blend_file_badly_written:
            checks["custom_shaders"] = False
            checks["custom_shaders_status"] = "NOT VALID"
            checks["custom_shaders_status_verbose"] = "NOT VALID. This is not a .blend file path."
        else:
            checks["custom_shaders"] = False
            checks["custom_shaders_status"] = "NOT FOUND"
            checks["custom_shaders_status_verbose"] = "NOT FOUND. No .blend file can't be found at the specified path."

    return checks