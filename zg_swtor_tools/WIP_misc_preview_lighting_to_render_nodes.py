import bpy

import os
from pathlib import Path
from bpy.app.handlers import persistent

# references:
# https://blender.stackexchange.com/questions/262233/how-do-i-grab-the-header-in-an-area/262239#262239
# https://docs.blender.org/manual/en/latest/interface/window_system/introduction.html

# The main Blender window sub-windows are called areas. Each area is a container for an editor. The area container is further subdivided into up to 5 regions, only two of which are always visible: the main region and the header region. The other areas include the toolbar on the right, the side panel on the right, and the last operation panel on the lower left.

# You can't have a header without the main region and you can't have a main region without a header.

# However, the header is a type of menu and you can create menus that mimic it in full or in part. These menus can pop up in the main region. Most of the context menus in the 3D Viewport are submenus of the header menu, for example.


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