import bpy
import addon_utils
from pathlib import Path


# 3D VIEWPORT PANEL ---------------------------------------------

# Addon Status sub-panel
class ZGSWTOR_PT_status(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "ZG SWTOR Tools Status"

    def draw(self, context):

        # Checks:
        
        # Extracted SWTOR assets' "resources" folder. 
        swtor_resources_folderpath = bpy.context.preferences.addons[__package__].preferences.swtor_resources_folderpath
        resources_folder_exists = ( Path(swtor_resources_folderpath) / "art/shaders/materials").exists()
        # .gr2 Importer Addon
        gr2_addon_exists = addon_utils.check("io_scene_gr2")[1]
        legacy_gr2_addon_exists = addon_utils.check("io_scene_gr2_legacy")[1]
        # Custom shaders .blend file
        custom_shaders_blend_file_exists =  Path(bpy.context.preferences.addons[__package__].preferences.swtor_custom_shaders_blendfile_path).is_file()


        layout = self.layout
        layout.scale_y = 0.7

        # Show whether the 'resources' folder is set correctly in Preferences.
        zgswtor_addon_status = layout.column(align=True)
        # zgswtor_addon_status.scale_y = 0.7
        
        if resources_folder_exists == True:
            zgswtor_addon_status.label(text="• 'resources' Folder: SET")
        else:
            zgswtor_addon_status.label(text="• 'resources' Folder: NOT SET")

        if custom_shaders_blend_file_exists == True:
            zgswtor_addon_status.label(text="• Custom Shaders: SET")
        else:
            zgswtor_addon_status.label(text="• Custom Shaders: NOT SET")

        if gr2_addon_exists == True:
            zgswtor_addon_status.label(text="• .gr2 Addon: MODERN VERSION SET")
        else:
            if legacy_gr2_addon_exists == True:
                zgswtor_addon_status.label(text="• .gr2 Addon: LEGACY VERSION SET")
            else:
                zgswtor_addon_status.label(text="• .gr2 Addon: UNAVAILABLE")

        
        if (
            resources_folder_exists == False
            or custom_shaders_blend_file_exists == False
            or gr2_addon_exists == False
            ):
            zgswtor_addon_status.label(text=" ")
            zgswtor_addon_status.label(text="Tools in red require setting Addon")
            zgswtor_addon_status.label(text="preferences (check their tooltips).")

# Files Tools sub-panel
class ZGSWTOR_PT_files_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Files Tools"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        gral_y_scaling_factor = 0.9

        # CHECKS:
        # Extracted SWTOR assets' "resources" folder. 
        swtor_resources_folderpath = bpy.context.preferences.addons[__package__].preferences.swtor_resources_folderpath
        resources_folder_exists = ( Path(swtor_resources_folderpath) / "art/shaders/materials").exists()
        # .gr2 Importer Addon
        gr2_addon_exists = addon_utils.check("io_scene_gr2")[1]
        # Custom shaders .blend file
        custom_shaders_blend_file_exists =  Path(bpy.context.preferences.addons[__package__].preferences.swtor_custom_shaders_blendfile_path).is_file()


        layout = self.layout
        layout.scale_y = gral_y_scaling_factor


        # character_assembler UI
        tool_section = layout.box().column(align=True)
        tool_section.enabled = resources_folder_exists
        tool_section.alert = tool_section.enabled is False
        tool_section.label(text="PC / NPC Importer")
        tool_section.operator("zgswtor.character_assembler", text="Select 'paths.json' File")
        tool_section.prop(context.scene, "swca_prefix_str", text="Prefix")
        tool_section.prop(context.scene, "swca_gather_only_bool", text="Gather Assets only")
        tool_section.prop(context.scene, "swca_dont_overwrite_bool", text="Don't Overwrite Assets")
        tool_section.prop(context.scene, "swca_collect_bool", text="Collect By In-Game Names")
        tool_section.prop(context.scene, "swca_import_armor_only", text="Import Armor Gear Only")
        tool_section.prop(context.scene, "swca_import_skeleton_bool", text="Import Rigging Skeleton")
        tool_section.prop(context.scene, "swca_bind_to_skeleton_bool", text="Bind Objects To Skeleton",)

        


# Materials Tools sub-panel
class ZGSWTOR_PT_materials_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Materials Tools"

    def draw(self, context):

        gral_y_scaling_factor = 0.9

        # CHECKS:
        # Extracted SWTOR assets' "resources" folder. 
        swtor_resources_folderpath = bpy.context.preferences.addons[__package__].preferences.swtor_resources_folderpath
        resources_folder_exists = ( Path(swtor_resources_folderpath) / "art/shaders/materials").exists()
        # .gr2 Importer Addon
        gr2_addon_exists = addon_utils.check("io_scene_gr2")[1]
        # Custom shaders .blend file
        custom_shaders_blend_file_exists =  Path(bpy.context.preferences.addons[__package__].preferences.swtor_custom_shaders_blendfile_path).is_file()


        layout = self.layout
        layout.scale_y = gral_y_scaling_factor


        # process_uber_mats UI
        tool_section = layout.box().column(align=True)
        tool_section.enabled = resources_folder_exists and gr2_addon_exists
        tool_section.alert = tool_section.enabled is False

                
        tool_section.label(text="Process Static Object Materials in")

        split = tool_section.split(factor= 0.60, align=True)
        col_left, col_right = split.column(align=True), split.column(align=True)

        process_mats_sel = col_left.operator("zgswtor.process_uber_mats", text="Selected Objects")
        col_left.enabled = len(bpy.context.selected_objects) != 0
        process_mats_sel.use_selection_only = True

        process_mats_all = col_right.operator("zgswtor.process_uber_mats", text="All Objects")
        col_right.enabled = len(bpy.data.objects) != 0
        process_mats_all.use_selection_only = False

        process_mats_sel = tool_section.prop(context.scene, "use_overwrite_bool", text="Overwrite Materials")
        process_mats_all = tool_section.prop(context.scene, "use_collect_colliders_bool", text="Collect Collider Objects")
        


        # CUSTOM SWTOR SHADERS SECTION
        # add_custom_external_swtor_shaders UI
        # combined with
        # customize_swtor_shaders UI
        tool_section = layout.box().column(align=True)
        tool_section.enabled = custom_shaders_blend_file_exists
        tool_section.alert = tool_section.enabled is False
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
        
        gral_y_scaling_factor = 0.8

        layout = self.layout
        layout.scale_y = gral_y_scaling_factor


        # quickscale UI
        tool_section = layout.box()
        row = tool_section.row(align=True)
        row.operator("zgswtor.quickscale", text="Downscale").action = "DOWNSCALE"
        in_row = row.row()
        in_row.scale_x = 0.9  # for a non-50% contiguous row region
        in_row.prop(context.scene, "zgswtor_quickscale_factor", text="")
        row.operator("zgswtor.quickscale", text="Upscale").action = "UPSCALE"

        # Apply Transforms
        row = tool_section.row(align=True)
        row.label(text="Apply Transforms")
        in_row = row.row(align=True)
        in_row.scale_x = 0.60
        # Passing multiple properties to an operator.
        # See: https://b3d.interplanety.org/en/executing-operators-with-parameters/

        applPosButton = in_row.operator("object.transform_apply", text="Loc.")
        applPosButton.location = True
        applPosButton.rotation = False
        applPosButton.scale = False
        applPosButton.properties = False

        applRotButton = in_row.operator("object.transform_apply", text="Rot.",)
        applRotButton.location = False
        applRotButton.rotation = True
        applRotButton.scale = False
        applRotButton.properties = False

        applSclButton = in_row.operator("object.transform_apply", text="Scale")
        applSclButton.location = False
        applSclButton.rotation = False
        applSclButton.scale = True
        applSclButton.properties = False

        # Non-editable Transform data to check the effects of Apply Transforms 
        # row = tool_section.row(align=False)
        # row.scale_y = .70
        # row.enabled = False
        # col = row.column(align=True)
        # col.prop(context.object, "location", text="Location")
        # col = row.column(align=True)
        # col.prop(context.object, "rotation_euler", text="Rotation")
        # col = row.column(align=True)
        # col.prop(context.object, "scale", text="Scale")


        # remove_doubles UI
        tool_section = layout.box()
        col=tool_section.column(align=True)
        col.operator("zgswtor.remove_doubles", text="Merge Double Vertices")
        # remove_doubles_edit_mode UI
        col.operator("zgswtor.remove_doubles_edit_mode", text="Merge Selected Double Vertices")


        # set_modifiers UI
        tool_section = layout.box()
        grid = tool_section.grid_flow(row_major=True, columns=2, align=True)
        grid.operator("zgswtor.set_modifiers", text="Add SubD").action = "add_subd"
        grid.operator("zgswtor.set_modifiers", text="Add Multires").action = "add_multires"
        grid.operator("zgswtor.set_modifiers", text="Add Displace").action = "add_displace"
        grid.operator("zgswtor.set_modifiers", text="Add Solidify").action = "add_solidify"
        grid.operator("zgswtor.set_modifiers", text="Add Smooth Corrective").action = "add_smooth_corrective"
        grid.operator("zgswtor.set_modifiers", text="Add Shrinkwrap").action = "add_shrinkwrap"
        row = tool_section.row(align=True)
        split = row.split(factor=0.55, align=True)
        col_left, col_right = split.column(align=True), split.column(align=True)
        col_left.label(text="Shrinkwrap Target")
        col_right.prop(context.scene, "shrinkwrap_target", text="")





        row = tool_section.row()
        row.operator("zgswtor.set_modifiers", text="Remove These Modifiers").action = "remove_them"

        row = tool_section.row()
        row.label(text="Set Armature as")
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
        layout.scale_y = 0.8


        #### Block of simple custom operators:
        tool_section = layout.box()
        col=tool_section.column(align=False)
        col.operator("zgswtor.set_dds", text="Set all .dds images to Raw/Packed")
        col.operator("zgswtor.selected_vertices_to_sculpt_mask", text="Mask Selected Verts from Sculpting")


        # row = tool_section.row(align=True)
        # row.operator("zgswtor.turn_animation_180", text="Turn Animation 180°")



        #### Block of simple already existing Blender operators:
        tool_section = layout.box()
        
        # Simplify 
        row = tool_section.row(align=True)

        row.prop(context.scene.render, "use_simplify", text=" Simplify")
        in_row = row.row()  # for a non-50% contiguous row region
        in_row.scale_x = 1.2
        in_row.prop(context.scene.render, "simplify_subdivision", text="Max SubD")

        # Pose Position / Reset Position
        tool_section = layout.box()

        row = tool_section.row(align=True)
        row.label(text="Armatures In Scene:")
        # Arbitrary selected objects limit to avoid
        # the whole panel grinding to a halt in cases
        # of selected whole worlds and such.
        if context.scene.objects:
            for obj in context.scene.objects:
                if obj.type == "ARMATURE":
                    armature_col = tool_section.column(align=True)
                    armature_col.label(text=obj.name)
                    armature_buttons = armature_col.row(align=True)
                    armature_buttons.prop(obj.data, "pose_position", expand=True)







# ---------------------------------------------------------------
# SHADER EDITOR PANEL -------------------------------------------
# ---------------------------------------------------------------

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
    ZGSWTOR_PT_status,
    ZGSWTOR_PT_files_tools,
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