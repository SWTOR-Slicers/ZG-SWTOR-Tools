from multiprocessing import context
import bpy
from bpy.types import Operator, Panel
from bpy_extras.io_utils import ImportHelper



class ZGSWTOR_PT_SaveImagesBySubstring(Operator, ImportHelper):
    bl_idname = "zgswtor.save_images_by_substring"
    bl_label = "Save Images"
    bl_description = "Save all images in the .Blend project whose names share the piece of text\nentered in the text input field.\n\n• If no text is entered, all images will be saved.\n\n• Requires images with actual image data in them (for example, Image Texture nodes\n   set for baking can hold images that have no data until it is baked into them)"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls,context):
        for img in bpy.data.images:
            if context.scene.SBI_common_text_in_names in img.name:
                return True
        return False

    
    filter_glob: bpy.props.StringProperty(
        default="*.png",
        options={'HIDDEN'},
    )


    # Custom properties
    common_text_in_names: bpy.props.StringProperty(
        name="Common Text",
        description="Specify the common text in the names of all the images\nthat are to be saved.",
        options={'HIDDEN'},
    )

    case_sensitive: bpy.props.BoolProperty(
        name="Case-Sensitive",
        description="The common piece of text has to be an exact upper/lowercase match.",
        default=True,
        options={'HIDDEN'},
    )

    directory: bpy.props.StringProperty(
        subtype='DIR_PATH',
        # options={'HIDDEN'},
    )


    def execute(self, context):
        self.common_text_in_names = context.scene.SBI_common_text_in_names
        self.case_sensitive = context.scene.SBI_case_sensitive

        # Iterate through all images in the current blend file
        for img in bpy.data.images:
            
            if self.case_sensitive:
                test_name = img.name
                test_common_name = self.common_text_in_names
            else:
                test_name = img.name.lower()
                test_common_name = self.common_text_in_names.lower()
                
            if test_common_name in test_name and img.has_data:
                # Save the image to the specified directory. I'm using .save_render
                # because for some reason seems to behave better than .save,
                # at least for freshly created baked texturemaps.

                filepath =  f"{self.directory}/{img.name}.png"
                
                img_settings = context.scene.render.image_settings
                
                img_settings.file_format = 'PNG'
                img_settings.color_mode = 'RGBA'
                
                img.save_render(filepath)

        return {'FINISHED'}



# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_PT_SaveImagesBySubstring)
    
    bpy.types.Scene.SBI_common_text_in_names = bpy.props.StringProperty(
        name="Common Text In Names",
        description="Piece of text common to all the images' names",
        default="BAKED-",
    )
    bpy.types.Scene.SBI_case_sensitive = bpy.props.BoolProperty(
        name="Case-Sensitive",
        description="The common piece of text has to be an exact upper/lowercase match.",
        default=True,
        options={'HIDDEN'},
    )

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_PT_SaveImagesBySubstring)
    
    del bpy.types.Scene.SBI_common_text_in_names
    del bpy.types.Scene.SBI_case_sensitive

if __name__ == "__main__":
    register()
