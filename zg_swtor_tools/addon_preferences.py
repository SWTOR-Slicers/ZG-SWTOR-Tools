import bpy
import os
from pathlib import Path


from .utils.addon_checks import requirements_checks


ADDON_ROOT = __file__.rsplit(__name__.rsplit(".")[0])[0] + __name__.rsplit(".")[0]

Y_SCALING_GRAL = 0.9
Y_SCALING_INFO = 0.65
Y_SCALING_SPACER = 0.3


class addonPreferences(bpy.types.AddonPreferences):
    bl_idname = "zg_swtor_tools"

    # Preferences properties --------------------

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
        default = os.path.join(ADDON_ROOT, "rsrc", "Custom SWTOR Shaders.blend"),
        maxlen = 1024
    )
    
    # Behavior of some tools when processing SWTOR objects with custom mesh scaling
    # (the new scale settings in the .gr2 importer Add-on, which are recorded in the
    # imported objects' as a 'gr2_scale' custom property)
    use_gr2_scale_custom_prop: bpy.props.BoolProperty(
        name = "Use SWTOR Objects' Mesh Scale Data If Available",
        description = "If a SWTOR object has a 'gr2_scale' custom property, added by a .gr2 Importer Add-on,\nmesh size-sensitive tools will consider that data over any other assumed or set scalings\n(such as the default 1.0 or a .gr2 Add-on's importing prefs settings)",
        default = True,
    )



    # UI ----------------------------------------
    
    def draw(self, context):
        
        checks = requirements_checks()
        
        
        layout = self.layout


        # resources folderpath preferences UI
        pref_box = layout.box()
        
        col=pref_box.column(align=True)
        col.scale_y = Y_SCALING_INFO
        col.label(text="Path to the 'resources' folder in a SWTOR assets extraction")
        col.label(text="produced by the Slicers GUI app, EasyMYP, or any similar tool.")

        col=pref_box.column()
        col.prop(self, 'swtor_resources_folderpath', expand=True, )
        
        col.alert = not checks["resources"]
        col.label(text="Status: " + checks["resources_status_verbose"])



        # Custom SWTOR shaders blendfile folderpath UI
        pref_box = layout.box()
        
        col=pref_box.column(align=True)
        col.scale_y = Y_SCALING_INFO
        col.label(text="Path to a .blend file holding customizable replacement SWTOR shaders. By default,")
        col.label(text="it uses the one stored inside this Add-on. A path to a different one can be set here.")
        
        col=pref_box.column()
        col.prop(self, 'swtor_custom_shaders_blendfile_path', expand=True, )
        
        col.alert = not checks["custom_shaders"]
        col.label(text="Status: " + checks["custom_shaders_status_verbose"])

        col.operator("zgswtor.reset_custom_shaders_prefs_to_internal", text="Reset to internal Custom Shaders file")



        # SWTOR objects' scaling data usage UI
        pref_box = layout.box()

        col=pref_box.column()
        col.prop(self, 'use_gr2_scale_custom_prop', text="Use SWTOR objects' mesh scale data if available and relevant to any ZG Tool.")


# reset_custom_shaders_prefs_to_internal Operator -------------------------


class ZGSWTOR_OT_reset_custom_shaders_prefs_to_internal(bpy.types.Operator):
    bl_idname = "zgswtor.reset_custom_shaders_prefs_to_internal"
    bl_label = "ZG Custom Shaders Reset To Internal"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Resets the Custom Shaders .blend file Preference\nto use the file inside this Add-on's folder"

    @classmethod
    def poll(cls,context):
        checks = requirements_checks()
        if not checks["custom_shaders"]:
            return True
        else:
            return False


    def execute(self, context):
        
        # Default Custom shaders .blend file's filepath
        default_custom_shaders_blend_filepath = os.path.join(os.path.dirname(__file__), "rsrc" + os.sep + "Custom SWTOR Shaders.blend")

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