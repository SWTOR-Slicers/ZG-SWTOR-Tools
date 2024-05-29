from os import unlink
import bpy


def selected_collections():
    '''
    Returns selected collections
    in Outliner
    '''
    
    context = bpy.context

    selected_collections = []

    screen=context.window.screen
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'OUTLINER':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        with context.temp_override(
                            screen=screen,
                            window=window,
                            area=area,
                            region=region,
                        ):
                            if context.space_data.display_mode == "VIEW_LAYER":
                                for item in context.selected_ids:
                                    if item.bl_rna.identifier == "Collection":
                                        selected_collections.append(item)
                                # We can break the area looping here
                                return selected_collections
                                
    return selected_collections


class ZGSWTOR_OT_group_collections(bpy.types.Operator):
    bl_idname = "zgswtor.group_collections"
    bl_label = "ZG Group Areas' Collections"
    bl_description = "Groups SWTOR Areas (Collections) based on a common initial part of their names\npreceding a selected separator (a repeating underline, typically).\n\n• Grouping Collections are prefixed with an hyphen to prevent naming conflicts\n   (as Blender doesn't allow for multiple Collections with the same name,\n   it would start adding ugly '.001'-style suffixes around).\n\n• The results will be ordered alphabetically.\n\n• All grouped Collections will be set as Disabled in the View Layer to prevent Blender\n   becoming unresponsive in the case of large areas and whole worlds\n   (grouping Collections in new ones makes them visible otherwise)."
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls,context):
        if bpy.data.collections:
            return True
        else:
            return False

    action: bpy.props.EnumProperty(
        name="Group Collections",
        description = "Groups SWTOR Areas (Collections) based on a common initial part of their names\npreceding a selected separator (an underline, typically) and its index if it is a repeating one.\n\n• Selected Collections must be at a same level in the Outliner's hierarchy.\n\n• As Blender doesn't allow for multiple Collections with the same name,\n   some of them might gain unpleasant '.001'-style suffixes)\n\n• All grouped Collections will be set as disabled in the View Layer to prevent Blender\n   becoming unresponsive in the case of large areas and whole worlds\n   (grouping Collections in new ones would make them visible otherwise)",
        items=[
            ("GROUP_SEL", "Group Selection", "Group Selection"),
            ("GROUP_ALL", "Group All", "Group All"),
            ('FLATTEN_ALL', "Flatten And Clean Hierarchy", "Put all Collections directly under the Scene Collection\nand delete the emptied Grouping Collections")
            ],
        options={'HIDDEN'},
    )

    separator: bpy.props.StringProperty(
        name="Separator",
        description="Separator character in the Collections' names (típically an underline)",
        default="_",
        options={'HIDDEN'},
    )

    position: bpy.props.IntProperty(
        name="Position",
        description="Position of the separator that will determine the common part\nof the Collections' names to group them by",
        default=1,
        min=1,
        max=99,
        options={'HIDDEN'},
    )

    disable_collections: bpy.props.BoolProperty(
        name="Disable Collections in ViewLayer",
        description="All Collections are set as disabled in the View Layer to keep\nBlender responsive in the case of large areas and whole worlds\n(normally, grouping Collections into new ones makes them visible)",
        default=True,
        options={'HIDDEN'},
    )

    sort_collections: bpy.props.BoolProperty(
        name="Sort Collections in Outliner",
        description="Orders the Collections in the Outliner alphabetically. If disabled,\nGrouped Collections will be added to the bottom of the Outliner\nby creation order.",
        default=True,
        options={'HIDDEN'},
    )


    def execute(self, context):
        self.position = context.scene.GC_coll_grouping_position
        self.separator = context.scene.GC_coll_grouping_separator
        self.disable_collections = context.scene.GC_disable_collections
        self.sort_collections = context.scene.GC_sort_collections

        if self.action == "GROUP_ALL":
            group_collections(bpy.data.collections, self.separator, self.position)
        elif self.action == "GROUP_SEL":
            group_collections(selected_collections(), self.separator, self.position)
        elif self.action == "FLATTEN_ALL": # YET TO BE FINISHED
            flatten_all_collections(cleanup=True)

        if self.sort_collections:
            sort_all_collections()
        
        if self.disable_collections:
            # Disable all collections in the view layer as a precaution against
            # Blender becoming unresponsive.
            bpy.ops.zgswtor.exclude_include_collections(action='DISABLE_ALL')
            
        return {'FINISHED'}



def group_collections(collections, separator, pos):
    """
    Groups collections based on the common part of their names up to the nth repetition of the separator.
    Includes collections whose name is short by one separator from the chosen occurrence.
    Ensures that resulting grouping collections are children of the same parent collection if applicable.
    
    :param collections: List of collections to be grouped
    :param separator: Separator string used in collection names
    :param pos: position of the separator to consider for grouping
    """
    # Create a dictionary to hold the groups
    
    is_selection = collections != bpy.data.collections
    
    grouped_collections = {}

    for collection in collections:
        if collection.name.startswith('- '):
            continue
        
        # Split the collection name using the separator
        parts = collection.name.split(separator)
        
        # Determine the common name up to the nth repetition of the separator
        if len(parts) >= pos:
            common_name = separator.join(parts[:pos])
        elif len(parts) == pos - 1:
            common_name = separator.join(parts[:pos-1])
        else:
            continue
        
        # Determine the parent collection
        parent_collection = None
        # if is_selection:
        for parent in bpy.data.collections:
            if collection in list(parent.children):
                parent_collection = parent
                break
        
        # Create or retrieve the grouping collection
        group_name = f"- {common_name}"
        
        if (group_name, parent_collection) not in grouped_collections:
            # Prevent re-nesting if the grouping collection existed already
            if group_name in bpy.data.collections:
                continue
            
            # Create a new collection for the group if it doesn't exist
            new_collection = bpy.data.collections.new(name=group_name)
            if parent_collection:
                parent_collection.children.link(new_collection)
            else:
                bpy.context.scene.collection.children.link(new_collection)
            grouped_collections[(group_name, parent_collection)] = new_collection
        
        # Move the collection under the grouping collection
        grouped_collections[(group_name, parent_collection)].children.link(collection)
        if parent_collection:
            parent_collection.children.unlink(collection)
        else:
            bpy.context.scene.collection.children.unlink(collection)


def sort_all_collections():
    '''
    https://blender.stackexchange.com/questions/157562/sorting-collections-alphabetically-in-the-outliner
    Unlinks all collections and relinks them by alphabetical order,
    as Blender only orders collections by the order they were linked
    (the Outliner only sorts objects alphabetically, not Collections).
    Works through all Scenes in the Blender project.
    '''
    collections = bpy.data.collections[:]
    collections.extend(scene.collection for scene in bpy.data.scenes)
    for col in collections:
        for c in sorted(col.children, key=lambda c: c.name.lower()):
            col.children.unlink(c)
            col.children.link(c)


def sort_selected_collection():
    '''
    https://blender.stackexchange.com/questions/157562/sorting-collections-alphabetically-in-the-outliner
    '''
    context = bpy.context

    def all_colls(c):
        def walk(col):
            yield col
            for c in col.children:
                yield from walk(c)
        return set(walk(c))

    assert(context.collection) # poll cannot be None.

    for col in all_colls(context.collection):
        for c in sorted(col.children, key=lambda c: c.name.lower()):
            col.children.unlink(c)
            col.children.link(c)


def get_collections_hierarchy():
    '''
    Generates a dict with collections' names as keys
    and a list of their parent collections' names as values
    '''
    def find_parent_collection(child_collection):
        # Iterate through all collections in the scene
        for collection in bpy.data.collections:
            if child_collection.name in collection.children.keys():
                return collection
        return None

    collections_dict = {}
    
    # Iterate through all collections in the scene
    for collection in bpy.data.collections:
        parent_collection = find_parent_collection(collection)
        if parent_collection:
            collections_dict[collection.name] = parent_collection.name
        else:
            collections_dict[collection.name] = None  # No parent collection (it's a top-level collection)
    
    return collections_dict


def collection_has_objects(collection):
    # Check if the collection has any objects directly
    if collection.objects:
        return True
    
    # Recursively check child collections
    for child_collection in collection.children:
        if collection_has_objects(child_collection):
            return True
    
    return False

def flatten_all_collections(cleanup=False):

    collections = bpy.data.collections
    cols_dict = get_collections_hierarchy()

    for col_name in cols_dict:
        if cols_dict[col_name]:
            parent_name = cols_dict[col_name]
            collections[parent_name].children.unlink(collections[col_name])
            
    # if cleanup:
    #     for collection in bpy.data.collections:
    #         if collection.name.startswith("- ") and not collection_has_objects(collection):
    #             bpy.data.collections.remove(collection, do_unlink=True)
                
        



# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_group_collections)

    bpy.types.Scene.GC_coll_grouping_separator = bpy.props.StringProperty(
        name="Separator",
        description="Separator character in the Collections' names (típically an underline)",
        default="_",
    )

    bpy.types.Scene.GC_coll_grouping_position = bpy.props.IntProperty(
        name="Position",
        description="Position of the separator that will determine the common part\nof the Collections' names to group them by",
        min = 1,
        max = 99,
        soft_min = 1,
        soft_max = 10,
        step = 1,
        default = 1,
    )
    
    bpy.types.Scene.GC_disable_collections = bpy.props.BoolProperty(
        name="Disable Collections in ViewLayer",
        description="All Collections are set as disabled in the View Layer to keep\nBlender responsive in the case of large areas and whole worlds\n(normally, grouping Collections into new ones makes them visible)",
        default=True,
    )

    bpy.types.Scene.GC_sort_collections = bpy.props.BoolProperty(
        name="Sort Collections in Outliner",
        description="Orders the Collections in the Outliner alphabetically. If disabled,\nGrouped Collections will be added to the bottom of the Outliner\nby creation order.",
        default=True,
    )



def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_group_collections)

    del bpy.types.Scene.GC_coll_grouping_position
    del bpy.types.Scene.GC_coll_grouping_separator


if __name__ == "__main__":
    register()