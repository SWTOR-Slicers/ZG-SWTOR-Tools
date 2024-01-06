import bpy

import os
from pathlib import Path
from bpy.app.handlers import persistent


class ZGSWTOR_OT_skinsettings_ng_in_3d_viewer(bpy.types.Operator):
    bl_idname = "zgswtor.skinsettings_ng_in_3d_viewer"
    bl_label = "ZG Apply Skin Settings-Holder Nodegroup to selected objects"
    bl_description = "Applies a Skin Settings-holding \"control panel\" Nodegroup to selected objects's SkinB materials\nso that the skin in all the body parts of a character can be adjusted from a single set of controls.\n\nIt's only applied to Custom SWTOR SkinB Shaders, even if other non-skin objects are selected.\nThat said, the Groups can be manually added to non-skin materials to use their skin data or\nany other data (manually added to the Group or calculated inside) in any fashion.\n\n• Requires a selection of objects.\n• Automatically chooses the head's SkinB settings as the default values\n   if found in the selection. Otherwise, it'll use other body parts' settings"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects:
            return True
        else:
            return False

    
    
    def execute(self, context):
        bpy.context.window.cursor_set("WAIT")

        if not "SWTOR - SkinB Shader" in bpy.data.node_groups:
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, "No Custom SWTOR SkinB Shaders present in this project")
            return {"CANCELLED"}

        if not "SW Template - Character's Skin Settings" in bpy.data.node_groups:
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, "No Skin Settings Nodegroup template present in this project")
            return {"CANCELLED"}

        if context.scene.apply_skinsettings_name == "" or context.scene.apply_skinsettings_name.strip() == "":
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, "Please enter a character's name for the Skin Settings Nodegroup")
            context.scene.apply_skinsettings_name = ""
            return {"CANCELLED"}


        # Check for selected objects' skin materials, find head skin material.
        objs = bpy.context.selected_objects
        
        skin_mats = []
        ref_mat = None  # material to be used as skin data reference

        for obj in objs:
            if obj.material_slots:
                for slot in obj.material_slots:
                    if "SWTOR - SkinB Shader" in slot.material.node_tree.nodes:
                        skin_mats.append(slot.material)
                                                   
                        # Rather not that super-robust head detection
                        if "head" in slot.material.name:
                            ref_mat = slot.material.name

        if skin_mats == []:
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, "No SkinB materials present in the selected objects")
            return {"CANCELLED"}

        # If no heads detected, use any other skin body part as reference
        if ref_mat == None:
            ref_mat = skin_mats[0].name



        # Prepare character-specific local skin settings Nodegroup -----------------------------
        
        character_name = context.scene.apply_skinsettings_name
        zg_skinsettings_name = character_name + "Skin Settings"

        if zg_skinsettings_name in bpy.data.node_groups:
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, 'A "' + zg_skinsettings_name + '" Nodegroup already exists.')
            context.scene.apply_skinsettings_name = ""
            return {"CANCELLED"}
        
        # Make a local copy of template "SW Template - Character's Skin Settings" Nodegroup
        # using zg_skinsettings_name as its name. 
        zg_skinsettings_local = bpy.data.node_groups["SW Template - Character's Skin Settings"].copy()
        zg_skinsettings_local.name = zg_skinsettings_name



        # Cycle through Materials --------------------------------------------------------------


        for mat in skin_mats:
            
            mat_nodes = mat.node_tree.nodes
            mat_links = mat.node_tree.links
            zg_skinb_node = mat_nodes["SWTOR - SkinB Shader"]
            
            # Add an instance of the Nodegroup to the Material or use the existing one
            if not zg_skinsettings_name in mat_nodes:
                zg_skinsettings_node = mat_nodes.new(type="ShaderNodeGroup")
                zg_skinsettings_node.node_tree = bpy.data.node_groups[zg_skinsettings_local.name]
                zg_skinsettings_node.name = zg_skinsettings_name
                zg_skinsettings_node.width = 250
                zg_skinsettings_node.location = -450, -650
            else:
                zg_skinsettings_node = mat_nodes[zg_skinsettings_name]


            # Connect Skin Settings Nodegroup to SkinB Nodegroup
            for output in zg_skinsettings_node.outputs:
                if output.hide_value == False and output.name in zg_skinb_node.inputs:
                    mat_links.new(zg_skinsettings_node.outputs[output.name],zg_skinb_node.inputs[output.name])


            # Special rewiring for Twi'lek characters if checkboxed
            if context.scene.apply_skinsettings_twilek == True:
                mat_links.new(zg_skinsettings_node.outputs["Twi'lek GlossMap Color"],zg_skinb_node.inputs["_s GlossMap Color"])
                mat_links.new(zg_skinsettings_node.outputs["Twi'lek GlossMap Alpha"],zg_skinb_node.inputs["_s GlossMap Alpha"])


            # If material = skin reference material, copy SkinB values to Skin Settings Nodegroup
            if mat.name == ref_mat:
                
                # Skin Settings Nodegroup's Group Output Node where to copy the SkinB values into
                zg_skinsettings_nodegroup_output = bpy.data.node_groups[zg_skinsettings_name].nodes["Group Output"]
                
                # Cycle through outputs' names to find matching SkinB inputs and copy their values
                for output in zg_skinsettings_node.outputs:
                    # Skip label-like outputs
                    if output.hide_value == False and output.name in zg_skinb_node.inputs:
                        zg_skinsettings_nodegroup_output.inputs[output.name].default_value = zg_skinb_node.inputs[output.name].default_value


        context.scene.apply_skinsettings_name = ""
        
        bpy.context.window.cursor_set("DEFAULT")
        return {"FINISHED"}


# UI is set in ui.py





# Registrations

def register():
    bpy.types.Scene.apply_skinsettings_twilek = bpy.props.BoolProperty(
        name="Override Twi'lek GlossMaps",
        description="If ticked, disconnects the GlossMaps and connects\nsimpler common values in their place.\n\n(For some reason, Twi'lek heads' GlossMaps don't match\nhumanoid bodies' ones, producing a noticeable seam effect)",
        default = False,
    )
    bpy.types.Scene.apply_skinsettings_name = bpy.props.StringProperty(
        name="Skin Settings Nodegroup's prefix name",
        description="Name of the character to apply to\nthe Nodegroup's name (\"<name>'s Skin Settings\").\n\n• It is case-sensitive.\n• Adds a \"Skin Settings\" to the entered name. Any desired separator\n   characters (spaces, hyphens, etc.) have to be entered in the name.\n• The Group's name can be changed manually afterwards.\n• This field reverts to empty after application.",
        subtype = "NONE",
        default = "",
    )
    bpy.utils.register_class(ZGSWTOR_OT_skinsettings_ng_in_3d_viewer)

def unregister():
    del bpy.types.Scene.apply_skinsettings_twilek
    del bpy.types.Scene.apply_skinsettings_name
    bpy.utils.unregister_class(ZGSWTOR_OT_skinsettings_ng_in_3d_viewer)


if __name__ == "__main__":
    register()