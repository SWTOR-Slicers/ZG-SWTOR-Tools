import bpy

class ZGSWTOR_OT_set_custom_shaders_values(bpy.types.Operator):

    bl_label = "ZG Set Custom Shaders' Values"
    bl_idname = "zgswtor.set_custom_shaders_values"
    bl_description = "Changes chosen values and settings in a selection of objects or all objects' materials.\n\n• The checkboxes determine which settings will be collectively affected.\n• The Nodegroup inputs-level changes only act on Nodegroups with matching input names\n   (that excludes the .gr2 Add-on's default SWTOR shaders)\n• Check the Material-Level Settings' Show Backface's tooltips"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls,context):
        if bpy.data.materials:
            return True
        else:
            return False


    # Properties

    use_selection_only: bpy.props.BoolProperty(
        name="Selection-only",
        description='Applies the value changes to the current selection of objects only',
        default = False,
        options={'HIDDEN'}
    )





    specular: bpy.props.FloatProperty(
        name="Specular Strength",
        description="Custom SWTOR Shaders' Specular Strength",
        default = 1.0,
        min=0,
        max=20,
        options={'HIDDEN'},
    )
    specular_checkbox: bpy.props.BoolProperty(
        name="Specular Strength Checkbox",
        description="Allow Specular Strength to be altered",
        default = False,
        options={'HIDDEN'},
    )
    
    
    roughness: bpy.props.FloatProperty(
        name="Roughness Factor",
        description="Custom SWTOR Shaders' Roughness Factor",
        default = 1.0,
        min=0,
        max=1,
        options={'HIDDEN'},
    )
    roughness_checkbox: bpy.props.BoolProperty(
        name="Roughness Factor Checkbox",
        description="Allow Roughness Factor to be altered",
        default = False,
        options={'HIDDEN'},
    )
    
    
    emission: bpy.props.FloatProperty(
        name="Emission Strength",
        description="Custom SWTOR Shaders' Emission Strength",
        default = 1.0,
        min=1,
        max=50,
        options={'HIDDEN'},
    )
    emission_checkbox: bpy.props.BoolProperty(
        name="Emission Strength Checkbox",
        description="Allow Emission Strength to be altered",
        default = False,
        options={'HIDDEN'},
    )


    saturation: bpy.props.FloatProperty(
        name="Emissiveness Saturation",
        description="Custom SWTOR Shaders' Emissiveness Saturation",
        default = 1.0,
        min=1,
        max=20,
        options={'HIDDEN'},
    )
    saturation_checkbox: bpy.props.BoolProperty(
        name="Emissiveness Saturation Checkbox",
        description="Allow Emissiveness Saturation to be altered",
        default = False,
        options={'HIDDEN'},
    )


    normal: bpy.props.FloatProperty(
        name="Normals' Strength",
        description="Custom SWTOR Shaders' Normal Strength",
        default = 1.0,
        min=1,
        max=20,
        options={'HIDDEN'},
    )
    normal_checkbox: bpy.props.BoolProperty(
        name="Normal Strength Checkbox",
        description="Allow Normal Strength to be altered",
        default = False,
        options={'HIDDEN'},
    )


    blend_mode: bpy.props.EnumProperty(
        name="Blend Mode",
        description="Material's Blend Mode",
        items=[
            ("OPAQUE", "Opaque", "Set Materials' Blend mode to Opaque\nand Shadow Mode to Opaque."),
            ("CLIP", "Clip", "Set Materials' Blend mode to Alpha Clip\nand Shadow Mode to Alpha Clip."),
            ("HASHED", "Hashed", "Set Materials' Blend mode to Alpha Hashed\nand Shadow Mode to Alpha Hashed."),
            ("BLEND", "Blend", "Set Materials' Blend mode to Alpha Blend,\nShadow Mode to Alpha Hashed,\nand disable Show Backface."),
            ],
        default = "BLEND",
        options={'HIDDEN'},
    )
    blend_mode_checkbox: bpy.props.BoolProperty(
        name="Blend Mode Checkbox",
        description="Allow Blend Mode to be altered",
        default = False,
        options={'HIDDEN'},
    )


    show_backface: bpy.props.EnumProperty(
        name="Show Backface",
        description="Materials' Show Backface property",
        items=[
            ("YES", "Yes", "Set Materials' Show Backface property to True\n(renders multiple transparent layers).\n\nThis setting's effect is only visible in materials\nwith Blend Mode set to Alpha Blend, and on EEVEE."),
            ("NO", "No", "Set Materials' Show Backface property to False.\n\nThis setting's effect is only visible in materials\nwith Blend Mode set to Alpha Blend, and on EEVEE."),
            ],
        default = "NO",
        options={'HIDDEN'},
    )
    show_backface_checkbox: bpy.props.BoolProperty(
        name="Show Backface Checkbox",
        description="Allow Show Backface setting to be altered",
        default = False,
        options={'HIDDEN'},
    )



    def execute(self, context):
        
        context.window.cursor_set("WAIT")  # Show wait cursor icon

        # Nodegroup-level Properties
        self.specular = context.scene.scsv_specular
        self.specular_checkbox = context.scene.scsv_specular_checkbox
        self.roughness = context.scene.scsv_roughness
        self.roughness_checkbox = context.scene.scsv_roughness_checkbox
        self.emission = context.scene.scsv_emission
        self.emission_checkbox = context.scene.scsv_emission_checkbox
        self.saturation = context.scene.scsv_saturation_checkbox
        self.saturation_checkbox = context.scene.scsv_saturation_checkbox
        self.normal = context.scene.scsv_normal
        self.normal_checkbox = context.scene.scsv_normal_checkbox

        there_are_nodegroup_level_changes = (
            self.specular_checkbox or
            self.roughness_checkbox or
            self.emission_checkbox or
            self.saturation_checkbox or
            self.normal_checkbox
            )
                            

        # Material-level Properties
        self.blend_mode = context.scene.scsv_blend_mode
        self.blend_mode_checkbox = context.scene.scsv_blend_mode_checkbox
        self.show_backface = context.scene.scsv_show_backface
        self.show_backface_checkbox = context.scene.scsv_show_backface_checkbox
        
        there_are_material_level_changes = (
            self.blend_mode_checkbox or
            self.show_backface_checkbox
        )


        if not (there_are_nodegroup_level_changes or there_are_material_level_changes):
            context.window.cursor_set("DEFAULT")  # Show normal cursor icon
            return {"CANCELLED"}


        if self.use_selection_only:
            selected_objs = context.selected_objects
        else:
            selected_objs = bpy.data.objects


        materials_changes_report = 0

        for obj in selected_objs:
            if obj.type == "MESH":
                print("--------------")
                print("Object: " + obj.name)
                if obj.material_slots:
                    for mat_slot in obj.material_slots:
                        mat = mat_slot.material
                        
                        material_was_changed = False
                        
                        # Material-level settings changes
                        if there_are_material_level_changes:
                            material_was_changed = True  # They are guaranteed at the material level

                            if self.blend_mode_checkbox:
                                material_was_changed = True
                                mat.blend_method = self.blend_mode
                                                                
                                if mat.blend_method == "OPAQUE":
                                    mat.shadow_method = "OPAQUE"
                                
                                if mat.blend_method == "CLIP":
                                    mat.shadow_method = "CLIP"
                                    
                                if mat.blend_method == "HASHED":
                                    mat.shadow_method = "HASHED"
                                
                                if mat.blend_method == "BLEND":
                                    mat.shadow_method = "HASHED"
                                    mat.show_transparent_back = False
                                
                            if self.show_backface_checkbox:
                                mat.show_transparent_back = (self.show_backface == "YES")
                                

                        # Nodegroup-level settings changes
                        if there_are_nodegroup_level_changes:
                        
                            node_tree = mat.node_tree
                            for node in node_tree.nodes:
                                if "swtor" in node.name.lower() or "koda" in node.name.lower():
                                    print("    Material: " + mat.name)
                                    for input in node.inputs:
                                        
                                        input_name = input.name.lower()
                                        
                                        if self.specular_checkbox and ("specular" in input_name and not "palette" in input_name ):
                                            input.default_value = self.specular
                                            material_was_changed = True
                                            
                                        if self.roughness_checkbox and "roughness" in input_name:
                                            input.default_value = self.roughness
                                            material_was_changed = True
                                            
                                        if self.emission_checkbox and ("emission strength" in input_name or "emissive strength" in input_name ):
                                            input.default_value = self.emission
                                            material_was_changed = True
                                            
                                        if self.saturation_checkbox and ("emission saturation" in input_name or "emissive saturation" in input_name ):
                                            input.default_value = self.saturation
                                            material_was_changed = True
                                            
                                        if self.normal_checkbox and "normal strength" in input_name:
                                            input.default_value = self.normal
                                            material_was_changed = True
                                        
                                        
                        # Counter for final report
                        if material_was_changed:
                            materials_changes_report += 1


        context.window.cursor_set("DEFAULT")  # Show normal cursor icon
        if materials_changes_report == 1:
            self.report({'INFO'}, str(materials_changes_report) + " applicable Material processed" )
        else:
            self.report({'INFO'}, str(materials_changes_report) + " applicable Materials processed" )
        return {"FINISHED"}


# UI is set in addon_ui.py



# ------------------------------------------------------------------
# Registrations

def register():
    
    bpy.utils.register_class(ZGSWTOR_OT_set_custom_shaders_values)

    bpy.types.Scene.scsv_specular= bpy.props.FloatProperty(
        name="Specular Strength",
        description="Custom SWTOR Shaders' Specular Strength",
        default = 1.0,
        min=0,
        max=20,
        options={'HIDDEN'},
    )
    bpy.types.Scene.scsv_specular_checkbox= bpy.props.BoolProperty(
        name="Specular Strength Checkbox",
        description="Allow Specular Strength to be altered",
        default = False,
        options={'HIDDEN'},
    )
    
    
    bpy.types.Scene.scsv_roughness= bpy.props.FloatProperty(
        name="Roughness Factor",
        description="Custom SWTOR Shaders' Roughness Factor",
        default = 1.0,
        min=0,
        max=1,
        options={'HIDDEN'},
    )
    bpy.types.Scene.scsv_roughness_checkbox= bpy.props.BoolProperty(
        name="Roughness Factor Checkbox",
        description="Allow Roughness Factor to be altered",
        default = False,
        options={'HIDDEN'},
    )
    
    
    bpy.types.Scene.scsv_emission= bpy.props.FloatProperty(
        name="Emission Strength",
        description="Custom SWTOR Shaders' Emission Strength",
        default = 1.0,
        min=1,
        max=50,
        options={'HIDDEN'},
    )
    bpy.types.Scene.scsv_emission_checkbox= bpy.props.BoolProperty(
        name="Emission Strength Checkbox",
        description="Allow Emission Strength to be altered",
        default = False,
        options={'HIDDEN'},
    )


    bpy.types.Scene.scsv_saturation= bpy.props.FloatProperty(
        name="Emissiveness Saturation",
        description="Custom SWTOR Shaders' Emissiveness Saturation",
        default = 1.0,
        min=1,
        max=20,
        options={'HIDDEN'},
    )
    bpy.types.Scene.scsv_saturation_checkbox= bpy.props.BoolProperty(
        name="Emissiveness Saturation Checkbox",
        description="Allow Emissiveness Saturation to be altered",
        default = False,
        options={'HIDDEN'},
    )


    bpy.types.Scene.scsv_normal= bpy.props.FloatProperty(
        name="Normals' Strength",
        description="Custom SWTOR Shaders' Normal Strength",
        default = 1.0,
        min=1,
        max=20,
        options={'HIDDEN'},
    )
    bpy.types.Scene.scsv_normal_checkbox= bpy.props.BoolProperty(
        name="Normal Strength Checkbox",
        description="Allow Normal Strength to be altered",
        default = False,
        options={'HIDDEN'},
    )


    bpy.types.Scene.scsv_blend_mode= bpy.props.EnumProperty(
        name="Blend Mode",
        description="Materials' Blend Mode",
        items=[
            ("OPAQUE", "Opaque", "Set Materials' Blend mode to Opaque\nand Shadow Mode to Opaque."),
            ("CLIP", "Clip", "Set Materials' Blend mode to Alpha Clip\nand Shadow Mode to Alpha Clip."),
            ("HASHED", "Hashed", "Set Materials' Blend mode to Alpha Hashed\nand Shadow Mode to Alpha Hashed."),
            ("BLEND", "Blend", "Set Materials' Blend mode to Alpha Blend,\nShadow Mode to Alpha Hashed,\nand disable Show Backface."),
            ],
        default = "BLEND",
        options={'HIDDEN'},
    )
    bpy.types.Scene.scsv_blend_mode_checkbox= bpy.props.BoolProperty(
        name="Blend Mode Checkbox",
        description="Allow Blend Mode to be altered",
        default = False,
        options={'HIDDEN'},
    )

    bpy.types.Scene.scsv_show_backface= bpy.props.EnumProperty(
        name="Show Backface",
        description="Materials' Show Backface property",
        items=[
            ("YES", "Yes", "Set Materials' Show Backface property to True\n(renders multiple transparent layers).\n\nThis setting's effect is only visible in materials\nwith Blend Mode set to Alpha Blend, and on EEVEE."),
            ("NO", "No", "Set Materials' Show Backface property to False.\n\nThis setting's effect is only visible in materials\nwith Blend Mode set to Alpha Blend, and on EEVEE."),
            ],
        default = "NO",
        options={'HIDDEN'},
    )
    bpy.types.Scene.scsv_show_backface_checkbox= bpy.props.BoolProperty(
        name="Show Backface Checkbox",
        description="Allow Show Backface setting to be altered",
        default = False,
        options={'HIDDEN'},
    )






def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_set_custom_shaders_values)
    
    del bpy.types.Scene.scsv_specular
    del bpy.types.Scene.scsv_specular_checkbox
    del bpy.types.Scene.scsv_roughness
    del bpy.types.Scene.scsv_roughness_checkbox
    del bpy.types.Scene.scsv_emission
    del bpy.types.Scene.scsv_emission_checkbox
    del bpy.types.Scene.scsv_saturation
    del bpy.types.Scene.scsv_saturation_checkbox
    del bpy.types.Scene.scsv_normal
    del bpy.types.Scene.scsv_normal_checkbox
    del bpy.types.Scene.scsv_blend_mode
    del bpy.types.Scene.scsv_blend_mode_checkbox
    del bpy.types.Scene.scsv_show_backface
    del bpy.types.Scene.scsv_show_backface_checkbox


if __name__ == "__main__":
    register()