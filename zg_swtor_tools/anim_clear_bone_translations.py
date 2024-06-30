import bpy

class ZGSWTOR_OT_clear_bone_translations(bpy.types.Operator):
    bl_idname = "zgswtor.clear_bone_translations"
    bl_label = "Clear Bones' Translations"
    bl_description = "Clears all translation data from all bones in an armature, and\nall keyframes' translations if animated. it's meant to correct\nimperfections in imported animations that distort characters'\nbodies (they might need manual adjustments afterwards to\ncompensate for what the translations added to the poses).\n\nDoesn't affect the GrannyRootBone, Master, and Bip01 bones\nthat contribute to major movements in the stage"
    bl_options = {'REGISTER', 'UNDO'}
    
        
    def execute(self, context):
        obj = context.object
        if obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Active object is not an armature")
            return {'CANCELLED'}
        
        excluded_bones = {"GrannyRootBone", "Master", "Bip01"}
        
        bones = obj.pose.bones
        
        if obj.animation_data and obj.animation_data.action:
            fcurves = obj.animation_data.action.fcurves
            for bone in bones:
                if bone.name in excluded_bones:
                    continue
                for fcurve in fcurves:
                    if fcurve.data_path.startswith(f'pose.bones["{bone.name}"].location'):
                        fcurves.remove(fcurve)
        
        # Clear the translation data by setting location to zero
        for bone in bones:
            if bone.name in excluded_bones:
                continue
            bone.location = (0.0, 0.0, 0.0)
        
        self.report({'INFO'}, "Cleared bone translation data")
        return {'FINISHED'}


# UI is in addon_ui.py


# Registrations
def register():
    bpy.utils.register_class(ZGSWTOR_OT_clear_bone_translations)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_clear_bone_translations)

if __name__ == "__main__":
    register()
