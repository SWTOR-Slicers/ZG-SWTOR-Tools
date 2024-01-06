import bpy


class ZGSWTOR_OT_rimlightsettings_ng_in_3d_viewer(bpy.types.Operator):
    bl_idname = "zgswtor.rimlightsettings_ng_in_3d_viewer"
    bl_label = "ZG Apply Rim Light Settings-Holder Nodegroup to selected objects"
    bl_description = "Applies a Rim Light Settings-holding \"control panel\" Nodegroup to selected objects.\n\n• Only works on Custom SWTOR Shaders.\n• Requires a selection of objects"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls,context):
        if bpy.context.selected_objects:
            return True
        else:
            return False

    
    
    def execute(self, context):
        bpy.context.window.cursor_set("WAIT")

        if (not "SWTOR - Uber Shader" in bpy.data.node_groups
        and not "SWTOR - Creature Shader" in bpy.data.node_groups
        and not "SWTOR - Garment Shader" in bpy.data.node_groups
        and not "SWTOR - SkinB Shader" in bpy.data.node_groups
        and not "SWTOR - HairC Shader" in bpy.data.node_groups):
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, "No Custom SWTOR Shaders present in this project")
            return {"CANCELLED"}

        if not "SW Template - Rim Light Settings" in bpy.data.node_groups:
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, "No Rim Light Settings Nodegroup template present in this project")
            return {"CANCELLED"}

        if context.scene.apply_rimlightsettings_name == "" or context.scene.apply_rimlightsettings_name.strip() == "":
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, "Please enter a name for the Skin Settings Nodegroup")
            context.scene.apply_rimlightsettings_name = ""
            return {"CANCELLED"}


        objs = bpy.context.selected_objects
        
        # Prepare named local Rim Light settings Nodegroup -----------------------------
        
        zg_rimlightsettings_name = context.scene.apply_rimlightsettings_name + " Skin Settings"

        if zg_rimlightsettings_name in bpy.data.node_groups:
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, 'A "' + zg_rimlightsettings_name + '" Nodegroup already exists.')
            context.scene.apply_rimlightsettings_name = ""
            return {"CANCELLED"}
        
        # Make a local copy of template "SW Template - Rim Light Settings" Nodegroup
        # using zg_rimlightsettings_name as its name. 
        zg_rimlightsettings_local = bpy.data.node_groups["SW Template - Rim Light Settings"].copy()
        zg_rimlightsettings_local.name = zg_rimlightsettings_name



        # Cycle through Materials --------------------------------------------------------------

        for obj in objs:
            if obj.material_slots:
                for slot in material_slots:
                    mat = slot.material
            
                    mat_nodes = mat.node_tree.nodes
                    if len(mat_nodes) == 0:
                        print("Material " + mat.name + " has no nodes.")
                        continue

                    mat_links = mat.node_tree.links

                    # Find in material's node tree a Custom SWTOR Shader to connect to

                    for node in mat_nodes:
                        if "SWTOR - " in node.name and not "Eye" in node.name:
                            if node.name == "SWTOR - SkinB Shader" and preserve_skinsettings_rimlight == True:
                                continue
                            else: 
                                # Add an instance of the Nodegroup to the Material or use the existing one
                                if not zg_rimlightsettings_name in mat_nodes:
                                    zg_rimlightsettings_node = mat_nodes.new(type="ShaderNodeGroup")
                                    zg_rimlightsettings_node.node_tree = bpy.data.node_groups[zg_rimlightsettings_local.name]
                                    zg_rimlightsettings_node.name = zg_rimlightsettings_name
                                    zg_rimlightsettings_node.width = 250
                                    zg_rimlightsettings_node.location = -450, -650
                                else:
                                    zg_rimlightsettings_node = mat_nodes[zg_rimlightsettings_name]


                                    # Connect Rim Light Settings Nodegroup to Custom SWTOR Nodegroup
                                    for output in zg_rimlightsettings_node.outputs:
                                        if output.hide_value == False and output.name in target_zg_node.inputs:
                                            mat_links.new(zg_rimlightsettings_node.outputs[output.name],target_zg_node.inputs[output.name])


                                    # Special rewiring for Twi'lek characters if checkboxed
                                    if context.scene.apply_skinsettings_twilek == True:
                                        mat_links.new(zg_rimlightsettings_node.outputs["Twi'lek GlossMap Color"],target_zg_node.inputs["_s GlossMap Color"])
                                        mat_links.new(zg_rimlightsettings_node.outputs["Twi'lek GlossMap Alpha"],target_zg_node.inputs["_s GlossMap Alpha"])


                                    # If material = skin reference material, copy SkinB values to Skin Settings Nodegroup
                                    if mat.name == ref_mat:
                                        
                                        # Skin Settings Nodegroup's Group Output Node where to copy the SkinB values into
                                        zg_rimlightsettings_nodegroup_output = bpy.data.node_groups[zg_rimlightsettings_name].nodes["Group Output"]
                                        
                                        # Cycle through outputs' names to find matching SkinB inputs and copy their values
                                        for output in zg_rimlightsettings_node.outputs:
                                            # Skip label-like outputs
                                            if output.hide_value == False and output.name in target_zg_node.inputs:
                                                zg_rimlightsettings_nodegroup_output.inputs[output.name].default_value = target_zg_node.inputs[output.name].default_value


        context.scene.apply_rimlightsettings_name = ""
        
        bpy.context.window.cursor_set("DEFAULT")
        return {"FINISHED"}


# UI is set in ui.py





# Registrations

def register():
    bpy.types.Scene.preserve_skinsettings_rimlight = bpy.props.BoolProperty(
        name="Override Twi'lek GlossMaps",
        description="If ticked, disconnects the GlossMaps and connects\nsimpler common values in their place.\n\n(For some reason, Twi'lek heads' GlossMaps don't match\nhumanoid bodies' ones, producing a noticeable seam effect)",
        default = False,
    )
    bpy.types.Scene.apply_rimlightsettings_name = bpy.props.StringProperty(
        name="Skin Settings Nodegroup's prefix name",
        description="Name of the character to apply to\nthe Nodegroup's name (\"<name>'s Skin Settings\").\n\n• It is case-sensitive.\n• This field reverts to empty after application.\nCan be changed manually later on.",
        subtype = "NONE",
        default = "",
    )
    bpy.utils.register_class(ZGSWTOR_OT_rimlightsettings_ng_in_3d_viewer)

def unregister():
    del bpy.types.Scene.preserve_skinsettings_rimlight
    del bpy.types.Scene.apply_rimlightsettings_name
    bpy.utils.unregister_class(ZGSWTOR_OT_rimlightsettings_ng_in_3d_viewer)


if __name__ == "__main__":
    register()