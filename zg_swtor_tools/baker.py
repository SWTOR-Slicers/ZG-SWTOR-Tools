import bpy
import os
from pathlib import Path


# -------------------------------------------------------------
class ZGSWTOR_OT_convert_to_legacy_materials(bpy.types.Operator):
    bl_idname = "zgswtor.convert_to_legacy_materials"
    bl_label = "ZG Convert Materials to Legacy Shaders"
    bl_description = "Converts all SWTOR materials in the Blender project to Legacy Shaders-based ones.\nThose shaders work better with Blender's PBR-oriented baking functionality.\n\n• Requires the presence of Materials produced by the current .gr2 Importer Addon.\n\n(The Legacy Shaders used by this Addon are contained in a Blender project stored\nin the Addon's folder, which can be freely modified as long as no Materials, Shaders,\nor Shaders' Inputs and Outputs are renamed, as that would break this tool's workings)"
    bl_options = {'REGISTER', 'UNDO'}


    add_baking_targets_bool: bpy.props.BoolProperty(
        name="Add Baking Target Nodes",
        description='Adds an Active Texturemap Node as a baking target to every\nSWTOR material converted to a Legacy Shader-based one',
        default = True,
        options={'HIDDEN'}
        )



    def execute(self, context):


        # Append the Legacy materials from the auxiliary .blend file inside the Addon 
        
        legacy_materials_blend_filepath = os.path.join(os.path.dirname(__file__), "Legacy SWTOR Shaders and Materials.blend")

        if Path(legacy_materials_blend_filepath).exists() == False:
            self.report({"WARNING"}, "Unable to find the custom SWTOR shaders .blend file inside this Addon's directory.")
            return {"CANCELLED"}

        legacy_materials_path = bpy.path.native_pathsep(legacy_materials_blend_filepath + "/Material")

        legacy_materials_names = {
            "CREATURE" : "SWLEGACY Template: Creature Shader",
            "EYE"      : "SWLEGACY Template: Eye Shader",
            "GARMENT"  : "SWLEGACY Template: Garment Shader",
            "HAIRC"    : "SWLEGACY Template: HairC Shader",
            "SKINB"    : "SWLEGACY Template: SkinB Shader",
            "UBER"     : "SWLEGACY Template: Uber Shader",
        }
        
        legacy_shaders_names = {
            "Creature Shader",
            "Eye Shader",
            "Garment Shader",
            "HairC Shader",
            "SkinB Shader",
            "Uber Shader",
        }
        
        # As there are some inconsistencies in the modern shaders'
        # camelcase names, I'll lowercase their names as dict keys
        # and do the same when looking them up.
        modern_texturemap_nodes_names_to_legacy = {
            "_d"            : "_d DiffuseMap",
            "_h"            : "_h PaletteMap",
            "_m"            : "_m PaletteMaskMap",
            "_n"            : "_n RotationMap",
            "_s"            : "_s GlossMap",
            "complexionmap" : "ComplexionMap",
            "agemap"        : "AgeMap",
            "facepaintmap"  : "FacepaintMap",
            "directionmap"  : "DirectionMap",
        }
        
        # As the legacy shaders don't have methods to set their properties
        # I'll match modern shader props to input fields names.
        # Flush Tone will need a conditional because its data will go
        # from a color to three separate float fields.
        modern_shader_prop_names_to_legacy_fields = {
            "palette1_hue"                 : "Palette1.X",
            "palette1_saturation"          : "Palette1.Y",
            "palette1_brightness"          : "Palette1.Z",
            "palette1_contrast"            : "Palette1.W",
            "palette1_specular"            : "Palette1 Specular",
            "palette1_metallic_specular"   : "Palette1 Metallic Specular",
            "palette2_hue"                 : "Palette2.X",
            "palette2_saturation"          : "Palette2.Y",
            "palette2_brightness"          : "Palette2.Z",
            "palette2_contrast"            : "Palette2.W",
            "palette2_specular"            : "Palette2 Specular",
            "palette2_metallic_specular"   : "Palette2 Metallic Specular",
            "flesh_brightness"             : "FleshBrightness",
            "flush_tone"                   : "FlushTone",  # there will be a conditional for this one
        }
        
        
        material_settings_properties = {
            "use_backface_culling",
            "blend_method",
            "shadow_method",
            "alpha_threshold",
            "use_screen_refraction",
            "refraction_depth",
            "use_sss_translucency",
            "pass_index",
        }
        
        
        
        
        for legacy_material_name in legacy_materials_names.values():
            if legacy_material_name not in bpy.data.materials:
                try:
                    bpy.ops.wm.append(
                    filename=legacy_material_name,
                    directory=legacy_materials_path,
                    do_reuse_local_id=True,  # This seems to be failing, hence the checking
                    set_fake=True,
                    link=False,
                    )
                except:
                    self.report({"WARNING"}, "Unable to find the " + legacy_material_name + " in the .blend file holding the Legacy SWTOR Materials in this Addon's directory.")
                    return {"CANCELLED"}
            
        
        # Convert existing Modern SWTOR Shaders-based materials to use the Legacy templates.
        
        converted_materials_counter = 0
        
        if bpy.data.materials == None:
            self.report({"WARNING"}, "No objects present in this Blender Scene.")
            return {"CANCELLED"}


        materials_converted_counter = 0
        
        for obj in bpy.data.objects:
            if hasattr(obj, 'material_slots') is False:
                continue
            else:
                for material_slot in obj.material_slots:
                    is_swtor_material = False
                    modern_shader_nodegroup = None
                    
                    # Check that the material has any modern SWTOR shader
                    for node in material_slot.material.node_tree.nodes:
                        if hasattr(node, 'derived'):
                            is_swtor_material = True
                            modern_shader_nodegroup = node
                            break
                    
                    # if it has, process the material
                    if is_swtor_material:
                        # Put a copy of the appropriate legacy material template
                        # in the material slot. Keep the modern material around
                        # for copying its data to the legacy one.
                        modern_mat = material_slot.material
                        material_slot.material = bpy.data.materials[ legacy_materials_names[node.derived] ].copy()
                        material_slot.material.name = modern_mat.name + " - LGC"
                        legacy_mat = material_slot.material
                        
                        converted_materials_counter += 1
                        
                        # Copy material's settings.
                        for mat_prop in material_settings_properties:
                            if hasattr(modern_mat, mat_prop):
                                setattr( legacy_mat, mat_prop, getattr(modern_mat, mat_prop) )

                        # Process texturemap nodes.
                        for node in modern_shader_nodegroup.node_tree.nodes:
                            if node.type == "TEX_IMAGE":
                                legacy_node_name = modern_texturemap_nodes_names_to_legacy[node.name.lower()]
                                if legacy_node_name in legacy_mat.node_tree.nodes:
                                    equiv_legacy_node = legacy_mat.node_tree.nodes[legacy_node_name]
                                    
                                    equiv_legacy_node.image = node.image
                                    equiv_legacy_node.interpolation = node.interpolation
                                    # Colorspace_settings, alpha_mode and others are
                                    # image properties, not node's ones. We assume
                                    # them correctly set by the modern .gr2 importer .

                        # Copy SWTOR shaders' parameters settings
                        if modern_shader_nodegroup:
                            # determine legacy SWTOR nodegroup
                            for node in legacy_mat.node_tree.nodes:
                                if node.name in legacy_shaders_names:
                                    legacy_shader_nodegroup = node
                                    break

                            # Frustratingly, I can use input names as keys to a node's inputs,
                            # but I can't do an "if input name in inputs", seemingly. That's
                            # why this dict of input names to input positions.
                            legacy_inputs_names = {}
                            for n, input in enumerate(legacy_shader_nodegroup.inputs):
                                legacy_inputs_names[input.name] = n
                                print(input.name, n)
                                

                            for prop in modern_shader_prop_names_to_legacy_fields:
                                if hasattr(modern_shader_nodegroup, prop):
                                    
                                    if prop == "flush_tone" and "FlushTone.X" in legacy_shader_nodegroup.inputs:
                                        flush_tone_color = modern_shader_nodegroup.flush_tone
                                        legacy_shader_nodegroup.inputs["FlushTone.X"].default_value = flush_tone_color[0]
                                        legacy_shader_nodegroup.inputs["FlushTone.Y"].default_value = flush_tone_color[1]
                                        legacy_shader_nodegroup.inputs["FlushTone.Z"].default_value = flush_tone_color[2]
                                    else:
                                        legacy_inputs = legacy_shader_nodegroup.inputs
                                        if modern_shader_prop_names_to_legacy_fields[prop] in legacy_inputs_names:
                                            input_position = legacy_inputs_names[ modern_shader_prop_names_to_legacy_fields[prop] ]
                                            legacy_inputs[input_position].default_value = getattr(modern_shader_nodegroup, prop)
                                        
                                    
                                    
                        
                                
                   
        if converted_materials_counter == 0:
            self.report({"WARNING"}, "No modern SWTOR shaders used in this Blender Scene's materials.")
            return {"CANCELLED"}
        else:
            # Deduplicate nodegroups and materials
            bpy.ops.zgswtor.deduplicate_nodegroups()
            bpy.ops.zgswtor.deduplicate_materials()
            
            # Add baking targets
            if context.scene.add_baking_targets_bool == True:
                for legacy_mat in [mat for mat in bpy.data.materials if " - LGC" in mat.name]:
                    legacy_mat_nodes = legacy_mat.node_tree.nodes
                    
                    # I use the existence of a "_d DiffuseMap" as a way to get
                    # the max texture map size SWTOR uses for this particular material. 
                    if "_d DiffuseMap" in legacy_mat_nodes:
                        size_ref = legacy_mat_nodes["_d DiffuseMap"].image.size[0]
                    else:
                        size_ref = 1024
                        
                    bake_target_image = bpy.data.images.new(
                        name="baked-" + legacy_mat.name.replace(" - LGC", ""),
                        width=size_ref,
                        height=size_ref,
                        alpha=True,
                    )
                    bake_target_image.alpha_mode = "CHANNEL_PACKED"
                    bake_target_image.colorspace_settings.name = "Raw"
            
                    bake_target_node = legacy_mat_nodes.new("ShaderNodeTexImage")
                    bake_target_node.location = [-140, 600]
                    bake_target_node.width = 300
                    bake_target_node.use_custom_color = True
                    bake_target_node.color = (0.0, 0.0, 0.0)
                    bake_target_node.image = bake_target_image
                    
                    legacy_mat_nodes.active = bake_target_node
                
                
            
            
            self.report({'INFO'}, "Conversion finished")
            return {"FINISHED"}
                   
                   

# -------------------------------------------------------------
# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_convert_to_legacy_materials)
    bpy.types.Scene.add_baking_targets_bool = bpy.props.BoolProperty(
        name="Add Baking Target Nodes",
        description='Adds an Active Texturemap Node as a baking target to every\nSWTOR material converted to a Legacy Shader-based one',
        default = True,
    )



def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_convert_to_legacy_materials)
    del bpy.types.Scene.add_baking_targets_bool

if __name__ == "__main__":
    register()
