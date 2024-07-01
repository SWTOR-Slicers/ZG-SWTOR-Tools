import bpy

# Custom operator to apply transformations
class ZGSWTOR_OT_set_swtor_obj_custom_props(bpy.types.Operator):
    bl_idname = "zgswtor.set_swtor_obj_custom_props"
    bl_label = "Set Custom Properties"
    bl_description = "This tool will be very rarely used, but it can come in handy when dealing with\nobjects, SWTOR's or otherwise, imported with different scales or axis order types.\n\nIt manually applies to a selection of objects, or to all objects in the Scene,\ncustom Object Properties that are relevant to SWTOR tools such as animation\nimporters or Modifiers (and to non-SWTOR objects that will co-exist with them),\nso that it is easy to coordinate them.\n\nIt doesn't actually perform the conversions these properties imply. For that,\nthere is the Apply tool above, which annotates the properties nanyway, if set so"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    # Check that there is a selection of objects
    # (all object types are valid)
    # (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        return len(bpy.data.objects) > 0

    
    use_selection_only: bpy.props.BoolProperty(
        name="Apply To Selected Objects Only",
        description="Set custom object properties in selected objects only",
        default=True,
        options={'HIDDEN'}
    )
    
    gr2_axis_conversion: bpy.props.BoolProperty(
        name="gr2_axis_conversion",
        description="If set to 'ticked' (to True), the object is supposed to have been converted\nto Blender's 'Z-is-Up' coordinate system by 'applying' a x=90º rotation.\n\nSWTOR's coordinate system is 'Y-is-up' vs. Blender's 'Z-is-up'.\nTo compensate for that in a reversible manner, the .gr2 importer\nnormally sets the object's rotation to X=90º at the Object level.\nAs this can be a nuisance outside a modding use case,\nthis can be done ('applied') it at the Mesh level, instead",
        default=False,
        options={'HIDDEN'}
    )
    
    gr2_scale: bpy.props.FloatProperty(
        name="gr2_scale",
        description="If set to a value different to 1.0, the object is supposed\nto have been scaled at the Mesh level by that value.\n\nSWTOR sizes objects in decimeters, while Blender defaults to meters.\nThis mismatch, while innocuous, is an obstacle when doing physics\nsimulations, automatic weighting from bones, or other processes\nwhere Blender requires real world-like sizes to succeed.\n\n(Normally, using the objects' Scale parameter suffices, but when the objects are\nin complicated parent-child hierarchies and inheriting scale values (such as\nwhen parented to a scaled skeleton) they can get difficult to disentangle.\nScaling via 'applying' transformations can simplify things a whole lot)",
        default=1.0,
        options={'HIDDEN'}
    )


    def execute(self, context):
        
        # self.use_selection_only = context.scene.OCP_use_selection_only
        
        objects = context.scene.objects if not self.use_selection_only else context.selected_objects
        
        for obj in objects:
            obj["gr2_axis_conversion"] = self.gr2_axis_conversion
            obj["gr2_scale"] = self.gr2_scale
        
        return {'FINISHED'}


# UI is set in addon_ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_set_swtor_obj_custom_props)
    
    bpy.types.Scene.OCP_use_selection_only = bpy.props.BoolProperty(
        name="Apply To Selected Objects Only",
        description="Set custom object properties in selected objects only",
        default=False,
    )
    
    bpy.types.Scene.OCP_gr2_axis_conversion = bpy.props.BoolProperty(
        name="gr2_axis_conversion",
        description="If set to 'ticked' (to True), the object is supposed to have been converted\nto Blender's 'Z-is-Up' coordinate system by 'applying' a x=90º rotation.\n\nSWTOR's coordinate system is 'Y-is-up' vs. Blender's 'Z-is-up'.\nTo compensate for that in a reversible manner, the .gr2 importer\nnormally sets the object's rotation to X=90º at the Object level.\nAs this can be a nuisance outside a modding use case,\nthis can be done ('applied') it at the Mesh level, instead",
        default=False,
    )
    
    bpy.types.Scene.OCP_gr2_scale = bpy.props.FloatProperty(
        name="gr2_scale",
        description="If set to a value different to 1.0, the object is supposed\nto have been scaled at the Mesh level by that value.\n\nSWTOR sizes objects in decimeters, while Blender defaults to meters.\nThis mismatch, while innocuous, is an obstacle when doing physics\nsimulations, automatic weighting from bones, or other processes\nwhere Blender requires real world-like sizes to succeed.\n\n(Normally, using the objects' Scale parameter suffices, but when the objects are\nin complicated parent-child hierarchies and inheriting scale values (such as\nwhen parented to a scaled skeleton) they can get difficult to disentangle.\nScaling via 'applying' transformations can simplify things a whole lot)",
        default=1.0,
    )

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_set_swtor_obj_custom_props)
    
    del bpy.types.Scene.OCP_use_selection_only
    del bpy.types.Scene.OCP_gr2_axis_conversion
    del bpy.types.Scene.OCP_gr2_scale

if __name__ == "__main__":
    register()
