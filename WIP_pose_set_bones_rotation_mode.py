import bpy

class ZGSWTOR_OT_quickscale(bpy.types.Operator):
    bl_idname = "zgswtor.set_bones_rotation_mode"
    bl_label = "ZG Set Bones' Rotation Mode"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Changes bones' rotation mode from SWTOR's default quaternion to any other one AND BACK. Works in both whole armature objects or specific bones while in Pose Mode."

    # Check that there is a selection of objects (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        return bpy.data.armatures    

    # PROPERTIES

    action: bpy.props.EnumProperty(
        name="Bone Rotation Mode",
        items=[
            ("QUATERNION", "Quaternion", "No Gimbal Lock"),
            ("XYZ", "XYZ Euler", "XYZ Euler: prone to Gimbal Lock"),
            ("XZY", "XZY Euler", "XYZ Euler: prone to Gimbal Lock"),
            ("YXZ", "YXZ Euler", "XYZ Euler: prone to Gimbal Lock"),
            ("YZX", "YZX Euler", "XYZ Euler: prone to Gimbal Lock"),
            ("ZXY", "ZXY Euler", "XYZ Euler: prone to Gimbal Lock"),
            ("ZYX", "ZYX Euler", "XYZ Euler: prone to Gimbal Lock"),
            ("AXIS_ANGLE", "Axis Angle", "Axis Angle (W + XYZ): Defines a rotation around some axis devined by 3D vector"),
            ],
        options={'HIDDEN'}
        )

    use_selection_only : bpy.props.BoolProperty(
        name="Apply To selected Armatures Or Armature Bones Only",
        description="Apply to any armature among a selection of objects, or to\nany selected Bone while in Pose Mode.",
        options={'HIDDEN'},
    )

    
    def execute(self, context):


        scale = bpy.context.scene.zgswtor_quickscale_factor

        selected_objects = [obj for obj in bpy.context.selected_objects if not obj.parent]

        if selected_objects:
            if self.action == "UPSCALE":
                for obj in selected_objects:
                    obj.scale *= scale
                    obj.location *= scale
            elif self.action == "DOWNSCALE":
                for obj in selected_objects:
                    obj.scale /= scale
                    obj.location /= scale

        return {"FINISHED"}


# UI is set in ui.py

# Registrations

def register():
    bpy.types.Scene.zgswtor_quickscale_factor = bpy.props.FloatProperty(
        name="",
        description="Scaling Factor. Recommended values are:\n\n- 10 for simplicity (characters look superhero-like tall, over 2 m.).\n\n- Around 8 for accuracy (characters show more realistic heights)",
        min = 1.0,
        max = 100.0,
        soft_min = 7.0,
        soft_max = 10.0,
        step = 25,
        precision = 2,
        default = 10,
    )
    bpy.utils.register_class(ZGSWTOR_OT_set_bones_rotation_mode)

def unregister():
    del bpy.types.Scene.zgswtor_quickscale_factor
    bpy.utils.unregister_class(ZGSWTOR_OT_set_bones_rotation_mode)


if __name__ == "__main__":
    register()