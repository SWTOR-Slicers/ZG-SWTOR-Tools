import bpy

class ZGSWTOR_OT_set_custom_shaders_values(bpy.types.Operator):

    bl_label = "ZG Set Custom Shaders' Values"
    bl_idname = "zgswtor.set_custom_shaders_values"
    bl_description = "Changes the values of some Custom SWTOR Shaders' settings\nin a selection or in all objects in the Scene that use them.\n\n• Only acts on Materials that use Custom SWTOR Shaders.\n• The checkboxes determine which settings will be affected"
    bl_options = {'REGISTER', 'UNDO'}

    # @classmethod
    # def poll(cls,context):
    #     if context.selectable_objects:
    #         return True
    #     else:
    #         return False


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



    def execute(self, context):
        
        context.window.cursor_set("WAIT")  # Show wait cursor icon

        if self.use_selection_only:
            selected_objs = context.selected_objects
        else:
            selected_objs = bpy.data.objects

        # Properties
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


        for obj in selected_objs:
            if obj.type == "MESH":
                print("--------------")
                print("Object: " + obj.name)
                if obj.material_slots:
                    for mat_slot in obj.material_slots:
                        mat = mat_slot.material
                        node_tree = mat.node_tree
                        for node in node_tree.nodes:
                            # if node.name.startswith("SWTOR - "):
                            if node.type == "GROUP":
                                print("    Material: " + mat.name)
                                for input in node.inputs:
                                    if self.specular_checkbox and "Specular Strength" in input.name:
                                        input.default_value = self.specular
                                    if self.roughness_checkbox and "Roughness Factor" in input.name:
                                        input.default_value = self.roughness
                                    if self.emission_checkbox and "Emission Strength" in input.name:
                                        input.default_value = self.emission
                                    if self.saturation_checkbox and "Emission Saturation Factor" in input.name:
                                        input.default_value = self.saturation
                                    if self.normal_checkbox and "Normal Strength" in input.name:
                                        input.default_value = self.normal
                                        
                                        
        bpy.context.window.cursor_set("DEFAULT")  # Show normal cursor icon
                                    
        return {"FINISHED"}


# UI is set in ui.py



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

if __name__ == "__main__":
    register()