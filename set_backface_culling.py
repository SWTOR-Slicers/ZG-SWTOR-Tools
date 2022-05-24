import bpy

class ZGSWTOR_OT_set_backface_culling(bpy.types.Operator):
    bl_idname = "zgswtor.set_backface_culling"
    bl_label = "ZG Backface Culling"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Sets the selected objects' materials' Backface Culling.\nIf set to on, single-sided objects' rear faces become invisible.\n\nIf the materials are shared by several objects,\nthe effect will affect those objects, too, even if not selected"

    # Check that there is a selection of objects (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects:
            return True
        else:
            return False


    # Property for the UI buttons to call different actions.
    # See: https://b3d.interplanety.org/en/calling-functions-by-pressing-buttons-in-blender-custom-ui/
    action: bpy.props.EnumProperty(
        name="Backface Culling",
        items=[
            ("BACKFACE_CULLING_ON", "On", "On"),
            ("BACKFACE_CULLING_OFF", "Off", "Off")
            ]
        )

    # Methods doing the actual setting of Backface Culling    
    @staticmethod
    def set_backface_culling_on(mats):
        for mat in mats:
            mat.use_backface_culling = True

    @staticmethod
    def set_backface_culling_off(mats):
        for mat in mats:
            mat.use_backface_culling = False

    
    def execute(self, context):
        bpy.context.window.cursor_set("WAIT")

        selected_objects = [obj for obj in bpy.context.selected_editable_objects
                            if obj.type == "MESH" and not "skeleton" in obj.name]
        
        if selected_objects:
            
            mats = []
            
            for obj in selected_objects:
                for mat_slot in obj.material_slots:
                    mats.append(mat_slot.material)

            if mats:
                if self.action == "BACKFACE_CULLING_ON":
                    self.set_backface_culling_on(mats)
                elif self.action == "BACKFACE_CULLING_OFF":
                    self.set_backface_culling_off(mats)

            bpy.context.window.cursor_set("DEFAULT")
            return {"FINISHED"}

        else:
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, "No objects with materials were selected.")
            return {"CANCELLED"}


# UI is set in ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_set_backface_culling)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_set_backface_culling)

if __name__ == "__main__":
    register()