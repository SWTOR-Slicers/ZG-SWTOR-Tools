import bpy
from bpy.types import LayerCollection

class ZGSWTOR_OT_group_collections(bpy.types.Operator):
    bl_idname = "zgswtor.group_collections"
    bl_label = "ZG Group Areas' Collections"
    bl_description = "Groups SWTOR Areas (Collections) using a repeating string in their names\nas a group name separator (an underline, typically).\n\n• As Blender doesn't allow for multiple Collections with the same name,\n   some of them might gain unpleasant '.001'-style suffixes)\n\n• All Collections will be set as disabled in the View Layer to prevent Blender\n   becoming unresponsive in the case of large areas and whole worlds\n   (grouping Collections in new ones would make them visible otherwise)"
    bl_options = {'REGISTER', 'UNDO'}

    levels: bpy.props.IntProperty(
        name="Levels",
        description="Number of levels to group",
        default=1,
        min=1,
        max=100,
    )

    separator: bpy.props.StringProperty(
        name="Separator",
        description="Separator character/s",
        default="_"
    )


    def execute(self, context):
        self.levels = context.scene.GC_coll_grouping_levels
        self.separator = context.scene.GC_coll_grouping_separator

        root_collection = context.scene.collection
        
        self.group_collections_recursive(context, root_collection, self.separator, self.levels, 0)
        
        for coll in bpy.data.collections:
            pass
            
        return {'FINISHED'}



    # Functions
    def group_collections_recursive(self, context, root_collection, separator, levels, current_level):
        if levels <= 0:
            return
                
        view_layer_collections = context.view_layer.layer_collection.children

        # Dict with key = new parent coll and values = list of new children colls
        # (note that keys and values are Collection datablocks, not their names)
        collections_to_group = {}

        # Find collections with similar prefixes and group them in hat Dict
        for child_collection in root_collection.children:
            if child_collection.name[0] != separator:
                child_collection_name_parts = child_collection.name.split(separator)
                if len(child_collection_name_parts) > 1:
                    group_name = child_collection_name_parts[0 + current_level]
                    if group_name not in collections_to_group:
                        collections_to_group[group_name] = [child_collection]
                    else:
                        collections_to_group[group_name].append(child_collection)

        # Process the Dict
        for group_name, group_members in collections_to_group.items():
            # Create a new collection for the group
            new_group = bpy.data.collections.new(group_name)
            root_collection.children.link(new_group)
            
            # Move the group members into the new collection
            for group_member in group_members:
                new_group.children.link(group_member)
                # view_layer_collections[group_member.name].exclude = True

                if group_member.name in bpy.context.scene.collection.children:
                    bpy.context.scene.collection.children.unlink(group_member)
                    # Check the logic of this checking. Might be for failed
                    # or manually moved around cols that no longer are in the
                    # previous parent col
            
                # Delete the branch name from the group_member's name
                group_member.name = group_member.name.split(separator, 1)[1]
            # Recursively group the new collection
            self.group_collections_recursive(context, new_group, separator, levels - 1, current_level)
            
        # Disable all collections in the view layer as a precaution against
        # Blender becoming unresponsive.
        bpy.ops.zgswtor.exclude_all_collections()
            
        return {'FINISHED'}


# ---------------------------------------------------------------------------------



class ZGSWTOR_OT_exclude_all_collections(bpy.types.Operator):
    bl_idname = "zgswtor.exclude_all_collections"
    bl_label = "ZG Exclude All Collections From View Layer"
    bl_description = "Disable/Include all Collections in the View Layer, including Child Collections\n(unticks / ticks their checkboxes in the Outliner)"
    bl_options = {'REGISTER', 'UNDO'}


    untick: bpy.props.BoolProperty(
        name="Disable Collections' in View Layer",
        description="Untick Collections and children Collections's checkboxes in the Outliner",
        default=True
    )

    def execute(self, context):
        # self.untick = bpy.types.Scene.EAC_untick
        root_collection = context.view_layer.layer_collection
        exclude_collection_recursive(root_collection, self.untick)            
        return {'FINISHED'}



# ---------------------------------------------------------------------------------
# Functions

def exclude_collection_recursive( collection, untick):
    for child in collection.children:
        print(child.name)
        if not len(child.children):
            child.exclude = untick
        else:
            exclude_collection_recursive(child, untick)
            child.exclude = untick

    return                






# Registrations

classes = [
    ZGSWTOR_OT_group_collections,
    ZGSWTOR_OT_exclude_all_collections,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.GC_coll_grouping_levels = bpy.props.IntProperty(
        name="Levels",
        description="Levels of Collection grouping (number of separators\nto take into account)",
        min = 1,
        max = 100,
        soft_min = 1,
        soft_max = 10,
        step = 1,
        default = 1
    )
    bpy.types.Scene.GC_coll_grouping_separator = bpy.props.StringProperty(
        name="Separator",
        description="Separator character",
        maxlen= 5,
        default="_"
    )

    bpy.types.Scene.EAC_untick = bpy.props.BoolProperty(
        name="Disable Collections' in View Layer",
        description="Untick Collections and children Collections's checkboxes in the Outliner",
        default=True
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.GC_coll_grouping_levels
    del bpy.types.Scene.GC_coll_grouping_separator



if __name__ == "__main__":
    register()