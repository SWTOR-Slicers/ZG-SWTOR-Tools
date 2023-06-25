import bpy
import os
from pathlib import Path

class addonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # Preferences properties --------------------

    default_custom_shaders_blendfile = os.path.join(os.path.dirname(__file__), "Custom SWTOR Shaders.blend")



    # resources folderpath
    swtor_resources_folderpath: bpy.props.StringProperty(
        name = "SWTOR Resources",
        description = 'Path to the "resources" folder produced by a SWTOR assets extraction',
        subtype = "DIR_PATH",
        default = "Choose or type the folder's path",
        maxlen = 1024
    )
    # Custom SWTOR shaders blendfile folderpath
    swtor_custom_shaders_blendfile_path: bpy.props.StringProperty(
        name = "Custom Shaders .blend",
        description = "Path to a Blend file holding custom replacement SWTOR shaders\nfor the current modern ones.\n\n• It defaults to the one stored inside the addon",
        subtype = "FILE_PATH",
        default = default_custom_shaders_blendfile,
        maxlen = 1024
    )


    # UI ----------------------------------------
    
    def draw(self, context):
        layout = self.layout

        # resources folderpath preferences UI
        pref_box = layout.box()
        col=pref_box.column()
        col.scale_y = 0.7
        col.label(text="Path to the 'resources' folder in a SWTOR assets extraction")
        col.label(text="produced by the Slicers GUI app, EasyMYP, or any similar tool.")
        pref_box.prop(self, 'swtor_resources_folderpath', expand=True)

        # Custom SWTOR shaders blendfile folderpath UI
        pref_box = layout.box()
        col=pref_box.column()
        col.scale_y = 0.7
        col.label(text="Path to a .blend file holding custom replacement SWTOR shaders")
        col.label(text="for the current modern ones. By default, it uses the one stored")
        col.label(text="inside the Addon. A path to a different one can be set here.")
        pref_box.prop(self, 'swtor_custom_shaders_blendfile_path', expand=True, )


# Registrations

def register():
    bpy.utils.register_class(addonPreferences)

def unregister():
    bpy.utils.unregister_class(addonPreferences)

if __name__ == "__main__":
    register()