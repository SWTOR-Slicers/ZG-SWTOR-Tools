import bpy

class ZGSWTOR_OT_sync_with_gr2(bpy.types.Operator):
    bl_idname = "zgswtor.sync_with_gr2"
    bl_label = "Syncronize Some Props With .gr2 Add-on's Ones"
    bl_description = "Operator that syncronizes some of this Add-on's tools' scene properties\n with those of the .gr2 Importer Add-on's preferences when those are modified in\naddon_ui"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
    
        gr2_prefs = bpy.context.preferences.addons["io_scene_gr2"].preferences

        scene_props = bpy.context.scene
        
        scene_props['ZGSAA_ApplySceneScale'] = gr2_prefs.gr2_scale_object
        scene_props['ZGSAA_SceneScaleFactor'] = gr2_prefs.gr2_scale_factor
        
        return {"FINISHED"}


# Registrations
def register():
    bpy.utils.register_class(ZGSWTOR_OT_sync_with_gr2)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_sync_with_gr2)

if __name__ == "__main__":
    register()
