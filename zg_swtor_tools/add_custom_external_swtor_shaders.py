import bpy
from bpy import app

import os
from pathlib import Path
from bpy.app.handlers import persistent

# -------------------------------------------------------------
# Handler for detecting opening a new blendfile and updating
# UI options properties accordingly
@persistent
def handler_new_blendfile(scene):
    # Check that we aren't editing the custom shaders template file
    # to prevent from appending/linking the shaders to itself
    # and set a prop to control the UI's related widgets

    shaders_lib_filepath = bpy.context.preferences.addons[
        __package__].preferences.swtor_custom_shaders_blendfile_path

    open_blend_filepath = bpy.data.filepath

    if open_blend_filepath == shaders_lib_filepath:
        bpy.context.scene.enable_adding_custom_shaders = False
        bpy.context.scene.enable_linking_custom_shaders = False
    else:
        bpy.context.scene.enable_adding_custom_shaders = True
        bpy.context.scene.enable_linking_custom_shaders = True

bpy.app.handlers.load_post.append(handler_new_blendfile)


# -------------------------------------------------------------
class ZGSWTOR_OT_add_custom_external_swtor_shaders(bpy.types.Operator):
    bl_idname = "zgswtor.add_custom_external_swtor_shaders"
    bl_label = "ZG Add Custom SWTOR Shaders"
    bl_description = "Appends or links custom SWTOR shaders from\nan external Blender templates file.\n\n• Requires setting a path to an appropriate .blend file holding\n   customizable SWTOR shaders in this Addon\'s Preferences"
    bl_options = {'REGISTER', 'UNDO'}

    # linking vs appending flag property
    link: bpy.props.BoolProperty(
        name="Link custom shaders",
        description='If adding custom SWTOR shaders,\nlink them instead of appending them',
        default=False,
        options={'HIDDEN'}
    )

    def execute(self, context):

        shaders_lib_filepath = context.preferences.addons[__package__].preferences.swtor_custom_shaders_blendfile_path

        if Path(shaders_lib_filepath).exists() == False:
            self.report({"WARNING"}, "Unable to find a custom SWTOR shaders .blend file. Please check this add-on's preference settings: either the path to such file hasn't been introduced or is incorrect.")
            return {"CANCELLED"}

        open_blend_filepath = bpy.data.filepath

        swtor_shaders_path = bpy.path.native_pathsep(shaders_lib_filepath + "/NodeTree")

        if bpy.data.scenes["Scene"].use_linking_bool:
            self.link = bpy.data.scenes["Scene"].use_linking_bool
            report_text_ending = "linked."
        else:
            report_text_ending = "appended."

        swtor_shaders_names = [
            "SWTOR - Creature Shader",
            "SWTOR - Eye Shader",
            "SWTOR - Garment Shader",
            "SWTOR - HairC Shader",
            "SWTOR - SkinB Shader",
            "SWTOR - Uber Shader",
            "SW Template - Character's Skin Settings"
        ]
        
        if app.version >= (3, 0, 0):
            for swtor_shader_name in swtor_shaders_names:
                try:
                    bpy.ops.wm.append(
                    filename=swtor_shader_name,
                    directory=swtor_shaders_path,
                    do_reuse_local_id=True,
                    set_fake=True,
                    link=self.link
                    )
                except:
                    self.report({"WARNING"}, "Unable to find some or all of the required custom SWTOR Shaders in the .blend file set in this add-on's preference settings. Please check that the filepath is correct and that the .blend file contains all six basic SWTOR shaders.")
                    return {"CANCELLED"}

        else:
            # Blender 2.x.x has no do_reuse_local_id, so,
            # a dedupe of nodegroups is needed.
            for swtor_shader_name in swtor_shaders_names:
                try:
                    bpy.ops.wm.append(
                    filename=swtor_shader_name,
                    directory=swtor_shaders_path,
                    set_fake=True,
                    link=self.link
                    )
                except:
                    self.report({"WARNING"}, "Unable to find some or all of the required custom SWTOR Shaders in the .blend file set in this add-on's preference settings. Please check that the filepath is correct and that the .blend file contains all six basic SWTOR shaders.")
                    return {"CANCELLED"}
            bpy.ops.zgswtor.deduplicate_nodegroups()
                
        self.report({'INFO'}, "Custom SWTOR Shaders " + report_text_ending)

        return {"FINISHED"}



# -------------------------------------------------------------
# Registrations

def register():
    bpy.app.handlers.load_pre.append(handler_new_blendfile)

    bpy.types.Scene.use_linking_bool = bpy.props.BoolProperty(
        name="Link custom materials",
        description='If adding custom SWTOR shaders,\nlink them instead of appending them',
        default=True
    )
    bpy.types.Scene.enable_adding_custom_shaders = bpy.props.BoolProperty(
        name="Disable adding custom SWTOR shaders",
        description='Disable linking custom SWTOR shaders',
    )
    bpy.types.Scene.enable_linking_custom_shaders = bpy.props.BoolProperty(
        name="Disable linking custom SWTOR shaders",
        description='Disable linking custom SWTOR shaders',
    )

    bpy.utils.register_class(ZGSWTOR_OT_add_custom_external_swtor_shaders)


def unregister():
    bpy.app.handlers.load_pre.append(handler_new_blendfile)

    del bpy.types.Scene.use_linking_bool
    del bpy.types.Scene.enable_adding_custom_shaders
    del bpy.types.Scene.enable_linking_custom_shaders

    bpy.utils.unregister_class(ZGSWTOR_OT_add_custom_external_swtor_shaders)


if __name__ == "__main__":
    register()
