import sys
import importlib

# Add-on Metadata

bl_info = {
    "name": "ZG SWTOR Tools",
    "author": "ZeroGravitas",
    "version": (1, 2, 0),
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
    'process_uber_mats',
    'remove_doubles',
    'remove_doubles_edit_mode',
    'deduplicate_materials',
    'deduplicate_nodegroups',
    'set_backface_culling',
    'quickscale',
    'set_modifiers',
    'customize_swtor_shaders',
    'add_custom_external_swtor_shaders',
    'set_dds',
    'skinsettings_ng_in_shader_editor',
    'skinsettings_ng_in_3d_viewer',
    'shaders_io_linker',
    'shaders_io_copier',
    'selected_vertices_to_sculpt_mask',
    # 'turn_animation_180',
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