import bpy
import bmesh





def guess_phys_vertex_groups_names(obj):
    '''
    Tries to detect in SWTOR objects Vertex Groups
    mean to match physiscs-driven .clo bones.
    
    Those follow a <common_part_nn> pattern, with
    nn being numbers that start somewhere in the
    "00" to "09" range and go beyond, often with
    omissions.
    
    Mostly. There are exceptions.
    
    As most normal VGs in SWTOR objects, when doing
    numbering, they use single digit ones, this
    seems a reasonable approach.
    '''    
    
    # Mesh object check (redundant in this module)
    # if obj is None or obj.type != 'MESH':
    #     print("No active mesh object selected.")
    #     return None
        
    for vg in obj.vertex_groups:
        name = vg.name
        if len(name) > 3 and name[-3:-2] == "_" and name[-2:].isdigit():
            common_part = name[:-3]
            return common_part
        
    return None



def merge_vertex_groups(obj, destination_vertex_group_name, common_name_part, delete_originals=False):
    # Ensure we are in Object Mode
    if bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create the target vertex group if it does not exist
    if destination_vertex_group_name not in obj.vertex_groups:
        merged_vertex_group = obj.vertex_groups.new(name=destination_vertex_group_name)
    else:
        merged_vertex_group = obj.vertex_groups[destination_vertex_group_name]
    
    # Find all vertex groups that match the pattern
    groups_to_merge = [vg for vg in obj.vertex_groups if common_name_part in vg.name]
    if not groups_to_merge:
        print()
        print(f"No VGs with '{common_name_part}' in their names")
        print()

        return None
        
    # Collect all vertex weights
    vertex_weights = {}
    
    for vg in groups_to_merge:
        print(vg.name)
        for v in obj.data.vertices:
            for g in v.groups:
                if g.group == vg.index:
                    if v.index not in vertex_weights:
                        vertex_weights[v.index] = g.weight
                    else:
                        vertex_weights[v.index] = max(vertex_weights[v.index], g.weight)
    
    # Assign collected weights to the target group
    for v_index, weight in vertex_weights.items():
        merged_vertex_group.add([v_index], weight, 'REPLACE')
    
    # Optionally delete the original vertex groups
    if delete_originals:
        for vg in groups_to_merge:
            obj.vertex_groups.remove(vg)

    merged_vg_amount_report = len(groups_to_merge)
    print()
    print(f"{merged_vg_amount_report} vertex groups merged.")
    print()
    
    return merged_vg_amount_report
            





# Main
# region

class ZGSWTOR_OT_merge_phys_vertex_groups(bpy.types.Operator):
    bl_idname = "zgswtor.merge_phys_vgs"
    bl_label = "ZG Merge Physics Vertex Groups"
    bl_description = "Looks for Vertex Groups with names matching SWTOR physics bones' patterns\n(ending in double digit numbers) or using a manually input common text,\nand copies their vertices to a new Vertex Group named 'physics' to\nfacilitate applying Blender physics or custom bones by the user.\n\n• If not using Best-Guess, requires entering a text to find partial matches by"
    bl_options = {'REGISTER', "UNDO"}


    # Check that there is a selection of objects and that we are in Object mode
    # (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        for obj in bpy.data.objects:
            if obj.type == "MESH":
                return True
        return False
    

    use_selection_only : bpy.props.BoolProperty(
        name="Apply To Selected Objects Only",
        description="Apply to selected objects only.",
        default=True,
        options={'HIDDEN'},
    )

    delete_originals : bpy.props.BoolProperty(
        name="Delete source Vertex groups",
        description="Delete the Vertex Groups with a 'newton' in their names after their vertices\nhave been copied to a new 'physics' Vertex Group",
        default=False,
        options={'HIDDEN'},
    )
    
    use_best_guess : bpy.props.BoolProperty(
        name="Best Guess",
        description="Guess which Vertex Groups are physics bones-related by looking for VG names\nending with a '_nn' (such as 'newtonparticle_lekku_02', 'newtonparticle_lekku_06',\netc.).\n\nChecking the results for any mistake in the Console is strongly advised",
        default=True,
        options={'HIDDEN'},
    )

    vg_names_common_part : bpy.props.StringProperty(
        name="Common Text In Vertex Groups' Names",
        description="Vertex Groups whose names contain this text will be processed",
        default="",
        options={'HIDDEN'},
    )

# endregion

    def execute(self, context):

        context.window.cursor_set("WAIT")  # Show wait cursor icon

        if self.use_selection_only == True:
            objs = [obj for obj in bpy.context.selected_objects if obj.type == "MESH"]
            if not objs:
                self.report({"WARNING"}, "No mesh objects were selected.")
                return {"CANCELLED"}
        else:
            objs = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    
        
        self.delete_originals = context.scene.MPVG_delete_originals
        self.use_best_guess   = context.scene.MPVG_use_best_guess
        self.vg_names_common_part  = context.scene.MPVG_vg_names_common_part


        objs_with_no_phys_vgs_merged = 0

        for obj in objs:
            
            print()
            print()
            print(obj.name)
            print("-" * len(obj.name))
            
            
            
            if self.use_best_guess:
                phys_vg_name_common_part = guess_phys_vertex_groups_names(obj)
                if phys_vg_name_common_part is None:
                    result = None
                    objs_with_no_phys_vgs_merged += 1
                    
                    print("Best-guessing the Physics Vertex Groups' common name failed. Check the object's VG names and enter one manually.")
                    self.report({'WARNING'}, f"Obj: {obj.name}. No VGs were merged. Attempting to guess their names failed. Try a manual one.")
                    
                    continue
                
                else:
                    
                    result = merge_vertex_groups(obj, "PHYSICS", phys_vg_name_common_part, delete_originals=self.delete_originals)
                    
                    if result == None:
                        objs_with_no_phys_vgs_merged += 1
                        self.report({'WARNING'}, f"Obj: {obj.name}. No VGs were merged. The guessed matching text '{phys_vg_name_common_part}' failed.")
                    else:
                        self.report({'INFO'}, f"Obj: {obj.name}. {result} VGs were merged.")
                    
            else:
                
                result = merge_vertex_groups(obj, "PHYSICS", self.vg_names_common_part, delete_originals=self.delete_originals)
        
                if result == None:
                    objs_with_no_phys_vgs_merged += 1
                    self.report({'WARNING'}, f"Obj: {obj.name}. No VGs were merged. The matching text '{self.vg_names_common_part}' wasn't found in their names.")
                else:
                    self.report({'INFO'}, f"Obj: {obj.name}. {result} VGs were merged.")

        if objs_with_no_phys_vgs_merged > 0:
            self.report({'WARNING'}, f"{objs_with_no_phys_vgs_merged} of {len(objs)} object/s didn't produce a merged Physics VG. Check Info Editor or Console for details.")
        else:
            self.report({'INFO'}, f"{len(objs)} object/s successfully processed.")

        bpy.context.window.cursor_set("DEFAULT")  # Show normal cursor icon
        return {"FINISHED"}

# UI is set in addon_ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_merge_phys_vertex_groups)

    bpy.types.Scene.MPVG_delete_originals = bpy.props.BoolProperty(
        name="Delete source Vertex groups",
        description="Delete the Vertex Groups with a 'newton' in their names after their vertices\nhave been copied to a new 'physics' Vertex Group",
        default=False,
    )

    bpy.types.Scene.MPVG_use_best_guess = bpy.props.BoolProperty(
        name="Best Guess",
        description="Guess which Vertex Groups are physics bones-related by looking for VG names\nending with a '_nn' (such as 'newtonparticle_lekku_02', 'newtonparticle_lekku_06',\netc.).\n\nChecking the results for any mistake in the Console is strongly advised",
        default=True,
    )

    bpy.types.Scene.MPVG_vg_names_common_part = bpy.props.StringProperty(
        name="Common Text In Vertex Groups' Names",
        description="Vertex Groups whose names contain this text will be processed",
        default="",
    )

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_merge_phys_vertex_groups)
    
    del bpy.types.Scene.MPVG_delete_originals
    del bpy.types.Scene.MPVG_use_best_guess
    del bpy.types.Scene.MPVG_vg_names_common_part


if __name__ == "__main__":
    register()