from tabnanny import check
import bpy

class ZGSWTOR_OT_set_modifiers(bpy.types.Operator):
    bl_idname = "zgswtor.set_modifiers"
    bl_label = "SWTOR Tools"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Adds / removes Subdivision, MultiRes, Displace and Solidify Modifiers,\nwith sensible settings for SWTOR asset work.\n\n• Requires a selection of objects.\n• Preserves Armature Modifiers from removal and allows for their repositioning"


    # Property for the UI buttons to call different actions.
    # See: https://b3d.interplanety.org/en/calling-functions-by-pressing-buttons-in-blender-custom-ui/
    action: bpy.props.EnumProperty(
        name="Scaling Type",
        items=[
            ("add_subd", "Add Subdivision Modifier", "Add Subdivision Modifier"),
            ("add_multires", "Add Multires Modifier", "Add Multires Modifier"),
            ("add_displace", "Add Displace Modifier", "Add Displace Modifier"),
            ("add_solidify", "Add Solidify Modifier", "Add Solidify Modifier"),
            ("remove_them", "Remove All Modifiers", "Remove All Modifiers of these types"),
            ("armature_first", "Remove All Modifiers", "Set Armature as first Modifier"),
            ("armature_last", "Remove All Modifiers", "Set Armature as last Modifier\nor next to last Multires"),
            ],
        options={'HIDDEN'}
        )

    # Check that there is a selection of objects (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects:
            return True
        else:
            return False


    # METHODS

    @staticmethod
    def add_subd(obj):
        bpy.context.window.cursor_set("WAIT")
        if not "Subdivision" in obj.modifiers:
            mod = obj.modifiers.new(name= "Subdivision", type="SUBSURF")

    @staticmethod
    def add_multires(obj):
        bpy.context.window.cursor_set("WAIT")
        if not "Multires" in obj.modifiers:
            mod = obj.modifiers.new(name= "Multires", type="MULTIRES")
            bpy.ops.object.multires_subdivide({'object': obj}, modifier="Multires", mode='CATMULL_CLARK')

    @staticmethod
    def add_displace(obj):
        bpy.context.window.cursor_set("WAIT")
        if not "Displace" in obj.modifiers:
            mod = obj.modifiers.new(name= "Displace", type="DISPLACE")
            mod.strength = 0.0002

    @staticmethod
    def add_solidify(obj):
        bpy.context.window.cursor_set("WAIT")
        if not "Solidify" in obj.modifiers:
            mod = obj.modifiers.new(name= "Solidify", type="SOLIDIFY")
            mod.thickness = 0.0002

    @staticmethod
    def remove_them(obj):
        bpy.context.window.cursor_set("WAIT")
        removable_modifiers = [
            "Subdivision",
            "Multires",
            "Displace",
            "Solidify"
        ]
        if obj.modifiers:
            for mod in obj.modifiers:
                if mod.name in removable_modifiers:
                    obj.modifiers.remove(obj.modifiers.get(mod.name))

    @staticmethod
    def armature_first(obj):
        bpy.context.window.cursor_set("WAIT")
        index = obj.modifiers.find("Armature")
        if index != -1:
            for i in range(index):
                bpy.ops.object.modifier_move_up({'object': obj}, modifier="Armature")

    @staticmethod
    def armature_last(obj):
        bpy.context.window.cursor_set("WAIT")
        index = obj.modifiers.find("Armature")
        if index != -1:
            mod_stack_depth = len(obj.modifiers)
            if index < mod_stack_depth:
                for i in range(mod_stack_depth - index - 1):
                    try:
                        bpy.ops.object.modifier_move_down({'object': obj}, modifier="Armature")
                    except:
                        pass  # in case of failure because of Multires/SubD priority

    
    def execute(self, context):
        selected_objects = [obj for obj in bpy.context.selected_editable_objects
                            if obj.type == "MESH" and not "skeleton" in obj.name]
        
        if selected_objects:
            for selected_obj in selected_objects:
                obj = bpy.data.objects[selected_obj.name]
                if self.action == "add_subd":
                    self.add_subd(obj)
                elif self.action == "add_multires":
                    self.add_multires(obj)
                elif self.action == "add_displace":
                    self.add_displace(obj)
                elif self.action == "add_solidify":
                    self.add_solidify(obj)
                elif self.action == "remove_them":
                    self.remove_them(obj)
                elif self.action == "armature_first":
                    self.armature_first(obj)
                elif self.action == "armature_last":
                    self.armature_last(obj)


            bpy.context.window.cursor_set("DEFAULT")
            return {"FINISHED"}

        else:
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, "No modifiable objects were selected.")
            return {"CANCELLED"}


# UI is set in ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_set_modifiers)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_set_modifiers)

if __name__ == "__main__":
    register()