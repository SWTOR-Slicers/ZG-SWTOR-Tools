import bpy

            
def selected_outliner_items(context):
    '''
    Returns selected outliner items
    as a list of RNA objects (in the
    Python sense) including Collections
    '''

    objects_and_collections_in_selection = []

    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'OUTLINER':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        with context.temp_override(window=window, area=area, region=region):
                            for item in context.selected_ids:
                                if item not in objects_and_collections_in_selection:
                                    objects_and_collections_in_selection.append(item)
                                
    return(objects_and_collections_in_selection)
    




class ZGSWTOR_OT_prefixer(bpy.types.Operator):
    bl_label = "Prefix Names In Selected Items"
    bl_idname = "zgswtor.prefixer"
    bl_description = "Adds a prefix to the names of all selected Collections and objects\n(meshes, skeletons, lights, etc.), and to Materials used by those meshes.\n\n• Requires a selection of items in the 3D Viewer or in the Outliner.\n• Accepts Collections as items to prefix.\n• Please include your own separators between the prefix\n   and the original names in the prefix text: spaces, hyphens, etc.\n\nPrefixing helps avoid name conflicts between successive SWTOR imports\nin a same Blender project, and facilitates organization"
    bl_options = {'REGISTER', 'UNDO'}


    # Check that there is a selection of objects 
    # in the 3D Viewer and/or in any Outliner,
    # (which lets us include hidden objects)
    # in order to enable the operator.
    @classmethod
    def poll(cls,context):
        if bpy.context.mode == "OBJECT" and bpy.context.selected_objects:
            enable_operator = True
        else:
            enable_operator = False
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'OUTLINER':
                        for region in area.regions:
                            if region.type == 'WINDOW':
                                with context.temp_override(window=window, area=area, region=region):
                                    if context.selected_ids:
                                        for item in context.selected_ids:
                                            if isinstance(item, bpy.types.Collection):
                                                # Collections don't have type, hence
                                                # this kind of checking.
                                                enable_operator = True
                                                break
                                            elif hasattr(item, "type"):
                                                # If it has a type it can be any kind of object
                                                # including meshes, lights, etc.
                                                enable_operator = True
                                                break
        return enable_operator


    # Some properties
    
    prefix: bpy.props.StringProperty(
        name="Prefix",
        default="",
        options={'HIDDEN'}
    )

    prefix_mats_skeletons: bpy.props.BoolProperty(
        name="Prefix Materials and Skeletons Too",
        description="Prefixes not just the objects (meshes and skeletons)\nbut the Materials and internal skeleton data-blocks linked to them, too",
        default = True,
        options={'HIDDEN'}
    )

    def execute(self, context):
        
        self.prefix = context.scene.zg_prefix  # Retrieve the prefix from the scene property
        
        self.prefix_mats_skeletons = context.scene.zg_prefix_mats_skeletons_bool
        
        prefixable_rna_types = [
            "Armature",
            "CacheFile",
            "Camera",
            "Collection",
            "Curve",
            "Curves",
            "Lattice",
            "Light",
            "LightProbe",
            "MetaBall",
            "Object",
            "ParticleSettings",
            "PointCloud",
            "Text",
        ]

        # Combine 3DVIEW's selected objects with Outliner's selected objects without
        # producing repetitions. Not sure if necessary (Blender's behavior when maximizing
        # an editor and occluding the Outliner is a bit strange).
        all_selected_items = list( set(context.selected_objects + selected_outliner_items(context)) )
        
        for item in all_selected_items:
            if item.bl_rna.identifier in prefixable_rna_types:
                if not item.name.startswith(self.prefix):
                                
                    if item.bl_rna.identifier == "Object":
                        
                        print(item.type, item.name)
                        
                        if item.type == "MESH" and self.prefix_mats_skeletons == True:
                                for material_slot in item.material_slots:
                                    if not material_slot.name.startswith(self.prefix):
                                        material_slot.material.name = self.prefix + material_slot.material.name

                        if item.type == "ARMATURE" and self.prefix_mats_skeletons == True:
                            if not bpy.data.armatures[item.name].name.startswith(self.prefix):
                                bpy.data.armatures[item.name].name = self.prefix + bpy.data.armatures[item.name].name
                                
                    # Done last to avoid trouble processing
                    # its linked datablocks
                    item.name = self.prefix + item.name

        return {'FINISHED'}




def register():
    bpy.utils.register_class(ZGSWTOR_OT_prefixer)
    
    bpy.types.Scene.zg_prefix = bpy.props.StringProperty(
        name="Prefix text",
        description = "Please include in the prefix any separator between it\nand the original name: spaces, hyphens, etc\n\n• Confirm entered text with TAB, ENTER, RETURN\n   or by clicking outside the text field",
        default=""
        )
    bpy.types.Scene.zg_prefix_mats_skeletons_bool = bpy.props.BoolProperty(
        name="Prefix Materials and Armatures Too",
        description="Prefixes not just the objects (meshes and skeletons)\nbut the Materials and internal skeleton data-blocks linked to them, too",
        default = True
    )

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_prefixer)
    
    del bpy.types.Scene.zg_prefix
    del bpy.types.Scene.zg_prefix_mats_skeletons_bool


if __name__ == "__main__":
    register()
