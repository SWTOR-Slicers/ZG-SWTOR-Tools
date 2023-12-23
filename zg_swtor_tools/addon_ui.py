from json import tool
from re import T
import bpy
import os

import addon_utils
from pathlib import Path



from .utils.addon_checks import requirements_checks



ADDON_ROOT = __file__.rsplit(__name__.rsplit(".")[0])[0] + __name__.rsplit(".")[0]

Y_SCALING_GRAL = 0.9
Y_SCALING_INFO = 0.75
Y_SCALING_SPACER = 0.3



# 3D VIEWPORT PANEL ---------------------------------------------

# Addon Status sub-panel
class ZGSWTOR_PT_status(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "ZG SWTOR Tools Status"

    def draw(self, context):
        
        checks = requirements_checks()

        layout = self.layout
        layout.scale_y = Y_SCALING_GRAL

        tool_section = layout.column(align=True)
        tool_section.scale_y = Y_SCALING_INFO
        
        tool_section.alert = not checks["gr2"]
        tool_section.label(text="• .gr2 Add-on: " + checks["gr2_status"])

        tool_section.alert = not checks["resources"]
        tool_section.label(text="• 'resources' Folder: " + checks["resources_status"])

        tool_section.alert = not checks["custom_shaders"]
        tool_section.label(text="• Custom Shaders: " + checks["custom_shaders_status"])


        tool_section_pref = layout.column(align=True)
        tool_section_pref.scale_y = Y_SCALING_GRAL
        tool_section_pref.operator("zgswtor.open_addon_preferences", text="Add-on's Preferences")


        tool_section.alert = False
        if (
            checks["resources"] == False
            or checks["custom_shaders"] == False
            or checks["gr2"] == False
            ):
            
            # ---- spacer
            tool_section_spacer = tool_section.column(align=True)
            tool_section_spacer.scale_y = Y_SCALING_SPACER
            tool_section_spacer.label(text="")
            # -----------
            
            tool_section_info = layout.column(align=True)
            tool_section_info.scale_y = Y_SCALING_INFO
            tool_section_info.label(text="Tools showing up in red need")
            tool_section_info.label(text="to satisfy certain requirements")
            tool_section_info.label(text="(more info in their tooltips).")
            
            # ---- spacer
            tool_section_spacer = tool_section.column(align=True)
            tool_section_spacer.scale_y = Y_SCALING_SPACER
            tool_section_spacer.label(text="")
            # -----------


# Area Tools sub-panel
class ZGSWTOR_PT_area_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Area Tools"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        checks = requirements_checks()

        layout = self.layout
        layout.scale_y = Y_SCALING_GRAL

        # character_assembler UI
        tool_section = layout.box().column(align=True)
        tool_section.scale_y = 1.0
        tool_section.enabled = checks["resources"]
        tool_section.alert = tool_section.enabled is False
        
        tool_section.label(text="SWTOR Area Assembler")
        tool_section.operator("zgswtor.area_assembler", text="Select Area's .json Files")

        tool_section_props = tool_section.column(align=True)
        tool_section_props.scale_y = Y_SCALING_GRAL
        tool_section_props.prop(context.scene, "ZGSAA_ApplyFinalRotation",    text="Apply Final Rotation")
        tool_section_props.prop(context.scene, "ZGSAA_ApplyMaterials",        text="Process Named Materials")
        tool_section_props.prop(context.scene, "ZGSAA_ApplySceneScale",       text="Apply x10 Scene Scale")
        tool_section_props.prop(context.scene, "ZGSAA_SkipDBOObjects",        text="Skip dbo Objects")
        tool_section_props.prop(context.scene, "ZGSAA_CreateSceneLights",     text="Create Scene Lights")
        tool_section_props.prop(context.scene, "ZGSAA_CollectionObjects",     text="Collect Objects By Type")
        tool_section_props.prop(context.scene, "ZGSAA_MergeMultiMeshObjects", text="Merge Multi-Mesh Objects")
        tool_section_props.prop(context.scene, "ZGSAA_ShowFullReport",        text="Full Report In Terminal")
        
        # ---- spacer
        tool_section_spacer = tool_section.column(align=True)
        tool_section_spacer.scale_y = Y_SCALING_SPACER
        tool_section_spacer.label(text="")
        # -----------
        
        tool_section_props = tool_section.column(align=True)
        tool_section_props.scale_y = Y_SCALING_INFO
        tool_section_props.label(text="To keep Blender responsive")
        tool_section_props.label(text="after importing massive areas:")
        tool_section_props = tool_section.column(align=True)
        tool_section_props.scale_y = Y_SCALING_GRAL
        tool_section_props.prop(context.scene, "ZGSAA_HideAfterImport",       text="Hide Objects",)
        tool_section_props.prop(context.scene, "ZGSAA_ExcludeAfterImport",    text="Hide Collections' Contents",)



        # group_collections UI
        tool_section = layout.box().column(align=False)
        
        tool_section.operator("zgswtor.group_collections", text="Group Areas in SubCollections")
        split = tool_section.split(factor= 0.70, align=False)
        col_left, col_right = split.column(align=True).row(align=False), split.column(align=True).row(align=False)
        col_left.label(text="Grouping Separator")
        col_right.prop(context.scene, "GC_coll_grouping_separator", text="")
        split = tool_section.split(factor= 0.70, align=False)
        col_left, col_right = split.column(align=True).row(align=False), split.column(align=True).row(align=False)
        col_left.label(text="Grouping Levels")
        col_right.prop(context.scene, "GC_coll_grouping_levels", text="")
        
        
        
        # exclude_all_collections UI
        tool_section = layout.box().column(align=False)
        tool_section.label(text="All Collections In Outliner")
        row = tool_section.row(align=True)
        disable = row.operator("zgswtor.exclude_all_collections", text="Disable")
        disable.untick = True
        disable = row.operator("zgswtor.exclude_all_collections", text="Enable")
        disable.untick = False



# Character Tools sub-panel
class ZGSWTOR_PT_character_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Character Tools"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        checks = requirements_checks()        

        layout = self.layout
        layout.scale_y = Y_SCALING_GRAL


        # character_assembler UI
        tool_section = layout.box().column(align=True)
        
        tool_section.label(text="Character Assembler")

        if not checks["resources"]:
        # tool_section.enabled = checks["resources"]
            tool_section_info = tool_section.column(align=True)
            tool_section_info.scale_y = Y_SCALING_INFO
            tool_section_info.alert = True
            tool_section_info.label(text="Without setting a resources")
            tool_section_info.label(text="folder, success will depend")
            tool_section_info.label(text="on the PC/NPC folder already")
            tool_section_info.label(text="holding ALL its assets.")
            
            # ---- spacer
            tool_section_spacer = tool_section.column(align=True)
            tool_section_spacer.scale_y = Y_SCALING_SPACER
            tool_section_spacer.label(text="")
            # -----------
            
            tool_section_info.alert = False

        tool_section.scale_y = 1.0
        tool_section.operator("zgswtor.character_assembler", text="Select 'paths.json' File")
        
        # Options whose availability depends on a 'resources' folder in Preferences
        tool_section_dimmables = tool_section.column(align=True)
        tool_section_dimmables.enabled = checks["resources"]
        tool_section_dimmables.prop(context.scene, "zg_swca_gather_only_bool", text="Gather Assets only")
        tool_section_dimmables.prop(context.scene, "zg_swca_dont_overwrite_bool", text="Don't Overwrite Assets")
        tool_section = tool_section.column(align=True)
        tool_section.prop(context.scene, "zg_swca_collect_bool", text="Collect By In-Game Names")
        tool_section.prop(context.scene, "zg_swca_import_armor_only", text="Import Armor Gear Only")
        tool_section.prop(context.scene, "zg_swca_import_skeleton_bool", text="Import Rigging Skeleton")
        tool_section.prop(context.scene, "zg_swca_bind_to_skeleton_bool", text="Bind Objects To Skeleton",)
        
        
        # prefixer UI
        tool_section = layout.box()
        
        tool_section_info = tool_section.column(align=True)
        tool_section_info.scale_y = Y_SCALING_INFO
        tool_section_info.label(text="It is advisable to change the")
        tool_section_info.label(text="character's Objects, Materials")
        tool_section_info.label(text="and Skeleton names to avoid")
        tool_section_info.label(text="conflicts with further imports.")
        
        col=tool_section.column(align=False)
        col.operator("zgswtor.prefixer", text="Prefix Selected Items' Names")
        col.prop(context.scene, "zg_prefix", text = "Prefix")
        col.prop(context.scene, "zg_prefix_mats_skeletons_bool", text="Prefix their Materials / Skeletons")
        


# Materials Tools sub-panel
class ZGSWTOR_PT_materials_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Materials Tools"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        Y_SCALING_GRAL = 0.9

        checks = requirements_checks()

        layout = self.layout
        layout.scale_y = Y_SCALING_GRAL


        # PROCESS NAMED MATERIALS UI
        tool_section = layout.box().column(align=True)
        tool_section.enabled = checks["resources"] and checks["gr2"]
        tool_section.alert = tool_section.enabled is False

        tool_section.label(text="Process Named Materials In")

        split = tool_section.split(factor= 0.60, align=True)
        col_left, col_right = split.column(align=True), split.column(align=True)

        process_mats_sel = col_left.operator("zgswtor.process_named_mats", text="Selected Objects")
        col_left.enabled = len(bpy.context.selected_objects) != 0
        process_mats_sel.use_selection_only = True

        process_mats_all = col_right.operator("zgswtor.process_named_mats", text="All Objects")
        col_right.enabled = len(bpy.data.objects) != 0
        process_mats_all.use_selection_only = False

        process_mats_sel = tool_section.prop(context.scene, "use_overwrite_bool", text="Overwrite Materials")
        process_mats_all = tool_section.prop(context.scene, "use_collect_colliders_bool", text="Collect Collider Objects")


        # CUSTOM SWTOR SHADERS SECTION
        # add_custom_external_swtor_shaders UI
        # combined with
        # customize_swtor_shaders UI
        tool_section = layout.box().column(align=True)
        tool_section.enabled = checks["custom_shaders"]
        tool_section.alert = tool_section.enabled is False
        tool_section.row(align=True).label(text="Convert to Custom Shaders")
        # tool_section.operator("zgswtor.customize_swtor_shaders", text="Convert to Custom Shaders")
        
        split = tool_section.split(factor= 0.60, align=True)
        col_left, col_right = split.column(align=True), split.column(align=True)

        process_mats_sel = col_left.operator("zgswtor.customize_swtor_shaders", text="Selected Objects")
        col_left.enabled = len(bpy.context.selected_objects) != 0
        process_mats_sel.use_selection_only = True

        process_mats_all = col_right.operator("zgswtor.customize_swtor_shaders", text="All Objects")
        col_right.enabled = len(bpy.data.objects) != 0
        process_mats_all.use_selection_only = False
        
        dimmable_row1 = tool_section.row(align=True)
        dimmable_row1.enabled = context.scene.enable_adding_custom_shaders
        dimmable_row1.operator("zgswtor.add_custom_external_swtor_shaders", text="Just Add Shaders To Project")
        dimmable_row2 = tool_section.row(align=True)
        dimmable_row2.enabled = context.scene.enable_linking_custom_shaders
        dimmable_row2.prop(context.scene, "use_linking_bool", text="Link instead of Append")
        tool_section.prop(context.scene, "preserve_atroxa_bool", text="Preserve Original Shaders")
        
        tool_section.label(text="")


        # set_custom_shaders_values UI
        # (belongs to the same Custom Shaders toolset)
        tool_section.label(text="Apply to Custom Shaders")
        split=tool_section.split(factor=0.7)
        split.scale_x = 0.5
        split.scale_y = 0.7
        
        col = split.column(align=True)
        col.prop(context.scene, "scsv_specular_checkbox", text="Specular Str.")
        col.prop(context.scene, "scsv_roughness_checkbox", text="Roughness Fac.")
        col.prop(context.scene, "scsv_emission_checkbox", text="Emission Str.")
        col.prop(context.scene, "scsv_saturation_checkbox", text="Emiss. Saturation")
        col.prop(context.scene, "scsv_normal_checkbox", text="Normal Str.")


        col = split.column(align=True)
        col.prop(context.scene, "scsv_specular", text="")
        col.prop(context.scene, "scsv_roughness", text="")
        col.prop(context.scene, "scsv_emission", text="")
        col.prop(context.scene, "scsv_saturation", text="")
        col.prop(context.scene, "scsv_normal", text="")


        split = tool_section.split(factor= 0.60, align=True)
        col_left, col_right = split.column(align=True), split.column(align=True)

        scsv_to_selection = col_left.operator("zgswtor.set_custom_shaders_values", text="Selected Objects")
        col_left.enabled = len(bpy.context.selected_objects) != 0
        scsv_to_selection.use_selection_only = True

        scsv_to_all = col_right.operator("zgswtor.set_custom_shaders_values", text="All Objects")
        col_right.enabled = len(bpy.data.objects) != 0
        scsv_to_all.use_selection_only = False

        tool_section.label(text="")


        # skinsettings_ng_in_3d_viewer UI
        # (belongs to the same Custom Shaders toolset)
        tool_section.operator("zgswtor.skinsettings_ng_in_3d_viewer", text="Create Skin Settings Group")
        row = tool_section.row()
        in_row = row.row(align=True)  # for setting a non-50% contiguous row region
        in_row.scale_x = 0.95  # Percentage of a full half row
        in_row.label(text="PC-NPC name")
        row.prop(context.scene, "apply_skinsettings_name", text="")
        tool_section.prop(context.scene, "apply_skinsettings_twilek", text="Override Twi'lek Gloss")
        

        # set_backface_culling UI
        tool_section = layout.box()
        row = tool_section.row(align=True)
        row.operator("zgswtor.set_backface_culling", text="Set Backface Culling On").action="BACKFACE_CULLING_ON"
        
        in_row = row.row()  # for setting a non-50% contiguous row region
        in_row.scale_x = 0.35
        in_row.operator("zgswtor.set_backface_culling", text="Off").action="BACKFACE_CULLING_OFF"


        # deduplicate_nodegroups and deduplicate_materials UIs
        tool_section = layout.box().column(align=True)
        tool_section.operator("zgswtor.deduplicate_materials", text="Deduplicate All Materials")
        tool_section.operator("zgswtor.deduplicate_nodegroups", text="Deduplicate All Nodegroups")
        # Already existing Purge operator
        tool_section.operator("outliner.orphans_purge", text="Purge All Orphan Data").do_recursive=True



        # set_dds UIs
        tool_section = layout.box()
        col=tool_section.column(align=False)
        col.operator("zgswtor.set_dds", text="Set all .dds to Non-Color")










# Objects Tools sub-panel
class ZGSWTOR_PT_objects_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Objects Tools"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        

        layout = self.layout
        layout.scale_y = Y_SCALING_GRAL


        # quickscale UI
        tool_section = layout.box().column(align=True)
        row = tool_section.row(align=True).label(text="Scale Selected Objects")
        row = tool_section.row(align=True)
        row.operator("zgswtor.quickscale", text="Down").action = "DOWNSCALE"
        in_row = row.row()
        in_row.scale_x = 0.9  # for a non-50% contiguous row region
        in_row.prop(context.scene, "zgswtor_quickscale_factor", text="",)
        row.operator("zgswtor.quickscale", text="Up").action = "UPSCALE"
        # ---- spacer
        tool_section_spacer = tool_section.column(align=True)
        tool_section_spacer.scale_y = Y_SCALING_SPACER
        tool_section_spacer.label(text="")
        # -----------
        # Apply Transforms
        row = tool_section.row(align=True)
        # Passing multiple properties to an operator.
        # See: https://b3d.interplanety.org/en/executing-operators-with-parameters/

        row.label(text="Apply")

        applPosButton = row.operator("object.transform_apply", text="ALL")
        applPosButton.location = True
        applPosButton.rotation = True
        applPosButton.scale = True
        applPosButton.properties = False

        # row.label(text="")

        applPosButton = row.operator("object.transform_apply", text="Loc.")
        applPosButton.location = True
        applPosButton.rotation = False
        applPosButton.scale = False
        applPosButton.properties = False

        applRotButton = row.operator("object.transform_apply", text="Rot.",)
        applRotButton.location = False
        applRotButton.rotation = True
        applRotButton.scale = False
        applRotButton.properties = False

        applSclButton = row.operator("object.transform_apply", text="Scale")
        applSclButton.location = False
        applSclButton.rotation = False
        applSclButton.scale = True
        applSclButton.properties = False


        # remove_doubles UI
        tool_section = layout.box()
        col=tool_section.column(align=True)
        col.operator("zgswtor.remove_doubles", text="Merge Double Vertices")
        # remove_doubles_edit_mode UI
        col.operator("zgswtor.remove_doubles_edit_mode", text="Merge Selected Double Vertices")


        # set_modifiers UI
        tool_section = layout.box()
        tool_section.label(text="Add Modifier To Selection")
        grid = tool_section.grid_flow(row_major=True, columns=2, align=True)
        grid.operator("zgswtor.set_modifiers", text="SubD").action = "add_subd"
        grid.operator("zgswtor.set_modifiers", text="Multires").action = "add_multires"
        grid.operator("zgswtor.set_modifiers", text="Displace").action = "add_displace"
        grid.operator("zgswtor.set_modifiers", text="Solidify").action = "add_solidify"
        grid.operator("zgswtor.set_modifiers", text="Smooth Corrective").action = "add_smooth_corrective"
        shbutton=grid.row(align=True)
        shbutton.active = (bpy.context.scene.ZGshrinkwrap_target != None)
        shbutton.operator("zgswtor.set_modifiers", text="Shrinkwrap").action = "add_shrinkwrap"
        row = tool_section.row(align=True)
        split = row.split(factor=0.55, align=True)
        col_left, col_right = split.column(align=True), split.column(align=True)
        col_left.label(text="Shrinkw. Target")
        col_right.prop(context.scene, "ZGshrinkwrap_target", text="")





        row = tool_section.row()
        row.operator("zgswtor.set_modifiers", text="Remove These Modifiers").action = "remove_them"

        row = tool_section.row()
        row.label(text="Set Armature as")
        in_row = row.row(align=True)  # for setting a non-50% contiguous row region
        in_row.scale_x = 0.55
        in_row.operator("zgswtor.set_modifiers", text="First").action = "armature_first"
        in_row.operator("zgswtor.set_modifiers", text="Last").action = "armature_last"

        row = tool_section.row()
        row.label(text="Preserve Volume")
        in_row = row.row(align=True)  # for setting a non-50% contiguous row region
        in_row.scale_x = 0.55  # Percentage of a full half row
        in_row.operator("zgswtor.set_modifiers", text="On").action = "preserve_volume_on"
        in_row.operator("zgswtor.set_modifiers", text="Off").action = "preserve_volume_off"




# Pose/Sculpt Tools sub-panel
class ZGSWTOR_PT_pose_sculpt_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Pose & Sculpt Tools"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout
        layout.scale_y = Y_SCALING_GRAL

        # Pose Position / Reset Position UI
        tool_section = layout.box().column(align=True)
        tool_section.label(text="Armatures In Scene:")
        if context.scene.objects:
            armature_col = tool_section.column(align=True)
            for obj in context.scene.objects:
                if obj.type == "ARMATURE":
                    # ---- spacer
                    tool_section_spacer = tool_section.column(align=True)
                    tool_section_spacer.scale_y = Y_SCALING_SPACER
                    tool_section_spacer.label(text="")
                    # -----------
                    armature_col = tool_section.column(align=True)
                    armature_col.label(text=obj.name)
                    armature_buttons = armature_col.row(align=True)
                    armature_buttons.prop(obj.data, "pose_position", expand=True)

                    
        # selected_vertices_to_sculpt_mask UI
        tool_section = layout.box()
        tool_section.operator("zgswtor.selected_vertices_to_sculpt_mask", text="Mask Selected Verts from Sculpting")





# Baking Tools sub-panel
class ZGSWTOR_PT_misc_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Baking Tools"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        Y_SCALING_GRAL = 0.9
        Y_SCALING_INFO = 0.75
        Y_SCALING_SPACER = 0.3

        layout = self.layout
        layout.scale_y = Y_SCALING_GRAL

        # CONVERT TO LEGACY MATERIALS UI
        tool_section = layout.box().column(align=True)

        tool_section.label(text="Convert To Legacy Materials")
                
        split = tool_section.split(factor= 0.60, align=True)
        col_left, col_right = split.column(align=True), split.column(align=True)

        process_mats_sel = col_left.operator("zgswtor.convert_to_legacy_materials", text="Selected Objects")
        col_left.enabled = len(bpy.context.selected_objects) != 0
        process_mats_sel.clm_use_selection_only = True

        process_mats_all = col_right.operator("zgswtor.convert_to_legacy_materials", text="All Objects")
        col_right.enabled = len(bpy.data.objects) != 0
        process_mats_all.clm_use_selection_only = False

        tool_section.prop(context.scene, "zg_add_baking_targets_bool", text="Add Baking Target Nodes")




# Misc. Tools sub-panel
# class ZGSWTOR_PT_misc_tools(bpy.types.Panel):
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"
#     bl_category = "ZG SWTOR"
#     bl_label = "SWTOR Misc. Tools"
#     bl_options = {'DEFAULT_CLOSED'}

#     def draw(self, context):

#         Y_SCALING_GRAL = 0.9
#         Y_SCALING_INFO = 0.75
#         Y_SCALING_SPACER = 0.3

#         layout = self.layout
#         layout.scale_y = Y_SCALING_GRAL


#         #### Block of simple custom operators:

#         # row = tool_section.row(align=True)
#         # row.operator("zgswtor.turn_animation_180", text="Turn Animation 180°")

#         tool_section = layout.box()
#         col=tool_section.column(align=False)
#         col.operator("zgswtor.prefixer", text="Prefix Selected Items' Names")
#         col.prop(context.scene, "zg_prefix", text = "Prefix")
#         col.prop(context.scene, "zg_prefix_mats_skeletons_bool", text="Prefix their Materials / Skeletons")









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
        tool_section = layout.box().column(align=False)
        
        checks = requirements_checks()

        # skinsettings_ng_in_shader_editor UI
        
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
    ZGSWTOR_PT_area_tools,
    ZGSWTOR_PT_character_tools,
    # ZGSWTOR_PT_collections_tools,
    ZGSWTOR_PT_materials_tools,
    ZGSWTOR_PT_objects_tools,
    ZGSWTOR_PT_pose_sculpt_tools,
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