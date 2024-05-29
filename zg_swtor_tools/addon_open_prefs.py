import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty

# Operator to open the ZG SWTOR Tools' preferences window
class ZGSWTOR_OT_open_zg_preferences(Operator):
    bl_idname = "zgswtor.open_zg_addon_preferences"
    bl_label = "ZG Open ZG SWTOR Tools Add-on's Preferences"

    def execute(self, context):
        bpy.ops.screen.userpref_show(section="ADDONS")
        bpy.ops.preferences.addon_show(module="zg_swtor_tools")
        return {'FINISHED'}


# Operator to open the .gr2 importer add-on's preferences window
class ZGSWTOR_OT_open_gr2_preferences(Operator):
    bl_idname = "zgswtor.open_gr2_addon_preferences"
    bl_label = "ZG Open .gr2 Importer Add-on's Preferences"

    def execute(self, context):
        bpy.ops.screen.userpref_show(section="ADDONS")
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
