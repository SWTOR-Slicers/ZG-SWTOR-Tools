# For references to approaches to the subject, see:
# https://blender.stackexchange.com/questions/45992/how-to-remove-duplicated-node-groups
# https://gist.github.com/IPv6/0886731e6e98b6968cb1ffa0b8d5900e
# https://meshlogic.github.io/posts/blender/scripting/eliminate-material-duplicates/ (the one used here)


import bpy



class ZGSWTOR_OT_deduplicate_materials(bpy.types.Operator):

    bl_idname = "zgswtor.deduplicate_materials"
    bl_label = "ZG Deduplicate Materials"
    bl_description = "Replaces all Materials with numbered suffixes (.001, .002, etc.)\nwith instances of the non-suffixed original Materials.\n\nThis operator affects all Materials in the current Scene\nand doesn't require a selection"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls,context):
        if bpy.data.materials:
            return True
        else:
            return False


    def execute(self, context):
        bpy.context.window.cursor_set("WAIT")

        mat_count_report = 0

        mats = bpy.data.materials

        for obj in bpy.data.objects:
            for slot in obj.material_slots:

                # Get the material name as 3-tuple (base, separator, extension)
                (base, sep, ext) = slot.name.rpartition('.')

                # Replace the numbered duplicate with the original if found
                if ext.isnumeric():
                    if base in mats:
                        print("  For object '%s' replace '%s' with '%s'" % (obj.name, slot.name, base))
                        slot.material = mats.get(base)
                        mat_count_report += 1

        bpy.context.window.cursor_set("DEFAULT")
        self.report({'INFO'}, str(mat_count_report) + " duplicate Materials deduped and set to zero users" )
        return {'FINISHED'}


# UI is set in addon_ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_deduplicate_materials)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_deduplicate_materials)

if __name__ == "__main__":
    register()