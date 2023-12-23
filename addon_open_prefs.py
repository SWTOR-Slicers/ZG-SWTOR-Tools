import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty

# Operator to open the preferences window
class ZGSWTOR_OT_open_preferences(Operator):
    bl_idname = "zgswtor.open_addon_preferences"
    bl_label = "ZG Open Add-on's Preferences"

    def execute(self, context):
        bpy.ops.screen.userpref_show(section="ADDONS")
        bpy.data.window_managers["WinMan"].addon_search = "ZG SWTOR Tools"
        return {'FINISHED'}

# Register and Unregister
def register():
    bpy.utils.register_class(ZGSWTOR_OT_open_preferences)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_open_preferences)

if __name__ == "__main__":
    register()
