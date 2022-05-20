import bpy


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
        tool_section.operator("zgswtor.process_uber_mats", text="Process Uber Materials")
        tool_section.prop(context.scene, "use_overwrite_bool", text="Overwrite Uber Materials")
        tool_section.prop(context.scene, "use_collect_colliders_bool", text="Collect Collider Objects")


        # add_custom_external_swtor_shaders UI
        
        tool_section = layout.box().column(align=True)
        dimmable_row = tool_section.row(align=True)
        dimmable_row.enabled = not context.scene.blendfile_is_template_bool
        dimmable_row.operator("zgswtor.add_custom_external_swtor_shaders", text="Add Custom SWTOR Shaders")
        # customize_swtor_shaders UI
        tool_section.operator("zgswtor.customize_swtor_shaders", text="Convert to Custom SWTOR Shaders")
        print("bpy.types.Scene.blendfile_is_template_bool =",context.scene.blendfile_is_template_bool)
        dimmable_row = tool_section.row(align=True)
        new_shaders_filepath = bpy.context.preferences.addons[__package__].preferences.swtor_custom_shaders_blendfile_path        
        open_blend_file = bpy.data.filepath

        dimmable_row.enabled = not new_shaders_filepath == open_blend_file
        dimmable_row.prop(context.scene, "use_linking_bool", text="Link instead of Append")
        tool_section.prop(context.scene, "preserve_atroxa_bool", text="Preserve Original Shaders")
        


        # deduplicate_nodegroups UI
        tool_section = layout.box()
        tool_section.operator("zgswtor.deduplicate_nodegroups", text="Deduplicate All Nodegroups")


        # set_backface_culling UI
        tool_section = layout.box()
        row = tool_section.row(align=True)
        row.operator("zgswtor.set_backface_culling", text="Set Backface Culling On").action="BACKFACE_CULLING_ON"
        
        in_row = row.row()  # for setting a non-50% contiguous row region
        in_row.scale_x = 0.35
        in_row.operator("zgswtor.set_backface_culling", text="Off").action="BACKFACE_CULLING_OFF"


        # # adjust_normals_emissives UI
        # tool_section = layout.box()
        # split = tool_section.split()
        
        # col = split.column(align=True)
        # col.scale_y = 0.9
        # col.label(text="Shader")
        # col.label(text="Uber")
        # col.label(text="Creature")
        # col.label(text="Garment")
        # col.label(text="SkinB")
        # col.label(text="HairC")
        # col.label(text="Eye")

        # col = split.column(align=True)
        # col.scale_y = 0.9
        # col.label(text="Normals")
        # col.prop(context.scene, "uber_normals_fac", slider=True)
        # col.prop(context.scene, "creature_normals_fac", slider=True)
        # col.prop(context.scene, "garment_normals_fac", slider=True)
        # col.prop(context.scene, "skinb_normals_fac", slider=True)
        # col.prop(context.scene, "hairc_normals_fac", slider=True)
        # col.prop(context.scene, "eye_normals_fac", slider=True)

        # col = split.column(align=True)
        # col.scale_y = 0.9
        # col.label(text="Emission")
        # col.prop(context.scene, "uber_emission_fac", slider=True)
        # col.prop(context.scene, "creature_emission_fac", slider=True)
        # col.prop(context.scene, "garment_emission_fac", slider=True)
        # col.prop(context.scene, "skinb_emission_fac", slider=True)
        # col.prop(context.scene, "hairc_emission_fac", slider=True)
        # col.prop(context.scene, "eye_emission_fac", slider=True)




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
        row.operator("zgswtor.quickscale", text="Upscale").action = "UPSCALE"
        
        in_row = row.row()  # for a non-50% contiguous row region
        in_row.scale_x = 0.9
        in_row.prop(context.scene, "zgswtor_quickscale_factor", text="")
        
        row.operator("zgswtor.quickscale", text="Downscale").action = "DOWNSCALE"


        # remove_doubles UI
        tool_section = layout.box()
        tool_section.operator("zgswtor.remove_doubles", text="Merge Double Vertices")


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




# Scene Tools sub-panel
class ZGSWTOR_PT_scene_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG SWTOR"
    bl_label = "SWTOR Misc. Tools"

    def draw(self, context):
        layout = self.layout
        tool_section = layout.box()

        # Simplify (copy of existing operators)
        row = tool_section.row(align=True)
        row.prop(context.scene.render, "use_simplify", text=" Simplify")
        in_row = row.row()  # for a non-50% contiguous row region
        in_row.scale_x = 1.2
        in_row.prop(context.scene.render, "simplify_subdivision", text="Max SubD")

        # Pose Position / Reset Position (copy of existing operators)
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


        
# Registrations

classes = [
    ZGSWTOR_PT_materials_tools,
    ZGSWTOR_PT_objects_tools,
    ZGSWTOR_PT_scene_tools
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    
if __name__ == "__main__":
    register()