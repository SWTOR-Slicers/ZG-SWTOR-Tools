import bpy


def add_prefix_to_name(obj, prefix):
    """
    Add the prefix to the object's name, avoiding accidental repetition.
    """
    if not obj.name.startswith(prefix):
        if obj.type == "ARMATURE":
            if not bpy.data.armatures[obj.name].name.startswith(prefix):
                bpy.data.armatures[obj.name].name = prefix + bpy.data.armatures[obj.name].name
        obj.name = prefix + obj.name


def add_prefix_to_material_name(obj, prefix):
    """
    Add the prefix to the materials' names of the object.
    """
    for material_slot in obj.material_slots:
        if not material_slot.name.startswith(prefix):
            material_slot.material.name = prefix + material_slot.material.name


def add_prefix_to_collections(obj, prefix):
    """
    Add the prefix to the collections the object belongs to.
    """
    for collection in bpy.data.collections:
        if obj.name in collection.objects:
            if not collection.name.startswith(prefix):
                collection.name = prefix + collection.name



def selected_collections(context):
    """
    Get selected Collections in Outliner without needing to be in that context.
    """
    # Based on
    # https://blender.stackexchange.com/questions/293205/python-how-to-get-selected-collections-list
    # and
    # https://blender.stackexchange.com/questions/203729/python-get-selected-objects-in-outliner

    for area in context.screen.areas:
        if area.type == 'OUTLINER':
            with context.temp_override(area=area):
                return [item for item in context.selected_ids if isinstance(item, bpy.types.Collection)]
            

class SWTOR_OT_AddPrefixOperator(bpy.types.Operator):
    """"""
    bl_idname = "swtor.add_prefix_operator"
    bl_description = "Adds a prefix to the names of all selected Objects, their Materials, and the Collections they are linked to.\nThis renaming is necessary to avoid name collisions between successive character imports in a same Blender project.\n\nPlease include your own separators between the prefix and the names: spaces, a hyphen, etc.\n\n• Requires a selection of objects"
    bl_label = "Prefix Names In Selected Objects, Their Materials And Collections They Are Linked To"
    bl_options = {'REGISTER', 'UNDO'}

    # Check that there is a selection of objects and that we are in Object mode
    # (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects and bpy.context.mode == "OBJECT":
            return True
        else:
            return False

    prefix: bpy.props.StringProperty(name="Prefix", default="")

    def execute(self, context):
        selected_objects = context.selected_objects
        
        self.prefix = context.scene.prefix  # Retrieve the prefix from the scene property
        
        for obj in selected_objects:
            add_prefix_to_name(obj, self.prefix)
            add_prefix_to_material_name(obj, self.prefix)
            add_prefix_to_collections(obj, self.prefix)

        return {'FINISHED'}


class SWTOR_PT_AddPrefixPanel(bpy.types.Panel):
    """Add Prefix Panel"""
    bl_label = "Character Prefixer"
    bl_idname = "SWTOR_PT_add_prefix_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SWTOR Character Tools"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.scale_y = 0.7
        col.label(text="Adds a prefix to all selected")
        col.label(text="Objects, their Materials, and")
        col.label(text="Collections they are linked to.")
        col.label(text=" ")

        col.label(text="Recommended after importing")
        col.label(text="a Character or a set of armor,")
        col.label(text="to prevent name collisions with")
        col.label(text="further Character importings.")
        col.label(text=" ")

        col.label(text="Please include your own")
        col.label(text="separators at the end of the")
        col.label(text="prefix (spaces, hyphens, etc.):")

        # col.label(text=" ")

        row = layout.row()
        row.prop(context.scene, 'prefix', text="")

        row = layout.row()
        row.operator("swtor.add_prefix_operator", text="Add Prefix")


def register():
    bpy.utils.register_class(SWTOR_OT_AddPrefixOperator)
    bpy.utils.register_class(SWTOR_PT_AddPrefixPanel)
    bpy.types.Scene.prefix = bpy.props.StringProperty(
        name="Prefix text",
        description = "Text to prefix the names of all selected Objects, their Materials, and the Collections they are linked to with.\nThis renaming is necessary to avoid name collisions between successive character imports in a same Blender project.\n\nPlease include your own separators between the prefix and the names: spaces, a hyphen, etc.\n\n• Requires a selection of objects",
        default=""
        )


def unregister():
    bpy.utils.unregister_class(SWTOR_OT_AddPrefixOperator)
    bpy.utils.unregister_class(SWTOR_PT_AddPrefixPanel)
    del bpy.types.Scene.prefix


if __name__ == "__main__":
    register()
