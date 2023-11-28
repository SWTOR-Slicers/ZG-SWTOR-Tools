import bpy

class ZGSWTOR_OT_set_dds(bpy.types.Operator):
    bl_idname = "zgswtor.set_dds"
    bl_label = "ZG Set .dds"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Sets all .dds texture files to Non-Color\nso that Blender process them as raw data.\n\nThis operator affects all .dds in the current Scene\nand doesn't require a selection"


    
    def execute(self, context):
        bpy.context.window.cursor_set("WAIT")

        selected_texturemaps = [img for img in bpy.data.images if ".dds" in img.name]
        
        if selected_texturemaps:
            
            for img in selected_texturemaps:
                print(img.name)
                img.colorspace_settings.name = "Non-Color"

            bpy.context.window.cursor_set("DEFAULT")
            return {"FINISHED"}

        else:
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, "No texturemaps with names containing '.dds' found.")
            return {"CANCELLED"}


# UI is set in ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_set_dds)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_set_dds)

if __name__ == "__main__":
    register()