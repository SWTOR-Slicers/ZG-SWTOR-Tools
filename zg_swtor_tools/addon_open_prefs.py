import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty



def blender_prefs_with_custom_size(pref_window_width,  pref_window_height):
    # based on code by "Rombout Versluijs, Pan Beep (Beep) https://github.com/schroef.
    # See:
    # https://github.com/schroef/Custom-Preferences-Size
    # and:
    # https://projects.blender.org/blender/blender/issues/71935#818493
    
    # This sets the prefs window's dimensions and opens it,
    # but once open it sets its values back to their original settings
    # for future manual openings as a precaution.
    
    # Modify scene settings
    render = bpy.context.scene.render
    prefs = bpy.context.preferences
    view = prefs.view
    orgResX = render.resolution_x
    orgResY = render.resolution_y
    render.resolution_x = int(pref_window_width)
    render.resolution_y = int(pref_window_height)
    orgDispMode = view.render_display_type
    view.render_display_type = "WINDOW"

    # Call image editor window
    bpy.ops.render.view_show("INVOKE_DEFAULT")

    # Change area type
    area = bpy.context.window_manager.windows[-1].screen.areas[0]
    area.type = "PREFERENCES"

    # Restore old values
    view.render_display_type = orgDispMode
    render.resolution_x = orgResX
    render.resolution_y = orgResY


# Operator to open the ZG SWTOR Tools' preferences window
class ZGSWTOR_OT_open_zg_preferences(Operator):
    bl_idname = "zgswtor.open_zg_addon_preferences"
    bl_label = "ZG Open ZG SWTOR Tools Add-on's Preferences"
    bl_description = "Open ZG SWTOR Tools Add-on's Preferences"

    def execute(self, context):
        # bpy.ops.screen.userpref_show(section="ADDONS")
        
        blender_prefs_with_custom_size(640, 512)
        bpy.ops.preferences.addon_show(module="zg_swtor_tools")
        return {'FINISHED'}


# Operator to open the .gr2 importer add-on's preferences window
class ZGSWTOR_OT_open_gr2_preferences(Operator):
    bl_idname = "zgswtor.open_gr2_addon_preferences"
    bl_label = "ZG Open .gr2 Importer Add-on's Preferences"


    def execute(self, context):
        # bpy.ops.screen.userpref_show(section="ADDONS")
        
        blender_prefs_with_custom_size(640, 512)
        bpy.ops.preferences.addon_show(module="io_scene_gr2")
        return {'FINISHED'}


# Registrations
def register():
    bpy.utils.register_class(ZGSWTOR_OT_open_zg_preferences)
    bpy.utils.register_class(ZGSWTOR_OT_open_gr2_preferences)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_open_gr2_preferences)
    bpy.utils.unregister_class(ZGSWTOR_OT_open_zg_preferences)

if __name__ == "__main__":
    register()
