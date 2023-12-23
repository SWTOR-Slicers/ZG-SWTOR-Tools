import bpy
import sys
import importlib

# Add-on Metadata

bl_info = {
    "name": "ZG SWTOR Tools",
    "author": "ZeroGravitas",
    "version": (1, 4, 0),
    "blender": (2, 83, 0),
    "category": "SWTOR",
    "location": "View 3D > Sidebar > ZG SWTOR",
    "description": "Diverse SWTOR asset-handling tools",
    "doc_url": "https://github.com/SWTOR-Slicers/zg_swtor_tools",
    "tracker_url": "",
}

# This Add-on's code is compatible with both Blender 3.6 and 4.x
# by having alternate versions of each module.
#
# To simplify things, the modules with the operators are inside
# two Blender version-related subfolders.
# 
# We are discriminating using the major version number (3 and 4)
# to give some leeway (some tools might fail below 3.1, though).

# Determine Blender version
blender_version_major_number, blender_version_minor_number , _ = bpy.app.version

if blender_version_major_number == 4:
    zglib = "zglib4"
else:
    zglib = "zglib3"


# Add-on modules loader:
# Simplifies coding the loading of the modules to keeping a list of their names
# (See https://b3d.interplanety.org/en/creating-multifile-add-on-for-blender/ ).
# We could just load all the modules inside the relevant subfolders, but this
# lets us be more selective while developing them.

baseModulesNames = [
    'addon_property_group',
    'addon_preferences',
    'addon_open_prefs',
    'addon_ui',
]

toolModulesNames = [
    'area_assembler',
    'area_collections_tools',
    'bake_convert_to_legacy_materials',
    'character_assembler',
    'character_prefixer',
    'mat_add_custom_external_swtor_shaders',
    'mat_customize_swtor_shaders',
    'mat_deduplicate_materials',
    'mat_deduplicate_nodegroups',
    'mat_process_named_materials',
    'mat_set_backface_culling',
    'mat_set_dds',
    'mat_set_custom_shaders_values',
    'mat_shaders_io_copier',
    'mat_shaders_io_linker',
    'mat_skinsettings_ng_in_3d_viewer',
    'mat_skinsettings_ng_in_shader_editor',
    'obj_quickscale',
    'obj_remove_doubles_edit_mode',
    'obj_remove_doubles',
    'obj_set_modifiers',
    'sculpt_mask_out_selected_vertices',
    ]

# build dict modulesFullNames:
modulesFullNames = {}

for currentModuleName in baseModulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))
    
for currentModuleName in toolModulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}.{}'.format(__name__, zglib, currentModuleName))


for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        # If the module had been loaded already, recompile it and reload it
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        # Loads the module in the app's global symbols table
        # globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)


def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()
    

def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()
 
if __name__ == "__main__":
    register()#
