import bpy

class ZGSWTOR_OT_copypaste_palettes(bpy.types.Operator):

    bl_label = "ZG CopyPaste SWTOR Shader Palette Data"
    bl_idname = "zgswtor.copypaste_palettes"
    bl_description = 'Copies palette data between SWTOR shaders.\n\n• Requires an Active object with a modern or custom SWTOR Shader to copy from, and a selection of objects with SWTOR shaders to paste to'
    bl_options = {'REGISTER', 'UNDO'}

    # ------------------------------------------------------------------
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
        name="Scaling Type",
        items=[
            ("copy_p1", "Copy Palette1 Data", "Copy Palette1 Data"),
            ("copy_p2", "Copy Palette2 Data", "Copy Palette2 Data"),
            ("copy_pp", "Copy both Palettes Data", "Copy both Palettes Data"),
            ("paste_p1", "Paste Palette1 Data", "Paste Palette1 Data"),
            ("paste_p2", "Paste Palette2 Data", "Paste Palette2 Data"),
            ("paste_pp", "Paste both Palettes Data", "Paste both Palettes Data"),
            ("paste_p12", "Paste Palette1 Data to P2", "Paste Palette1 Data to P2"),
            ("paste_p21", "Paste Palette2 to P1", "Paste Palette2 to P1"),
            ("paste_pp1221", "Cross-Paste both Palettes Data", "Cross-Paste both Palettes Data"),
            ],
        options={'HIDDEN'}
        )


    # METHODS

    @staticmethod
    def copy_p1(obj):
        if not "Subdivision" in obj.modifiers:
            mod = obj.modifiers.new(name= "Subdivision", type="SUBSURF")


    def execute(self, context):
        
        selected_objects = [obj for obj in bpy.context.selected_editable_objects
                            if obj.type == "MESH" and not "skeleton" in obj.name]
        
        if selected_objects:
            bpy.context.window.cursor_set("WAIT")
            for selected_obj in selected_objects:
                obj = bpy.data.objects[selected_obj.name]
                if self.action == "copy_p1":
                    self.copy_p1(obj)
                elif self.action == "copy_p2":
                    self.copy_p2(obj)
                elif self.action == "copy_pp":
                    self.copy_pp(obj)
                elif self.action == "paste_p1":
                    self.paste_p1(obj)
                elif self.action == "paste_p2":
                    self.paste_p2(obj)
                elif self.action == "paste_pp":
                    self.paste_pp(obj)
                elif self.action == "paste_p12":
                    self.paste_p12(obj)
                elif self.action == "paste_p21":
                    self.paste_p21(obj)
                elif self.action == "paste_pp1221":
                    self.paste_pp1221(obj)


            bpy.context.window.cursor_set("DEFAULT")
            return {"FINISHED"}

        else:
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, "No modifiable objects were selected.")
            return {"CANCELLED"}


# UI is set in ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_copypaste_palettes)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_copypaste_palettes)

if __name__ == "__main__":
    register()