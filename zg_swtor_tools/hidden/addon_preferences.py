import bpy
import os
from pathlib import Path

class addonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # Preferences properties --------------------

    default_custom_shaders_blendfile = os.path.join(os.path.dirname(__file__), "resources" + os.sep + "Custom SWTOR Shaders.blend")

    # resources folderpath
    swtor_resources_folderpath: bpy.props.StringProperty(
        name = "Resources Folder",
        description = 'Path to the "resources" folder produced by a SWTOR assets extraction',
        subtype = "DIR_PATH",
        default = "Choose or type the folder's path",
        maxlen = 1024
    )
    # Custom SWTOR shaders blendfile folderpath
    swtor_custom_shaders_blendfile_path: bpy.props.StringProperty(
        name = "Custom Shaders File",
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
        col.label(text="inside the Add-on. A path to a different one can be set here.")
        pref_box.prop(self, 'swtor_custom_shaders_blendfile_path', expand=True, )
        
        
        # Custom shaders .blend files' filepaths (selected vs. default)
        # Currently selected one
        swtor_custom_shaders_blendfile_path = bpy.context.preferences.addons["zg_swtor_tools"].preferences.swtor_custom_shaders_blendfile_path
        # Default one
        default_custom_shaders_blend_filepath = os.path.join(os.path.dirname(__file__), "resources" + os.sep + "Custom SWTOR Shaders.blend")

        if swtor_custom_shaders_blendfile_path == default_custom_shaders_blend_filepath:
            pref_box.label(text="STATUS: currently set to internal Custom Shaders file.")
        else:
            if swtor_custom_shaders_blendfile_path == "" or swtor_custom_shaders_blendfile_path == None:
                pref_box.label(text="STATUS: not set.")
            elif swtor_custom_shaders_blendfile_path.endswith(".blend"):
                if os.path.isfile(swtor_custom_shaders_blendfile_path):
                    pref_box.label(text="STATUS: currently set to an external Blender file.")
                else:
                    pref_box.label(text="WARNING: currently set to a non existing file. Please check")
            else:
                pref_box.label(text="WARNING: currently set to an incorrect, non-Blender file.")
                
            pref_box.operator("zgswtor.reset_custom_shaders_prefs_to_internal", text="Reset to internal Custom Shaders file")

        pass


class ZGSWTOR_OT_reset_custom_shaders_prefs_to_internal(bpy.types.Operator):
    bl_idname = "zgswtor.reset_custom_shaders_prefs_to_internal"
    bl_label = "ZG Custom Shaders Reset To Internal"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Resets the Custom Shaders .blend file Preferences\nto use the one inside the Add-on's folder"

    def execute(self, context):
        
        # Default Custom shaders .blend file's filepath
        default_custom_shaders_blend_filepath = os.path.join(os.path.dirname(__file__), "resources" + os.sep + "Custom SWTOR Shaders.blend")

        context.preferences.addons["zg_swtor_tools"].preferences["swtor_custom_shaders_blendfile_path"] = default_custom_shaders_blend_filepath
        
        return {"FINISHED"}



# Registrations

def register():
    bpy.utils.register_class(addonPreferences)
    bpy.utils.register_class(ZGSWTOR_OT_reset_custom_shaders_prefs_to_internal)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_reset_custom_shaders_prefs_to_internal)
    bpy.utils.unregister_class(addonPreferences)

if __name__ == "__main__":
    register()