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



def create_layer_collections_dictionary():
    '''
    Creates a dict with:
        key=layer_collection.name
        value=layer_collection object
    so that we can match collections to their
    layer_collections and use .include = True or False
    on them.
    '''

    # Get the current context and view layer
    context = bpy.context
    view_layer = context.view_layer

    # Initialize an empty dictionary to store layer collections
    layer_collections_dict = {}

    # Include the view layer itself in the dictionary
    layer_collections_dict[view_layer.name] = view_layer

    # Include the direct children of the view layer
    for direct_child_collection in view_layer.layer_collection.children:
        layer_collections_dict[direct_child_collection.name] = direct_child_collection
        # Recursively populate the dictionary with collections and their child collections
        recursive_collect_collections(direct_child_collection, layer_collections_dict)

    return layer_collections_dict

def recursive_collect_collections(collection, result_dict):
    # Recursively collect all child collections
    for child_collection in collection.children:
        # Use the .name property as the key and the layer collection object as the value
        result_dict[child_collection.name] = child_collection
        # Recursively process child collections
        recursive_collect_collections(child_collection, result_dict)







class ZGSWTOR_OT_exclude_include_collections(bpy.types.Operator):
    bl_idname = "zgswtor.exclude_include_collections"
    bl_label = "ZG Exclude/Include hierarchies of Collections From the View Layer"
    bl_description = "Exclude/Include Collections in the View Layer (unticks / ticks their checkboxes in the Outliner)\nwith the ability to affect their hierarchies of children Collections.\n\n• Excluding a parent Collection always excludes its children Collections.\nThe Scene Collection can't be excluded (it is the View Layer's root)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls,context):
        if bpy.data.collections:
            return True
        else:
            return False


    action: bpy.props.EnumProperty(
        name="Disable/Enable Collections' in View Layer",
        items=[
            ("DISABLE_SEL", "Disable Selected", "Disable Selected"),
            ("DISABLE_ALL", "Disable All", "Disable All"),
            ("ENABLE_SEL", "Enable Selected", "Enable Selected"),
            ("ENABLE_ALL", "Enable All", "Enable All"),
            ],
        options={'HIDDEN'},
        # description="Disable/Enable Collections in the View Layer (unticks / ticks their checkboxes in the Outliner)\nto manage slowdowns in massive scenes",
    )
    
    recursive: bpy.props.BoolProperty(
        name="Affect Selected Collections' Hierarchies",
        description="Process Collections' hierarchies of children Collections, if any",
        default=True,
        options={'HIDDEN'},
    )


    def execute(self, context):
        
        bpy.context.window.cursor_set("WAIT")

        self.recursive = bpy.context.scene.EAC_recursive
        
        layer_collections_dict = create_layer_collections_dictionary()
        
        if self.action == "DISABLE_ALL":
            # Get the root layer_collection out of the dict
            # as it has no .exclude property method
            layer_collections_dict.pop(context.view_layer.name)
            
            for view_collection in layer_collections_dict:
                layer_collections_dict[view_collection].exclude = True

        if self.action == "ENABLE_ALL":
            # Get the root layer_collection out of the dict
            # as it has no .exclude property method
            layer_collections_dict.pop(context.view_layer.name)
            
            for view_collection in layer_collections_dict:
                layer_collections_dict[view_collection].exclude = False
            
        if self.action == "DISABLE_SEL":
            collections = selected_collections()
            
            for collection in collections:
                layer_collections_dict[collection.name].exclude = True
                if self.recursive:
                    if collection.children_recursive:
                        for child in collection.children_recursive:
                            layer_collections_dict[child.name].exclude = True

        if self.action == "ENABLE_SEL":
            collections = selected_collections()
            for collection in collections:
                layer_collections_dict[collection.name].exclude = False
                if self.recursive:
                    if collection.children_recursive:
                        for child in collection.children_recursive:
                            layer_collections_dict[child.name].exclude = False


        bpy.context.window.cursor_set("DEFAULT")

        return {'FINISHED'}






# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_exclude_include_collections)
    
    bpy.types.Scene.EAC_recursive = bpy.props.BoolProperty(
        name="Affect Selected Collections' Hierarchies",
        description="Process Collections' hierarchies of children Collections, if any",
        default=True
    )


def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_exclude_include_collections)

    del bpy.types.Scene.EAC_recursive


if __name__ == "__main__":
    register()