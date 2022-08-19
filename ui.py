import bpy


# 3D VIEWPORT PANEL ---------------------------------------------

# Materials Tools sub-panel
class ZGSWTOR_PT_materials_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Materials Tools"

    def draw(self, context):
        layout = self.layout


        # process_uber_mats UI
        tool_section = layout.box().column(align=True)
        
        resources_folder_exists = True
        modern_gr2_addon = True
        legacy_gr2_addon = True
        
        if resources_folder_exists == True and (modern_gr2_addon or legacy_gr2_addon): 
            tool_section.operator("zgswtor.process_uber_mats", text="Process Uber Materials")
            tool_section.prop(context.scene, "use_overwrite_bool", text="Overwrite Uber Materials")
            tool_section.prop(context.scene, "use_collect_colliders_bool", text="Collect Collider Objects")
        else:
            tool_section.label(text="PROCESS UBER MATERIALS")
            if resources_folder_exists == False:
                pass
            if (modern_gr2_addon or legacy_gr2_addon) == False:
                pass
        

        # CUSTOM SWTOR SHADERS SECTION
        # add_custom_external_swtor_shaders UI
        # combined with
        # customize_swtor_shaders UI
        tool_section = layout.box().column(align=True)
        dimmable_row1 = tool_section.row(align=True)
        dimmable_row1.enabled = context.scene.enable_adding_custom_shaders
        dimmable_row1.operator("zgswtor.add_custom_external_swtor_shaders", text="Add Custom SWTOR Shaders")
        tool_section.operator("zgswtor.customize_swtor_shaders", text="Convert to Custom SWTOR Shaders")
        dimmable_row2 = tool_section.row(align=True)
        dimmable_row2.enabled = context.scene.enable_linking_custom_shaders
        dimmable_row2.prop(context.scene, "use_linking_bool", text="Link instead of Append")
        tool_section.prop(context.scene, "preserve_atroxa_bool", text="Preserve Original Shaders")
        
        # skinsettings_ng_in_3d_viewer UI
        tool_section = layout.box().column(align=False)
        tool_section.operator("zgswtor.skinsettings_ng_in_3d_viewer", text="Apply New Skin Settings Group")
        row = tool_section.row()
        in_row = row.row(align=True)  # for setting a non-50% contiguous row region
        in_row.scale_x = 0.90  # Percentage of a full half row
        in_row.label(text="PC-NPC name")
        row.prop(context.scene, "apply_skinsettings_name", text="")
        tool_section.prop(context.scene, "apply_skinsettings_twilek")




        # deduplicate_nodegroups and deduplicate_materials UIs
        tool_section = layout.box().column(align=True)
        tool_section.operator("zgswtor.deduplicate_materials", text="Deduplicate All Materials")
        tool_section.operator("zgswtor.deduplicate_nodegroups", text="Deduplicate All Nodegroups")
        # Already existing Purge operator
        tool_section.operator("outliner.orphans_purge", text="Purge All Orphan Data Recursively").do_recursive=True



        # set_backface_culling UI
        tool_section = layout.box()
        row = tool_section.row(align=True)
        row.operator("zgswtor.set_backface_culling", text="Set Backface Culling On").action="BACKFACE_CULLING_ON"
        
        in_row = row.row()  # for setting a non-50% contiguous row region
        in_row.scale_x = 0.35
        in_row.operator("zgswtor.set_backface_culling", text="Off").action="BACKFACE_CULLING_OFF"






# Objects Tools sub-panel
class ZGSWTOR_PT_objects_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Objects Tools"

    def draw(self, context):
        layout = self.layout

        # quickscale UI
        tool_section = layout.box()
        row = tool_section.row(align=True)
        row.operator("zgswtor.quickscale", text="Downscale").action = "DOWNSCALE"
        in_row = row.row()  # for a non-50% contiguous row region
        in_row.scale_x = 0.9
        in_row.prop(context.scene, "zgswtor_quickscale_factor", text="")
        row.operator("zgswtor.quickscale", text="Upscale").action = "UPSCALE"


        # remove_doubles UI
        tool_section = layout.box()
        col=tool_section.column(align=True)
        col.operator("zgswtor.remove_doubles", text="Merge Double Vertices")
        # remove_doubles_edit_mode UI
        col.operator("zgswtor.remove_doubles_edit_mode", text="Merge Selected Double Vertices")



        # set_modifiers UI
        tool_section = layout.box()
        grid = tool_section.grid_flow(columns=2, align=True)
        grid.operator("zgswtor.set_modifiers", text="Add SubD").action = "add_subd"
        grid.operator("zgswtor.set_modifiers", text="Add Displace").action = "add_displace"
        grid.operator("zgswtor.set_modifiers", text="Add Multires").action = "add_multires"
        grid.operator("zgswtor.set_modifiers", text="Add Solidify").action = "add_solidify"
        row = tool_section.row()
        row.operator("zgswtor.set_modifiers", text="Remove These Modifiers").action = "remove_them"
        row = tool_section.row()
        row.label(text="Move Armature to")
        in_row = row.row(align=True)  # for setting a non-50% contiguous row region
        in_row.scale_x = 0.55
        in_row.operator("zgswtor.set_modifiers", text="First").action = "armature_first"
        in_row.operator("zgswtor.set_modifiers", text="Last").action = "armature_last"
        row = tool_section.row()
        row.label(text="Use Preserve Volume")
        in_row = row.row(align=True)  # for setting a non-50% contiguous row region
        in_row.scale_x = 0.55  # Percentage of a full half row
        in_row.operator("zgswtor.set_modifiers", text="On").action = "preserve_volume_on"
        in_row.operator("zgswtor.set_modifiers", text="Off").action = "preserve_volume_off"




# Misc. Tools sub-panel
class ZGSWTOR_PT_misc_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Misc. Tools"

    def draw(self, context):
        layout = self.layout

        #### Block of simple custom operators:
        tool_section = layout.box()
        row = tool_section.row(align=True)
        row.operator("zgswtor.set_dds", text="Set all .dds to Raw/Packed")

        #### Block of simple already existing Blender operators:
        tool_section = layout.box()
        
        # Simplify
        row = tool_section.row(align=True)
        row.prop(context.scene.render, "use_simplify", text=" Simplify")
        in_row = row.row()  # for a non-50% contiguous row region
        in_row.scale_x = 1.2
        in_row.prop(context.scene.render, "simplify_subdivision", text="Max SubD")

        # Pose Position / Reset Position
        row = tool_section.row(align=True)
        if context.object:
            if context.object.type == "ARMATURE":
                row.prop(context.object.data, "pose_position", expand=True)
            else:
                row.label(text="POSE / REST an Active Armature")
        else:
            row.label(text="POSE / REST an Active Armature")

        # Lock camera to view
        row = tool_section.row(align=True)
        row.prop(context.space_data, "lock_camera", text="Camera to View")            



# SHADER EDITOR PANEL -------------------------------------------

class ZGSWTOR_PT_shader_tools(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Tools"

    def draw(self, context):
        layout = self.layout

        # skinsettings_ng_in_shader_editor UI
        tool_section = layout.box().column(align=False)
        
        tool_section.operator("zgswtor.skinsettings_ng_in_shader_editor", text="Add New Skin Settings Group").action="ADD_NEW_SKINSETTINGS"
        row = tool_section.row()
        in_row = row.row(align=False)  # for setting a non-50% contiguous row region
        in_row.scale_x = 0.90  # Percentage of a full half row
        in_row.label(text="PC-NPC Name")
        row.prop(context.scene, "use_skinsettings_name", text="")

        # tool_section.operator("zgswtor.skinsettings_ng_in_shader_editor", text="Add existing Skin Settings Group").action="ADD_EXISTING_SKINSETTINGS"
        # build skinsettings nodegroups list
        skinsettings_nodegroups = []
        # for ng in bpy.data.node_groups:
        #     if "Skin Settings" in ng.name and not "Template" in ng.name:
        #         skinsettings_nodegroups.append(ng)
        # Show list
        # col = tool_section.column()
        # for ng in skinsettings_nodegroups:
        #     op = col.operator('matalogue.goto_group', text=ng.name, emboss=True, icon='NODETREE')
        #     op.tree_type = "ShaderNodeTree"
        #     op.tree = ng.name



        tool_section.operator("zgswtor.skinsettings_ng_in_shader_editor", text="Copy SkinB Data to Skin Settings Group").action="COPY_TO_SKINSETTINGS"
        tool_section.operator("zgswtor.skinsettings_ng_in_shader_editor", text="Connect Skin Group to SkinB Shader").action="CONNECT_SKINSETTINGS"
        tool_section.prop(context.scene,"use_skinsettings_twilek", text="Override Twi'lek GlossMap")
        tool_section.operator("zgswtor.skinsettings_ng_in_shader_editor", text="Disconnect Skin Group from SkinB Shader").action="DISCONNECT_SKINSETTINGS"

        tool_section = layout.box()
        row = tool_section.row(align=True)
        row.operator("zgswtor.shaders_io_linker", text="Link Matching Inputs/Outputs")

        tool_section = layout.box()
        col = tool_section.column(align=True)
        col.label(text="Copy Matching Inputs/Outputs' Values:")
        col.operator("zgswtor.shaders_io_copier", text="From Nodegroup To Active Nodegroup").action = "ng_to_ng"
        col.operator("zgswtor.shaders_io_copier", text="From Nodegroup To Settings Group").action = "ng_to_st"
        col.operator("zgswtor.shaders_io_copier", text="From Settings Group To Nodegroup").action = "st_to_ng"



# Registrations

classes = [
    ZGSWTOR_PT_materials_tools,
    ZGSWTOR_PT_objects_tools,
    ZGSWTOR_PT_misc_tools,
    ZGSWTOR_PT_shader_tools
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    
if __name__ == "__main__":
    register()