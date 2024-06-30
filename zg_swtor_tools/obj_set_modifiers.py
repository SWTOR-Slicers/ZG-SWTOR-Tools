import bpy

from .utils.addon_checks import requirements_checks

class ZGSWTOR_OT_set_modifiers(bpy.types.Operator):
    bl_idname = "zgswtor.set_modifiers"
    bl_label = "ZG Set Modifiers"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Adds to several objects at once a Modifier, with sensible settings for SWTOR asset work.\n\n• Requires a selection of objects.\n• Doesn't allow for more than one modifier of the same type\n   (those will have to be added manually).\n• The Remove option doesn't affect any present Armature Modifier"

    # Check that there is a selection of objects (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects:
            return True
        else:
            return False


    # Property for the UI buttons to call different actions.
    # See: https://b3d.interplanety.org/en/calling-functions-by-pressing-buttons-in-blender-custom-ui/
    action: bpy.props.EnumProperty(
        name="Set Modifier Action",
        items=[
            ("add_subd", "Add Subdivision Modifier", "Add Subdivision Modifier"),
            ("add_multires", "Add Multires Modifier", "Add Multires Modifier"),
            ("add_displace", "Add Displace Modifier", "Add Displace Modifier"),
            ("add_solidify", "Add Solidify Modifier", "Add Solidify Modifier"),
            ("add_smooth_corrective", "Add Smooth Corrective", "Add Smooth Corrective"),
            ("add_shrinkwrap", "Add Shrinkwrap Modifier", "Add Shrinkwrap Modifier"),
            ("remove_them", "Remove All Modifiers", "Remove All Modifiers of these types"),
            ("armature_first", "Remove All Modifiers", "Set Armatures as first Modifiers"),
            ("armature_last", "Remove All Modifiers", "Set Armatures as last Modifiers\nor next to last Multires"),
            ("preserve_volume_on", "Armatures' Preserve Volume On", "Set Armatures to preserve volume"),
            ("preserve_volume_off", "Armatures' Preserve Volume Off", "Set Armatures to not preserve volume"),
            ],
        options={'HIDDEN'}
        )


    # METHODS

    @staticmethod
    def add_subd(obj):
        bpy.context.window.cursor_set("WAIT")
        mod_exists = False
        if obj.modifiers:
            for mod in obj.modifiers:
                if mod.type == "SUBSURF":
                    mod_exists = True
                    break
        if not mod_exists:
            mod = obj.modifiers.new(name= "Subdivision", type="SUBSURF")
            mod.levels = 2
            mod.render_levels = 2
            mod.quality = 3
            mod.use_custom_normals = True
            mod.use_creases = True
            mod.show_only_control_edges = False
            mod.use_limit_surface = False

    @staticmethod
    def add_multires(obj):
        bpy.context.window.cursor_set("WAIT")
        mod_exists = False
        if obj.modifiers:
            for mod in obj.modifiers:
                if mod.type == "MULTIRES":
                    mod_exists = True
                    break
        if not mod_exists:
            mod = obj.modifiers.new(name= "Multires", type="MULTIRES")
            bpy.ops.object.multires_subdivide(
                modifier=mod.name,
                mode='CATMULL_CLARK'
            ) # Apply a level of SubD
            mod.levels = 2
            mod.render_levels = 2
            mod.sculpt_levels = 2
            mod.quality = 3
            mod.use_custom_normals = True
            mod.boundary_smooth = "PRESERVE_CORNERS"
            mod.use_creases = True
            mod.show_only_control_edges = False
            
    @staticmethod
    def add_displace(obj, gr2_scale):
        bpy.context.window.cursor_set("WAIT")
        mod_exists = False
        if obj.modifiers:
            for mod in obj.modifiers:
                if mod.type == "DISPLACE":
                    mod_exists = True
                    break
        if not mod_exists:
            mod = obj.modifiers.new(name= "Displace", type="DISPLACE")
            mod.strength = 0.0004 * gr2_scale

    @staticmethod
    def add_solidify(obj, gr2_scale):
        bpy.context.window.cursor_set("WAIT")
        mod_exists = False
        if obj.modifiers:
            for mod in obj.modifiers:
                if mod.type == "SOLIDIFY":
                    mod_exists = True
                    break
        if not mod_exists:
            mod = obj.modifiers.new(name= "Solidify", type="SOLIDIFY")
            mod.thickness = 0.0004 * gr2_scale

    @staticmethod
    def add_smooth_corrective(obj):
        bpy.context.window.cursor_set("WAIT")
        mod_exists = False
        if obj.modifiers:
            for mod in obj.modifiers:
                if mod.type == "CORRECTIVE_SMOOTH":
                    mod_exists = True
                    break
        if not mod_exists:
            mod = obj.modifiers.new(name= "CorrectiveSmooth", type="CORRECTIVE_SMOOTH")
            mod.factor = 0.250
            mod.iterations = 3
            mod.scale = 1.5
            mod.smooth_type = "LENGTH_WEIGHTED"
            mod.use_only_smooth = False
            mod.use_pin_boundary = False
            mod.rest_source = "ORCO"

    @staticmethod
    def add_shrinkwrap(obj, gr2_scale):
        if not bpy.context.scene.ZGshrinkwrap_target:
            return
        
        if  bpy.context.scene.ZGshrinkwrap_target == obj:
            return
        
        bpy.context.window.cursor_set("WAIT")
        mod_exists = False
        if obj.modifiers:
            for mod in obj.modifiers:
                if mod.type == "SHRINKWRAP":
                    mod_exists = True
                    break
        if not mod_exists:
            mod = obj.modifiers.new(name= "Shrinkwrap", type="SHRINKWRAP")
            mod.wrap_method = "TARGET_PROJECT"
            mod.wrap_mode = "OUTSIDE"
            mod.offset = 0.0004 * gr2_scale
            mod.target = bpy.context.scene.ZGshrinkwrap_target

    @staticmethod
    def remove_them(obj):
        bpy.context.window.cursor_set("WAIT")
        removable_modifiers = [
            "SUBSURF",
            "MULTIRES",
            "DISPLACE",
            "SOLIDIFY",
            "SHRINKWRAP",
            "CORRECTIVE_SMOOTH",
        ]
        if obj.modifiers:
            for mod in obj.modifiers:
                if mod.type in removable_modifiers:
                    obj.modifiers.remove(obj.modifiers.get(mod.name))

    @staticmethod
    def armature_ordering(obj, move_to_top=True):
        # Get all armature modifiers along with their original index and properties        
        armature_modifiers = [(i, mod, mod.show_expanded) for i, mod in enumerate(obj.modifiers) if mod.type == 'ARMATURE']
        
        # Extract the relevant properties before removing the modifiers
        armature_mod_data = []
        for i, mod, show_expanded in armature_modifiers:
            armature_mod_data.append((
                i,
                mod.name,
                mod.object,
                mod.vertex_group,
                mod.use_apply_on_spline,
                mod.use_multi_modifier,
                mod.invert_vertex_group,
                mod.use_bone_envelopes,
                mod.use_deform_preserve_volume,
                mod.show_viewport,
                mod.show_render,
                mod.show_in_editmode,
                mod.show_on_cage,
                show_expanded,
            ))        
        
        # Sort the armature modifiers by the specified criteria, then by their original index:
        # * Not named IK or FK.
        # * IK.
        # * FK.
        # Lambda version:
        # armature_mod_data.sort(key=lambda mod: (
        #     ('ik' in mod[2].name.lower(), 'fk' in mod[2].name.lower(), mod[2].name, mod[0])
        # ))
        # Funtion version
        def armature_sort_key(mod):
            # Extracts sorting criteria based on the armature name and original index
            name = mod[2].name.lower()
            return ('fk' in name, 'ik' in name, name, mod[0])

        armature_mod_data.sort(key=armature_sort_key)
        
        # Remove the armature modifiers from the object
        for _, mod, _ in armature_modifiers:
            obj.modifiers.remove(mod)
        
        # Re-add the armature modifiers at the top or bottom
        initial_mod_count = len(obj.modifiers)
        if move_to_top:
            insert_index = 0
        else:
            insert_index = initial_mod_count
            armature_mod_data.reverse()
        
        for mod_data in armature_mod_data:
            new_mod = obj.modifiers.new(mod_data[1], 'ARMATURE')
            new_mod.object = mod_data[2]
            new_mod.vertex_group = mod_data[3]
            new_mod.use_apply_on_spline = mod_data[4]
            new_mod.use_multi_modifier = mod_data[5]
            new_mod.invert_vertex_group = mod_data[6]
            new_mod.use_bone_envelopes = mod_data[7]
            new_mod.use_deform_preserve_volume = mod_data[8]
            new_mod.show_viewport = mod_data[9]
            new_mod.show_render = mod_data[10]
            new_mod.show_in_editmode = mod_data[11]
            new_mod.show_on_cage = mod_data[12]
            new_mod.show_expanded = mod_data[13]
            
            # Move the modifier to the top or bottom
            obj.modifiers.move(len(obj.modifiers) - 1, insert_index)
            if move_to_top:
                insert_index += 1

    @staticmethod
    def armature_last(obj):
        bpy.context.window.cursor_set("WAIT")
        if obj.modifiers:
            armature_exists = False
            for idx in range(len(obj.modifiers)):
                mod = obj.modifiers[idx]
                if mod.type == "ARMATURE":
                    armature_exists = True
                    break
                
            if armature_exists:
                mod_stack_depth = len(obj.modifiers)
                if idx < mod_stack_depth:
                    for i in range(mod_stack_depth - idx - 1):
                        bpy.ops.object.modifier_move_down(modifier=mod.name)

    @staticmethod
    def preserve_volume_on(obj):
        bpy.context.window.cursor_set("WAIT")
        if obj.modifiers:
            for idx in range(len(obj.modifiers)):
                mod = obj.modifiers[idx]
                if mod.type == "ARMATURE":
                    obj.modifiers[mod.name].use_deform_preserve_volume = True

    @staticmethod
    def preserve_volume_off(obj):
        bpy.context.window.cursor_set("WAIT")
        if obj.modifiers:
            for idx in range(len(obj.modifiers)):
                mod = obj.modifiers[idx]
                if mod.type == "ARMATURE":
                    obj.modifiers[mod.name].use_deform_preserve_volume = False

    
    
    def execute(self, context):
        selected_objects = [obj for obj in bpy.context.selected_editable_objects
                            if obj.type == "MESH" and not "skeleton" in obj.name]
        
        if selected_objects:
            
            # Checking if we must handle SWTOR objects' custom properties about their meshes' scales
            use_gr2_scale_custom_prop = context.preferences.addons["zg_swtor_tools"].preferences.use_gr2_scale_custom_prop

            # Checking if we are dealing with a .gr2 Add-on with scaling parameters
            checks = requirements_checks()
            if checks["gr2HasParams"]:
                if context.preferences.addons["io_scene_gr2"].preferences.gr2_scale_object:
                    gr2_scale = context.preferences.addons["io_scene_gr2"].preferences.gr2_scale_factor
                else:
                    gr2_scale = 1.0
            else:
                gr2_scale = 1.0
            
            print(f"Global Scale for size-sensitive Modifiers' settings = {gr2_scale}")
            if use_gr2_scale_custom_prop:
                print("SWTOR objects with custom 'gr_scale' properties will use their own.")
            

            for selected_obj in selected_objects:
                
                # If the object was scaled on import and keeps
                # the data in a custom property, use that instead
                if "gr2_scale" in selected_obj and use_gr2_scale_custom_prop:
                    gr2_scale = selected_obj["gr2_scale"]
                else:
                    gr2_scale = gr2_scale

                obj = bpy.data.objects[selected_obj.name]
                if self.action == "add_subd":
                    self.add_subd(obj)
                elif self.action == "add_multires":
                    self.add_multires(obj)
                elif self.action == "add_displace":
                    self.add_displace(obj, gr2_scale)
                elif self.action == "add_solidify":
                    self.add_solidify(obj, gr2_scale)
                elif self.action == "add_smooth_corrective":
                    self.add_smooth_corrective(obj)
                elif self.action == "add_shrinkwrap":
                    if bpy.context.scene.ZGshrinkwrap_target == obj:
                        self.report({"WARNING"}, "Object can't shrinkwrap itself. Choose a different target.")
                        bpy.context.window.cursor_set("DEFAULT")
                        return {"FINISHED"}
                    else:
                        if bpy.context.scene.ZGshrinkwrap_target == None:
                            self.report({"WARNING"}, "Please choose a Shrinkwrap target.")
                            bpy.context.window.cursor_set("DEFAULT")
                            return {"CANCELLED"}
                        else:
                            self.add_shrinkwrap(obj, gr2_scale)
                elif self.action == "remove_them":
                    self.remove_them(obj)
                elif self.action == "armature_first":
                    self.armature_ordering(obj, move_to_top=True)
                elif self.action == "armature_last":
                    self.armature_ordering(obj, move_to_top=False)
                elif self.action == "preserve_volume_on":
                    self.preserve_volume_on(obj)
                elif self.action == "preserve_volume_off":
                    self.preserve_volume_off(obj)


            bpy.context.window.cursor_set("DEFAULT")
            return {"FINISHED"}

        else:
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, "No modifiable objects were selected.")
            return {"CANCELLED"}


# UI is set in addon_ui.py


# Registrations

def register():
    bpy.types.Scene.ZGshrinkwrap_target = bpy.props.PointerProperty(type=bpy.types.Object)
    
    bpy.utils.register_class(ZGSWTOR_OT_set_modifiers)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_set_modifiers)
    
    del bpy.types.Scene.ZGshrinkwrap_target

if __name__ == "__main__":
    register()