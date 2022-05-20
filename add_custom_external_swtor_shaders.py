import bpy
import os
from pathlib import Path


class ZGSWTOR_OT_add_custom_external_swtor_shaders(bpy.types.Operator):
    bl_idname = "zgswtor.add_custom_external_swtor_shaders"
    bl_label = "SWTOR Tools"
    bl_description = "Appends or links custom SWTOR shaders from\nan external .blend templates file."
    bl_options = {'REGISTER', 'UNDO'}


    # Checks that we aren't working on the .blend file holding the
    # customized SWTOR shaders templates, greying out the UI widgets otherwise.
    @classmethod
    def poll(cls,context):
        new_shaders_filepath = bpy.context.preferences.addons[__package__].preferences.swtor_custom_shaders_blendfile_path        
        open_blend_file = bpy.data.filepath
        if new_shaders_filepath == open_blend_file:
            return False
        else:
            return True


    # linking vs appending flag property
    link: bpy.props.BoolProperty(
        name="Link custom shaders",
        description='If adding custom SWTOR shaders,\nlink them instead of appending them',
        default = False,
        options={'HIDDEN'}
        )


    def execute(self, context):

        new_shaders_filepath = bpy.context.preferences.addons[__package__].preferences.swtor_custom_shaders_blendfile_path
        
        open_blend_file = bpy.data.filepath
        
        if open_blend_file == new_shaders_filepath:
            context.scene.blendfile_is_template_bool = True
        else:
            context.scene.blendfile_is_template_bool = False

        swtor_shaders_path = bpy.path.native_pathsep(bpy.context.preferences.addons[__package__].preferences.swtor_custom_shaders_blendfile_path + "/NodeTree")

        if bpy.data.scenes["Scene"].use_linking_bool:
            self.link = bpy.data.scenes["Scene"].use_linking_bool
    
        swtor_shaders_names = [
            "SWTOR - Creature Shader",
            "SWTOR - Eye Shader",
            "SWTOR - Garment Shader",
            "SWTOR - HairC Shader",
            "SWTOR - SkinB Shader",
            "SWTOR - Uber Shader"
        ]
        for swtor_shader_name in swtor_shaders_names:
            bpy.ops.wm.append(
                filename = swtor_shader_name,
                directory = swtor_shaders_path,
                do_reuse_local_id = True,
                set_fake = True,
                link = self.link
                )

        return {"FINISHED"}


# Registrations

def register():
    bpy.types.Scene.use_linking_bool = bpy.props.BoolProperty(
        name="Link custom materials",
        description='If adding custom SWTOR shaders,\nlink them instead of appending them',
        default = True
    )
    bpy.types.Scene.blendfile_is_template_bool = bpy.props.BoolProperty(
        name="Blend File is Shaders Template File",
        description='Flag to hide UI options while editing the .blend file containing the custom shaders',
        default = True,
    )

    bpy.utils.register_class(ZGSWTOR_OT_add_custom_external_swtor_shaders)


def unregister():
    del bpy.types.Scene.use_linking_bool
    del bpy.types.Scene.blendfile_is_template_bool

    bpy.utils.unregister_class(ZGSWTOR_OT_add_custom_external_swtor_shaders)

if __name__ == "__main__":
    register()