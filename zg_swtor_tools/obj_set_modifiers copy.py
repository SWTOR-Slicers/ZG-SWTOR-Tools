import bpy

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
    def armature_first(obj):
        bpy.context.window.cursor_set("WAIT")
        if obj.modifiers:
            armature_exists = False
            for idx in range(len(obj.modifiers)):
                mod = obj.modifiers[idx]
                if mod.type == "ARMATURE":
                    armature_exists = True
                    break
            
            if armature_exists:
                for i in range(idx):
                    bpy.ops.object.modifier_move_up(modifier=mod.name)

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
                    break

    @staticmethod
    def preserve_volume_off(obj):
        bpy.context.window.cursor_set("WAIT")
        if obj.modifiers:
            for idx in range(len(obj.modifiers)):
                mod = obj.modifiers[idx]
                if mod.type == "ARMATURE":
                    obj.modifiers[mod.name].use_deform_preserve_volume = False
                    break

    
    
    def execute(self, context):
        selected_objects = [obj for obj in bpy.context.selected_editable_objects
                            if obj.type == "MESH" and not "skeleton" in obj.name]
        
        if selected_objects:
            
            gr2_scale = 1.0
            gr2_addon_prefs = bpy.context.preferences.addons["io_scene_gr2"].preferences
            if hasattr(gr2_addon_prefs, 'gr2_scale_object'):
                if gr2_addon_prefs.gr2_scale_object:
                    gr2_scale = gr2_addon_prefs.gr2_scale_factor

            for selected_obj in selected_objects:
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
                    self.armature_first(obj)
                elif self.action == "armature_last":
                    self.armature_last(obj)
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