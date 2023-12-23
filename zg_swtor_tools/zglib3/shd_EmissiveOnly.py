import bpy

def create_EmissiveOnly_nodegroup():

    node_tree1 = bpy.data.node_groups.get('EmissiveOnly')
    if not node_tree1:
        node_tree1 = bpy.data.node_groups.new('EmissiveOnly', 'ShaderNodeTree')
        for node in node_tree1.nodes:
            node_tree1.nodes.remove(node)
        # INPUTS
        input = node_tree1.inputs.new('NodeSocketColor', '_d DIffuseColor')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = (1.0, 1.0, 1.0, 1.0)
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'name'):
            input.name = '_d DIffuseColor'
        input = node_tree1.inputs.new('NodeSocketFloat', 'Emissive Strength')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = 4.0
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 1000000.0
        if hasattr(input, 'min_value'):
            input.min_value = 1.0
        if hasattr(input, 'name'):
            input.name = 'Emissive Strength'
        # OUTPUTS
        output = node_tree1.outputs.new('NodeSocketShader', 'Shader')
        if hasattr(output, 'attribute_domain'):
            output.attribute_domain = 'POINT'
        if hasattr(output, 'hide_in_modifier'):
            output.hide_in_modifier = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Shader'
        # NODES
        add_shader_1 = node_tree1.nodes.new('ShaderNodeAddShader')
        if hasattr(add_shader_1, 'color'):
            add_shader_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(add_shader_1, 'hide'):
            add_shader_1.hide = False
        if hasattr(add_shader_1, 'location'):
            add_shader_1.location = (107.830322265625, 8.104637145996094)
        if hasattr(add_shader_1, 'mute'):
            add_shader_1.mute = False
        if hasattr(add_shader_1, 'name'):
            add_shader_1.name = 'Add Shader'
        if hasattr(add_shader_1, 'status'):
            add_shader_1.status = False
        if hasattr(add_shader_1, 'use_custom_color'):
            add_shader_1.use_custom_color = False
        if hasattr(add_shader_1, 'width'):
            add_shader_1.width = 140.0

        group_output_1 = node_tree1.nodes.new('NodeGroupOutput')
        if hasattr(group_output_1, 'color'):
            group_output_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(group_output_1, 'hide'):
            group_output_1.hide = False
        if hasattr(group_output_1, 'is_active_output'):
            group_output_1.is_active_output = True
        if hasattr(group_output_1, 'location'):
            group_output_1.location = (297.830322265625, -0.0)
        if hasattr(group_output_1, 'mute'):
            group_output_1.mute = False
        if hasattr(group_output_1, 'name'):
            group_output_1.name = 'Group Output'
        if hasattr(group_output_1, 'status'):
            group_output_1.status = False
        if hasattr(group_output_1, 'use_custom_color'):
            group_output_1.use_custom_color = False
        if hasattr(group_output_1, 'width'):
            group_output_1.width = 140.0

        gamma_1 = node_tree1.nodes.new('ShaderNodeGamma')
        if hasattr(gamma_1, 'color'):
            gamma_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(gamma_1, 'hide'):
            gamma_1.hide = False
        if hasattr(gamma_1, 'location'):
            gamma_1.location = (-287.8037109375, 89.03213500976562)
        if hasattr(gamma_1, 'mute'):
            gamma_1.mute = False
        if hasattr(gamma_1, 'name'):
            gamma_1.name = 'Gamma'
        if hasattr(gamma_1, 'status'):
            gamma_1.status = False
        if hasattr(gamma_1, 'use_custom_color'):
            gamma_1.use_custom_color = False
        if hasattr(gamma_1, 'width'):
            gamma_1.width = 132.87872314453125
        input_ = next((input_ for input_ in gamma_1.inputs if input_.identifier=='Color'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (1.0, 1.0, 1.0, 1.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Color'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in gamma_1.inputs if input_.identifier=='Gamma'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 2.200000047683716
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Gamma'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        output = next((output for output in gamma_1.outputs if output.identifier=='Color'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0, 0.0)
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Color'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        group_input_1 = node_tree1.nodes.new('NodeGroupInput')
        if hasattr(group_input_1, 'color'):
            group_input_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(group_input_1, 'hide'):
            group_input_1.hide = False
        if hasattr(group_input_1, 'location'):
            group_input_1.location = (-467.38623046875, 16.677505493164062)
        if hasattr(group_input_1, 'mute'):
            group_input_1.mute = False
        if hasattr(group_input_1, 'name'):
            group_input_1.name = 'Group Input'
        if hasattr(group_input_1, 'status'):
            group_input_1.status = False
        if hasattr(group_input_1, 'use_custom_color'):
            group_input_1.use_custom_color = False
        if hasattr(group_input_1, 'width'):
            group_input_1.width = 140.0
        if hasattr(group_input_1.outputs[0], 'default_value'):
            group_input_1.outputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
        if hasattr(group_input_1.outputs[0], 'display_shape'):
            group_input_1.outputs[0].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[0], 'enabled'):
            group_input_1.outputs[0].enabled = True
        if hasattr(group_input_1.outputs[0], 'hide'):
            group_input_1.outputs[0].hide = False
        if hasattr(group_input_1.outputs[0], 'hide_value'):
            group_input_1.outputs[0].hide_value = False
        if hasattr(group_input_1.outputs[0], 'name'):
            group_input_1.outputs[0].name = '_d DIffuseColor'
        if hasattr(group_input_1.outputs[0], 'show_expanded'):
            group_input_1.outputs[0].show_expanded = False
        if hasattr(group_input_1.outputs[1], 'default_value'):
            group_input_1.outputs[1].default_value = 4.0
        if hasattr(group_input_1.outputs[1], 'display_shape'):
            group_input_1.outputs[1].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[1], 'enabled'):
            group_input_1.outputs[1].enabled = True
        if hasattr(group_input_1.outputs[1], 'hide'):
            group_input_1.outputs[1].hide = False
        if hasattr(group_input_1.outputs[1], 'hide_value'):
            group_input_1.outputs[1].hide_value = False
        if hasattr(group_input_1.outputs[1], 'name'):
            group_input_1.outputs[1].name = 'Emissive Strength'
        if hasattr(group_input_1.outputs[1], 'show_expanded'):
            group_input_1.outputs[1].show_expanded = False

        transparent_bsdf_1 = node_tree1.nodes.new('ShaderNodeBsdfTransparent')
        if hasattr(transparent_bsdf_1, 'color'):
            transparent_bsdf_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(transparent_bsdf_1, 'hide'):
            transparent_bsdf_1.hide = False
        if hasattr(transparent_bsdf_1, 'location'):
            transparent_bsdf_1.location = (-87.3004150390625, -66.45764923095703)
        if hasattr(transparent_bsdf_1, 'mute'):
            transparent_bsdf_1.mute = False
        if hasattr(transparent_bsdf_1, 'name'):
            transparent_bsdf_1.name = 'Transparent BSDF'
        if hasattr(transparent_bsdf_1, 'status'):
            transparent_bsdf_1.status = False
        if hasattr(transparent_bsdf_1, 'use_custom_color'):
            transparent_bsdf_1.use_custom_color = False
        if hasattr(transparent_bsdf_1, 'width'):
            transparent_bsdf_1.width = 137.43377685546875
        input_ = next((input_ for input_ in transparent_bsdf_1.inputs if input_.identifier=='Color'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (1.0, 1.0, 1.0, 1.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Color'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in transparent_bsdf_1.inputs if input_.identifier=='Weight'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Weight'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False

        emission_1 = node_tree1.nodes.new('ShaderNodeEmission')
        if hasattr(emission_1, 'color'):
            emission_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(emission_1, 'hide'):
            emission_1.hide = False
        if hasattr(emission_1, 'location'):
            emission_1.location = (-87.30040740966797, 40.799949645996094)
        if hasattr(emission_1, 'mute'):
            emission_1.mute = False
        if hasattr(emission_1, 'name'):
            emission_1.name = 'Emission'
        if hasattr(emission_1, 'status'):
            emission_1.status = False
        if hasattr(emission_1, 'use_custom_color'):
            emission_1.use_custom_color = False
        if hasattr(emission_1, 'width'):
            emission_1.width = 134.86758422851562
        input_ = next((input_ for input_ in emission_1.inputs if input_.identifier=='Color'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (1.0, 1.0, 1.0, 1.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Color'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in emission_1.inputs if input_.identifier=='Strength'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 4.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Strength'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in emission_1.inputs if input_.identifier=='Weight'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Weight'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False

        # LINKS
        node_tree1.links.new(gamma_1.outputs[0], emission_1.inputs[0])
        node_tree1.links.new(add_shader_1.outputs[0], group_output_1.inputs[0])
        node_tree1.links.new(emission_1.outputs[0], add_shader_1.inputs[0])
        node_tree1.links.new(transparent_bsdf_1.outputs[0], add_shader_1.inputs[1])
        node_tree1.links.new(group_input_1.outputs[1], emission_1.inputs[1])
        node_tree1.links.new(group_input_1.outputs[0], gamma_1.inputs[0])

    return