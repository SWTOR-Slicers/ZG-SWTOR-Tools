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

# Add-on modules loader:
# Simplifies coding the loading of the modules to keeping a list of their names
# (See https://b3d.interplanety.org/en/creating-multifile-add-on-for-blender/ )

modulesNames = [
    'ui',
    'preferences',
    'open_addon_prefs',
    'area_assembler',
    'add_custom_external_swtor_shaders',
    'character_assembler',
    'convert_to_legacy_materials',
    'customize_swtor_shaders',
    'deduplicate_materials',
    'deduplicate_nodegroups',
    'collections_tools',
    'prefixer',
    'process_named_mats',
    'quickscale',
    'remove_doubles_edit_mode',
    'remove_doubles',
    'selected_vertices_to_sculpt_mask',
    'set_backface_culling',
    'set_dds',
    'set_modifiers',
    'shaders_io_copier',
    'shaders_io_linker',
    'skinsettings_ng_in_3d_viewer',
    'skinsettings_ng_in_shader_editor',
    ]
  
modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
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
