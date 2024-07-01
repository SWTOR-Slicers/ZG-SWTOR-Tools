import bpy

# Custom operator to apply transformations
class ZGSWTOR_OT_apply_transforms(bpy.types.Operator):
    bl_idname = "zgswtor.apply_transforms"
    bl_label = "Apply Transforms & Custom Props"
    bl_description = "Apply Transformations operators to convert SWTOR objects and skeletons' scales and axis orders\nso that they match others that were imported with different .gr2 import settings (for example,\nobjects imported with older versions of the .gr2 Importer Add-on and objects done with the\n most recent one's scale and/or axis conversion settings.\n\nIdeally, this tool would be applied to objects that are in a neutral position (0,0,0) and\n rotation (either 0º,0º,0º, or the old, usual axis-correcting 90º,0º,0º).\n\nannotated or modified accordingly"


    action: bpy.props.EnumProperty(
        name="Action",
        items=[
            ('BOTH', "Both", "Apply Scale and Rotation transformations"),
            ('SCALE', "Scale", "Apply scale transformation"),
            ('ROTATION', "Rotation", "Apply rotation transformation"),
        ],
        options={'HIDDEN'}
    )
    
    set_custom_props: bpy.props.BoolProperty(
        name="Set Custom .gr2 Object Properties",
        description="Creates or modifies SWTOR Objects/Skeletons' custom properties to annotate\nscale and axis conversion data relative to what a SWTOR object with neutral\nimport settings would show (gr2_scale = 1.0, gr2_axis_conversion = False)",
        default=True,
        options={'HIDDEN'}
    )

    def execute(self, context):
        self.set_custom_props = context.scene.OAT_set_custom_props
        
        if self.set_custom_props:
            for obj in context.selected_objects:
                if self.action == 'BOTH' or self.action == 'SCALE':
                    if 'gr2_scale' in obj:
                        obj['gr2_scale'] *= obj.scale[0]
                    else:
                        obj['gr2_scale'] = obj.scale[0]
                        
                if self.action == 'BOTH' or self.action == 'ROTATE':
                    obj['gr2_axis_conversion'] = obj.rotation_euler[0] != 1.5707963705062866

        if self.action == 'SCALE':
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=True)
        elif self.action == 'ROTATION':
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False, properties=True)
        elif self.action == 'BOTH':
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True, properties=True)


        return {'FINISHED'}


# UI is set in addon_ui.py


# Registrations
def register():
    
    bpy.types.Scene.OAT_set_custom_props = bpy.props.BoolProperty(
        name="Set Custom .gr2 Object Properties",
        description="Creates or modifies SWTOR Objects/Skeletons' custom properties to annotate\nscale and axis conversion data relative to what a SWTOR object with neutral\nimport settings would show (gr2_scale = 1.0, gr2_axis_conversion = False)",
        default = True,
    )
    
    bpy.utils.register_class(ZGSWTOR_OT_apply_transforms)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_apply_transforms)
    del bpy.types.Scene.OAT_set_custom_props

if __name__ == "__main__":
    register()
