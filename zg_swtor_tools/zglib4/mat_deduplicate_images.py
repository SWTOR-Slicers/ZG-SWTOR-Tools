# For references to approaches to the subject, see:
# https://blender.stackexchange.com/questions/45992/how-to-remove-duplicated-node-groups
# https://gist.github.com/IPv6/0886731e6e98b6968cb1ffa0b8d5900e
# https://meshlogic.github.io/posts/blender/scripting/eliminate-material-duplicates/ (the one used here)


import bpy



class ZGSWTOR_OT_deduplicate_images(bpy.types.Operator):

    bl_idname = "zgswtor.deduplicate_images"
    bl_label = "ZG Deduplicate Images"
    bl_description = "Replaces all images whose names end with numbered suffixes\n(.001, .002, etc.) with instances of a non-suffixed original.\n\nThis operator affects all images in the current Scene\nand doesn't require a selection"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls,context):
        if bpy.data.images:
            return True
        else:
            return False


    def execute(self, context):
        bpy.context.window.cursor_set("WAIT")

        img_count_report = 0

        for img in bpy.data.images:
            if img.name[-3:].isdigit():
                img.user_remap(img)
                bpy.data.images.remove(img)
                img_count_report += 1

        bpy.context.window.cursor_set("DEFAULT")
        self.report({'INFO'}, str(img_count_report) + " duplicate images deduped and set to zero users" )
        return {'FINISHED'}


# UI is set in ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_deduplicate_images)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_deduplicate_images)

if __name__ == "__main__":
    register()