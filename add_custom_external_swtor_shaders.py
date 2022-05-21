import bpy
import os
from pathlib import Path
from bpy.app.handlers import persistent

print("-------------")
print("CALLED")
print("-------------")

# Handler for detecting opening a new blendfile and updating
# UI options properties accordingly
@persistent
def handler_new_blendfile(scene):
    # Check that we aren't editing the custom shaders template file
    # to prevent from appending/linking the shaders to itself
    # and set a prop to control the UI's related widgets
    
    shaders_lib_filepath = bpy.context.preferences.addons[__package__].preferences.swtor_custom_shaders_blendfile_path
        
    open_blend_filepath = bpy.data.filepath
        
    if open_blend_filepath == shaders_lib_filepath:
        bpy.context.scene.enable_adding_custom_shaders = False
        bpy.context.scene.enable_linking_custom_shaders = False
    else:
        bpy.context.scene.enable_adding_custom_shaders = True
        bpy.context.scene.enable_linking_custom_shaders = True

    print("----------------------")
    print("Pref =", shaders_lib_filepath)
    print("blend=", open_blend_filepath)

    print("HANDL - adding = ",bpy.context.scene.enable_adding_custom_shaders)
    print("HANDL - linking= ",bpy.context.scene.enable_linking_custom_shaders)

        
bpy.app.handlers.load_post.append(handler_new_blendfile)



class ZGSWTOR_OT_add_custom_external_swtor_shaders(bpy.types.Operator):
    bl_idname = "zgswtor.add_custom_external_swtor_shaders"
    bl_label = "SWTOR Tools"
    bl_description = "Appends or links custom SWTOR shaders from\nan external .blend templates file."
    bl_options = {'REGISTER', 'UNDO'}

    # @classmethod
    # def poll(cls,context):
    #     shaders_lib_filepath = context.preferences.addons[__package__].preferences.swtor_custom_shaders_blendfile_path
    #     open_blend_filepath = bpy.data.filepath
    #     if open_blend_filepath != shaders_lib_filepath:
    #         return True
    #     else:
    #         return False

    # linking vs appending flag property
    link: bpy.props.BoolProperty(
        name="Link custom shaders",
        description='If adding custom SWTOR shaders,\nlink them instead of appending them',
        default = False,
        options={'HIDDEN'}
        )

    def execute(self, context):

        shaders_lib_filepath = context.preferences.addons[__package__].preferences.swtor_custom_shaders_blendfile_path
        
        open_blend_filepath = bpy.data.filepath
        
        # if open_blend_filepath == shaders_lib_filepath:
        #     context.scene.enable_adding_custom_shaders = False
        #     context.scene.enable_linking_custom_shaders = False
        # else:
        #     context.scene.enable_adding_custom_shaders = True
        #     context.scene.enable_linking_custom_shaders = True


        swtor_shaders_path = bpy.path.native_pathsep(shaders_lib_filepath + "/NodeTree")

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
    bpy.app.handlers.load_pre.append(handler_new_blendfile)

    bpy.types.Scene.use_linking_bool = bpy.props.BoolProperty(
        name="Link custom materials",
        description='If adding custom SWTOR shaders,\nlink them instead of appending them',
        default = False
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