import bpy


class ZGSWTOR_OT_skinsettings_ng_in_shader_editor(bpy.types.Operator):
    bl_idname = "zgswtor.skinsettings_ng_in_shader_editor"
    bl_label = "ZG Add Skin Settings-Holder Nodegroup"
    bl_description = "Appends and manages skin settings-holding nodegroups."
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls,context):
        if context.material:
            if "SWTOR - SkinB Shader" in bpy.data.materials[context.material.name].node_tree.nodes and "SW Template - Character's Skin Settings" in bpy.data.node_groups:
                return True
            else:
                return False
        else:
            return False


    def update_skinsettings_nodegroups_list():
        pass
    
    # PROPERTIES

    # Property for the UI buttons to call different actions.
    # See: https://b3d.interplanety.org/en/calling-functions-by-pressing-buttons-in-blender-custom-ui/
    
    action: bpy.props.EnumProperty(
        name="skinsettings_actions",
        items=[
            ("ADD_NEW_SKINSETTINGS",
            "Add New Skin Settings Group",
            "Add New Skin Settings-Holder Nodegroup"),

            ("ADD_EXISTING_SKINSETTINGS",
            "Add Existing Skin Settings Group",
            "Add Existing Skin Settings-Holder Nodegroup"),

            ("COPY_TO_SKINSETTINGS",
            "Copy Shader Settings to Skin Group",
            "Copy data from Skin Shader to Nodegroup"),

            ("CONNECT_SKINSETTINGS",
            "Connect Skin Group to Shader",
            "Connect Nodegroup to Skin Shader"),

            ("DISCONNECT_SKINSETTINGS",
            "Disconnect Skin Group from Shader",
            "Disconnect Skin Group from Shader")
            ],
        options={'HIDDEN'}
        )

    
    def execute(self, context):
        bpy.context.window.cursor_set("WAIT")

        mat_node_tree = bpy.data.materials[context.material.name].node_tree
        mat_nodes = mat_node_tree.nodes
        mat_links = mat_node_tree.links

        if self.action == "ADD_NEW_SKINSETTINGS":

            if context.scene.use_skinsettings_name == "" or context.scene.use_skinsettings_name.strip() == "":
                bpy.context.window.cursor_set("DEFAULT")
                self.report({"WARNING"}, "Please enter a character's name for the Skin Settings Nodegroup")
                context.scene.use_skinsettings_name = ""
                return {"CANCELLED"}

            character_name = context.scene.use_skinsettings_name
            zg_skinsettings_name = character_name + "'s Skin Settings"

            if zg_skinsettings_name in bpy.data.node_groups:
                bpy.context.window.cursor_set("DEFAULT")
                self.report({"WARNING"}, 'A "' + zg_skinsettings_name + '" Nodegroup already exists.')
                context.scene.use_skinsettings_name = ""
                return {"CANCELLED"}
            
            # Make a local copy of template "SW Template - Character's Skin Settings" Nodegroup
            # using zg_skinsettings_name as its name. 
            zg_skinsettings_local = bpy.data.node_groups["SW Template - Character's Skin Settings"].copy()
            zg_skinsettings_local.name = zg_skinsettings_name

            # Add an instance of the Nodegroup to the Material
            zg_skinsettings_node = mat_nodes.new(type="ShaderNodeGroup")
            zg_skinsettings_node.node_tree = bpy.data.node_groups[zg_skinsettings_local.name]
            zg_skinsettings_node.name = zg_skinsettings_name
            zg_skinsettings_node.width = 250
            zg_skinsettings_node.location = -450, -650

            context.scene.use_skinsettings_name = ""

        elif self.action == "ADD_EXISTING_SKINSETTINGS":

            skinsetting_nodegroups=[]
            for ng in bpy.data.node_groups:
                if "Skin Settings" in ng.name and ng.name != "SW Template - Character's Skin Settings":
                    skinsetting_nodegroups.append( (ng.name, ng.name, ng.name) )
            skinsettings_ng_in_shader_editors_list = skinsetting_nodegroups

            # Make a local copy of linked "SW Template - Character's Skin Settings" nodegroup
            zg_skinsettings_local = bpy.data.node_groups["SW Template - Character's Skin Settings"].copy()
            zg_skinsettings_local.name = "NAME Skin Settings"

            # Add an instance of the Nodegroup to the Material
            zg_skinsettings_node = mat_nodes.new(type="ShaderNodeGroup")
            zg_skinsettings_node.node_tree = bpy.data.node_groups[zg_skinsettings_local.name]
            
            zg_skinsettings_node.width = 250
            zg_skinsettings_node.location = -450, -650

        elif self.action == "COPY_TO_SKINSETTINGS":

            # Detect Skin Settings Nodegroups in the selection
            selected_nodes = bpy.context.selected_nodes

            zg_skinsettings_node = None
            for node in selected_nodes:
                if "Skin Settings" in node.name:
                    # zg_skinsettings_node = node  <-- This doesn't work
                    zg_skinsettings_node = bpy.data.node_groups[node.name]  # This does
                    break
            if zg_skinsettings_node == None:
                bpy.context.window.cursor_set("DEFAULT")
                self.report({"WARNING"}, "No selected Character Skin Settings Nodegroup")
                context.scene.use_skinsettings_name = ""
                return {"CANCELLED"}

            # Copy SkinB input values to Skin Settings Nodegroup's Output Node's values
            zg_skinb_node = mat_nodes["SWTOR - SkinB Shader"]

            zg_skinsettings_nodegroup_output = zg_skinsettings_node.nodes["Group Output"]


            for output in zg_skinsettings_node.outputs:
                if output.hide_value == False and output.name in zg_skinb_node.inputs:  # If sockets aren't cosmetic then do
                    zg_skinsettings_nodegroup_output.inputs[output.name].default_value = zg_skinb_node.inputs[output.name].default_value

            if context.scene.use_skinsettings_twilek == True:
                mat_links.new(zg_skinsettings_node.outputs["Twi'lek GlossMap Color"],zg_skinb_node.inputs["_s GlossMap Color"])
                mat_links.new(zg_skinsettings_node.outputs["Twi'lek GlossMap Alpha"],zg_skinb_node.inputs["_s GlossMap Alpha"])
                # mat_links.remove(zg_skinsettings_node.outputs["Twi'lek GlossMap Alpha"],zg_skinb_node.inputs["_s GlossMap Alpha"])

        elif self.action == "CONNECT_SKINSETTINGS":

            # Detect Skin Settings Nodegroups in the selection
            # and make sure of selecting a single one
            selected_nodes = bpy.context.selected_nodes
            zg_skinsettings_nodes = []
            for node in selected_nodes:
                if "Skin Settings" in node.name:
                    zg_skinsettings_nodes.append(node)
            if len(zg_skinsettings_nodes) == 0:
                bpy.context.window.cursor_set("DEFAULT")
                self.report({"WARNING"}, "No selected Character Skin Settings Nodegroup")
                context.scene.use_skinsettings_name = ""
                return {"CANCELLED"}
            if len(zg_skinsettings_nodes) > 1:
                bpy.context.window.cursor_set("DEFAULT")
                self.report({"WARNING"}, "Too many Character Skin Settings Nodegroups selected. Select a single one")
                context.scene.use_skinsettings_name = ""
                return {"CANCELLED"}

            zg_skinsettings_node = zg_skinsettings_nodes[0]
            zg_skinb_node = mat_nodes["SWTOR - SkinB Shader"]

            for output in zg_skinsettings_node.outputs:
                if output.hide_value == False and output.name in zg_skinb_node.inputs:
                    mat_links.new(zg_skinsettings_node.outputs[output.name],zg_skinb_node.inputs[output.name])
            
            # Special rewiring for Twi'lek characters if checkboxed
            if context.scene.use_skinsettings_twilek == True:
                mat_links.new(zg_skinsettings_node.outputs["Twi'lek GlossMap Color"],zg_skinb_node.inputs["_s GlossMap Color"])
                mat_links.new(zg_skinsettings_node.outputs["Twi'lek GlossMap Alpha"],zg_skinb_node.inputs["_s GlossMap Alpha"])


        elif self.action == "DISCONNECT_SKINSETTINGS":
            links_to_delete = []
            for link in mat_links:
                if "Skin Settings" in link.from_node.name:
                    links_to_delete.append(link)
            if len(links_to_delete) > 0:
                for link in links_to_delete:
                    mat_links.remove(link)


        context.scene.apply_skinsettings_name = ""

        bpy.context.window.cursor_set("DEFAULT")
        return {"FINISHED"}


# UI is set in ui.py

# Registrations

def register():
    bpy.types.Scene.use_skinsettings_twilek = bpy.props.BoolProperty(
        name="Override Twi'lek GlossMaps",
        description="If True, disconnect GlossMaps in SkinB shader and connect\nSkin Settings Nodegroup's Twi'lek ones.",
        default = False,
    )
    bpy.types.Scene.use_skinsettings_name = bpy.props.StringProperty(
        name="Skin Settings Nodegroup's prefix name",
        description="Name of the character to apply to\nthe Nodegroup's name (\"<name>'s Skin Settings\").\n\n• It is case-sensitive.\n• This field reverts to empty after application.\nCan be changed manually later on.",
        subtype = "NONE",
        default = "",
    )
    # bpy.types.Scene[skinsettings_available] = bpy.props.EnumProperty(
    #     items=[
    #         ()
    #     ]
    # )

    bpy.utils.register_class(ZGSWTOR_OT_skinsettings_ng_in_shader_editor)

def unregister():
    del bpy.types.Scene.use_skinsettings_twilek
    del bpy.types.Scene.use_skinsettings_name
    # del bpy.types.Scene.skinsettings_ng_in_shader_editors_list
    bpy.utils.unregister_class(ZGSWTOR_OT_skinsettings_ng_in_shader_editor)


if __name__ == "__main__":
    register()