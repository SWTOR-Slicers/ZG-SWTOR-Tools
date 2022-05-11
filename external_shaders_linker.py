import bpy
import os
from pathlib import Path


class ZGSWTOR_OT_external_shaders_linker(bpy.types.Operator):
    bl_idname = "zgswtor.external_shaders_linker"
    bl_label = "SWTOR Tools"
    bl_description = "Links the shaders from the .blend templates file."

    def execute(self, context):

        addon_folder = Path(os.path.dirname(os.path.abspath(__file__)))
        swtor_shaders_blend_file = Path("New SWTOR Custom Shaders.blend")
        shaders_blend_subdir = Path("NodeTree")

#        swtor_shaders_path = str(addon_folder / swtor_shaders_blend_file / shaders_blend_subdir)
        swtor_shaders_path = "/Volumes/RECURSOS/3D SWTOR/SWTOR SHADERS/New SWTOR Custom Shaders.blend/NodeTree"
        
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
                link = True
                )

        return {"FINISHED"}


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_external_shaders_linker)


def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_external_shaders_linker)

if __name__ == "__main__":
    register()