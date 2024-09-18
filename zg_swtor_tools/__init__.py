import bpy
import sys
import importlib

# Add-on Metadata

bl_info = {
    "name": "ZG SWTOR Tools",
    "author": "ZeroGravitas",
    "version": (2, 0, 2),
    "blender": (3, 5, 0),
    "category": "SWTOR",
    "location": "View 3D > Sidebar > ZG SWTOR",
    "description": "Diverse SWTOR asset-handling tools",
    "doc_url": "https://github.com/SWTOR-Slicers/WikiPedia/wiki/ZG-SWTOR-Tools-Add-on",
    "tracker_url": "",
}


# Add-on modules loader:
# Simplifies coding the loading of the modules to keeping a list of their names
# (See https://b3d.interplanety.org/en/creating-multifile-add-on-for-blender/ ).

# In add-on's main folder 
modulesNames = [
    'addon_sync_with_gr2_addon_props',
    'addon_preferences',
    'addon_open_prefs',
    'addon_ui',
    
    'area_assembler',
    'area_collections_exclude_include',
    'area_collections_group_by_name',
    'area_reset_group_transforms',  # IN USE?
    
    'bake_convert_to_legacy_materials',
    'bake_twilek_corrections',
    'bake_save_images',
    
    'char_character_assembler',
    'char_character_prefixer',
    'char_merge_phys_vertex_groups',
    'char_pc_assembler',

    'mat_add_custom_external_swtor_shaders',
    'mat_customize_swtor_shaders',
    'mat_deduplicate_images',
    'mat_deduplicate_materials',
    'mat_deduplicate_nodegroups',
    'mat_process_named_materials',
    'mat_set_dds',
    'mat_set_backface_culling',
    'mat_set_custom_shaders_values',
    'mat_shaders_io_copier',
    'mat_shaders_io_linker',
    'mat_skinsettings_ng_in_3d_viewer',
    'mat_skinsettings_ng_in_shader_editor',

    'obj_apply_transforms',
    'obj_set_swtor_obj_custom_props',
    'obj_quickscale',
    'obj_remove_doubles',
    'obj_remove_doubles_edit_mode',
    'obj_set_modifiers',
    
    'sculpt_mask_out_selected_vertices',
    'anim_clear_bone_translations',
]



# build dict modulesFullNames (full directory paths):
modulesFullNames = {}

# For modules in add-on's main folder 
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

# Load (or reload) modules
for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        # If the module had been loaded already, recompile it and reload it
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        # Loads the module in the app's global symbols table
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)


def register():
    # If a module has a register function, execute it
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()
    

def unregister():
    # If a module has an unregister function, execute it
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()
 
if __name__ == "__main__":
    register()
