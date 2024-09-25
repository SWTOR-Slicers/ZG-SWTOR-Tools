import bpy

# Custom operator to apply transformations
class ZGSWTOR_OT_apply_transforms(bpy.types.Operator):
    bl_idname = "zgswtor.apply_transforms"
    bl_label = "Apply Transforms & Custom Props"
    bl_description = "Apply Transformations operators to convert SWTOR objects and skeletons' scales and rotations.\n\n• Requires a selection of objects\n\nTypically, they only might need to be used on SWTOR objects imported with the default, neutral\nsettings, which produce 1/10 of \"real life\" sizes and apply a 90º x-rotation to match Blender's\nZ-is-up axis scheme. For those, only applying Rotation and/or Scale is needed.\n\n(Position is there, too, but mostly for completeness' sake)\n\nThese tools are the same as the Apply tools Blender offers in the Object > Apply menu, but they\nare set to use the Apply Properties option (which would usually mean a trip to the Undo Box\nto tick its checkbox), so that the transforms are applied on any involved Modifiers and the like.\n\nIt is recommended to use these tools on objects that are in a neutral position (0,0,0) and\n rotation (either 0º,0º,0º, or the old, usual axis-correcting 90º,0º,0º)"


    # Check that there is a selection of objects (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects:
            return True
        else:
            return False


    action: bpy.props.EnumProperty(
        name="Action",
        items=[
            ('LOCATION', "Position", "Apply position transformation"),
            ('ROTATION', "Rotation", "Apply rotation transformation"),
            ('SCALE', "Scale", "Apply scale transformation"),
            ('ROTATION_SCALE', "Rotation+Scale", "Apply Scale and Rotation transformations"),
            ('ALL', "All", "Apply All transformations"),
        ],
        options={'HIDDEN'}
    )
    
    set_custom_props: bpy.props.BoolProperty(
        name="Set Custom .gr2 Object Properties",
        description="Annotates SWTOR Objects/Skeletons with custom properties that store the\nscale and axis conversion data relative to what a SWTOR object with neutral\nimport settings would show (gr2_scale = 1.0, gr2_axis_conversion = False)\n\n(Position data isn't included)",
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

        elif self.action == 'LOCATION':
            bpy.ops.object.transform_apply(location=True, rotation=False, scale=False, properties=True)
        elif self.action == 'ROTATION':
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False, properties=True)
        if self.action == 'SCALE':
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=True)
        elif self.action == 'ROTATION_SCALE':
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True, properties=True)
        elif self.action == 'ALL':
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True, properties=True)


        return {'FINISHED'}


# UI is set in addon_ui.py


# Registrations
def register():
    
    bpy.types.Scene.OAT_set_custom_props = bpy.props.BoolProperty(
        name="Set Custom .gr2 Object Properties",
        description="Annotates SWTOR Objects/Skeletons with custom properties that store the\nscale and axis conversion data relative to what a SWTOR object with neutral\nimport settings would show (gr2_scale = 1.0, gr2_axis_conversion = False)\n\n(Position data isn't included)",
        default = True,
    )
    
    bpy.utils.register_class(ZGSWTOR_OT_apply_transforms)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_apply_transforms)
    del bpy.types.Scene.OAT_set_custom_props

if __name__ == "__main__":
    register()
