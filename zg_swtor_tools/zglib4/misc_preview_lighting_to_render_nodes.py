import bpy

import os
from pathlib import Path
from bpy.app.handlers import persistent


class ZGSWTOR_OT_preview_lighting_to_render_nodes(bpy.types.Operator):
    bl_idname = "zgswtor.preview_lighting_to_render_nodes"
    bl_label = "ZG Convert current preview lighting settings to World nodes"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}


    # @classmethod
    # def poll(cls,context):
    #     if bpy.context.selected_objects:
    #         return True
    #     else:
    #         return False

    
    
    def execute(self, context):
        current_window = bpy.context.screen
        return {"FINISHED"}


# UI





# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_preview_lighting_to_render_nodes)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_preview_lighting_to_render_nodes)


if __name__ == "__main__":
    register()