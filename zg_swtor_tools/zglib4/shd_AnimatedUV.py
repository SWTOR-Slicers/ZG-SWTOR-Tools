import bpy

def create_AnimatedUV_nodegroup(material_datablock):
    
    # MATERIAL
    material_datablock.use_nodes = True
    node_tree0 = material_datablock.node_tree

    for node in node_tree0.nodes:
        node_tree0.nodes.remove(node)
    # NODES
    material_output_0 = node_tree0.nodes.new('ShaderNodeOutputMaterial')
    if hasattr(material_output_0, 'color'):
        material_output_0.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(material_output_0, 'hide'):
        material_output_0.hide = False
    if hasattr(material_output_0, 'is_active_output'):
        material_output_0.is_active_output = True
    if hasattr(material_output_0, 'location'):
        material_output_0.location = (640.0, 200.0)
    if hasattr(material_output_0, 'mute'):
        material_output_0.mute = False
    if hasattr(material_output_0, 'name'):
        material_output_0.name = 'Material Output'
    if hasattr(material_output_0, 'status'):
        material_output_0.status = False
    if hasattr(material_output_0, 'target'):
        material_output_0.target = 'ALL'
    if hasattr(material_output_0, 'use_custom_color'):
        material_output_0.use_custom_color = False
    if hasattr(material_output_0, 'width'):
        material_output_0.width = 140.0
    input_ = next((input_ for input_ in material_output_0.inputs if input_.identifier=='Displacement'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.0, 0.0, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'CIRCLE'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = True
        if hasattr(input_, 'name'):
            input_.name = 'Displacement'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in material_output_0.inputs if input_.identifier=='Thickness'), None)
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
            input_.hide_value = True
        if hasattr(input_, 'name'):
            input_.name = 'Thickness'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False

    animatedtexture2_0 = node_tree0.nodes.new('ShaderNodeTexImage')
    if hasattr(animatedtexture2_0, 'color'):
        animatedtexture2_0.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(animatedtexture2_0, 'extension'):
        animatedtexture2_0.extension = 'REPEAT'
    if hasattr(animatedtexture2_0, 'hide'):
        animatedtexture2_0.hide = False
    if hasattr(animatedtexture2_0, 'interpolation'):
        animatedtexture2_0.interpolation = 'Cubic'
    if hasattr(animatedtexture2_0, 'label'):
        animatedtexture2_0.label = 'AnimatedTexture2'
    if hasattr(animatedtexture2_0, 'location'):
        animatedtexture2_0.location = (-260.0, -263.8889465332031)
    if hasattr(animatedtexture2_0, 'mute'):
        animatedtexture2_0.mute = False
    if hasattr(animatedtexture2_0, 'name'):
        animatedtexture2_0.name = 'AnimatedTexture2'
    if hasattr(animatedtexture2_0, 'projection'):
        animatedtexture2_0.projection = 'FLAT'
    if hasattr(animatedtexture2_0, 'projection_blend'):
        animatedtexture2_0.projection_blend = 0.0
    if hasattr(animatedtexture2_0, 'status'):
        animatedtexture2_0.status = False
    if hasattr(animatedtexture2_0, 'use_custom_color'):
        animatedtexture2_0.use_custom_color = False
    if hasattr(animatedtexture2_0, 'width'):
        animatedtexture2_0.width = 319.5576171875
    input_ = next((input_ for input_ in animatedtexture2_0.inputs if input_.identifier=='Vector'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.0, 0.0, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'CIRCLE'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = True
        if hasattr(input_, 'name'):
            input_.name = 'Vector'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in animatedtexture2_0.outputs if output.identifier=='Color'), None)
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
    output = next((output for output in animatedtexture2_0.outputs if output.identifier=='Alpha'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'CIRCLE'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Alpha'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    animatedtexture1_0 = node_tree0.nodes.new('ShaderNodeTexImage')
    if hasattr(animatedtexture1_0, 'color'):
        animatedtexture1_0.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(animatedtexture1_0, 'extension'):
        animatedtexture1_0.extension = 'REPEAT'
    if hasattr(animatedtexture1_0, 'hide'):
        animatedtexture1_0.hide = False
    if hasattr(animatedtexture1_0, 'interpolation'):
        animatedtexture1_0.interpolation = 'Cubic'
    if hasattr(animatedtexture1_0, 'label'):
        animatedtexture1_0.label = 'AnimatedTexture1'
    if hasattr(animatedtexture1_0, 'location'):
        animatedtexture1_0.location = (-260.0, 46.03678894042969)
    if hasattr(animatedtexture1_0, 'mute'):
        animatedtexture1_0.mute = False
    if hasattr(animatedtexture1_0, 'name'):
        animatedtexture1_0.name = 'AnimatedTexture1'
    if hasattr(animatedtexture1_0, 'projection'):
        animatedtexture1_0.projection = 'FLAT'
    if hasattr(animatedtexture1_0, 'projection_blend'):
        animatedtexture1_0.projection_blend = 0.0
    if hasattr(animatedtexture1_0, 'status'):
        animatedtexture1_0.status = False
    if hasattr(animatedtexture1_0, 'use_custom_color'):
        animatedtexture1_0.use_custom_color = False
    if hasattr(animatedtexture1_0, 'width'):
        animatedtexture1_0.width = 319.9089050292969
    input_ = next((input_ for input_ in animatedtexture1_0.inputs if input_.identifier=='Vector'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.0, 0.0, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'CIRCLE'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = True
        if hasattr(input_, 'name'):
            input_.name = 'Vector'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in animatedtexture1_0.outputs if output.identifier=='Color'), None)
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
    output = next((output for output in animatedtexture1_0.outputs if output.identifier=='Alpha'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'CIRCLE'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Alpha'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    _d_diffusemap_0 = node_tree0.nodes.new('ShaderNodeTexImage')
    if hasattr(_d_diffusemap_0, 'color'):
        _d_diffusemap_0.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(_d_diffusemap_0, 'extension'):
        _d_diffusemap_0.extension = 'REPEAT'
    if hasattr(_d_diffusemap_0, 'hide'):
        _d_diffusemap_0.hide = False
    if hasattr(_d_diffusemap_0, 'interpolation'):
        _d_diffusemap_0.interpolation = 'Cubic'
    if hasattr(_d_diffusemap_0, 'label'):
        _d_diffusemap_0.label = '_d DiffuseMap'
    if hasattr(_d_diffusemap_0, 'location'):
        _d_diffusemap_0.location = (-256.3918151855469, 348.74383544921875)
    if hasattr(_d_diffusemap_0, 'mute'):
        _d_diffusemap_0.mute = False
    if hasattr(_d_diffusemap_0, 'name'):
        _d_diffusemap_0.name = '_d DiffuseMap'
    if hasattr(_d_diffusemap_0, 'projection'):
        _d_diffusemap_0.projection = 'FLAT'
    if hasattr(_d_diffusemap_0, 'projection_blend'):
        _d_diffusemap_0.projection_blend = 0.0
    if hasattr(_d_diffusemap_0, 'status'):
        _d_diffusemap_0.status = False
    if hasattr(_d_diffusemap_0, 'use_custom_color'):
        _d_diffusemap_0.use_custom_color = False
    if hasattr(_d_diffusemap_0, 'width'):
        _d_diffusemap_0.width = 321.44732666015625
    input_ = next((input_ for input_ in _d_diffusemap_0.inputs if input_.identifier=='Vector'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.0, 0.0, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'CIRCLE'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = True
        if hasattr(input_, 'name'):
            input_.name = 'Vector'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in _d_diffusemap_0.outputs if output.identifier=='Color'), None)
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
    output = next((output for output in _d_diffusemap_0.outputs if output.identifier=='Alpha'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'CIRCLE'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Alpha'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    node_tree1 = bpy.data.node_groups.get('SW Aux - TransformAllUV')
    if not node_tree1:
        node_tree1 = bpy.data.node_groups.new('SW Aux - TransformAllUV', 'ShaderNodeTree')
        for node in node_tree1.nodes:
            node_tree1.nodes.remove(node)
        # INPUTS
        input = node_tree1.interface.new_socket(name='animTexUVScrollSpeed0', socket_type='NodeSocketVector', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = (0.0, 0.0, 0.0)
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 3.4028234663852886e+38
        if hasattr(input, 'min_value'):
            input.min_value = -3.4028234663852886e+38
        if hasattr(input, 'name'):
            input.name = 'animTexUVScrollSpeed0'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketVector'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='animTexRotationPivot0', socket_type='NodeSocketVector', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = (0.0, 0.0, 0.0)
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 3.4028234663852886e+38
        if hasattr(input, 'min_value'):
            input.min_value = -3.4028234663852886e+38
        if hasattr(input, 'name'):
            input.name = 'animTexRotationPivot0'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketVector'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='animTexRotationSpeed0', socket_type='NodeSocketFloat', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = 0.0
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 3.4028234663852886e+38
        if hasattr(input, 'min_value'):
            input.min_value = -3.4028234663852886e+38
        if hasattr(input, 'name'):
            input.name = 'animTexRotationSpeed0'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketFloat'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='animTexUVScrollSpeed1', socket_type='NodeSocketVector', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = (0.0, 0.0, 0.0)
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 3.4028234663852886e+38
        if hasattr(input, 'min_value'):
            input.min_value = -3.4028234663852886e+38
        if hasattr(input, 'name'):
            input.name = 'animTexUVScrollSpeed1'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketVector'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='animTexRotationPivot1', socket_type='NodeSocketVector', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = (0.0, 0.0, 0.0)
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 3.4028234663852886e+38
        if hasattr(input, 'min_value'):
            input.min_value = -3.4028234663852886e+38
        if hasattr(input, 'name'):
            input.name = 'animTexRotationPivot1'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketVector'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='animTexRotationSpeed1', socket_type='NodeSocketFloat', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = 0.0
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 3.4028234663852886e+38
        if hasattr(input, 'min_value'):
            input.min_value = -3.4028234663852886e+38
        if hasattr(input, 'name'):
            input.name = 'animTexRotationSpeed1'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketFloat'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='animTexUVScrollSpeed2', socket_type='NodeSocketVector', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = (0.0, 0.0, 0.0)
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 3.4028234663852886e+38
        if hasattr(input, 'min_value'):
            input.min_value = -3.4028234663852886e+38
        if hasattr(input, 'name'):
            input.name = 'animTexUVScrollSpeed2'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketVector'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='animTexRotationPivot2', socket_type='NodeSocketVector', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = (0.0, 0.0, 0.0)
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 3.4028234663852886e+38
        if hasattr(input, 'min_value'):
            input.min_value = -3.4028234663852886e+38
        if hasattr(input, 'name'):
            input.name = 'animTexRotationPivot2'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketVector'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='animTexRotationSpeed2', socket_type='NodeSocketFloat', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = 0.0
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 3.4028234663852886e+38
        if hasattr(input, 'min_value'):
            input.min_value = -3.4028234663852886e+38
        if hasattr(input, 'name'):
            input.name = 'animTexRotationSpeed2'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketFloat'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='Animation Offset', socket_type='NodeSocketFloat', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = 0.5
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 10000.0
        if hasattr(input, 'min_value'):
            input.min_value = -10000.0
        if hasattr(input, 'name'):
            input.name = 'Animation Offset'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketFloat'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        # OUTPUTS
        output = node_tree1.interface.new_socket(name='animTex0TransformedUVs', socket_type='NodeSocketVector', in_out='OUTPUT')
        if hasattr(output, 'attribute_domain'):
            output.attribute_domain = 'POINT'
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0)
        if hasattr(output, 'force_non_field'):
            output.force_non_field = False
        if hasattr(output, 'hide_in_modifier'):
            output.hide_in_modifier = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'max_value'):
            output.max_value = 3.4028234663852886e+38
        if hasattr(output, 'min_value'):
            output.min_value = -3.4028234663852886e+38
        if hasattr(output, 'name'):
            output.name = 'animTex0TransformedUVs'
        if hasattr(output, 'socket_type'):
            output.socket_type = 'NodeSocketVector'
        if hasattr(output, 'subtype'):
            output.subtype = 'NONE'
        output = node_tree1.interface.new_socket(name='animTex1TransformedUVs', socket_type='NodeSocketVector', in_out='OUTPUT')
        if hasattr(output, 'attribute_domain'):
            output.attribute_domain = 'POINT'
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0)
        if hasattr(output, 'force_non_field'):
            output.force_non_field = False
        if hasattr(output, 'hide_in_modifier'):
            output.hide_in_modifier = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'max_value'):
            output.max_value = 3.4028234663852886e+38
        if hasattr(output, 'min_value'):
            output.min_value = -3.4028234663852886e+38
        if hasattr(output, 'name'):
            output.name = 'animTex1TransformedUVs'
        if hasattr(output, 'socket_type'):
            output.socket_type = 'NodeSocketVector'
        if hasattr(output, 'subtype'):
            output.subtype = 'NONE'
        output = node_tree1.interface.new_socket(name='animTex2TransformedUVs', socket_type='NodeSocketVector', in_out='OUTPUT')
        if hasattr(output, 'attribute_domain'):
            output.attribute_domain = 'POINT'
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0)
        if hasattr(output, 'force_non_field'):
            output.force_non_field = False
        if hasattr(output, 'hide_in_modifier'):
            output.hide_in_modifier = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'max_value'):
            output.max_value = 3.4028234663852886e+38
        if hasattr(output, 'min_value'):
            output.min_value = -3.4028234663852886e+38
        if hasattr(output, 'name'):
            output.name = 'animTex2TransformedUVs'
        if hasattr(output, 'socket_type'):
            output.socket_type = 'NodeSocketVector'
        if hasattr(output, 'subtype'):
            output.subtype = 'NONE'
        # NODES
        group_output_1 = node_tree1.nodes.new('NodeGroupOutput')
        if hasattr(group_output_1, 'color'):
            group_output_1.color = (0.0, 0.0, 0.3999914526939392)
        if hasattr(group_output_1, 'hide'):
            group_output_1.hide = False
        if hasattr(group_output_1, 'is_active_output'):
            group_output_1.is_active_output = True
        if hasattr(group_output_1, 'location'):
            group_output_1.location = (633.008056640625, -0.0)
        if hasattr(group_output_1, 'mute'):
            group_output_1.mute = False
        if hasattr(group_output_1, 'name'):
            group_output_1.name = 'Group Output'
        if hasattr(group_output_1, 'status'):
            group_output_1.status = False
        if hasattr(group_output_1, 'use_custom_color'):
            group_output_1.use_custom_color = True
        if hasattr(group_output_1, 'width'):
            group_output_1.width = 177.6431884765625
        if hasattr(group_output_1.inputs[0], 'default_value'):
            group_output_1.inputs[0].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_output_1.inputs[0], 'display_shape'):
            group_output_1.inputs[0].display_shape = 'CIRCLE'
        if hasattr(group_output_1.inputs[0], 'enabled'):
            group_output_1.inputs[0].enabled = True
        if hasattr(group_output_1.inputs[0], 'hide'):
            group_output_1.inputs[0].hide = False
        if hasattr(group_output_1.inputs[0], 'hide_value'):
            group_output_1.inputs[0].hide_value = False
        if hasattr(group_output_1.inputs[0], 'name'):
            group_output_1.inputs[0].name = 'animTex0TransformedUVs'
        if hasattr(group_output_1.inputs[0], 'show_expanded'):
            group_output_1.inputs[0].show_expanded = False
        if hasattr(group_output_1.inputs[1], 'default_value'):
            group_output_1.inputs[1].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_output_1.inputs[1], 'display_shape'):
            group_output_1.inputs[1].display_shape = 'CIRCLE'
        if hasattr(group_output_1.inputs[1], 'enabled'):
            group_output_1.inputs[1].enabled = True
        if hasattr(group_output_1.inputs[1], 'hide'):
            group_output_1.inputs[1].hide = False
        if hasattr(group_output_1.inputs[1], 'hide_value'):
            group_output_1.inputs[1].hide_value = False
        if hasattr(group_output_1.inputs[1], 'name'):
            group_output_1.inputs[1].name = 'animTex1TransformedUVs'
        if hasattr(group_output_1.inputs[1], 'show_expanded'):
            group_output_1.inputs[1].show_expanded = False
        if hasattr(group_output_1.inputs[2], 'default_value'):
            group_output_1.inputs[2].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_output_1.inputs[2], 'display_shape'):
            group_output_1.inputs[2].display_shape = 'CIRCLE'
        if hasattr(group_output_1.inputs[2], 'enabled'):
            group_output_1.inputs[2].enabled = True
        if hasattr(group_output_1.inputs[2], 'hide'):
            group_output_1.inputs[2].hide = False
        if hasattr(group_output_1.inputs[2], 'hide_value'):
            group_output_1.inputs[2].hide_value = False
        if hasattr(group_output_1.inputs[2], 'name'):
            group_output_1.inputs[2].name = 'animTex2TransformedUVs'
        if hasattr(group_output_1.inputs[2], 'show_expanded'):
            group_output_1.inputs[2].show_expanded = False

        reroute_001_1 = node_tree1.nodes.new('NodeReroute')
        if hasattr(reroute_001_1, 'color'):
            reroute_001_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(reroute_001_1, 'hide'):
            reroute_001_1.hide = False
        if hasattr(reroute_001_1, 'location'):
            reroute_001_1.location = (-81.34477233886719, -170.4523162841797)
        if hasattr(reroute_001_1, 'mute'):
            reroute_001_1.mute = False
        if hasattr(reroute_001_1, 'name'):
            reroute_001_1.name = 'Reroute.001'
        if hasattr(reroute_001_1, 'status'):
            reroute_001_1.status = False
        if hasattr(reroute_001_1, 'use_custom_color'):
            reroute_001_1.use_custom_color = False
        if hasattr(reroute_001_1, 'width'):
            reroute_001_1.width = 16.0

        reroute_006_1 = node_tree1.nodes.new('NodeReroute')
        if hasattr(reroute_006_1, 'color'):
            reroute_006_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(reroute_006_1, 'hide'):
            reroute_006_1.hide = False
        if hasattr(reroute_006_1, 'location'):
            reroute_006_1.location = (-81.34477233886719, -126.3909912109375)
        if hasattr(reroute_006_1, 'mute'):
            reroute_006_1.mute = False
        if hasattr(reroute_006_1, 'name'):
            reroute_006_1.name = 'Reroute.006'
        if hasattr(reroute_006_1, 'status'):
            reroute_006_1.status = False
        if hasattr(reroute_006_1, 'use_custom_color'):
            reroute_006_1.use_custom_color = False
        if hasattr(reroute_006_1, 'width'):
            reroute_006_1.width = 16.0

        reroute_007_1 = node_tree1.nodes.new('NodeReroute')
        if hasattr(reroute_007_1, 'color'):
            reroute_007_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(reroute_007_1, 'hide'):
            reroute_007_1.hide = False
        if hasattr(reroute_007_1, 'location'):
            reroute_007_1.location = (-81.34477233886719, -148.42457580566406)
        if hasattr(reroute_007_1, 'mute'):
            reroute_007_1.mute = False
        if hasattr(reroute_007_1, 'name'):
            reroute_007_1.name = 'Reroute.007'
        if hasattr(reroute_007_1, 'status'):
            reroute_007_1.status = False
        if hasattr(reroute_007_1, 'use_custom_color'):
            reroute_007_1.use_custom_color = False
        if hasattr(reroute_007_1, 'width'):
            reroute_007_1.width = 16.0

        group_input_1 = node_tree1.nodes.new('NodeGroupInput')
        if hasattr(group_input_1, 'color'):
            group_input_1.color = (0.3999914526939392, 0.0, 0.0)
        if hasattr(group_input_1, 'hide'):
            group_input_1.hide = False
        if hasattr(group_input_1, 'location'):
            group_input_1.location = (-557.6431884765625, -29.958396911621094)
        if hasattr(group_input_1, 'mute'):
            group_input_1.mute = False
        if hasattr(group_input_1, 'name'):
            group_input_1.name = 'Group Input'
        if hasattr(group_input_1, 'status'):
            group_input_1.status = False
        if hasattr(group_input_1, 'use_custom_color'):
            group_input_1.use_custom_color = True
        if hasattr(group_input_1, 'width'):
            group_input_1.width = 177.6431884765625
        if hasattr(group_input_1.outputs[0], 'default_value'):
            group_input_1.outputs[0].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_1.outputs[0], 'display_shape'):
            group_input_1.outputs[0].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[0], 'enabled'):
            group_input_1.outputs[0].enabled = True
        if hasattr(group_input_1.outputs[0], 'hide'):
            group_input_1.outputs[0].hide = False
        if hasattr(group_input_1.outputs[0], 'hide_value'):
            group_input_1.outputs[0].hide_value = False
        if hasattr(group_input_1.outputs[0], 'name'):
            group_input_1.outputs[0].name = 'animTexUVScrollSpeed0'
        if hasattr(group_input_1.outputs[0], 'show_expanded'):
            group_input_1.outputs[0].show_expanded = False
        if hasattr(group_input_1.outputs[1], 'default_value'):
            group_input_1.outputs[1].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_1.outputs[1], 'display_shape'):
            group_input_1.outputs[1].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[1], 'enabled'):
            group_input_1.outputs[1].enabled = True
        if hasattr(group_input_1.outputs[1], 'hide'):
            group_input_1.outputs[1].hide = False
        if hasattr(group_input_1.outputs[1], 'hide_value'):
            group_input_1.outputs[1].hide_value = False
        if hasattr(group_input_1.outputs[1], 'name'):
            group_input_1.outputs[1].name = 'animTexRotationPivot0'
        if hasattr(group_input_1.outputs[1], 'show_expanded'):
            group_input_1.outputs[1].show_expanded = False
        if hasattr(group_input_1.outputs[2], 'default_value'):
            group_input_1.outputs[2].default_value = 0.0
        if hasattr(group_input_1.outputs[2], 'display_shape'):
            group_input_1.outputs[2].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[2], 'enabled'):
            group_input_1.outputs[2].enabled = True
        if hasattr(group_input_1.outputs[2], 'hide'):
            group_input_1.outputs[2].hide = False
        if hasattr(group_input_1.outputs[2], 'hide_value'):
            group_input_1.outputs[2].hide_value = False
        if hasattr(group_input_1.outputs[2], 'name'):
            group_input_1.outputs[2].name = 'animTexRotationSpeed0'
        if hasattr(group_input_1.outputs[2], 'show_expanded'):
            group_input_1.outputs[2].show_expanded = False
        if hasattr(group_input_1.outputs[3], 'default_value'):
            group_input_1.outputs[3].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_1.outputs[3], 'display_shape'):
            group_input_1.outputs[3].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[3], 'enabled'):
            group_input_1.outputs[3].enabled = True
        if hasattr(group_input_1.outputs[3], 'hide'):
            group_input_1.outputs[3].hide = False
        if hasattr(group_input_1.outputs[3], 'hide_value'):
            group_input_1.outputs[3].hide_value = False
        if hasattr(group_input_1.outputs[3], 'name'):
            group_input_1.outputs[3].name = 'animTexUVScrollSpeed1'
        if hasattr(group_input_1.outputs[3], 'show_expanded'):
            group_input_1.outputs[3].show_expanded = False
        if hasattr(group_input_1.outputs[4], 'default_value'):
            group_input_1.outputs[4].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_1.outputs[4], 'display_shape'):
            group_input_1.outputs[4].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[4], 'enabled'):
            group_input_1.outputs[4].enabled = True
        if hasattr(group_input_1.outputs[4], 'hide'):
            group_input_1.outputs[4].hide = False
        if hasattr(group_input_1.outputs[4], 'hide_value'):
            group_input_1.outputs[4].hide_value = False
        if hasattr(group_input_1.outputs[4], 'name'):
            group_input_1.outputs[4].name = 'animTexRotationPivot1'
        if hasattr(group_input_1.outputs[4], 'show_expanded'):
            group_input_1.outputs[4].show_expanded = False
        if hasattr(group_input_1.outputs[5], 'default_value'):
            group_input_1.outputs[5].default_value = 0.0
        if hasattr(group_input_1.outputs[5], 'display_shape'):
            group_input_1.outputs[5].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[5], 'enabled'):
            group_input_1.outputs[5].enabled = True
        if hasattr(group_input_1.outputs[5], 'hide'):
            group_input_1.outputs[5].hide = False
        if hasattr(group_input_1.outputs[5], 'hide_value'):
            group_input_1.outputs[5].hide_value = False
        if hasattr(group_input_1.outputs[5], 'name'):
            group_input_1.outputs[5].name = 'animTexRotationSpeed1'
        if hasattr(group_input_1.outputs[5], 'show_expanded'):
            group_input_1.outputs[5].show_expanded = False
        if hasattr(group_input_1.outputs[6], 'default_value'):
            group_input_1.outputs[6].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_1.outputs[6], 'display_shape'):
            group_input_1.outputs[6].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[6], 'enabled'):
            group_input_1.outputs[6].enabled = True
        if hasattr(group_input_1.outputs[6], 'hide'):
            group_input_1.outputs[6].hide = False
        if hasattr(group_input_1.outputs[6], 'hide_value'):
            group_input_1.outputs[6].hide_value = False
        if hasattr(group_input_1.outputs[6], 'name'):
            group_input_1.outputs[6].name = 'animTexUVScrollSpeed2'
        if hasattr(group_input_1.outputs[6], 'show_expanded'):
            group_input_1.outputs[6].show_expanded = False
        if hasattr(group_input_1.outputs[7], 'default_value'):
            group_input_1.outputs[7].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_1.outputs[7], 'display_shape'):
            group_input_1.outputs[7].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[7], 'enabled'):
            group_input_1.outputs[7].enabled = True
        if hasattr(group_input_1.outputs[7], 'hide'):
            group_input_1.outputs[7].hide = False
        if hasattr(group_input_1.outputs[7], 'hide_value'):
            group_input_1.outputs[7].hide_value = False
        if hasattr(group_input_1.outputs[7], 'name'):
            group_input_1.outputs[7].name = 'animTexRotationPivot2'
        if hasattr(group_input_1.outputs[7], 'show_expanded'):
            group_input_1.outputs[7].show_expanded = False
        if hasattr(group_input_1.outputs[8], 'default_value'):
            group_input_1.outputs[8].default_value = 0.0
        if hasattr(group_input_1.outputs[8], 'display_shape'):
            group_input_1.outputs[8].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[8], 'enabled'):
            group_input_1.outputs[8].enabled = True
        if hasattr(group_input_1.outputs[8], 'hide'):
            group_input_1.outputs[8].hide = False
        if hasattr(group_input_1.outputs[8], 'hide_value'):
            group_input_1.outputs[8].hide_value = False
        if hasattr(group_input_1.outputs[8], 'name'):
            group_input_1.outputs[8].name = 'animTexRotationSpeed2'
        if hasattr(group_input_1.outputs[8], 'show_expanded'):
            group_input_1.outputs[8].show_expanded = False
        if hasattr(group_input_1.outputs[9], 'default_value'):
            group_input_1.outputs[9].default_value = 0.5
        if hasattr(group_input_1.outputs[9], 'display_shape'):
            group_input_1.outputs[9].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[9], 'enabled'):
            group_input_1.outputs[9].enabled = True
        if hasattr(group_input_1.outputs[9], 'hide'):
            group_input_1.outputs[9].hide = False
        if hasattr(group_input_1.outputs[9], 'hide_value'):
            group_input_1.outputs[9].hide_value = False
        if hasattr(group_input_1.outputs[9], 'name'):
            group_input_1.outputs[9].name = 'Animation Offset'
        if hasattr(group_input_1.outputs[9], 'show_expanded'):
            group_input_1.outputs[9].show_expanded = False

        math_1 = node_tree1.nodes.new('ShaderNodeMath')
        if hasattr(math_1, 'color'):
            math_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(math_1, 'hide'):
            math_1.hide = False
        if hasattr(math_1, 'location'):
            math_1.location = (-189.72097778320312, 50.7847900390625)
        if hasattr(math_1, 'mute'):
            math_1.mute = False
        if hasattr(math_1, 'name'):
            math_1.name = 'Math'
        if hasattr(math_1, 'operation'):
            math_1.operation = 'DIVIDE'
        if hasattr(math_1, 'status'):
            math_1.status = False
        if hasattr(math_1, 'use_clamp'):
            math_1.use_clamp = False
        if hasattr(math_1, 'use_custom_color'):
            math_1.use_custom_color = False
        if hasattr(math_1, 'width'):
            math_1.width = 140.0
        input_ = next((input_ for input_ in math_1.inputs if input_.identifier=='Value'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.5
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Value'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in math_1.inputs if input_.identifier=='Value_001'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 100.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Value'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in math_1.inputs if input_.identifier=='Value_002'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.5
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Value'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        output = next((output for output in math_1.outputs if output.identifier=='Value'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Value'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        animtex0uv_1 = node_tree1.nodes.new('ShaderNodeUVMap')
        if hasattr(animtex0uv_1, 'color'):
            animtex0uv_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(animtex0uv_1, 'from_instancer'):
            animtex0uv_1.from_instancer = False
        if hasattr(animtex0uv_1, 'hide'):
            animtex0uv_1.hide = False
        if hasattr(animtex0uv_1, 'label'):
            animtex0uv_1.label = 'animTex0UV'
        if hasattr(animtex0uv_1, 'location'):
            animtex0uv_1.location = (120.0, 369.7030944824219)
        if hasattr(animtex0uv_1, 'mute'):
            animtex0uv_1.mute = False
        if hasattr(animtex0uv_1, 'name'):
            animtex0uv_1.name = 'animTex0UV'
        if hasattr(animtex0uv_1, 'status'):
            animtex0uv_1.status = False
        if hasattr(animtex0uv_1, 'use_custom_color'):
            animtex0uv_1.use_custom_color = False
        if hasattr(animtex0uv_1, 'uv_map'):
            animtex0uv_1.uv_map = 'UVMap'
        if hasattr(animtex0uv_1, 'width'):
            animtex0uv_1.width = 130.0
        output = next((output for output in animtex0uv_1.outputs if output.identifier=='UV'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0)
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'UV'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        animtex1uv_1 = node_tree1.nodes.new('ShaderNodeUVMap')
        if hasattr(animtex1uv_1, 'color'):
            animtex1uv_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(animtex1uv_1, 'from_instancer'):
            animtex1uv_1.from_instancer = False
        if hasattr(animtex1uv_1, 'hide'):
            animtex1uv_1.hide = False
        if hasattr(animtex1uv_1, 'label'):
            animtex1uv_1.label = 'animTex1UV'
        if hasattr(animtex1uv_1, 'location'):
            animtex1uv_1.location = (120.0, 21.170574188232422)
        if hasattr(animtex1uv_1, 'mute'):
            animtex1uv_1.mute = False
        if hasattr(animtex1uv_1, 'name'):
            animtex1uv_1.name = 'animTex1UV'
        if hasattr(animtex1uv_1, 'status'):
            animtex1uv_1.status = False
        if hasattr(animtex1uv_1, 'use_custom_color'):
            animtex1uv_1.use_custom_color = False
        if hasattr(animtex1uv_1, 'uv_map'):
            animtex1uv_1.uv_map = 'UVMap.001'
        if hasattr(animtex1uv_1, 'width'):
            animtex1uv_1.width = 130.0
        output = next((output for output in animtex1uv_1.outputs if output.identifier=='UV'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0)
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'UV'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        reroute_002_1 = node_tree1.nodes.new('NodeReroute')
        if hasattr(reroute_002_1, 'color'):
            reroute_002_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(reroute_002_1, 'hide'):
            reroute_002_1.hide = False
        if hasattr(reroute_002_1, 'location'):
            reroute_002_1.location = (-81.34477233886719, 177.96875)
        if hasattr(reroute_002_1, 'mute'):
            reroute_002_1.mute = False
        if hasattr(reroute_002_1, 'name'):
            reroute_002_1.name = 'Reroute.002'
        if hasattr(reroute_002_1, 'status'):
            reroute_002_1.status = False
        if hasattr(reroute_002_1, 'use_custom_color'):
            reroute_002_1.use_custom_color = False
        if hasattr(reroute_002_1, 'width'):
            reroute_002_1.width = 16.0

        reroute_003_1 = node_tree1.nodes.new('NodeReroute')
        if hasattr(reroute_003_1, 'color'):
            reroute_003_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(reroute_003_1, 'hide'):
            reroute_003_1.hide = False
        if hasattr(reroute_003_1, 'location'):
            reroute_003_1.location = (-81.34477233886719, 225.6101531982422)
        if hasattr(reroute_003_1, 'mute'):
            reroute_003_1.mute = False
        if hasattr(reroute_003_1, 'name'):
            reroute_003_1.name = 'Reroute.003'
        if hasattr(reroute_003_1, 'status'):
            reroute_003_1.status = False
        if hasattr(reroute_003_1, 'use_custom_color'):
            reroute_003_1.use_custom_color = False
        if hasattr(reroute_003_1, 'width'):
            reroute_003_1.width = 16.0

        reroute_005_1 = node_tree1.nodes.new('NodeReroute')
        if hasattr(reroute_005_1, 'color'):
            reroute_005_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(reroute_005_1, 'hide'):
            reroute_005_1.hide = False
        if hasattr(reroute_005_1, 'location'):
            reroute_005_1.location = (-81.34477233886719, 201.90109252929688)
        if hasattr(reroute_005_1, 'mute'):
            reroute_005_1.mute = False
        if hasattr(reroute_005_1, 'name'):
            reroute_005_1.name = 'Reroute.005'
        if hasattr(reroute_005_1, 'status'):
            reroute_005_1.status = False
        if hasattr(reroute_005_1, 'use_custom_color'):
            reroute_005_1.use_custom_color = False
        if hasattr(reroute_005_1, 'width'):
            reroute_005_1.width = 16.0

        reroute_1 = node_tree1.nodes.new('NodeReroute')
        if hasattr(reroute_1, 'color'):
            reroute_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(reroute_1, 'hide'):
            reroute_1.hide = False
        if hasattr(reroute_1, 'location'):
            reroute_1.location = (-81.34477233886719, -473.99566650390625)
        if hasattr(reroute_1, 'mute'):
            reroute_1.mute = False
        if hasattr(reroute_1, 'name'):
            reroute_1.name = 'Reroute'
        if hasattr(reroute_1, 'status'):
            reroute_1.status = False
        if hasattr(reroute_1, 'use_custom_color'):
            reroute_1.use_custom_color = False
        if hasattr(reroute_1, 'width'):
            reroute_1.width = 16.0

        reroute_004_1 = node_tree1.nodes.new('NodeReroute')
        if hasattr(reroute_004_1, 'color'):
            reroute_004_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(reroute_004_1, 'hide'):
            reroute_004_1.hide = False
        if hasattr(reroute_004_1, 'location'):
            reroute_004_1.location = (-81.34477233886719, -521.1846923828125)
        if hasattr(reroute_004_1, 'mute'):
            reroute_004_1.mute = False
        if hasattr(reroute_004_1, 'name'):
            reroute_004_1.name = 'Reroute.004'
        if hasattr(reroute_004_1, 'status'):
            reroute_004_1.status = False
        if hasattr(reroute_004_1, 'use_custom_color'):
            reroute_004_1.use_custom_color = False
        if hasattr(reroute_004_1, 'width'):
            reroute_004_1.width = 16.0

        reroute_008_1 = node_tree1.nodes.new('NodeReroute')
        if hasattr(reroute_008_1, 'color'):
            reroute_008_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(reroute_008_1, 'hide'):
            reroute_008_1.hide = False
        if hasattr(reroute_008_1, 'location'):
            reroute_008_1.location = (-81.34477233886719, -497.60101318359375)
        if hasattr(reroute_008_1, 'mute'):
            reroute_008_1.mute = False
        if hasattr(reroute_008_1, 'name'):
            reroute_008_1.name = 'Reroute.008'
        if hasattr(reroute_008_1, 'status'):
            reroute_008_1.status = False
        if hasattr(reroute_008_1, 'use_custom_color'):
            reroute_008_1.use_custom_color = False
        if hasattr(reroute_008_1, 'width'):
            reroute_008_1.width = 16.0

        animtex2uv_1 = node_tree1.nodes.new('ShaderNodeUVMap')
        if hasattr(animtex2uv_1, 'color'):
            animtex2uv_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(animtex2uv_1, 'from_instancer'):
            animtex2uv_1.from_instancer = False
        if hasattr(animtex2uv_1, 'hide'):
            animtex2uv_1.hide = False
        if hasattr(animtex2uv_1, 'label'):
            animtex2uv_1.label = 'animTex2UV'
        if hasattr(animtex2uv_1, 'location'):
            animtex2uv_1.location = (120.0, -330.37445068359375)
        if hasattr(animtex2uv_1, 'mute'):
            animtex2uv_1.mute = False
        if hasattr(animtex2uv_1, 'name'):
            animtex2uv_1.name = 'animTex2UV'
        if hasattr(animtex2uv_1, 'status'):
            animtex2uv_1.status = False
        if hasattr(animtex2uv_1, 'use_custom_color'):
            animtex2uv_1.use_custom_color = False
        if hasattr(animtex2uv_1, 'uv_map'):
            animtex2uv_1.uv_map = 'UVMap.002'
        if hasattr(animtex2uv_1, 'width'):
            animtex2uv_1.width = 130.0
        output = next((output for output in animtex2uv_1.outputs if output.identifier=='UV'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0)
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'UV'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        reroute_011_1 = node_tree1.nodes.new('NodeReroute')
        if hasattr(reroute_011_1, 'color'):
            reroute_011_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(reroute_011_1, 'hide'):
            reroute_011_1.hide = False
        if hasattr(reroute_011_1, 'location'):
            reroute_011_1.location = (123.1505126953125, -542.7630004882812)
        if hasattr(reroute_011_1, 'mute'):
            reroute_011_1.mute = False
        if hasattr(reroute_011_1, 'name'):
            reroute_011_1.name = 'Reroute.011'
        if hasattr(reroute_011_1, 'status'):
            reroute_011_1.status = False
        if hasattr(reroute_011_1, 'use_custom_color'):
            reroute_011_1.use_custom_color = False
        if hasattr(reroute_011_1, 'width'):
            reroute_011_1.width = 16.0

        reroute_010_1 = node_tree1.nodes.new('NodeReroute')
        if hasattr(reroute_010_1, 'color'):
            reroute_010_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(reroute_010_1, 'hide'):
            reroute_010_1.hide = False
        if hasattr(reroute_010_1, 'location'):
            reroute_010_1.location = (123.1505126953125, -190.65792846679688)
        if hasattr(reroute_010_1, 'mute'):
            reroute_010_1.mute = False
        if hasattr(reroute_010_1, 'name'):
            reroute_010_1.name = 'Reroute.010'
        if hasattr(reroute_010_1, 'status'):
            reroute_010_1.status = False
        if hasattr(reroute_010_1, 'use_custom_color'):
            reroute_010_1.use_custom_color = False
        if hasattr(reroute_010_1, 'width'):
            reroute_010_1.width = 16.0

        reroute_009_1 = node_tree1.nodes.new('NodeReroute')
        if hasattr(reroute_009_1, 'color'):
            reroute_009_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(reroute_009_1, 'hide'):
            reroute_009_1.hide = False
        if hasattr(reroute_009_1, 'location'):
            reroute_009_1.location = (123.1505126953125, 157.68885803222656)
        if hasattr(reroute_009_1, 'mute'):
            reroute_009_1.mute = False
        if hasattr(reroute_009_1, 'name'):
            reroute_009_1.name = 'Reroute.009'
        if hasattr(reroute_009_1, 'status'):
            reroute_009_1.status = False
        if hasattr(reroute_009_1, 'use_custom_color'):
            reroute_009_1.use_custom_color = False
        if hasattr(reroute_009_1, 'width'):
            reroute_009_1.width = 16.0

        node_tree2 = bpy.data.node_groups.get('SW Aux - TransformUV')
        if not node_tree2:
            node_tree2 = bpy.data.node_groups.new('SW Aux - TransformUV', 'ShaderNodeTree')
            for node in node_tree2.nodes:
                node_tree2.nodes.remove(node)
            # INPUTS
            input = node_tree2.interface.new_socket(name='originalUVs', socket_type='NodeSocketVector', in_out='INPUT')
            if hasattr(input, 'attribute_domain'):
                input.attribute_domain = 'POINT'
            if hasattr(input, 'default_value'):
                input.default_value = (0.0, 0.0, 0.0)
            if hasattr(input, 'force_non_field'):
                input.force_non_field = False
            if hasattr(input, 'hide_in_modifier'):
                input.hide_in_modifier = False
            if hasattr(input, 'hide_value'):
                input.hide_value = False
            if hasattr(input, 'max_value'):
                input.max_value = 3.4028234663852886e+38
            if hasattr(input, 'min_value'):
                input.min_value = -3.4028234663852886e+38
            if hasattr(input, 'name'):
                input.name = 'originalUVs'
            if hasattr(input, 'socket_type'):
                input.socket_type = 'NodeSocketVector'
            if hasattr(input, 'subtype'):
                input.subtype = 'NONE'
            input = node_tree2.interface.new_socket(name='animTexUVScrollSpeed', socket_type='NodeSocketVector', in_out='INPUT')
            if hasattr(input, 'attribute_domain'):
                input.attribute_domain = 'POINT'
            if hasattr(input, 'default_value'):
                input.default_value = (0.0, 0.0, 0.0)
            if hasattr(input, 'force_non_field'):
                input.force_non_field = False
            if hasattr(input, 'hide_in_modifier'):
                input.hide_in_modifier = False
            if hasattr(input, 'hide_value'):
                input.hide_value = False
            if hasattr(input, 'max_value'):
                input.max_value = 3.4028234663852886e+38
            if hasattr(input, 'min_value'):
                input.min_value = -3.4028234663852886e+38
            if hasattr(input, 'name'):
                input.name = 'animTexUVScrollSpeed'
            if hasattr(input, 'socket_type'):
                input.socket_type = 'NodeSocketVector'
            if hasattr(input, 'subtype'):
                input.subtype = 'NONE'
            input = node_tree2.interface.new_socket(name='animTexUVRotationPivot', socket_type='NodeSocketVector', in_out='INPUT')
            if hasattr(input, 'attribute_domain'):
                input.attribute_domain = 'POINT'
            if hasattr(input, 'default_value'):
                input.default_value = (0.0, 0.0, 0.0)
            if hasattr(input, 'force_non_field'):
                input.force_non_field = False
            if hasattr(input, 'hide_in_modifier'):
                input.hide_in_modifier = False
            if hasattr(input, 'hide_value'):
                input.hide_value = False
            if hasattr(input, 'max_value'):
                input.max_value = 3.4028234663852886e+38
            if hasattr(input, 'min_value'):
                input.min_value = -3.4028234663852886e+38
            if hasattr(input, 'name'):
                input.name = 'animTexUVRotationPivot'
            if hasattr(input, 'socket_type'):
                input.socket_type = 'NodeSocketVector'
            if hasattr(input, 'subtype'):
                input.subtype = 'NONE'
            input = node_tree2.interface.new_socket(name='animTexRotationSpeed', socket_type='NodeSocketFloat', in_out='INPUT')
            if hasattr(input, 'attribute_domain'):
                input.attribute_domain = 'POINT'
            if hasattr(input, 'default_value'):
                input.default_value = 0.0
            if hasattr(input, 'force_non_field'):
                input.force_non_field = False
            if hasattr(input, 'hide_in_modifier'):
                input.hide_in_modifier = False
            if hasattr(input, 'hide_value'):
                input.hide_value = False
            if hasattr(input, 'max_value'):
                input.max_value = 3.4028234663852886e+38
            if hasattr(input, 'min_value'):
                input.min_value = -3.4028234663852886e+38
            if hasattr(input, 'name'):
                input.name = 'animTexRotationSpeed'
            if hasattr(input, 'socket_type'):
                input.socket_type = 'NodeSocketFloat'
            if hasattr(input, 'subtype'):
                input.subtype = 'NONE'
            input = node_tree2.interface.new_socket(name='ClockRandomOffset', socket_type='NodeSocketFloat', in_out='INPUT')
            if hasattr(input, 'attribute_domain'):
                input.attribute_domain = 'POINT'
            if hasattr(input, 'default_value'):
                input.default_value = 0.5
            if hasattr(input, 'force_non_field'):
                input.force_non_field = False
            if hasattr(input, 'hide_in_modifier'):
                input.hide_in_modifier = False
            if hasattr(input, 'hide_value'):
                input.hide_value = False
            if hasattr(input, 'max_value'):
                input.max_value = 10000.0
            if hasattr(input, 'min_value'):
                input.min_value = -10000.0
            if hasattr(input, 'name'):
                input.name = 'ClockRandomOffset'
            if hasattr(input, 'socket_type'):
                input.socket_type = 'NodeSocketFloat'
            if hasattr(input, 'subtype'):
                input.subtype = 'NONE'
            # OUTPUTS
            output = node_tree2.interface.new_socket(name='Value', socket_type='NodeSocketVector', in_out='OUTPUT')
            if hasattr(output, 'attribute_domain'):
                output.attribute_domain = 'POINT'
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0)
            if hasattr(output, 'force_non_field'):
                output.force_non_field = False
            if hasattr(output, 'hide_in_modifier'):
                output.hide_in_modifier = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'max_value'):
                output.max_value = 3.4028234663852886e+38
            if hasattr(output, 'min_value'):
                output.min_value = -3.4028234663852886e+38
            if hasattr(output, 'name'):
                output.name = 'Value'
            if hasattr(output, 'socket_type'):
                output.socket_type = 'NodeSocketVector'
            if hasattr(output, 'subtype'):
                output.subtype = 'NONE'
            # NODES
            const_2 = node_tree2.nodes.new('NodeFrame')
            if hasattr(const_2, 'color'):
                const_2.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
            if hasattr(const_2, 'hide'):
                const_2.hide = False
            if hasattr(const_2, 'label'):
                const_2.label = 'CONST'
            if hasattr(const_2, 'label_size'):
                const_2.label_size = 20
            if hasattr(const_2, 'location'):
                const_2.location = (-263.0, 107.0)
            if hasattr(const_2, 'mute'):
                const_2.mute = False
            if hasattr(const_2, 'name'):
                const_2.name = 'CONST'
            if hasattr(const_2, 'shrink'):
                const_2.shrink = True
            if hasattr(const_2, 'status'):
                const_2.status = False
            if hasattr(const_2, 'use_custom_color'):
                const_2.use_custom_color = False
            if hasattr(const_2, 'width'):
                const_2.width = 218.82159423828125

            vector_math_001_2 = node_tree2.nodes.new('ShaderNodeVectorMath')
            if hasattr(vector_math_001_2, 'color'):
                vector_math_001_2.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
            if hasattr(vector_math_001_2, 'hide'):
                vector_math_001_2.hide = False
            if hasattr(vector_math_001_2, 'location'):
                vector_math_001_2.location = (980.0, 520.0)
            if hasattr(vector_math_001_2, 'mute'):
                vector_math_001_2.mute = False
            if hasattr(vector_math_001_2, 'name'):
                vector_math_001_2.name = 'Vector Math.001'
            if hasattr(vector_math_001_2, 'operation'):
                vector_math_001_2.operation = 'ADD'
            if hasattr(vector_math_001_2, 'status'):
                vector_math_001_2.status = False
            if hasattr(vector_math_001_2, 'use_custom_color'):
                vector_math_001_2.use_custom_color = False
            if hasattr(vector_math_001_2, 'width'):
                vector_math_001_2.width = 140.0
            input_ = next((input_ for input_ in vector_math_001_2.inputs if input_.identifier=='Vector'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = (0.0, 0.0, 0.0)
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = True
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Vector'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in vector_math_001_2.inputs if input_.identifier=='Vector_001'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = (0.0, 0.0, 0.0)
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = True
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Vector'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in vector_math_001_2.inputs if input_.identifier=='Vector_002'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = (0.0, 0.0, 0.0)
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = False
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Vector'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in vector_math_001_2.inputs if input_.identifier=='Scale'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 1.0
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = False
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Scale'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            output = next((output for output in vector_math_001_2.outputs if output.identifier=='Vector'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = (0.0, 0.0, 0.0)
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Vector'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False
            output = next((output for output in vector_math_001_2.outputs if output.identifier=='Value'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = 0.0
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = False
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Value'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False

            math_001_2 = node_tree2.nodes.new('ShaderNodeMath')
            if hasattr(math_001_2, 'color'):
                math_001_2.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
            if hasattr(math_001_2, 'hide'):
                math_001_2.hide = False
            if hasattr(math_001_2, 'location'):
                math_001_2.location = (600.0, 560.0)
            if hasattr(math_001_2, 'mute'):
                math_001_2.mute = False
            if hasattr(math_001_2, 'name'):
                math_001_2.name = 'Math.001'
            if hasattr(math_001_2, 'operation'):
                math_001_2.operation = 'MULTIPLY'
            if hasattr(math_001_2, 'status'):
                math_001_2.status = False
            if hasattr(math_001_2, 'use_clamp'):
                math_001_2.use_clamp = False
            if hasattr(math_001_2, 'use_custom_color'):
                math_001_2.use_custom_color = False
            if hasattr(math_001_2, 'width'):
                math_001_2.width = 100.0
            input_ = next((input_ for input_ in math_001_2.inputs if input_.identifier=='Value'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 0.5
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = True
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Value'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in math_001_2.inputs if input_.identifier=='Value_001'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 0.5
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = True
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Value'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in math_001_2.inputs if input_.identifier=='Value_002'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 0.5
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = False
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Value'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            output = next((output for output in math_001_2.outputs if output.identifier=='Value'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = 0.0
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Value'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False

            math_005_2 = node_tree2.nodes.new('ShaderNodeMath')
            if hasattr(math_005_2, 'color'):
                math_005_2.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
            if hasattr(math_005_2, 'hide'):
                math_005_2.hide = False
            if hasattr(math_005_2, 'location'):
                math_005_2.location = (160.0, 320.0)
            if hasattr(math_005_2, 'mute'):
                math_005_2.mute = False
            if hasattr(math_005_2, 'name'):
                math_005_2.name = 'Math.005'
            if hasattr(math_005_2, 'operation'):
                math_005_2.operation = 'MULTIPLY'
            if hasattr(math_005_2, 'status'):
                math_005_2.status = False
            if hasattr(math_005_2, 'use_clamp'):
                math_005_2.use_clamp = False
            if hasattr(math_005_2, 'use_custom_color'):
                math_005_2.use_custom_color = False
            if hasattr(math_005_2, 'width'):
                math_005_2.width = 140.0
            input_ = next((input_ for input_ in math_005_2.inputs if input_.identifier=='Value'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 0.5
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = True
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Value'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in math_005_2.inputs if input_.identifier=='Value_001'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 0.032999999821186066
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = True
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Value'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in math_005_2.inputs if input_.identifier=='Value_002'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 0.5
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = False
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Value'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            output = next((output for output in math_005_2.outputs if output.identifier=='Value'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = 0.0
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Value'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False

            math_004_2 = node_tree2.nodes.new('ShaderNodeMath')
            if hasattr(math_004_2, 'color'):
                math_004_2.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
            if hasattr(math_004_2, 'hide'):
                math_004_2.hide = False
            if hasattr(math_004_2, 'location'):
                math_004_2.location = (20.0, 120.0)
            if hasattr(math_004_2, 'mute'):
                math_004_2.mute = False
            if hasattr(math_004_2, 'name'):
                math_004_2.name = 'Math.004'
            if hasattr(math_004_2, 'operation'):
                math_004_2.operation = 'MULTIPLY'
            if hasattr(math_004_2, 'status'):
                math_004_2.status = False
            if hasattr(math_004_2, 'use_clamp'):
                math_004_2.use_clamp = False
            if hasattr(math_004_2, 'use_custom_color'):
                math_004_2.use_custom_color = False
            if hasattr(math_004_2, 'width'):
                math_004_2.width = 108.08160400390625
            input_ = next((input_ for input_ in math_004_2.inputs if input_.identifier=='Value'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 0.5
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = True
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Value'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in math_004_2.inputs if input_.identifier=='Value_001'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 0.5
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = True
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Value'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in math_004_2.inputs if input_.identifier=='Value_002'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 0.5
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = False
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Value'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            output = next((output for output in math_004_2.outputs if output.identifier=='Value'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = 0.0
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Value'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False

            math_2 = node_tree2.nodes.new('ShaderNodeMath')
            if hasattr(math_2, 'color'):
                math_2.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
            if hasattr(math_2, 'hide'):
                math_2.hide = False
            if hasattr(math_2, 'label'):
                math_2.label = 'randClock'
            if hasattr(math_2, 'location'):
                math_2.location = (340.0, 280.0)
            if hasattr(math_2, 'mute'):
                math_2.mute = False
            if hasattr(math_2, 'name'):
                math_2.name = 'Math'
            if hasattr(math_2, 'operation'):
                math_2.operation = 'ADD'
            if hasattr(math_2, 'status'):
                math_2.status = False
            if hasattr(math_2, 'use_clamp'):
                math_2.use_clamp = False
            if hasattr(math_2, 'use_custom_color'):
                math_2.use_custom_color = False
            if hasattr(math_2, 'width'):
                math_2.width = 109.309326171875
            input_ = next((input_ for input_ in math_2.inputs if input_.identifier=='Value'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 0.5
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = True
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Value'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in math_2.inputs if input_.identifier=='Value_001'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 0.5
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = True
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Value'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in math_2.inputs if input_.identifier=='Value_002'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 0.5
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = False
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Value'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            output = next((output for output in math_2.outputs if output.identifier=='Value'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = 0.0
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Value'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False

            node_tree3 = bpy.data.node_groups.get('rotateUVs')
            if not node_tree3:
                node_tree3 = bpy.data.node_groups.new('rotateUVs', 'ShaderNodeTree')
                for node in node_tree3.nodes:
                    node_tree3.nodes.remove(node)
                # INPUTS
                input = node_tree3.interface.new_socket(name='Texcoords', socket_type='NodeSocketVector', in_out='INPUT')
                if hasattr(input, 'attribute_domain'):
                    input.attribute_domain = 'POINT'
                if hasattr(input, 'default_value'):
                    input.default_value = (0.0, 0.0, 0.0)
                if hasattr(input, 'force_non_field'):
                    input.force_non_field = False
                if hasattr(input, 'hide_in_modifier'):
                    input.hide_in_modifier = False
                if hasattr(input, 'hide_value'):
                    input.hide_value = False
                if hasattr(input, 'max_value'):
                    input.max_value = 3.4028234663852886e+38
                if hasattr(input, 'min_value'):
                    input.min_value = -3.4028234663852886e+38
                if hasattr(input, 'name'):
                    input.name = 'Texcoords'
                if hasattr(input, 'socket_type'):
                    input.socket_type = 'NodeSocketVector'
                if hasattr(input, 'subtype'):
                    input.subtype = 'NONE'
                input = node_tree3.interface.new_socket(name='center', socket_type='NodeSocketVector', in_out='INPUT')
                if hasattr(input, 'attribute_domain'):
                    input.attribute_domain = 'POINT'
                if hasattr(input, 'default_value'):
                    input.default_value = (0.0, 0.0, 0.0)
                if hasattr(input, 'force_non_field'):
                    input.force_non_field = False
                if hasattr(input, 'hide_in_modifier'):
                    input.hide_in_modifier = False
                if hasattr(input, 'hide_value'):
                    input.hide_value = False
                if hasattr(input, 'max_value'):
                    input.max_value = 3.4028234663852886e+38
                if hasattr(input, 'min_value'):
                    input.min_value = -3.4028234663852886e+38
                if hasattr(input, 'name'):
                    input.name = 'center'
                if hasattr(input, 'socket_type'):
                    input.socket_type = 'NodeSocketVector'
                if hasattr(input, 'subtype'):
                    input.subtype = 'NONE'
                input = node_tree3.interface.new_socket(name='Theta', socket_type='NodeSocketFloat', in_out='INPUT')
                if hasattr(input, 'attribute_domain'):
                    input.attribute_domain = 'POINT'
                if hasattr(input, 'default_value'):
                    input.default_value = 0.0
                if hasattr(input, 'force_non_field'):
                    input.force_non_field = False
                if hasattr(input, 'hide_in_modifier'):
                    input.hide_in_modifier = False
                if hasattr(input, 'hide_value'):
                    input.hide_value = False
                if hasattr(input, 'max_value'):
                    input.max_value = 3.4028234663852886e+38
                if hasattr(input, 'min_value'):
                    input.min_value = -3.4028234663852886e+38
                if hasattr(input, 'name'):
                    input.name = 'Theta'
                if hasattr(input, 'socket_type'):
                    input.socket_type = 'NodeSocketFloat'
                if hasattr(input, 'subtype'):
                    input.subtype = 'NONE'
                # OUTPUTS
                output = node_tree3.interface.new_socket(name='rotateduv', socket_type='NodeSocketVector', in_out='OUTPUT')
                if hasattr(output, 'attribute_domain'):
                    output.attribute_domain = 'POINT'
                if hasattr(output, 'default_value'):
                    output.default_value = (0.0, 0.0, 0.0)
                if hasattr(output, 'force_non_field'):
                    output.force_non_field = False
                if hasattr(output, 'hide_in_modifier'):
                    output.hide_in_modifier = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'max_value'):
                    output.max_value = 3.4028234663852886e+38
                if hasattr(output, 'min_value'):
                    output.min_value = -3.4028234663852886e+38
                if hasattr(output, 'name'):
                    output.name = 'rotateduv'
                if hasattr(output, 'socket_type'):
                    output.socket_type = 'NodeSocketVector'
                if hasattr(output, 'subtype'):
                    output.subtype = 'NONE'
                # NODES
                math_001_3 = node_tree3.nodes.new('ShaderNodeMath')
                if hasattr(math_001_3, 'color'):
                    math_001_3.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
                if hasattr(math_001_3, 'hide'):
                    math_001_3.hide = False
                if hasattr(math_001_3, 'location'):
                    math_001_3.location = (-360.0, 340.0)
                if hasattr(math_001_3, 'mute'):
                    math_001_3.mute = False
                if hasattr(math_001_3, 'name'):
                    math_001_3.name = 'Math.001'
                if hasattr(math_001_3, 'operation'):
                    math_001_3.operation = 'SINE'
                if hasattr(math_001_3, 'status'):
                    math_001_3.status = False
                if hasattr(math_001_3, 'use_clamp'):
                    math_001_3.use_clamp = False
                if hasattr(math_001_3, 'use_custom_color'):
                    math_001_3.use_custom_color = False
                if hasattr(math_001_3, 'width'):
                    math_001_3.width = 140.0
                input_ = next((input_ for input_ in math_001_3.inputs if input_.identifier=='Value'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 0.5
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Value'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in math_001_3.inputs if input_.identifier=='Value_001'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 0.5
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = False
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Value'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in math_001_3.inputs if input_.identifier=='Value_002'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 0.5
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = False
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Value'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                output = next((output for output in math_001_3.outputs if output.identifier=='Value'), None)
                if output:
                    if hasattr(output, 'default_value'):
                        output.default_value = 0.0
                    if hasattr(output, 'display_shape'):
                        output.display_shape = 'CIRCLE'
                    if hasattr(output, 'enabled'):
                        output.enabled = True
                    if hasattr(output, 'hide'):
                        output.hide = False
                    if hasattr(output, 'hide_value'):
                        output.hide_value = False
                    if hasattr(output, 'name'):
                        output.name = 'Value'
                    if hasattr(output, 'show_expanded'):
                        output.show_expanded = False

                math_3 = node_tree3.nodes.new('ShaderNodeMath')
                if hasattr(math_3, 'color'):
                    math_3.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
                if hasattr(math_3, 'hide'):
                    math_3.hide = False
                if hasattr(math_3, 'location'):
                    math_3.location = (-160.0, 520.0)
                if hasattr(math_3, 'mute'):
                    math_3.mute = False
                if hasattr(math_3, 'name'):
                    math_3.name = 'Math'
                if hasattr(math_3, 'operation'):
                    math_3.operation = 'MULTIPLY'
                if hasattr(math_3, 'status'):
                    math_3.status = False
                if hasattr(math_3, 'use_clamp'):
                    math_3.use_clamp = False
                if hasattr(math_3, 'use_custom_color'):
                    math_3.use_custom_color = False
                if hasattr(math_3, 'width'):
                    math_3.width = 132.6343994140625
                input_ = next((input_ for input_ in math_3.inputs if input_.identifier=='Value'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = -1.0
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Value'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in math_3.inputs if input_.identifier=='Value_001'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 0.5
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Value'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in math_3.inputs if input_.identifier=='Value_002'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 0.5
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = False
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Value'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                output = next((output for output in math_3.outputs if output.identifier=='Value'), None)
                if output:
                    if hasattr(output, 'default_value'):
                        output.default_value = 0.0
                    if hasattr(output, 'display_shape'):
                        output.display_shape = 'CIRCLE'
                    if hasattr(output, 'enabled'):
                        output.enabled = True
                    if hasattr(output, 'hide'):
                        output.hide = False
                    if hasattr(output, 'hide_value'):
                        output.hide_value = False
                    if hasattr(output, 'name'):
                        output.name = 'Value'
                    if hasattr(output, 'show_expanded'):
                        output.show_expanded = False

                combine_xyz_001_3 = node_tree3.nodes.new('ShaderNodeCombineXYZ')
                if hasattr(combine_xyz_001_3, 'color'):
                    combine_xyz_001_3.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
                if hasattr(combine_xyz_001_3, 'hide'):
                    combine_xyz_001_3.hide = False
                if hasattr(combine_xyz_001_3, 'location'):
                    combine_xyz_001_3.location = (20.0, 420.0)
                if hasattr(combine_xyz_001_3, 'mute'):
                    combine_xyz_001_3.mute = False
                if hasattr(combine_xyz_001_3, 'name'):
                    combine_xyz_001_3.name = 'Combine XYZ.001'
                if hasattr(combine_xyz_001_3, 'status'):
                    combine_xyz_001_3.status = False
                if hasattr(combine_xyz_001_3, 'use_custom_color'):
                    combine_xyz_001_3.use_custom_color = False
                if hasattr(combine_xyz_001_3, 'width'):
                    combine_xyz_001_3.width = 100.0
                input_ = next((input_ for input_ in combine_xyz_001_3.inputs if input_.identifier=='X'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 0.0
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'X'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in combine_xyz_001_3.inputs if input_.identifier=='Y'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 0.0
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Y'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in combine_xyz_001_3.inputs if input_.identifier=='Z'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 0.0
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Z'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                output = next((output for output in combine_xyz_001_3.outputs if output.identifier=='Vector'), None)
                if output:
                    if hasattr(output, 'default_value'):
                        output.default_value = (0.0, 0.0, 0.0)
                    if hasattr(output, 'display_shape'):
                        output.display_shape = 'CIRCLE'
                    if hasattr(output, 'enabled'):
                        output.enabled = True
                    if hasattr(output, 'hide'):
                        output.hide = False
                    if hasattr(output, 'hide_value'):
                        output.hide_value = False
                    if hasattr(output, 'name'):
                        output.name = 'Vector'
                    if hasattr(output, 'show_expanded'):
                        output.show_expanded = False

                math_002_3 = node_tree3.nodes.new('ShaderNodeMath')
                if hasattr(math_002_3, 'color'):
                    math_002_3.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
                if hasattr(math_002_3, 'hide'):
                    math_002_3.hide = False
                if hasattr(math_002_3, 'location'):
                    math_002_3.location = (-360.0, 180.0)
                if hasattr(math_002_3, 'mute'):
                    math_002_3.mute = False
                if hasattr(math_002_3, 'name'):
                    math_002_3.name = 'Math.002'
                if hasattr(math_002_3, 'operation'):
                    math_002_3.operation = 'COSINE'
                if hasattr(math_002_3, 'status'):
                    math_002_3.status = False
                if hasattr(math_002_3, 'use_clamp'):
                    math_002_3.use_clamp = False
                if hasattr(math_002_3, 'use_custom_color'):
                    math_002_3.use_custom_color = False
                if hasattr(math_002_3, 'width'):
                    math_002_3.width = 140.0
                input_ = next((input_ for input_ in math_002_3.inputs if input_.identifier=='Value'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 0.5
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Value'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in math_002_3.inputs if input_.identifier=='Value_001'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 0.5
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = False
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Value'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in math_002_3.inputs if input_.identifier=='Value_002'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 0.5
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = False
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Value'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                output = next((output for output in math_002_3.outputs if output.identifier=='Value'), None)
                if output:
                    if hasattr(output, 'default_value'):
                        output.default_value = 0.0
                    if hasattr(output, 'display_shape'):
                        output.display_shape = 'CIRCLE'
                    if hasattr(output, 'enabled'):
                        output.enabled = True
                    if hasattr(output, 'hide'):
                        output.hide = False
                    if hasattr(output, 'hide_value'):
                        output.hide_value = False
                    if hasattr(output, 'name'):
                        output.name = 'Value'
                    if hasattr(output, 'show_expanded'):
                        output.show_expanded = False

                dot_uv_sc_xy__3 = node_tree3.nodes.new('ShaderNodeVectorMath')
                if hasattr(dot_uv_sc_xy__3, 'color'):
                    dot_uv_sc_xy__3.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
                if hasattr(dot_uv_sc_xy__3, 'hide'):
                    dot_uv_sc_xy__3.hide = False
                if hasattr(dot_uv_sc_xy__3, 'label'):
                    dot_uv_sc_xy__3.label = 'dot( uv, sc.xy )'
                if hasattr(dot_uv_sc_xy__3, 'location'):
                    dot_uv_sc_xy__3.location = (280.0, 180.0)
                if hasattr(dot_uv_sc_xy__3, 'mute'):
                    dot_uv_sc_xy__3.mute = False
                if hasattr(dot_uv_sc_xy__3, 'name'):
                    dot_uv_sc_xy__3.name = 'dot( uv, sc.xy )'
                if hasattr(dot_uv_sc_xy__3, 'operation'):
                    dot_uv_sc_xy__3.operation = 'DOT_PRODUCT'
                if hasattr(dot_uv_sc_xy__3, 'status'):
                    dot_uv_sc_xy__3.status = False
                if hasattr(dot_uv_sc_xy__3, 'use_custom_color'):
                    dot_uv_sc_xy__3.use_custom_color = False
                if hasattr(dot_uv_sc_xy__3, 'width'):
                    dot_uv_sc_xy__3.width = 192.98297119140625
                input_ = next((input_ for input_ in dot_uv_sc_xy__3.inputs if input_.identifier=='Vector'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = (0.0, 0.0, 0.0)
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Vector'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in dot_uv_sc_xy__3.inputs if input_.identifier=='Vector_001'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = (0.0, 0.0, 0.0)
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Vector'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in dot_uv_sc_xy__3.inputs if input_.identifier=='Vector_002'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = (0.0, 0.0, 0.0)
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = False
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Vector'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in dot_uv_sc_xy__3.inputs if input_.identifier=='Scale'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 1.0
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = False
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Scale'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                output = next((output for output in dot_uv_sc_xy__3.outputs if output.identifier=='Vector'), None)
                if output:
                    if hasattr(output, 'default_value'):
                        output.default_value = (0.0, 0.0, 0.0)
                    if hasattr(output, 'display_shape'):
                        output.display_shape = 'CIRCLE'
                    if hasattr(output, 'enabled'):
                        output.enabled = False
                    if hasattr(output, 'hide'):
                        output.hide = False
                    if hasattr(output, 'hide_value'):
                        output.hide_value = False
                    if hasattr(output, 'name'):
                        output.name = 'Vector'
                    if hasattr(output, 'show_expanded'):
                        output.show_expanded = False
                output = next((output for output in dot_uv_sc_xy__3.outputs if output.identifier=='Value'), None)
                if output:
                    if hasattr(output, 'default_value'):
                        output.default_value = 0.0
                    if hasattr(output, 'display_shape'):
                        output.display_shape = 'CIRCLE'
                    if hasattr(output, 'enabled'):
                        output.enabled = True
                    if hasattr(output, 'hide'):
                        output.hide = False
                    if hasattr(output, 'hide_value'):
                        output.hide_value = False
                    if hasattr(output, 'name'):
                        output.name = 'Value'
                    if hasattr(output, 'show_expanded'):
                        output.show_expanded = False

                combine_xyz_3 = node_tree3.nodes.new('ShaderNodeCombineXYZ')
                if hasattr(combine_xyz_3, 'color'):
                    combine_xyz_3.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
                if hasattr(combine_xyz_3, 'hide'):
                    combine_xyz_3.hide = False
                if hasattr(combine_xyz_3, 'label'):
                    combine_xyz_3.label = 'rotatedUV'
                if hasattr(combine_xyz_3, 'location'):
                    combine_xyz_3.location = (560.0, 300.0)
                if hasattr(combine_xyz_3, 'mute'):
                    combine_xyz_3.mute = False
                if hasattr(combine_xyz_3, 'name'):
                    combine_xyz_3.name = 'Combine XYZ'
                if hasattr(combine_xyz_3, 'status'):
                    combine_xyz_3.status = False
                if hasattr(combine_xyz_3, 'use_custom_color'):
                    combine_xyz_3.use_custom_color = False
                if hasattr(combine_xyz_3, 'width'):
                    combine_xyz_3.width = 100.0
                input_ = next((input_ for input_ in combine_xyz_3.inputs if input_.identifier=='X'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 0.0
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'X'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in combine_xyz_3.inputs if input_.identifier=='Y'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 0.0
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Y'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in combine_xyz_3.inputs if input_.identifier=='Z'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 0.0
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Z'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                output = next((output for output in combine_xyz_3.outputs if output.identifier=='Vector'), None)
                if output:
                    if hasattr(output, 'default_value'):
                        output.default_value = (0.0, 0.0, 0.0)
                    if hasattr(output, 'display_shape'):
                        output.display_shape = 'CIRCLE'
                    if hasattr(output, 'enabled'):
                        output.enabled = True
                    if hasattr(output, 'hide'):
                        output.hide = False
                    if hasattr(output, 'hide_value'):
                        output.hide_value = False
                    if hasattr(output, 'name'):
                        output.name = 'Vector'
                    if hasattr(output, 'show_expanded'):
                        output.show_expanded = False

                vector_math_003_3 = node_tree3.nodes.new('ShaderNodeVectorMath')
                if hasattr(vector_math_003_3, 'color'):
                    vector_math_003_3.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
                if hasattr(vector_math_003_3, 'hide'):
                    vector_math_003_3.hide = False
                if hasattr(vector_math_003_3, 'location'):
                    vector_math_003_3.location = (800.0, 120.0)
                if hasattr(vector_math_003_3, 'mute'):
                    vector_math_003_3.mute = False
                if hasattr(vector_math_003_3, 'name'):
                    vector_math_003_3.name = 'Vector Math.003'
                if hasattr(vector_math_003_3, 'operation'):
                    vector_math_003_3.operation = 'ADD'
                if hasattr(vector_math_003_3, 'status'):
                    vector_math_003_3.status = False
                if hasattr(vector_math_003_3, 'use_custom_color'):
                    vector_math_003_3.use_custom_color = False
                if hasattr(vector_math_003_3, 'width'):
                    vector_math_003_3.width = 100.0
                input_ = next((input_ for input_ in vector_math_003_3.inputs if input_.identifier=='Vector'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = (0.0, 0.0, 0.0)
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Vector'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in vector_math_003_3.inputs if input_.identifier=='Vector_001'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = (0.0, 0.0, 0.0)
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Vector'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in vector_math_003_3.inputs if input_.identifier=='Vector_002'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = (0.0, 0.0, 0.0)
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = False
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Vector'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in vector_math_003_3.inputs if input_.identifier=='Scale'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 1.0
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = False
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Scale'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                output = next((output for output in vector_math_003_3.outputs if output.identifier=='Vector'), None)
                if output:
                    if hasattr(output, 'default_value'):
                        output.default_value = (0.0, 0.0, 0.0)
                    if hasattr(output, 'display_shape'):
                        output.display_shape = 'CIRCLE'
                    if hasattr(output, 'enabled'):
                        output.enabled = True
                    if hasattr(output, 'hide'):
                        output.hide = False
                    if hasattr(output, 'hide_value'):
                        output.hide_value = False
                    if hasattr(output, 'name'):
                        output.name = 'Vector'
                    if hasattr(output, 'show_expanded'):
                        output.show_expanded = False
                output = next((output for output in vector_math_003_3.outputs if output.identifier=='Value'), None)
                if output:
                    if hasattr(output, 'default_value'):
                        output.default_value = 0.0
                    if hasattr(output, 'display_shape'):
                        output.display_shape = 'CIRCLE'
                    if hasattr(output, 'enabled'):
                        output.enabled = False
                    if hasattr(output, 'hide'):
                        output.hide = False
                    if hasattr(output, 'hide_value'):
                        output.hide_value = False
                    if hasattr(output, 'name'):
                        output.name = 'Value'
                    if hasattr(output, 'show_expanded'):
                        output.show_expanded = False

                group_output_3 = node_tree3.nodes.new('NodeGroupOutput')
                if hasattr(group_output_3, 'color'):
                    group_output_3.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
                if hasattr(group_output_3, 'hide'):
                    group_output_3.hide = False
                if hasattr(group_output_3, 'is_active_output'):
                    group_output_3.is_active_output = True
                if hasattr(group_output_3, 'location'):
                    group_output_3.location = (960.0, 120.0)
                if hasattr(group_output_3, 'mute'):
                    group_output_3.mute = False
                if hasattr(group_output_3, 'name'):
                    group_output_3.name = 'Group Output'
                if hasattr(group_output_3, 'status'):
                    group_output_3.status = False
                if hasattr(group_output_3, 'use_custom_color'):
                    group_output_3.use_custom_color = False
                if hasattr(group_output_3, 'width'):
                    group_output_3.width = 140.0
                if hasattr(group_output_3.inputs[0], 'default_value'):
                    group_output_3.inputs[0].default_value = (0.0, 0.0, 0.0)
                if hasattr(group_output_3.inputs[0], 'display_shape'):
                    group_output_3.inputs[0].display_shape = 'CIRCLE'
                if hasattr(group_output_3.inputs[0], 'enabled'):
                    group_output_3.inputs[0].enabled = True
                if hasattr(group_output_3.inputs[0], 'hide'):
                    group_output_3.inputs[0].hide = False
                if hasattr(group_output_3.inputs[0], 'hide_value'):
                    group_output_3.inputs[0].hide_value = False
                if hasattr(group_output_3.inputs[0], 'name'):
                    group_output_3.inputs[0].name = 'rotateduv'
                if hasattr(group_output_3.inputs[0], 'show_expanded'):
                    group_output_3.inputs[0].show_expanded = False

                uv_3 = node_tree3.nodes.new('ShaderNodeVectorMath')
                if hasattr(uv_3, 'color'):
                    uv_3.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
                if hasattr(uv_3, 'hide'):
                    uv_3.hide = False
                if hasattr(uv_3, 'label'):
                    uv_3.label = 'uv'
                if hasattr(uv_3, 'location'):
                    uv_3.location = (-180.0, -20.0)
                if hasattr(uv_3, 'mute'):
                    uv_3.mute = False
                if hasattr(uv_3, 'name'):
                    uv_3.name = 'uv'
                if hasattr(uv_3, 'operation'):
                    uv_3.operation = 'SUBTRACT'
                if hasattr(uv_3, 'status'):
                    uv_3.status = False
                if hasattr(uv_3, 'use_custom_color'):
                    uv_3.use_custom_color = False
                if hasattr(uv_3, 'width'):
                    uv_3.width = 140.0
                input_ = next((input_ for input_ in uv_3.inputs if input_.identifier=='Vector'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = (0.0, 0.0, 0.0)
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Vector'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in uv_3.inputs if input_.identifier=='Vector_001'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = (0.0, 0.0, 0.0)
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Vector'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in uv_3.inputs if input_.identifier=='Vector_002'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = (0.0, 0.0, 0.0)
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = False
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Vector'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in uv_3.inputs if input_.identifier=='Scale'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 1.0
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = False
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Scale'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                output = next((output for output in uv_3.outputs if output.identifier=='Vector'), None)
                if output:
                    if hasattr(output, 'default_value'):
                        output.default_value = (0.0, 0.0, 0.0)
                    if hasattr(output, 'display_shape'):
                        output.display_shape = 'CIRCLE'
                    if hasattr(output, 'enabled'):
                        output.enabled = True
                    if hasattr(output, 'hide'):
                        output.hide = False
                    if hasattr(output, 'hide_value'):
                        output.hide_value = False
                    if hasattr(output, 'name'):
                        output.name = 'Vector'
                    if hasattr(output, 'show_expanded'):
                        output.show_expanded = False
                output = next((output for output in uv_3.outputs if output.identifier=='Value'), None)
                if output:
                    if hasattr(output, 'default_value'):
                        output.default_value = 0.0
                    if hasattr(output, 'display_shape'):
                        output.display_shape = 'CIRCLE'
                    if hasattr(output, 'enabled'):
                        output.enabled = False
                    if hasattr(output, 'hide'):
                        output.hide = False
                    if hasattr(output, 'hide_value'):
                        output.hide_value = False
                    if hasattr(output, 'name'):
                        output.name = 'Value'
                    if hasattr(output, 'show_expanded'):
                        output.show_expanded = False

                combine_xyz_002_3 = node_tree3.nodes.new('ShaderNodeCombineXYZ')
                if hasattr(combine_xyz_002_3, 'color'):
                    combine_xyz_002_3.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
                if hasattr(combine_xyz_002_3, 'hide'):
                    combine_xyz_002_3.hide = False
                if hasattr(combine_xyz_002_3, 'location'):
                    combine_xyz_002_3.location = (20.0, 280.0)
                if hasattr(combine_xyz_002_3, 'mute'):
                    combine_xyz_002_3.mute = False
                if hasattr(combine_xyz_002_3, 'name'):
                    combine_xyz_002_3.name = 'Combine XYZ.002'
                if hasattr(combine_xyz_002_3, 'status'):
                    combine_xyz_002_3.status = False
                if hasattr(combine_xyz_002_3, 'use_custom_color'):
                    combine_xyz_002_3.use_custom_color = False
                if hasattr(combine_xyz_002_3, 'width'):
                    combine_xyz_002_3.width = 100.0
                input_ = next((input_ for input_ in combine_xyz_002_3.inputs if input_.identifier=='X'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 0.0
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'X'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in combine_xyz_002_3.inputs if input_.identifier=='Y'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 0.0
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Y'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in combine_xyz_002_3.inputs if input_.identifier=='Z'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 0.0
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Z'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                output = next((output for output in combine_xyz_002_3.outputs if output.identifier=='Vector'), None)
                if output:
                    if hasattr(output, 'default_value'):
                        output.default_value = (0.0, 0.0, 0.0)
                    if hasattr(output, 'display_shape'):
                        output.display_shape = 'CIRCLE'
                    if hasattr(output, 'enabled'):
                        output.enabled = True
                    if hasattr(output, 'hide'):
                        output.hide = False
                    if hasattr(output, 'hide_value'):
                        output.hide_value = False
                    if hasattr(output, 'name'):
                        output.name = 'Vector'
                    if hasattr(output, 'show_expanded'):
                        output.show_expanded = False

                group_input_3 = node_tree3.nodes.new('NodeGroupInput')
                if hasattr(group_input_3, 'color'):
                    group_input_3.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
                if hasattr(group_input_3, 'hide'):
                    group_input_3.hide = False
                if hasattr(group_input_3, 'location'):
                    group_input_3.location = (-600.0, 80.0)
                if hasattr(group_input_3, 'mute'):
                    group_input_3.mute = False
                if hasattr(group_input_3, 'name'):
                    group_input_3.name = 'Group Input'
                if hasattr(group_input_3, 'status'):
                    group_input_3.status = False
                if hasattr(group_input_3, 'use_custom_color'):
                    group_input_3.use_custom_color = False
                if hasattr(group_input_3, 'width'):
                    group_input_3.width = 140.0
                if hasattr(group_input_3.outputs[0], 'default_value'):
                    group_input_3.outputs[0].default_value = (0.0, 0.0, 0.0)
                if hasattr(group_input_3.outputs[0], 'display_shape'):
                    group_input_3.outputs[0].display_shape = 'CIRCLE'
                if hasattr(group_input_3.outputs[0], 'enabled'):
                    group_input_3.outputs[0].enabled = True
                if hasattr(group_input_3.outputs[0], 'hide'):
                    group_input_3.outputs[0].hide = False
                if hasattr(group_input_3.outputs[0], 'hide_value'):
                    group_input_3.outputs[0].hide_value = False
                if hasattr(group_input_3.outputs[0], 'name'):
                    group_input_3.outputs[0].name = 'Texcoords'
                if hasattr(group_input_3.outputs[0], 'show_expanded'):
                    group_input_3.outputs[0].show_expanded = False
                if hasattr(group_input_3.outputs[1], 'default_value'):
                    group_input_3.outputs[1].default_value = (0.0, 0.0, 0.0)
                if hasattr(group_input_3.outputs[1], 'display_shape'):
                    group_input_3.outputs[1].display_shape = 'CIRCLE'
                if hasattr(group_input_3.outputs[1], 'enabled'):
                    group_input_3.outputs[1].enabled = True
                if hasattr(group_input_3.outputs[1], 'hide'):
                    group_input_3.outputs[1].hide = False
                if hasattr(group_input_3.outputs[1], 'hide_value'):
                    group_input_3.outputs[1].hide_value = False
                if hasattr(group_input_3.outputs[1], 'name'):
                    group_input_3.outputs[1].name = 'center'
                if hasattr(group_input_3.outputs[1], 'show_expanded'):
                    group_input_3.outputs[1].show_expanded = False
                if hasattr(group_input_3.outputs[2], 'default_value'):
                    group_input_3.outputs[2].default_value = 0.0
                if hasattr(group_input_3.outputs[2], 'display_shape'):
                    group_input_3.outputs[2].display_shape = 'CIRCLE'
                if hasattr(group_input_3.outputs[2], 'enabled'):
                    group_input_3.outputs[2].enabled = True
                if hasattr(group_input_3.outputs[2], 'hide'):
                    group_input_3.outputs[2].hide = False
                if hasattr(group_input_3.outputs[2], 'hide_value'):
                    group_input_3.outputs[2].hide_value = False
                if hasattr(group_input_3.outputs[2], 'name'):
                    group_input_3.outputs[2].name = 'Theta'
                if hasattr(group_input_3.outputs[2], 'show_expanded'):
                    group_input_3.outputs[2].show_expanded = False

                dot_uv_float2_sc_y_sc_x__3 = node_tree3.nodes.new('ShaderNodeVectorMath')
                if hasattr(dot_uv_float2_sc_y_sc_x__3, 'color'):
                    dot_uv_float2_sc_y_sc_x__3.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
                if hasattr(dot_uv_float2_sc_y_sc_x__3, 'hide'):
                    dot_uv_float2_sc_y_sc_x__3.hide = False
                if hasattr(dot_uv_float2_sc_y_sc_x__3, 'label'):
                    dot_uv_float2_sc_y_sc_x__3.label = 'dot( uv, float2( sc.y, -sc.x ) )'
                if hasattr(dot_uv_float2_sc_y_sc_x__3, 'location'):
                    dot_uv_float2_sc_y_sc_x__3.location = (280.0, 340.0)
                if hasattr(dot_uv_float2_sc_y_sc_x__3, 'mute'):
                    dot_uv_float2_sc_y_sc_x__3.mute = False
                if hasattr(dot_uv_float2_sc_y_sc_x__3, 'name'):
                    dot_uv_float2_sc_y_sc_x__3.name = 'dot( uv, float2( sc.y, -sc.x ) )'
                if hasattr(dot_uv_float2_sc_y_sc_x__3, 'operation'):
                    dot_uv_float2_sc_y_sc_x__3.operation = 'DOT_PRODUCT'
                if hasattr(dot_uv_float2_sc_y_sc_x__3, 'status'):
                    dot_uv_float2_sc_y_sc_x__3.status = False
                if hasattr(dot_uv_float2_sc_y_sc_x__3, 'use_custom_color'):
                    dot_uv_float2_sc_y_sc_x__3.use_custom_color = False
                if hasattr(dot_uv_float2_sc_y_sc_x__3, 'width'):
                    dot_uv_float2_sc_y_sc_x__3.width = 192.4620361328125
                input_ = next((input_ for input_ in dot_uv_float2_sc_y_sc_x__3.inputs if input_.identifier=='Vector'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = (0.0, 0.0, 0.0)
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Vector'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in dot_uv_float2_sc_y_sc_x__3.inputs if input_.identifier=='Vector_001'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = (0.0, 0.0, 0.0)
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = True
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Vector'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in dot_uv_float2_sc_y_sc_x__3.inputs if input_.identifier=='Vector_002'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = (0.0, 0.0, 0.0)
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = False
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Vector'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                input_ = next((input_ for input_ in dot_uv_float2_sc_y_sc_x__3.inputs if input_.identifier=='Scale'), None)
                if input_:
                    if hasattr(input_, 'default_value'):
                        input_.default_value = 1.0
                    if hasattr(input_, 'display_shape'):
                        input_.display_shape = 'CIRCLE'
                    if hasattr(input_, 'enabled'):
                        input_.enabled = False
                    if hasattr(input_, 'hide'):
                        input_.hide = False
                    if hasattr(input_, 'hide_value'):
                        input_.hide_value = False
                    if hasattr(input_, 'name'):
                        input_.name = 'Scale'
                    if hasattr(input_, 'show_expanded'):
                        input_.show_expanded = False
                output = next((output for output in dot_uv_float2_sc_y_sc_x__3.outputs if output.identifier=='Vector'), None)
                if output:
                    if hasattr(output, 'default_value'):
                        output.default_value = (0.0, 0.0, 0.0)
                    if hasattr(output, 'display_shape'):
                        output.display_shape = 'CIRCLE'
                    if hasattr(output, 'enabled'):
                        output.enabled = False
                    if hasattr(output, 'hide'):
                        output.hide = False
                    if hasattr(output, 'hide_value'):
                        output.hide_value = False
                    if hasattr(output, 'name'):
                        output.name = 'Vector'
                    if hasattr(output, 'show_expanded'):
                        output.show_expanded = False
                output = next((output for output in dot_uv_float2_sc_y_sc_x__3.outputs if output.identifier=='Value'), None)
                if output:
                    if hasattr(output, 'default_value'):
                        output.default_value = 0.0
                    if hasattr(output, 'display_shape'):
                        output.display_shape = 'CIRCLE'
                    if hasattr(output, 'enabled'):
                        output.enabled = True
                    if hasattr(output, 'hide'):
                        output.hide = False
                    if hasattr(output, 'hide_value'):
                        output.hide_value = False
                    if hasattr(output, 'name'):
                        output.name = 'Value'
                    if hasattr(output, 'show_expanded'):
                        output.show_expanded = False

                # LINKS
                node_tree3.links.new(group_input_3.outputs[0], uv_3.inputs[0])
                node_tree3.links.new(group_input_3.outputs[1], uv_3.inputs[1])
                node_tree3.links.new(dot_uv_sc_xy__3.outputs[1], combine_xyz_3.inputs[1])
                node_tree3.links.new(dot_uv_float2_sc_y_sc_x__3.outputs[1], combine_xyz_3.inputs[0])
                node_tree3.links.new(vector_math_003_3.outputs[0], group_output_3.inputs[0])
                node_tree3.links.new(combine_xyz_3.outputs[0], vector_math_003_3.inputs[0])
                node_tree3.links.new(group_input_3.outputs[1], vector_math_003_3.inputs[1])
                node_tree3.links.new(group_input_3.outputs[2], math_002_3.inputs[0])
                node_tree3.links.new(group_input_3.outputs[2], math_001_3.inputs[0])
                node_tree3.links.new(math_3.outputs[0], combine_xyz_001_3.inputs[1])
                node_tree3.links.new(math_001_3.outputs[0], combine_xyz_002_3.inputs[0])
                node_tree3.links.new(math_002_3.outputs[0], combine_xyz_002_3.inputs[1])
                node_tree3.links.new(math_001_3.outputs[0], math_3.inputs[0])
                node_tree3.links.new(math_002_3.outputs[0], combine_xyz_001_3.inputs[0])
                node_tree3.links.new(combine_xyz_001_3.outputs[0], dot_uv_float2_sc_y_sc_x__3.inputs[0])
                node_tree3.links.new(uv_3.outputs[0], dot_uv_float2_sc_y_sc_x__3.inputs[1])
                node_tree3.links.new(combine_xyz_002_3.outputs[0], dot_uv_sc_xy__3.inputs[0])
                node_tree3.links.new(uv_3.outputs[0], dot_uv_sc_xy__3.inputs[1])

            group_2 = node_tree2.nodes.new('ShaderNodeGroup')
            if hasattr(group_2, 'node_tree'):
                group_2.node_tree = bpy.data.node_groups.get('rotateUVs')
            if hasattr(group_2, 'color'):
                group_2.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
            if hasattr(group_2, 'hide'):
                group_2.hide = False
            if hasattr(group_2, 'location'):
                group_2.location = (780.0, 720.0)
            if hasattr(group_2, 'mute'):
                group_2.mute = False
            if hasattr(group_2, 'name'):
                group_2.name = 'Group'
            if hasattr(group_2, 'status'):
                group_2.status = False
            if hasattr(group_2, 'use_custom_color'):
                group_2.use_custom_color = False
            if hasattr(group_2, 'width'):
                group_2.width = 140.0
            if hasattr(group_2.inputs[0], 'default_value'):
                group_2.inputs[0].default_value = (0.0, 0.0, 0.0)
            if hasattr(group_2.inputs[0], 'display_shape'):
                group_2.inputs[0].display_shape = 'CIRCLE'
            if hasattr(group_2.inputs[0], 'enabled'):
                group_2.inputs[0].enabled = True
            if hasattr(group_2.inputs[0], 'hide'):
                group_2.inputs[0].hide = False
            if hasattr(group_2.inputs[0], 'hide_value'):
                group_2.inputs[0].hide_value = False
            if hasattr(group_2.inputs[0], 'name'):
                group_2.inputs[0].name = 'Texcoords'
            if hasattr(group_2.inputs[0], 'show_expanded'):
                group_2.inputs[0].show_expanded = False
            if hasattr(group_2.inputs[1], 'default_value'):
                group_2.inputs[1].default_value = (0.0, 0.0, 0.0)
            if hasattr(group_2.inputs[1], 'display_shape'):
                group_2.inputs[1].display_shape = 'CIRCLE'
            if hasattr(group_2.inputs[1], 'enabled'):
                group_2.inputs[1].enabled = True
            if hasattr(group_2.inputs[1], 'hide'):
                group_2.inputs[1].hide = False
            if hasattr(group_2.inputs[1], 'hide_value'):
                group_2.inputs[1].hide_value = False
            if hasattr(group_2.inputs[1], 'name'):
                group_2.inputs[1].name = 'center'
            if hasattr(group_2.inputs[1], 'show_expanded'):
                group_2.inputs[1].show_expanded = False
            if hasattr(group_2.inputs[2], 'default_value'):
                group_2.inputs[2].default_value = 0.0
            if hasattr(group_2.inputs[2], 'display_shape'):
                group_2.inputs[2].display_shape = 'CIRCLE'
            if hasattr(group_2.inputs[2], 'enabled'):
                group_2.inputs[2].enabled = True
            if hasattr(group_2.inputs[2], 'hide'):
                group_2.inputs[2].hide = False
            if hasattr(group_2.inputs[2], 'hide_value'):
                group_2.inputs[2].hide_value = False
            if hasattr(group_2.inputs[2], 'name'):
                group_2.inputs[2].name = 'Theta'
            if hasattr(group_2.inputs[2], 'show_expanded'):
                group_2.inputs[2].show_expanded = False
            if hasattr(group_2.outputs[0], 'default_value'):
                group_2.outputs[0].default_value = (0.0, 0.0, 0.0)
            if hasattr(group_2.outputs[0], 'display_shape'):
                group_2.outputs[0].display_shape = 'CIRCLE'
            if hasattr(group_2.outputs[0], 'enabled'):
                group_2.outputs[0].enabled = True
            if hasattr(group_2.outputs[0], 'hide'):
                group_2.outputs[0].hide = False
            if hasattr(group_2.outputs[0], 'hide_value'):
                group_2.outputs[0].hide_value = False
            if hasattr(group_2.outputs[0], 'name'):
                group_2.outputs[0].name = 'rotateduv'
            if hasattr(group_2.outputs[0], 'show_expanded'):
                group_2.outputs[0].show_expanded = False

            group_output_2 = node_tree2.nodes.new('NodeGroupOutput')
            if hasattr(group_output_2, 'color'):
                group_output_2.color = (0.0, 0.0, 0.3999914526939392)
            if hasattr(group_output_2, 'hide'):
                group_output_2.hide = False
            if hasattr(group_output_2, 'is_active_output'):
                group_output_2.is_active_output = True
            if hasattr(group_output_2, 'location'):
                group_output_2.location = (1180.0, 520.0)
            if hasattr(group_output_2, 'mute'):
                group_output_2.mute = False
            if hasattr(group_output_2, 'name'):
                group_output_2.name = 'Group Output'
            if hasattr(group_output_2, 'status'):
                group_output_2.status = False
            if hasattr(group_output_2, 'use_custom_color'):
                group_output_2.use_custom_color = True
            if hasattr(group_output_2, 'width'):
                group_output_2.width = 140.0
            if hasattr(group_output_2.inputs[0], 'default_value'):
                group_output_2.inputs[0].default_value = (0.0, 0.0, 0.0)
            if hasattr(group_output_2.inputs[0], 'display_shape'):
                group_output_2.inputs[0].display_shape = 'CIRCLE'
            if hasattr(group_output_2.inputs[0], 'enabled'):
                group_output_2.inputs[0].enabled = True
            if hasattr(group_output_2.inputs[0], 'hide'):
                group_output_2.inputs[0].hide = False
            if hasattr(group_output_2.inputs[0], 'hide_value'):
                group_output_2.inputs[0].hide_value = False
            if hasattr(group_output_2.inputs[0], 'name'):
                group_output_2.inputs[0].name = 'Value'
            if hasattr(group_output_2.inputs[0], 'show_expanded'):
                group_output_2.inputs[0].show_expanded = False

            randomsecondrange_2 = node_tree2.nodes.new('ShaderNodeValue')
            if hasattr(randomsecondrange_2, 'parent'):
                randomsecondrange_2.parent = node_tree2.nodes.get('CONST')
            if hasattr(randomsecondrange_2, 'color'):
                randomsecondrange_2.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
            if hasattr(randomsecondrange_2, 'hide'):
                randomsecondrange_2.hide = False
            if hasattr(randomsecondrange_2, 'label'):
                randomsecondrange_2.label = 'randomSecondRange'
            if hasattr(randomsecondrange_2, 'location'):
                randomsecondrange_2.location = (-5.4976806640625, -17.1622314453125)
            if hasattr(randomsecondrange_2, 'mute'):
                randomsecondrange_2.mute = False
            if hasattr(randomsecondrange_2, 'name'):
                randomsecondrange_2.name = 'randomSecondRange'
            if hasattr(randomsecondrange_2, 'status'):
                randomsecondrange_2.status = False
            if hasattr(randomsecondrange_2, 'use_custom_color'):
                randomsecondrange_2.use_custom_color = False
            if hasattr(randomsecondrange_2, 'width'):
                randomsecondrange_2.width = 158.82159423828125
            output = next((output for output in randomsecondrange_2.outputs if output.identifier=='Value'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = 10.0
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Value'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False

            _frame_driven_value_2 = node_tree2.nodes.new('ShaderNodeValue')
            if hasattr(_frame_driven_value_2, 'color'):
                _frame_driven_value_2.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
            if hasattr(_frame_driven_value_2, 'hide'):
                _frame_driven_value_2.hide = False
            if hasattr(_frame_driven_value_2, 'label'):
                _frame_driven_value_2.label = '#frame-driven Value'
            if hasattr(_frame_driven_value_2, 'location'):
                _frame_driven_value_2.location = (-23.030380249023438, 320.0)
            if hasattr(_frame_driven_value_2, 'mute'):
                _frame_driven_value_2.mute = False
            if hasattr(_frame_driven_value_2, 'name'):
                _frame_driven_value_2.name = '#frame-driven Value'
            if hasattr(_frame_driven_value_2, 'status'):
                _frame_driven_value_2.status = False
            if hasattr(_frame_driven_value_2, 'use_custom_color'):
                _frame_driven_value_2.use_custom_color = False
            if hasattr(_frame_driven_value_2, 'width'):
                _frame_driven_value_2.width = 148.6567840576172
            output = next((output for output in _frame_driven_value_2.outputs if output.identifier=='Value'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = 0.0
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Value'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False

            vector_math_2 = node_tree2.nodes.new('ShaderNodeVectorMath')
            if hasattr(vector_math_2, 'color'):
                vector_math_2.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
            if hasattr(vector_math_2, 'hide'):
                vector_math_2.hide = False
            if hasattr(vector_math_2, 'location'):
                vector_math_2.location = (798.6286010742188, 353.9390869140625)
            if hasattr(vector_math_2, 'mute'):
                vector_math_2.mute = False
            if hasattr(vector_math_2, 'name'):
                vector_math_2.name = 'Vector Math'
            if hasattr(vector_math_2, 'operation'):
                vector_math_2.operation = 'SCALE'
            if hasattr(vector_math_2, 'status'):
                vector_math_2.status = False
            if hasattr(vector_math_2, 'use_custom_color'):
                vector_math_2.use_custom_color = False
            if hasattr(vector_math_2, 'width'):
                vector_math_2.width = 100.0
            input_ = next((input_ for input_ in vector_math_2.inputs if input_.identifier=='Vector'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = (0.0, 0.0, 0.0)
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = True
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Vector'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in vector_math_2.inputs if input_.identifier=='Vector_001'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = (0.0, 0.0, 0.0)
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = False
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Vector'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in vector_math_2.inputs if input_.identifier=='Vector_002'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = (0.0, 0.0, 0.0)
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = False
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Vector'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in vector_math_2.inputs if input_.identifier=='Scale'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 1.0
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = True
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Scale'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            output = next((output for output in vector_math_2.outputs if output.identifier=='Vector'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = (0.0, 0.0, 0.0)
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Vector'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False
            output = next((output for output in vector_math_2.outputs if output.identifier=='Value'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = 0.0
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = False
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Value'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False

            group_input_2 = node_tree2.nodes.new('NodeGroupInput')
            if hasattr(group_input_2, 'color'):
                group_input_2.color = (0.3999914526939392, 0.0, 0.0)
            if hasattr(group_input_2, 'hide'):
                group_input_2.hide = False
            if hasattr(group_input_2, 'location'):
                group_input_2.location = (-280.0, 560.0)
            if hasattr(group_input_2, 'mute'):
                group_input_2.mute = False
            if hasattr(group_input_2, 'name'):
                group_input_2.name = 'Group Input'
            if hasattr(group_input_2, 'status'):
                group_input_2.status = False
            if hasattr(group_input_2, 'use_custom_color'):
                group_input_2.use_custom_color = True
            if hasattr(group_input_2, 'width'):
                group_input_2.width = 189.37701416015625
            if hasattr(group_input_2.outputs[0], 'default_value'):
                group_input_2.outputs[0].default_value = (0.0, 0.0, 0.0)
            if hasattr(group_input_2.outputs[0], 'display_shape'):
                group_input_2.outputs[0].display_shape = 'CIRCLE'
            if hasattr(group_input_2.outputs[0], 'enabled'):
                group_input_2.outputs[0].enabled = True
            if hasattr(group_input_2.outputs[0], 'hide'):
                group_input_2.outputs[0].hide = False
            if hasattr(group_input_2.outputs[0], 'hide_value'):
                group_input_2.outputs[0].hide_value = False
            if hasattr(group_input_2.outputs[0], 'name'):
                group_input_2.outputs[0].name = 'originalUVs'
            if hasattr(group_input_2.outputs[0], 'show_expanded'):
                group_input_2.outputs[0].show_expanded = False
            if hasattr(group_input_2.outputs[1], 'default_value'):
                group_input_2.outputs[1].default_value = (0.0, 0.0, 0.0)
            if hasattr(group_input_2.outputs[1], 'display_shape'):
                group_input_2.outputs[1].display_shape = 'CIRCLE'
            if hasattr(group_input_2.outputs[1], 'enabled'):
                group_input_2.outputs[1].enabled = True
            if hasattr(group_input_2.outputs[1], 'hide'):
                group_input_2.outputs[1].hide = False
            if hasattr(group_input_2.outputs[1], 'hide_value'):
                group_input_2.outputs[1].hide_value = False
            if hasattr(group_input_2.outputs[1], 'name'):
                group_input_2.outputs[1].name = 'animTexUVScrollSpeed'
            if hasattr(group_input_2.outputs[1], 'show_expanded'):
                group_input_2.outputs[1].show_expanded = False
            if hasattr(group_input_2.outputs[2], 'default_value'):
                group_input_2.outputs[2].default_value = (0.0, 0.0, 0.0)
            if hasattr(group_input_2.outputs[2], 'display_shape'):
                group_input_2.outputs[2].display_shape = 'CIRCLE'
            if hasattr(group_input_2.outputs[2], 'enabled'):
                group_input_2.outputs[2].enabled = True
            if hasattr(group_input_2.outputs[2], 'hide'):
                group_input_2.outputs[2].hide = False
            if hasattr(group_input_2.outputs[2], 'hide_value'):
                group_input_2.outputs[2].hide_value = False
            if hasattr(group_input_2.outputs[2], 'name'):
                group_input_2.outputs[2].name = 'animTexUVRotationPivot'
            if hasattr(group_input_2.outputs[2], 'show_expanded'):
                group_input_2.outputs[2].show_expanded = False
            if hasattr(group_input_2.outputs[3], 'default_value'):
                group_input_2.outputs[3].default_value = 0.0
            if hasattr(group_input_2.outputs[3], 'display_shape'):
                group_input_2.outputs[3].display_shape = 'CIRCLE'
            if hasattr(group_input_2.outputs[3], 'enabled'):
                group_input_2.outputs[3].enabled = True
            if hasattr(group_input_2.outputs[3], 'hide'):
                group_input_2.outputs[3].hide = False
            if hasattr(group_input_2.outputs[3], 'hide_value'):
                group_input_2.outputs[3].hide_value = False
            if hasattr(group_input_2.outputs[3], 'name'):
                group_input_2.outputs[3].name = 'animTexRotationSpeed'
            if hasattr(group_input_2.outputs[3], 'show_expanded'):
                group_input_2.outputs[3].show_expanded = False
            if hasattr(group_input_2.outputs[4], 'default_value'):
                group_input_2.outputs[4].default_value = 0.5
            if hasattr(group_input_2.outputs[4], 'display_shape'):
                group_input_2.outputs[4].display_shape = 'CIRCLE'
            if hasattr(group_input_2.outputs[4], 'enabled'):
                group_input_2.outputs[4].enabled = True
            if hasattr(group_input_2.outputs[4], 'hide'):
                group_input_2.outputs[4].hide = False
            if hasattr(group_input_2.outputs[4], 'hide_value'):
                group_input_2.outputs[4].hide_value = False
            if hasattr(group_input_2.outputs[4], 'name'):
                group_input_2.outputs[4].name = 'ClockRandomOffset'
            if hasattr(group_input_2.outputs[4], 'show_expanded'):
                group_input_2.outputs[4].show_expanded = False

            # LINKS
            node_tree2.links.new(group_input_2.outputs[0], group_2.inputs[0])
            node_tree2.links.new(group_input_2.outputs[2], group_2.inputs[1])
            node_tree2.links.new(math_001_2.outputs[0], group_2.inputs[2])
            node_tree2.links.new(math_004_2.outputs[0], math_2.inputs[1])
            node_tree2.links.new(math_005_2.outputs[0], math_2.inputs[0])
            node_tree2.links.new(group_input_2.outputs[3], math_001_2.inputs[0])
            node_tree2.links.new(math_2.outputs[0], math_001_2.inputs[1])
            node_tree2.links.new(_frame_driven_value_2.outputs[0], math_005_2.inputs[0])
            node_tree2.links.new(randomsecondrange_2.outputs[0], math_004_2.inputs[1])
            node_tree2.links.new(group_input_2.outputs[4], math_004_2.inputs[0])
            node_tree2.links.new(group_input_2.outputs[1], vector_math_2.inputs[0])
            node_tree2.links.new(math_2.outputs[0], vector_math_2.inputs[3])
            node_tree2.links.new(group_2.outputs[0], vector_math_001_2.inputs[0])
            node_tree2.links.new(vector_math_2.outputs[0], vector_math_001_2.inputs[1])
            node_tree2.links.new(vector_math_001_2.outputs[0], group_output_2.inputs[0])

        animtex1transformeduvs_1 = node_tree1.nodes.new('ShaderNodeGroup')
        if hasattr(animtex1transformeduvs_1, 'node_tree'):
            animtex1transformeduvs_1.node_tree = bpy.data.node_groups.get('SW Aux - TransformUV')
        if hasattr(animtex1transformeduvs_1, 'color'):
            animtex1transformeduvs_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(animtex1transformeduvs_1, 'hide'):
            animtex1transformeduvs_1.hide = False
        if hasattr(animtex1transformeduvs_1, 'label'):
            animtex1transformeduvs_1.label = 'animTex1TransformedUVs'
        if hasattr(animtex1transformeduvs_1, 'location'):
            animtex1transformeduvs_1.location = (300.0, -20.0)
        if hasattr(animtex1transformeduvs_1, 'mute'):
            animtex1transformeduvs_1.mute = False
        if hasattr(animtex1transformeduvs_1, 'name'):
            animtex1transformeduvs_1.name = 'animTex1TransformedUVs'
        if hasattr(animtex1transformeduvs_1, 'status'):
            animtex1transformeduvs_1.status = False
        if hasattr(animtex1transformeduvs_1, 'use_custom_color'):
            animtex1transformeduvs_1.use_custom_color = False
        if hasattr(animtex1transformeduvs_1, 'width'):
            animtex1transformeduvs_1.width = 200.0
        if hasattr(animtex1transformeduvs_1.inputs[0], 'default_value'):
            animtex1transformeduvs_1.inputs[0].default_value = (0.0, 0.0, 0.0)
        if hasattr(animtex1transformeduvs_1.inputs[0], 'display_shape'):
            animtex1transformeduvs_1.inputs[0].display_shape = 'CIRCLE'
        if hasattr(animtex1transformeduvs_1.inputs[0], 'enabled'):
            animtex1transformeduvs_1.inputs[0].enabled = True
        if hasattr(animtex1transformeduvs_1.inputs[0], 'hide'):
            animtex1transformeduvs_1.inputs[0].hide = False
        if hasattr(animtex1transformeduvs_1.inputs[0], 'hide_value'):
            animtex1transformeduvs_1.inputs[0].hide_value = False
        if hasattr(animtex1transformeduvs_1.inputs[0], 'name'):
            animtex1transformeduvs_1.inputs[0].name = 'originalUVs'
        if hasattr(animtex1transformeduvs_1.inputs[0], 'show_expanded'):
            animtex1transformeduvs_1.inputs[0].show_expanded = False
        if hasattr(animtex1transformeduvs_1.inputs[1], 'default_value'):
            animtex1transformeduvs_1.inputs[1].default_value = (-0.20000000298023224, 0.0, 0.0)
        if hasattr(animtex1transformeduvs_1.inputs[1], 'display_shape'):
            animtex1transformeduvs_1.inputs[1].display_shape = 'CIRCLE'
        if hasattr(animtex1transformeduvs_1.inputs[1], 'enabled'):
            animtex1transformeduvs_1.inputs[1].enabled = True
        if hasattr(animtex1transformeduvs_1.inputs[1], 'hide'):
            animtex1transformeduvs_1.inputs[1].hide = False
        if hasattr(animtex1transformeduvs_1.inputs[1], 'hide_value'):
            animtex1transformeduvs_1.inputs[1].hide_value = False
        if hasattr(animtex1transformeduvs_1.inputs[1], 'name'):
            animtex1transformeduvs_1.inputs[1].name = 'animTexUVScrollSpeed'
        if hasattr(animtex1transformeduvs_1.inputs[1], 'show_expanded'):
            animtex1transformeduvs_1.inputs[1].show_expanded = False
        if hasattr(animtex1transformeduvs_1.inputs[2], 'default_value'):
            animtex1transformeduvs_1.inputs[2].default_value = (0.5, 0.5, 0.0)
        if hasattr(animtex1transformeduvs_1.inputs[2], 'display_shape'):
            animtex1transformeduvs_1.inputs[2].display_shape = 'CIRCLE'
        if hasattr(animtex1transformeduvs_1.inputs[2], 'enabled'):
            animtex1transformeduvs_1.inputs[2].enabled = True
        if hasattr(animtex1transformeduvs_1.inputs[2], 'hide'):
            animtex1transformeduvs_1.inputs[2].hide = False
        if hasattr(animtex1transformeduvs_1.inputs[2], 'hide_value'):
            animtex1transformeduvs_1.inputs[2].hide_value = False
        if hasattr(animtex1transformeduvs_1.inputs[2], 'name'):
            animtex1transformeduvs_1.inputs[2].name = 'animTexUVRotationPivot'
        if hasattr(animtex1transformeduvs_1.inputs[2], 'show_expanded'):
            animtex1transformeduvs_1.inputs[2].show_expanded = False
        if hasattr(animtex1transformeduvs_1.inputs[3], 'default_value'):
            animtex1transformeduvs_1.inputs[3].default_value = 0.0
        if hasattr(animtex1transformeduvs_1.inputs[3], 'display_shape'):
            animtex1transformeduvs_1.inputs[3].display_shape = 'CIRCLE'
        if hasattr(animtex1transformeduvs_1.inputs[3], 'enabled'):
            animtex1transformeduvs_1.inputs[3].enabled = True
        if hasattr(animtex1transformeduvs_1.inputs[3], 'hide'):
            animtex1transformeduvs_1.inputs[3].hide = False
        if hasattr(animtex1transformeduvs_1.inputs[3], 'hide_value'):
            animtex1transformeduvs_1.inputs[3].hide_value = False
        if hasattr(animtex1transformeduvs_1.inputs[3], 'name'):
            animtex1transformeduvs_1.inputs[3].name = 'animTexRotationSpeed'
        if hasattr(animtex1transformeduvs_1.inputs[3], 'show_expanded'):
            animtex1transformeduvs_1.inputs[3].show_expanded = False
        if hasattr(animtex1transformeduvs_1.inputs[4], 'default_value'):
            animtex1transformeduvs_1.inputs[4].default_value = 0.10000000149011612
        if hasattr(animtex1transformeduvs_1.inputs[4], 'display_shape'):
            animtex1transformeduvs_1.inputs[4].display_shape = 'CIRCLE'
        if hasattr(animtex1transformeduvs_1.inputs[4], 'enabled'):
            animtex1transformeduvs_1.inputs[4].enabled = True
        if hasattr(animtex1transformeduvs_1.inputs[4], 'hide'):
            animtex1transformeduvs_1.inputs[4].hide = False
        if hasattr(animtex1transformeduvs_1.inputs[4], 'hide_value'):
            animtex1transformeduvs_1.inputs[4].hide_value = False
        if hasattr(animtex1transformeduvs_1.inputs[4], 'name'):
            animtex1transformeduvs_1.inputs[4].name = 'ClockRandomOffset'
        if hasattr(animtex1transformeduvs_1.inputs[4], 'show_expanded'):
            animtex1transformeduvs_1.inputs[4].show_expanded = False
        if hasattr(animtex1transformeduvs_1.outputs[0], 'default_value'):
            animtex1transformeduvs_1.outputs[0].default_value = (0.0, 0.0, 0.0)
        if hasattr(animtex1transformeduvs_1.outputs[0], 'display_shape'):
            animtex1transformeduvs_1.outputs[0].display_shape = 'CIRCLE'
        if hasattr(animtex1transformeduvs_1.outputs[0], 'enabled'):
            animtex1transformeduvs_1.outputs[0].enabled = True
        if hasattr(animtex1transformeduvs_1.outputs[0], 'hide'):
            animtex1transformeduvs_1.outputs[0].hide = False
        if hasattr(animtex1transformeduvs_1.outputs[0], 'hide_value'):
            animtex1transformeduvs_1.outputs[0].hide_value = False
        if hasattr(animtex1transformeduvs_1.outputs[0], 'name'):
            animtex1transformeduvs_1.outputs[0].name = 'Value'
        if hasattr(animtex1transformeduvs_1.outputs[0], 'show_expanded'):
            animtex1transformeduvs_1.outputs[0].show_expanded = False

        animtex2transformeduvs_1 = node_tree1.nodes.new('ShaderNodeGroup')
        if hasattr(animtex2transformeduvs_1, 'node_tree'):
            animtex2transformeduvs_1.node_tree = bpy.data.node_groups.get('SW Aux - TransformUV')
        if hasattr(animtex2transformeduvs_1, 'color'):
            animtex2transformeduvs_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(animtex2transformeduvs_1, 'hide'):
            animtex2transformeduvs_1.hide = False
        if hasattr(animtex2transformeduvs_1, 'label'):
            animtex2transformeduvs_1.label = 'animTex2TransformedUVs'
        if hasattr(animtex2transformeduvs_1, 'location'):
            animtex2transformeduvs_1.location = (300.0, -371.5450134277344)
        if hasattr(animtex2transformeduvs_1, 'mute'):
            animtex2transformeduvs_1.mute = False
        if hasattr(animtex2transformeduvs_1, 'name'):
            animtex2transformeduvs_1.name = 'animTex2TransformedUVs'
        if hasattr(animtex2transformeduvs_1, 'status'):
            animtex2transformeduvs_1.status = False
        if hasattr(animtex2transformeduvs_1, 'use_custom_color'):
            animtex2transformeduvs_1.use_custom_color = False
        if hasattr(animtex2transformeduvs_1, 'width'):
            animtex2transformeduvs_1.width = 200.0
        if hasattr(animtex2transformeduvs_1.inputs[0], 'default_value'):
            animtex2transformeduvs_1.inputs[0].default_value = (0.0, 0.0, 0.0)
        if hasattr(animtex2transformeduvs_1.inputs[0], 'display_shape'):
            animtex2transformeduvs_1.inputs[0].display_shape = 'CIRCLE'
        if hasattr(animtex2transformeduvs_1.inputs[0], 'enabled'):
            animtex2transformeduvs_1.inputs[0].enabled = True
        if hasattr(animtex2transformeduvs_1.inputs[0], 'hide'):
            animtex2transformeduvs_1.inputs[0].hide = False
        if hasattr(animtex2transformeduvs_1.inputs[0], 'hide_value'):
            animtex2transformeduvs_1.inputs[0].hide_value = False
        if hasattr(animtex2transformeduvs_1.inputs[0], 'name'):
            animtex2transformeduvs_1.inputs[0].name = 'originalUVs'
        if hasattr(animtex2transformeduvs_1.inputs[0], 'show_expanded'):
            animtex2transformeduvs_1.inputs[0].show_expanded = False
        if hasattr(animtex2transformeduvs_1.inputs[1], 'default_value'):
            animtex2transformeduvs_1.inputs[1].default_value = (0.10000000149011612, 0.0, 0.0)
        if hasattr(animtex2transformeduvs_1.inputs[1], 'display_shape'):
            animtex2transformeduvs_1.inputs[1].display_shape = 'CIRCLE'
        if hasattr(animtex2transformeduvs_1.inputs[1], 'enabled'):
            animtex2transformeduvs_1.inputs[1].enabled = True
        if hasattr(animtex2transformeduvs_1.inputs[1], 'hide'):
            animtex2transformeduvs_1.inputs[1].hide = False
        if hasattr(animtex2transformeduvs_1.inputs[1], 'hide_value'):
            animtex2transformeduvs_1.inputs[1].hide_value = False
        if hasattr(animtex2transformeduvs_1.inputs[1], 'name'):
            animtex2transformeduvs_1.inputs[1].name = 'animTexUVScrollSpeed'
        if hasattr(animtex2transformeduvs_1.inputs[1], 'show_expanded'):
            animtex2transformeduvs_1.inputs[1].show_expanded = False
        if hasattr(animtex2transformeduvs_1.inputs[2], 'default_value'):
            animtex2transformeduvs_1.inputs[2].default_value = (0.5, 0.5, 0.0)
        if hasattr(animtex2transformeduvs_1.inputs[2], 'display_shape'):
            animtex2transformeduvs_1.inputs[2].display_shape = 'CIRCLE'
        if hasattr(animtex2transformeduvs_1.inputs[2], 'enabled'):
            animtex2transformeduvs_1.inputs[2].enabled = True
        if hasattr(animtex2transformeduvs_1.inputs[2], 'hide'):
            animtex2transformeduvs_1.inputs[2].hide = False
        if hasattr(animtex2transformeduvs_1.inputs[2], 'hide_value'):
            animtex2transformeduvs_1.inputs[2].hide_value = False
        if hasattr(animtex2transformeduvs_1.inputs[2], 'name'):
            animtex2transformeduvs_1.inputs[2].name = 'animTexUVRotationPivot'
        if hasattr(animtex2transformeduvs_1.inputs[2], 'show_expanded'):
            animtex2transformeduvs_1.inputs[2].show_expanded = False
        if hasattr(animtex2transformeduvs_1.inputs[3], 'default_value'):
            animtex2transformeduvs_1.inputs[3].default_value = 0.0
        if hasattr(animtex2transformeduvs_1.inputs[3], 'display_shape'):
            animtex2transformeduvs_1.inputs[3].display_shape = 'CIRCLE'
        if hasattr(animtex2transformeduvs_1.inputs[3], 'enabled'):
            animtex2transformeduvs_1.inputs[3].enabled = True
        if hasattr(animtex2transformeduvs_1.inputs[3], 'hide'):
            animtex2transformeduvs_1.inputs[3].hide = False
        if hasattr(animtex2transformeduvs_1.inputs[3], 'hide_value'):
            animtex2transformeduvs_1.inputs[3].hide_value = False
        if hasattr(animtex2transformeduvs_1.inputs[3], 'name'):
            animtex2transformeduvs_1.inputs[3].name = 'animTexRotationSpeed'
        if hasattr(animtex2transformeduvs_1.inputs[3], 'show_expanded'):
            animtex2transformeduvs_1.inputs[3].show_expanded = False
        if hasattr(animtex2transformeduvs_1.inputs[4], 'default_value'):
            animtex2transformeduvs_1.inputs[4].default_value = 0.10000000149011612
        if hasattr(animtex2transformeduvs_1.inputs[4], 'display_shape'):
            animtex2transformeduvs_1.inputs[4].display_shape = 'CIRCLE'
        if hasattr(animtex2transformeduvs_1.inputs[4], 'enabled'):
            animtex2transformeduvs_1.inputs[4].enabled = True
        if hasattr(animtex2transformeduvs_1.inputs[4], 'hide'):
            animtex2transformeduvs_1.inputs[4].hide = False
        if hasattr(animtex2transformeduvs_1.inputs[4], 'hide_value'):
            animtex2transformeduvs_1.inputs[4].hide_value = False
        if hasattr(animtex2transformeduvs_1.inputs[4], 'name'):
            animtex2transformeduvs_1.inputs[4].name = 'ClockRandomOffset'
        if hasattr(animtex2transformeduvs_1.inputs[4], 'show_expanded'):
            animtex2transformeduvs_1.inputs[4].show_expanded = False
        if hasattr(animtex2transformeduvs_1.outputs[0], 'default_value'):
            animtex2transformeduvs_1.outputs[0].default_value = (0.0, 0.0, 0.0)
        if hasattr(animtex2transformeduvs_1.outputs[0], 'display_shape'):
            animtex2transformeduvs_1.outputs[0].display_shape = 'CIRCLE'
        if hasattr(animtex2transformeduvs_1.outputs[0], 'enabled'):
            animtex2transformeduvs_1.outputs[0].enabled = True
        if hasattr(animtex2transformeduvs_1.outputs[0], 'hide'):
            animtex2transformeduvs_1.outputs[0].hide = False
        if hasattr(animtex2transformeduvs_1.outputs[0], 'hide_value'):
            animtex2transformeduvs_1.outputs[0].hide_value = False
        if hasattr(animtex2transformeduvs_1.outputs[0], 'name'):
            animtex2transformeduvs_1.outputs[0].name = 'Value'
        if hasattr(animtex2transformeduvs_1.outputs[0], 'show_expanded'):
            animtex2transformeduvs_1.outputs[0].show_expanded = False

        animtex0transformeduvs_1 = node_tree1.nodes.new('ShaderNodeGroup')
        if hasattr(animtex0transformeduvs_1, 'node_tree'):
            animtex0transformeduvs_1.node_tree = bpy.data.node_groups.get('SW Aux - TransformUV')
        if hasattr(animtex0transformeduvs_1, 'color'):
            animtex0transformeduvs_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(animtex0transformeduvs_1, 'hide'):
            animtex0transformeduvs_1.hide = False
        if hasattr(animtex0transformeduvs_1, 'label'):
            animtex0transformeduvs_1.label = 'animTex0TransformedUVs'
        if hasattr(animtex0transformeduvs_1, 'location'):
            animtex0transformeduvs_1.location = (300.0, 328.53253173828125)
        if hasattr(animtex0transformeduvs_1, 'mute'):
            animtex0transformeduvs_1.mute = False
        if hasattr(animtex0transformeduvs_1, 'name'):
            animtex0transformeduvs_1.name = 'animTex0TransformedUVs'
        if hasattr(animtex0transformeduvs_1, 'status'):
            animtex0transformeduvs_1.status = False
        if hasattr(animtex0transformeduvs_1, 'use_custom_color'):
            animtex0transformeduvs_1.use_custom_color = False
        if hasattr(animtex0transformeduvs_1, 'width'):
            animtex0transformeduvs_1.width = 200.0
        if hasattr(animtex0transformeduvs_1.inputs[0], 'default_value'):
            animtex0transformeduvs_1.inputs[0].default_value = (0.0, 0.0, 0.0)
        if hasattr(animtex0transformeduvs_1.inputs[0], 'display_shape'):
            animtex0transformeduvs_1.inputs[0].display_shape = 'CIRCLE'
        if hasattr(animtex0transformeduvs_1.inputs[0], 'enabled'):
            animtex0transformeduvs_1.inputs[0].enabled = True
        if hasattr(animtex0transformeduvs_1.inputs[0], 'hide'):
            animtex0transformeduvs_1.inputs[0].hide = False
        if hasattr(animtex0transformeduvs_1.inputs[0], 'hide_value'):
            animtex0transformeduvs_1.inputs[0].hide_value = False
        if hasattr(animtex0transformeduvs_1.inputs[0], 'name'):
            animtex0transformeduvs_1.inputs[0].name = 'originalUVs'
        if hasattr(animtex0transformeduvs_1.inputs[0], 'show_expanded'):
            animtex0transformeduvs_1.inputs[0].show_expanded = False
        if hasattr(animtex0transformeduvs_1.inputs[1], 'default_value'):
            animtex0transformeduvs_1.inputs[1].default_value = (0.0, 0.0, 0.0)
        if hasattr(animtex0transformeduvs_1.inputs[1], 'display_shape'):
            animtex0transformeduvs_1.inputs[1].display_shape = 'CIRCLE'
        if hasattr(animtex0transformeduvs_1.inputs[1], 'enabled'):
            animtex0transformeduvs_1.inputs[1].enabled = True
        if hasattr(animtex0transformeduvs_1.inputs[1], 'hide'):
            animtex0transformeduvs_1.inputs[1].hide = False
        if hasattr(animtex0transformeduvs_1.inputs[1], 'hide_value'):
            animtex0transformeduvs_1.inputs[1].hide_value = False
        if hasattr(animtex0transformeduvs_1.inputs[1], 'name'):
            animtex0transformeduvs_1.inputs[1].name = 'animTexUVScrollSpeed'
        if hasattr(animtex0transformeduvs_1.inputs[1], 'show_expanded'):
            animtex0transformeduvs_1.inputs[1].show_expanded = False
        if hasattr(animtex0transformeduvs_1.inputs[2], 'default_value'):
            animtex0transformeduvs_1.inputs[2].default_value = (0.5, 0.5, 0.0)
        if hasattr(animtex0transformeduvs_1.inputs[2], 'display_shape'):
            animtex0transformeduvs_1.inputs[2].display_shape = 'CIRCLE'
        if hasattr(animtex0transformeduvs_1.inputs[2], 'enabled'):
            animtex0transformeduvs_1.inputs[2].enabled = True
        if hasattr(animtex0transformeduvs_1.inputs[2], 'hide'):
            animtex0transformeduvs_1.inputs[2].hide = False
        if hasattr(animtex0transformeduvs_1.inputs[2], 'hide_value'):
            animtex0transformeduvs_1.inputs[2].hide_value = False
        if hasattr(animtex0transformeduvs_1.inputs[2], 'name'):
            animtex0transformeduvs_1.inputs[2].name = 'animTexUVRotationPivot'
        if hasattr(animtex0transformeduvs_1.inputs[2], 'show_expanded'):
            animtex0transformeduvs_1.inputs[2].show_expanded = False
        if hasattr(animtex0transformeduvs_1.inputs[3], 'default_value'):
            animtex0transformeduvs_1.inputs[3].default_value = 0.0
        if hasattr(animtex0transformeduvs_1.inputs[3], 'display_shape'):
            animtex0transformeduvs_1.inputs[3].display_shape = 'CIRCLE'
        if hasattr(animtex0transformeduvs_1.inputs[3], 'enabled'):
            animtex0transformeduvs_1.inputs[3].enabled = True
        if hasattr(animtex0transformeduvs_1.inputs[3], 'hide'):
            animtex0transformeduvs_1.inputs[3].hide = False
        if hasattr(animtex0transformeduvs_1.inputs[3], 'hide_value'):
            animtex0transformeduvs_1.inputs[3].hide_value = False
        if hasattr(animtex0transformeduvs_1.inputs[3], 'name'):
            animtex0transformeduvs_1.inputs[3].name = 'animTexRotationSpeed'
        if hasattr(animtex0transformeduvs_1.inputs[3], 'show_expanded'):
            animtex0transformeduvs_1.inputs[3].show_expanded = False
        if hasattr(animtex0transformeduvs_1.inputs[4], 'default_value'):
            animtex0transformeduvs_1.inputs[4].default_value = 0.10000000149011612
        if hasattr(animtex0transformeduvs_1.inputs[4], 'display_shape'):
            animtex0transformeduvs_1.inputs[4].display_shape = 'CIRCLE'
        if hasattr(animtex0transformeduvs_1.inputs[4], 'enabled'):
            animtex0transformeduvs_1.inputs[4].enabled = True
        if hasattr(animtex0transformeduvs_1.inputs[4], 'hide'):
            animtex0transformeduvs_1.inputs[4].hide = False
        if hasattr(animtex0transformeduvs_1.inputs[4], 'hide_value'):
            animtex0transformeduvs_1.inputs[4].hide_value = False
        if hasattr(animtex0transformeduvs_1.inputs[4], 'name'):
            animtex0transformeduvs_1.inputs[4].name = 'ClockRandomOffset'
        if hasattr(animtex0transformeduvs_1.inputs[4], 'show_expanded'):
            animtex0transformeduvs_1.inputs[4].show_expanded = False
        if hasattr(animtex0transformeduvs_1.outputs[0], 'default_value'):
            animtex0transformeduvs_1.outputs[0].default_value = (0.0, 0.0, 0.0)
        if hasattr(animtex0transformeduvs_1.outputs[0], 'display_shape'):
            animtex0transformeduvs_1.outputs[0].display_shape = 'CIRCLE'
        if hasattr(animtex0transformeduvs_1.outputs[0], 'enabled'):
            animtex0transformeduvs_1.outputs[0].enabled = True
        if hasattr(animtex0transformeduvs_1.outputs[0], 'hide'):
            animtex0transformeduvs_1.outputs[0].hide = False
        if hasattr(animtex0transformeduvs_1.outputs[0], 'hide_value'):
            animtex0transformeduvs_1.outputs[0].hide_value = False
        if hasattr(animtex0transformeduvs_1.outputs[0], 'name'):
            animtex0transformeduvs_1.outputs[0].name = 'Value'
        if hasattr(animtex0transformeduvs_1.outputs[0], 'show_expanded'):
            animtex0transformeduvs_1.outputs[0].show_expanded = False

        # LINKS
        node_tree1.links.new(animtex0transformeduvs_1.outputs[0], group_output_1.inputs[0])
        node_tree1.links.new(animtex1transformeduvs_1.outputs[0], group_output_1.inputs[1])
        node_tree1.links.new(animtex2transformeduvs_1.outputs[0], group_output_1.inputs[2])
        node_tree1.links.new(group_input_1.outputs[9], math_1.inputs[0])
        node_tree1.links.new(reroute_009_1.outputs[0], animtex0transformeduvs_1.inputs[4])
        node_tree1.links.new(reroute_010_1.outputs[0], animtex1transformeduvs_1.inputs[4])
        node_tree1.links.new(reroute_011_1.outputs[0], animtex2transformeduvs_1.inputs[4])
        node_tree1.links.new(reroute_003_1.outputs[0], animtex0transformeduvs_1.inputs[1])
        node_tree1.links.new(reroute_006_1.outputs[0], animtex1transformeduvs_1.inputs[1])
        node_tree1.links.new(reroute_1.outputs[0], animtex2transformeduvs_1.inputs[1])
        node_tree1.links.new(animtex0uv_1.outputs[0], animtex0transformeduvs_1.inputs[0])
        node_tree1.links.new(animtex1uv_1.outputs[0], animtex1transformeduvs_1.inputs[0])
        node_tree1.links.new(animtex2uv_1.outputs[0], animtex2transformeduvs_1.inputs[0])
        node_tree1.links.new(reroute_005_1.outputs[0], animtex0transformeduvs_1.inputs[2])
        node_tree1.links.new(reroute_002_1.outputs[0], animtex0transformeduvs_1.inputs[3])
        node_tree1.links.new(reroute_007_1.outputs[0], animtex1transformeduvs_1.inputs[2])
        node_tree1.links.new(reroute_001_1.outputs[0], animtex1transformeduvs_1.inputs[3])
        node_tree1.links.new(reroute_008_1.outputs[0], animtex2transformeduvs_1.inputs[2])
        node_tree1.links.new(reroute_004_1.outputs[0], animtex2transformeduvs_1.inputs[3])
        node_tree1.links.new(group_input_1.outputs[6], reroute_1.inputs[0])
        node_tree1.links.new(group_input_1.outputs[5], reroute_001_1.inputs[0])
        node_tree1.links.new(group_input_1.outputs[2], reroute_002_1.inputs[0])
        node_tree1.links.new(group_input_1.outputs[0], reroute_003_1.inputs[0])
        node_tree1.links.new(group_input_1.outputs[8], reroute_004_1.inputs[0])
        node_tree1.links.new(group_input_1.outputs[1], reroute_005_1.inputs[0])
        node_tree1.links.new(group_input_1.outputs[3], reroute_006_1.inputs[0])
        node_tree1.links.new(group_input_1.outputs[4], reroute_007_1.inputs[0])
        node_tree1.links.new(group_input_1.outputs[7], reroute_008_1.inputs[0])
        node_tree1.links.new(math_1.outputs[0], reroute_009_1.inputs[0])
        node_tree1.links.new(math_1.outputs[0], reroute_010_1.inputs[0])
        node_tree1.links.new(math_1.outputs[0], reroute_011_1.inputs[0])

    sw_aux_transformalluv_0 = node_tree0.nodes.new('ShaderNodeGroup')
    if hasattr(sw_aux_transformalluv_0, 'node_tree'):
        sw_aux_transformalluv_0.node_tree = bpy.data.node_groups.get('SW Aux - TransformAllUV')
    if hasattr(sw_aux_transformalluv_0, 'color'):
        sw_aux_transformalluv_0.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(sw_aux_transformalluv_0, 'hide'):
        sw_aux_transformalluv_0.hide = False
    if hasattr(sw_aux_transformalluv_0, 'label'):
        sw_aux_transformalluv_0.label = 'SW Aux - TransformAllUV'
    if hasattr(sw_aux_transformalluv_0, 'location'):
        sw_aux_transformalluv_0.location = (-640.0, 300.0)
    if hasattr(sw_aux_transformalluv_0, 'mute'):
        sw_aux_transformalluv_0.mute = False
    if hasattr(sw_aux_transformalluv_0, 'name'):
        sw_aux_transformalluv_0.name = 'SW Aux - TransformAllUV'
    if hasattr(sw_aux_transformalluv_0, 'status'):
        sw_aux_transformalluv_0.status = False
    if hasattr(sw_aux_transformalluv_0, 'use_custom_color'):
        sw_aux_transformalluv_0.use_custom_color = False
    if hasattr(sw_aux_transformalluv_0, 'width'):
        sw_aux_transformalluv_0.width = 220.0
    if hasattr(sw_aux_transformalluv_0.inputs[0], 'default_value'):
        sw_aux_transformalluv_0.inputs[0].default_value = (0.0, 0.0, 0.0)
    if hasattr(sw_aux_transformalluv_0.inputs[0], 'display_shape'):
        sw_aux_transformalluv_0.inputs[0].display_shape = 'CIRCLE'
    if hasattr(sw_aux_transformalluv_0.inputs[0], 'enabled'):
        sw_aux_transformalluv_0.inputs[0].enabled = True
    if hasattr(sw_aux_transformalluv_0.inputs[0], 'hide'):
        sw_aux_transformalluv_0.inputs[0].hide = False
    if hasattr(sw_aux_transformalluv_0.inputs[0], 'hide_value'):
        sw_aux_transformalluv_0.inputs[0].hide_value = False
    if hasattr(sw_aux_transformalluv_0.inputs[0], 'name'):
        sw_aux_transformalluv_0.inputs[0].name = 'animTexUVScrollSpeed0'
    if hasattr(sw_aux_transformalluv_0.inputs[0], 'show_expanded'):
        sw_aux_transformalluv_0.inputs[0].show_expanded = False
    if hasattr(sw_aux_transformalluv_0.inputs[1], 'default_value'):
        sw_aux_transformalluv_0.inputs[1].default_value = (0.5, 0.5, 0.0)
    if hasattr(sw_aux_transformalluv_0.inputs[1], 'display_shape'):
        sw_aux_transformalluv_0.inputs[1].display_shape = 'CIRCLE'
    if hasattr(sw_aux_transformalluv_0.inputs[1], 'enabled'):
        sw_aux_transformalluv_0.inputs[1].enabled = True
    if hasattr(sw_aux_transformalluv_0.inputs[1], 'hide'):
        sw_aux_transformalluv_0.inputs[1].hide = False
    if hasattr(sw_aux_transformalluv_0.inputs[1], 'hide_value'):
        sw_aux_transformalluv_0.inputs[1].hide_value = False
    if hasattr(sw_aux_transformalluv_0.inputs[1], 'name'):
        sw_aux_transformalluv_0.inputs[1].name = 'animTexRotationPivot0'
    if hasattr(sw_aux_transformalluv_0.inputs[1], 'show_expanded'):
        sw_aux_transformalluv_0.inputs[1].show_expanded = False
    if hasattr(sw_aux_transformalluv_0.inputs[2], 'default_value'):
        sw_aux_transformalluv_0.inputs[2].default_value = 0.0
    if hasattr(sw_aux_transformalluv_0.inputs[2], 'display_shape'):
        sw_aux_transformalluv_0.inputs[2].display_shape = 'CIRCLE'
    if hasattr(sw_aux_transformalluv_0.inputs[2], 'enabled'):
        sw_aux_transformalluv_0.inputs[2].enabled = True
    if hasattr(sw_aux_transformalluv_0.inputs[2], 'hide'):
        sw_aux_transformalluv_0.inputs[2].hide = False
    if hasattr(sw_aux_transformalluv_0.inputs[2], 'hide_value'):
        sw_aux_transformalluv_0.inputs[2].hide_value = False
    if hasattr(sw_aux_transformalluv_0.inputs[2], 'name'):
        sw_aux_transformalluv_0.inputs[2].name = 'animTexRotationSpeed0'
    if hasattr(sw_aux_transformalluv_0.inputs[2], 'show_expanded'):
        sw_aux_transformalluv_0.inputs[2].show_expanded = False
    if hasattr(sw_aux_transformalluv_0.inputs[3], 'default_value'):
        sw_aux_transformalluv_0.inputs[3].default_value = (0.0, 0.0, 0.0)
    if hasattr(sw_aux_transformalluv_0.inputs[3], 'display_shape'):
        sw_aux_transformalluv_0.inputs[3].display_shape = 'CIRCLE'
    if hasattr(sw_aux_transformalluv_0.inputs[3], 'enabled'):
        sw_aux_transformalluv_0.inputs[3].enabled = True
    if hasattr(sw_aux_transformalluv_0.inputs[3], 'hide'):
        sw_aux_transformalluv_0.inputs[3].hide = False
    if hasattr(sw_aux_transformalluv_0.inputs[3], 'hide_value'):
        sw_aux_transformalluv_0.inputs[3].hide_value = False
    if hasattr(sw_aux_transformalluv_0.inputs[3], 'name'):
        sw_aux_transformalluv_0.inputs[3].name = 'animTexUVScrollSpeed1'
    if hasattr(sw_aux_transformalluv_0.inputs[3], 'show_expanded'):
        sw_aux_transformalluv_0.inputs[3].show_expanded = False
    if hasattr(sw_aux_transformalluv_0.inputs[4], 'default_value'):
        sw_aux_transformalluv_0.inputs[4].default_value = (0.5, 0.5, 0.0)
    if hasattr(sw_aux_transformalluv_0.inputs[4], 'display_shape'):
        sw_aux_transformalluv_0.inputs[4].display_shape = 'CIRCLE'
    if hasattr(sw_aux_transformalluv_0.inputs[4], 'enabled'):
        sw_aux_transformalluv_0.inputs[4].enabled = True
    if hasattr(sw_aux_transformalluv_0.inputs[4], 'hide'):
        sw_aux_transformalluv_0.inputs[4].hide = False
    if hasattr(sw_aux_transformalluv_0.inputs[4], 'hide_value'):
        sw_aux_transformalluv_0.inputs[4].hide_value = False
    if hasattr(sw_aux_transformalluv_0.inputs[4], 'name'):
        sw_aux_transformalluv_0.inputs[4].name = 'animTexRotationPivot1'
    if hasattr(sw_aux_transformalluv_0.inputs[4], 'show_expanded'):
        sw_aux_transformalluv_0.inputs[4].show_expanded = False
    if hasattr(sw_aux_transformalluv_0.inputs[5], 'default_value'):
        sw_aux_transformalluv_0.inputs[5].default_value = 0.0
    if hasattr(sw_aux_transformalluv_0.inputs[5], 'display_shape'):
        sw_aux_transformalluv_0.inputs[5].display_shape = 'CIRCLE'
    if hasattr(sw_aux_transformalluv_0.inputs[5], 'enabled'):
        sw_aux_transformalluv_0.inputs[5].enabled = True
    if hasattr(sw_aux_transformalluv_0.inputs[5], 'hide'):
        sw_aux_transformalluv_0.inputs[5].hide = False
    if hasattr(sw_aux_transformalluv_0.inputs[5], 'hide_value'):
        sw_aux_transformalluv_0.inputs[5].hide_value = False
    if hasattr(sw_aux_transformalluv_0.inputs[5], 'name'):
        sw_aux_transformalluv_0.inputs[5].name = 'animTexRotationSpeed1'
    if hasattr(sw_aux_transformalluv_0.inputs[5], 'show_expanded'):
        sw_aux_transformalluv_0.inputs[5].show_expanded = False
    if hasattr(sw_aux_transformalluv_0.inputs[6], 'default_value'):
        sw_aux_transformalluv_0.inputs[6].default_value = (0.0, 0.0, 0.0)
    if hasattr(sw_aux_transformalluv_0.inputs[6], 'display_shape'):
        sw_aux_transformalluv_0.inputs[6].display_shape = 'CIRCLE'
    if hasattr(sw_aux_transformalluv_0.inputs[6], 'enabled'):
        sw_aux_transformalluv_0.inputs[6].enabled = True
    if hasattr(sw_aux_transformalluv_0.inputs[6], 'hide'):
        sw_aux_transformalluv_0.inputs[6].hide = False
    if hasattr(sw_aux_transformalluv_0.inputs[6], 'hide_value'):
        sw_aux_transformalluv_0.inputs[6].hide_value = False
    if hasattr(sw_aux_transformalluv_0.inputs[6], 'name'):
        sw_aux_transformalluv_0.inputs[6].name = 'animTexUVScrollSpeed2'
    if hasattr(sw_aux_transformalluv_0.inputs[6], 'show_expanded'):
        sw_aux_transformalluv_0.inputs[6].show_expanded = False
    if hasattr(sw_aux_transformalluv_0.inputs[7], 'default_value'):
        sw_aux_transformalluv_0.inputs[7].default_value = (0.5, 0.5, 0.0)
    if hasattr(sw_aux_transformalluv_0.inputs[7], 'display_shape'):
        sw_aux_transformalluv_0.inputs[7].display_shape = 'CIRCLE'
    if hasattr(sw_aux_transformalluv_0.inputs[7], 'enabled'):
        sw_aux_transformalluv_0.inputs[7].enabled = True
    if hasattr(sw_aux_transformalluv_0.inputs[7], 'hide'):
        sw_aux_transformalluv_0.inputs[7].hide = False
    if hasattr(sw_aux_transformalluv_0.inputs[7], 'hide_value'):
        sw_aux_transformalluv_0.inputs[7].hide_value = False
    if hasattr(sw_aux_transformalluv_0.inputs[7], 'name'):
        sw_aux_transformalluv_0.inputs[7].name = 'animTexRotationPivot2'
    if hasattr(sw_aux_transformalluv_0.inputs[7], 'show_expanded'):
        sw_aux_transformalluv_0.inputs[7].show_expanded = False
    if hasattr(sw_aux_transformalluv_0.inputs[8], 'default_value'):
        sw_aux_transformalluv_0.inputs[8].default_value = 0.0
    if hasattr(sw_aux_transformalluv_0.inputs[8], 'display_shape'):
        sw_aux_transformalluv_0.inputs[8].display_shape = 'CIRCLE'
    if hasattr(sw_aux_transformalluv_0.inputs[8], 'enabled'):
        sw_aux_transformalluv_0.inputs[8].enabled = True
    if hasattr(sw_aux_transformalluv_0.inputs[8], 'hide'):
        sw_aux_transformalluv_0.inputs[8].hide = False
    if hasattr(sw_aux_transformalluv_0.inputs[8], 'hide_value'):
        sw_aux_transformalluv_0.inputs[8].hide_value = False
    if hasattr(sw_aux_transformalluv_0.inputs[8], 'name'):
        sw_aux_transformalluv_0.inputs[8].name = 'animTexRotationSpeed2'
    if hasattr(sw_aux_transformalluv_0.inputs[8], 'show_expanded'):
        sw_aux_transformalluv_0.inputs[8].show_expanded = False
    if hasattr(sw_aux_transformalluv_0.inputs[9], 'default_value'):
        sw_aux_transformalluv_0.inputs[9].default_value = 0.0
    if hasattr(sw_aux_transformalluv_0.inputs[9], 'display_shape'):
        sw_aux_transformalluv_0.inputs[9].display_shape = 'CIRCLE'
    if hasattr(sw_aux_transformalluv_0.inputs[9], 'enabled'):
        sw_aux_transformalluv_0.inputs[9].enabled = True
    if hasattr(sw_aux_transformalluv_0.inputs[9], 'hide'):
        sw_aux_transformalluv_0.inputs[9].hide = False
    if hasattr(sw_aux_transformalluv_0.inputs[9], 'hide_value'):
        sw_aux_transformalluv_0.inputs[9].hide_value = False
    if hasattr(sw_aux_transformalluv_0.inputs[9], 'name'):
        sw_aux_transformalluv_0.inputs[9].name = 'Animation Offset'
    if hasattr(sw_aux_transformalluv_0.inputs[9], 'show_expanded'):
        sw_aux_transformalluv_0.inputs[9].show_expanded = False
    if hasattr(sw_aux_transformalluv_0.outputs[0], 'default_value'):
        sw_aux_transformalluv_0.outputs[0].default_value = (0.0, 0.0, 0.0)
    if hasattr(sw_aux_transformalluv_0.outputs[0], 'display_shape'):
        sw_aux_transformalluv_0.outputs[0].display_shape = 'CIRCLE'
    if hasattr(sw_aux_transformalluv_0.outputs[0], 'enabled'):
        sw_aux_transformalluv_0.outputs[0].enabled = True
    if hasattr(sw_aux_transformalluv_0.outputs[0], 'hide'):
        sw_aux_transformalluv_0.outputs[0].hide = False
    if hasattr(sw_aux_transformalluv_0.outputs[0], 'hide_value'):
        sw_aux_transformalluv_0.outputs[0].hide_value = False
    if hasattr(sw_aux_transformalluv_0.outputs[0], 'name'):
        sw_aux_transformalluv_0.outputs[0].name = 'animTex0TransformedUVs'
    if hasattr(sw_aux_transformalluv_0.outputs[0], 'show_expanded'):
        sw_aux_transformalluv_0.outputs[0].show_expanded = False
    if hasattr(sw_aux_transformalluv_0.outputs[1], 'default_value'):
        sw_aux_transformalluv_0.outputs[1].default_value = (0.0, 0.0, 0.0)
    if hasattr(sw_aux_transformalluv_0.outputs[1], 'display_shape'):
        sw_aux_transformalluv_0.outputs[1].display_shape = 'CIRCLE'
    if hasattr(sw_aux_transformalluv_0.outputs[1], 'enabled'):
        sw_aux_transformalluv_0.outputs[1].enabled = True
    if hasattr(sw_aux_transformalluv_0.outputs[1], 'hide'):
        sw_aux_transformalluv_0.outputs[1].hide = False
    if hasattr(sw_aux_transformalluv_0.outputs[1], 'hide_value'):
        sw_aux_transformalluv_0.outputs[1].hide_value = False
    if hasattr(sw_aux_transformalluv_0.outputs[1], 'name'):
        sw_aux_transformalluv_0.outputs[1].name = 'animTex1TransformedUVs'
    if hasattr(sw_aux_transformalluv_0.outputs[1], 'show_expanded'):
        sw_aux_transformalluv_0.outputs[1].show_expanded = False
    if hasattr(sw_aux_transformalluv_0.outputs[2], 'default_value'):
        sw_aux_transformalluv_0.outputs[2].default_value = (0.0, 0.0, 0.0)
    if hasattr(sw_aux_transformalluv_0.outputs[2], 'display_shape'):
        sw_aux_transformalluv_0.outputs[2].display_shape = 'CIRCLE'
    if hasattr(sw_aux_transformalluv_0.outputs[2], 'enabled'):
        sw_aux_transformalluv_0.outputs[2].enabled = True
    if hasattr(sw_aux_transformalluv_0.outputs[2], 'hide'):
        sw_aux_transformalluv_0.outputs[2].hide = False
    if hasattr(sw_aux_transformalluv_0.outputs[2], 'hide_value'):
        sw_aux_transformalluv_0.outputs[2].hide_value = False
    if hasattr(sw_aux_transformalluv_0.outputs[2], 'name'):
        sw_aux_transformalluv_0.outputs[2].name = 'animTex2TransformedUVs'
    if hasattr(sw_aux_transformalluv_0.outputs[2], 'show_expanded'):
        sw_aux_transformalluv_0.outputs[2].show_expanded = False

    node_tree1 = bpy.data.node_groups.get('SWTOR - AnimatedUV Shader')
    if not node_tree1:
        node_tree1 = bpy.data.node_groups.new('SWTOR - AnimatedUV Shader', 'ShaderNodeTree')
        for node in node_tree1.nodes:
            node_tree1.nodes.remove(node)
        # INPUTS
        input = node_tree1.interface.new_socket(name='_d DiffuseMap Color', socket_type='NodeSocketColor', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = True
        if hasattr(input, 'name'):
            input.name = '_d DiffuseMap Color'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketColor'
        input = node_tree1.interface.new_socket(name='_d DiffuseMap Alpha', socket_type='NodeSocketFloat', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = 0.0
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 1.0
        if hasattr(input, 'min_value'):
            input.min_value = 0.0
        if hasattr(input, 'name'):
            input.name = '_d DiffuseMap Alpha'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketFloat'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='AnimatedTexture1 Color', socket_type='NodeSocketColor', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'name'):
            input.name = 'AnimatedTexture1 Color'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketColor'
        input = node_tree1.interface.new_socket(name='AnimatedTexture1 Alpha', socket_type='NodeSocketFloat', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = 0.0
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 1.0
        if hasattr(input, 'min_value'):
            input.min_value = 0.0
        if hasattr(input, 'name'):
            input.name = 'AnimatedTexture1 Alpha'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketFloat'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='AnimatedTexture2 Color', socket_type='NodeSocketColor', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'name'):
            input.name = 'AnimatedTexture2 Color'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketColor'
        input = node_tree1.interface.new_socket(name='AnimatedTexture2 Alpha', socket_type='NodeSocketFloat', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = 0.0
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 1.0
        if hasattr(input, 'min_value'):
            input.min_value = 0.0
        if hasattr(input, 'name'):
            input.name = 'AnimatedTexture2 Alpha'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketFloat'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='animTexTint0', socket_type='NodeSocketVector', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = (0.0, 0.0, 0.0)
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 3.4028234663852886e+38
        if hasattr(input, 'min_value'):
            input.min_value = -3.4028234663852886e+38
        if hasattr(input, 'name'):
            input.name = 'animTexTint0'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketVector'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='animTexTint1', socket_type='NodeSocketVector', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = (0.0, 0.0, 0.0)
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 3.4028234663852886e+38
        if hasattr(input, 'min_value'):
            input.min_value = -3.4028234663852886e+38
        if hasattr(input, 'name'):
            input.name = 'animTexTint1'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketVector'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='animTexTint2', socket_type='NodeSocketVector', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = (0.0, 0.0, 0.0)
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 3.4028234663852886e+38
        if hasattr(input, 'min_value'):
            input.min_value = -3.4028234663852886e+38
        if hasattr(input, 'name'):
            input.name = 'animTexTint2'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketVector'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='—— EXTRAS ——', socket_type='NodeSocketFloat', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = 0.0
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = True
        if hasattr(input, 'max_value'):
            input.max_value = 3.4028234663852886e+38
        if hasattr(input, 'min_value'):
            input.min_value = -3.4028234663852886e+38
        if hasattr(input, 'name'):
            input.name = '—— EXTRAS ——'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketFloat'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='Roughness Factor', socket_type='NodeSocketFloat', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = 0.0
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 1.0
        if hasattr(input, 'min_value'):
            input.min_value = 0.0
        if hasattr(input, 'name'):
            input.name = 'Roughness Factor'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketFloat'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='Emission Strength', socket_type='NodeSocketFloat', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = 1.0
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 1000000.0
        if hasattr(input, 'min_value'):
            input.min_value = 0.0
        if hasattr(input, 'name'):
            input.name = 'Emission Strength'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketFloat'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        input = node_tree1.interface.new_socket(name='Backface Culling Factor', socket_type='NodeSocketFloat', in_out='INPUT')
        if hasattr(input, 'attribute_domain'):
            input.attribute_domain = 'POINT'
        if hasattr(input, 'default_value'):
            input.default_value = 0.0
        if hasattr(input, 'force_non_field'):
            input.force_non_field = False
        if hasattr(input, 'hide_in_modifier'):
            input.hide_in_modifier = False
        if hasattr(input, 'hide_value'):
            input.hide_value = False
        if hasattr(input, 'max_value'):
            input.max_value = 1.0
        if hasattr(input, 'min_value'):
            input.min_value = 0.0
        if hasattr(input, 'name'):
            input.name = 'Backface Culling Factor'
        if hasattr(input, 'socket_type'):
            input.socket_type = 'NodeSocketFloat'
        if hasattr(input, 'subtype'):
            input.subtype = 'NONE'
        # OUTPUTS
        output = node_tree1.interface.new_socket(name='Shader', socket_type='NodeSocketShader', in_out='OUTPUT')
        if hasattr(output, 'attribute_domain'):
            output.attribute_domain = 'POINT'
        if hasattr(output, 'force_non_field'):
            output.force_non_field = False
        if hasattr(output, 'hide_in_modifier'):
            output.hide_in_modifier = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Shader'
        if hasattr(output, 'socket_type'):
            output.socket_type = 'NodeSocketShader'
        output = node_tree1.interface.new_socket(name='—— EXTRAS ——', socket_type='NodeSocketFloat', in_out='OUTPUT')
        if hasattr(output, 'attribute_domain'):
            output.attribute_domain = 'POINT'
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'force_non_field'):
            output.force_non_field = False
        if hasattr(output, 'hide_in_modifier'):
            output.hide_in_modifier = False
        if hasattr(output, 'hide_value'):
            output.hide_value = True
        if hasattr(output, 'max_value'):
            output.max_value = 0.0
        if hasattr(output, 'min_value'):
            output.min_value = 0.0
        if hasattr(output, 'name'):
            output.name = '—— EXTRAS ——'
        if hasattr(output, 'socket_type'):
            output.socket_type = 'NodeSocketFloat'
        if hasattr(output, 'subtype'):
            output.subtype = 'NONE'
        output = node_tree1.interface.new_socket(name='Diffuse Color AUX', socket_type='NodeSocketColor', in_out='OUTPUT')
        if hasattr(output, 'attribute_domain'):
            output.attribute_domain = 'POINT'
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(output, 'force_non_field'):
            output.force_non_field = False
        if hasattr(output, 'hide_in_modifier'):
            output.hide_in_modifier = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Diffuse Color AUX'
        if hasattr(output, 'socket_type'):
            output.socket_type = 'NodeSocketColor'
        output = node_tree1.interface.new_socket(name='Alpha AUX', socket_type='NodeSocketFloat', in_out='OUTPUT')
        if hasattr(output, 'attribute_domain'):
            output.attribute_domain = 'POINT'
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'force_non_field'):
            output.force_non_field = False
        if hasattr(output, 'hide_in_modifier'):
            output.hide_in_modifier = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'max_value'):
            output.max_value = 3.4028234663852886e+38
        if hasattr(output, 'min_value'):
            output.min_value = -3.4028234663852886e+38
        if hasattr(output, 'name'):
            output.name = 'Alpha AUX'
        if hasattr(output, 'socket_type'):
            output.socket_type = 'NodeSocketFloat'
        if hasattr(output, 'subtype'):
            output.subtype = 'NONE'
        # NODES
        zg_swtor_tools_identifier_1 = node_tree1.nodes.new('NodeFrame')
        if hasattr(zg_swtor_tools_identifier_1, 'color'):
            zg_swtor_tools_identifier_1.color = (0.6080166697502136, 0.0, 0.0)
        if hasattr(zg_swtor_tools_identifier_1, 'hide'):
            zg_swtor_tools_identifier_1.hide = False
        if hasattr(zg_swtor_tools_identifier_1, 'label'):
            zg_swtor_tools_identifier_1.label = 'ZG SWTOR TOOLS IDENTIFIER'
        if hasattr(zg_swtor_tools_identifier_1, 'label_size'):
            zg_swtor_tools_identifier_1.label_size = 20
        if hasattr(zg_swtor_tools_identifier_1, 'location'):
            zg_swtor_tools_identifier_1.location = (1150.0, 750.0)
        if hasattr(zg_swtor_tools_identifier_1, 'mute'):
            zg_swtor_tools_identifier_1.mute = False
        if hasattr(zg_swtor_tools_identifier_1, 'name'):
            zg_swtor_tools_identifier_1.name = 'ZG SWTOR TOOLS IDENTIFIER'
        if hasattr(zg_swtor_tools_identifier_1, 'shrink'):
            zg_swtor_tools_identifier_1.shrink = True
        if hasattr(zg_swtor_tools_identifier_1, 'status'):
            zg_swtor_tools_identifier_1.status = False
        if hasattr(zg_swtor_tools_identifier_1, 'use_custom_color'):
            zg_swtor_tools_identifier_1.use_custom_color = True
        if hasattr(zg_swtor_tools_identifier_1, 'width'):
            zg_swtor_tools_identifier_1.width = 388.4208984375

        zg_swtor_animateduv_shader_1 = node_tree1.nodes.new('NodeFrame')
        if hasattr(zg_swtor_animateduv_shader_1, 'parent'):
            zg_swtor_animateduv_shader_1.parent = node_tree1.nodes.get('ZG SWTOR TOOLS IDENTIFIER')
        if hasattr(zg_swtor_animateduv_shader_1, 'color'):
            zg_swtor_animateduv_shader_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(zg_swtor_animateduv_shader_1, 'hide'):
            zg_swtor_animateduv_shader_1.hide = False
        if hasattr(zg_swtor_animateduv_shader_1, 'label'):
            zg_swtor_animateduv_shader_1.label = 'ZG SWTOR - AnimatedUV Shader'
        if hasattr(zg_swtor_animateduv_shader_1, 'label_size'):
            zg_swtor_animateduv_shader_1.label_size = 20
        if hasattr(zg_swtor_animateduv_shader_1, 'location'):
            zg_swtor_animateduv_shader_1.location = (49.1768798828125, -8.0)
        if hasattr(zg_swtor_animateduv_shader_1, 'mute'):
            zg_swtor_animateduv_shader_1.mute = False
        if hasattr(zg_swtor_animateduv_shader_1, 'name'):
            zg_swtor_animateduv_shader_1.name = 'ZG SWTOR - AnimatedUV Shader'
        if hasattr(zg_swtor_animateduv_shader_1, 'shrink'):
            zg_swtor_animateduv_shader_1.shrink = False
        if hasattr(zg_swtor_animateduv_shader_1, 'status'):
            zg_swtor_animateduv_shader_1.status = False
        if hasattr(zg_swtor_animateduv_shader_1, 'use_custom_color'):
            zg_swtor_animateduv_shader_1.use_custom_color = False
        if hasattr(zg_swtor_animateduv_shader_1, 'width'):
            zg_swtor_animateduv_shader_1.width = 328.4208984375

        shader_design_by_c_3po_captnkoda_1 = node_tree1.nodes.new('NodeFrame')
        if hasattr(shader_design_by_c_3po_captnkoda_1, 'color'):
            shader_design_by_c_3po_captnkoda_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(shader_design_by_c_3po_captnkoda_1, 'hide'):
            shader_design_by_c_3po_captnkoda_1.hide = False
        if hasattr(shader_design_by_c_3po_captnkoda_1, 'label'):
            shader_design_by_c_3po_captnkoda_1.label = 'Shader design by C-3PO & CaptnKoda'
        if hasattr(shader_design_by_c_3po_captnkoda_1, 'label_size'):
            shader_design_by_c_3po_captnkoda_1.label_size = 20
        if hasattr(shader_design_by_c_3po_captnkoda_1, 'location'):
            shader_design_by_c_3po_captnkoda_1.location = (1199.0, 643.0)
        if hasattr(shader_design_by_c_3po_captnkoda_1, 'mute'):
            shader_design_by_c_3po_captnkoda_1.mute = False
        if hasattr(shader_design_by_c_3po_captnkoda_1, 'name'):
            shader_design_by_c_3po_captnkoda_1.name = 'Shader design by C-3PO & CaptnKoda'
        if hasattr(shader_design_by_c_3po_captnkoda_1, 'shrink'):
            shader_design_by_c_3po_captnkoda_1.shrink = True
        if hasattr(shader_design_by_c_3po_captnkoda_1, 'status'):
            shader_design_by_c_3po_captnkoda_1.status = False
        if hasattr(shader_design_by_c_3po_captnkoda_1, 'use_custom_color'):
            shader_design_by_c_3po_captnkoda_1.use_custom_color = False
        if hasattr(shader_design_by_c_3po_captnkoda_1, 'width'):
            shader_design_by_c_3po_captnkoda_1.width = 388.0234375

        vector_math_005_1 = node_tree1.nodes.new('ShaderNodeVectorMath')
        if hasattr(vector_math_005_1, 'color'):
            vector_math_005_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(vector_math_005_1, 'hide'):
            vector_math_005_1.hide = False
        if hasattr(vector_math_005_1, 'location'):
            vector_math_005_1.location = (-340.0, 160.0)
        if hasattr(vector_math_005_1, 'mute'):
            vector_math_005_1.mute = False
        if hasattr(vector_math_005_1, 'name'):
            vector_math_005_1.name = 'Vector Math.005'
        if hasattr(vector_math_005_1, 'operation'):
            vector_math_005_1.operation = 'MULTIPLY'
        if hasattr(vector_math_005_1, 'status'):
            vector_math_005_1.status = False
        if hasattr(vector_math_005_1, 'use_custom_color'):
            vector_math_005_1.use_custom_color = False
        if hasattr(vector_math_005_1, 'width'):
            vector_math_005_1.width = 100.0
        input_ = next((input_ for input_ in vector_math_005_1.inputs if input_.identifier=='Vector'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_005_1.inputs if input_.identifier=='Vector_001'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_005_1.inputs if input_.identifier=='Vector_002'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_005_1.inputs if input_.identifier=='Scale'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 1.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Scale'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        output = next((output for output in vector_math_005_1.outputs if output.identifier=='Vector'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0)
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Vector'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False
        output = next((output for output in vector_math_005_1.outputs if output.identifier=='Value'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = False
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Value'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        vector_math_006_1 = node_tree1.nodes.new('ShaderNodeVectorMath')
        if hasattr(vector_math_006_1, 'color'):
            vector_math_006_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(vector_math_006_1, 'hide'):
            vector_math_006_1.hide = False
        if hasattr(vector_math_006_1, 'location'):
            vector_math_006_1.location = (180.0, 219.40548706054688)
        if hasattr(vector_math_006_1, 'mute'):
            vector_math_006_1.mute = False
        if hasattr(vector_math_006_1, 'name'):
            vector_math_006_1.name = 'Vector Math.006'
        if hasattr(vector_math_006_1, 'operation'):
            vector_math_006_1.operation = 'DOT_PRODUCT'
        if hasattr(vector_math_006_1, 'status'):
            vector_math_006_1.status = False
        if hasattr(vector_math_006_1, 'use_custom_color'):
            vector_math_006_1.use_custom_color = False
        if hasattr(vector_math_006_1, 'width'):
            vector_math_006_1.width = 140.0
        input_ = next((input_ for input_ in vector_math_006_1.inputs if input_.identifier=='Vector'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_006_1.inputs if input_.identifier=='Vector_001'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.33333298563957214, 0.33333298563957214, 0.33333298563957214)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_006_1.inputs if input_.identifier=='Vector_002'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_006_1.inputs if input_.identifier=='Scale'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 1.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Scale'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        output = next((output for output in vector_math_006_1.outputs if output.identifier=='Vector'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0)
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = False
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Vector'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False
        output = next((output for output in vector_math_006_1.outputs if output.identifier=='Value'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Value'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        math_1 = node_tree1.nodes.new('ShaderNodeMath')
        if hasattr(math_1, 'color'):
            math_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(math_1, 'hide'):
            math_1.hide = False
        if hasattr(math_1, 'location'):
            math_1.location = (360.0, 219.40548706054688)
        if hasattr(math_1, 'mute'):
            math_1.mute = False
        if hasattr(math_1, 'name'):
            math_1.name = 'Math'
        if hasattr(math_1, 'operation'):
            math_1.operation = 'MULTIPLY'
        if hasattr(math_1, 'status'):
            math_1.status = False
        if hasattr(math_1, 'use_clamp'):
            math_1.use_clamp = True
        if hasattr(math_1, 'use_custom_color'):
            math_1.use_custom_color = False
        if hasattr(math_1, 'width'):
            math_1.width = 140.0
        input_ = next((input_ for input_ in math_1.inputs if input_.identifier=='Value'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.5
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Value'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in math_1.inputs if input_.identifier=='Value_001'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 1.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Value'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in math_1.inputs if input_.identifier=='Value_002'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.5
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Value'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        output = next((output for output in math_1.outputs if output.identifier=='Value'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Value'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        group_output_1 = node_tree1.nodes.new('NodeGroupOutput')
        if hasattr(group_output_1, 'color'):
            group_output_1.color = (0.0, 0.0, 0.3999914526939392)
        if hasattr(group_output_1, 'hide'):
            group_output_1.hide = False
        if hasattr(group_output_1, 'is_active_output'):
            group_output_1.is_active_output = True
        if hasattr(group_output_1, 'location'):
            group_output_1.location = (1320.0, 259.4054870605469)
        if hasattr(group_output_1, 'mute'):
            group_output_1.mute = False
        if hasattr(group_output_1, 'name'):
            group_output_1.name = 'Group Output'
        if hasattr(group_output_1, 'status'):
            group_output_1.status = False
        if hasattr(group_output_1, 'use_custom_color'):
            group_output_1.use_custom_color = True
        if hasattr(group_output_1, 'width'):
            group_output_1.width = 140.0
        if hasattr(group_output_1.inputs[1], 'default_value'):
            group_output_1.inputs[1].default_value = 0.0
        if hasattr(group_output_1.inputs[1], 'display_shape'):
            group_output_1.inputs[1].display_shape = 'CIRCLE'
        if hasattr(group_output_1.inputs[1], 'enabled'):
            group_output_1.inputs[1].enabled = True
        if hasattr(group_output_1.inputs[1], 'hide'):
            group_output_1.inputs[1].hide = True
        if hasattr(group_output_1.inputs[1], 'hide_value'):
            group_output_1.inputs[1].hide_value = True
        if hasattr(group_output_1.inputs[1], 'name'):
            group_output_1.inputs[1].name = '—— EXTRAS ——'
        if hasattr(group_output_1.inputs[1], 'show_expanded'):
            group_output_1.inputs[1].show_expanded = False
        if hasattr(group_output_1.inputs[2], 'default_value'):
            group_output_1.inputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_output_1.inputs[2], 'display_shape'):
            group_output_1.inputs[2].display_shape = 'CIRCLE'
        if hasattr(group_output_1.inputs[2], 'enabled'):
            group_output_1.inputs[2].enabled = True
        if hasattr(group_output_1.inputs[2], 'hide'):
            group_output_1.inputs[2].hide = False
        if hasattr(group_output_1.inputs[2], 'hide_value'):
            group_output_1.inputs[2].hide_value = False
        if hasattr(group_output_1.inputs[2], 'name'):
            group_output_1.inputs[2].name = 'Diffuse Color AUX'
        if hasattr(group_output_1.inputs[2], 'show_expanded'):
            group_output_1.inputs[2].show_expanded = False
        if hasattr(group_output_1.inputs[3], 'default_value'):
            group_output_1.inputs[3].default_value = 0.0
        if hasattr(group_output_1.inputs[3], 'display_shape'):
            group_output_1.inputs[3].display_shape = 'CIRCLE'
        if hasattr(group_output_1.inputs[3], 'enabled'):
            group_output_1.inputs[3].enabled = True
        if hasattr(group_output_1.inputs[3], 'hide'):
            group_output_1.inputs[3].hide = False
        if hasattr(group_output_1.inputs[3], 'hide_value'):
            group_output_1.inputs[3].hide_value = False
        if hasattr(group_output_1.inputs[3], 'name'):
            group_output_1.inputs[3].name = 'Alpha AUX'
        if hasattr(group_output_1.inputs[3], 'show_expanded'):
            group_output_1.inputs[3].show_expanded = False

        node_tree2 = bpy.data.node_groups.get('SW Aux - Backface Culling')
        if not node_tree2:
            node_tree2 = bpy.data.node_groups.new('SW Aux - Backface Culling', 'ShaderNodeTree')
            for node in node_tree2.nodes:
                node_tree2.nodes.remove(node)
            # INPUTS
            input = node_tree2.interface.new_socket(name='Principled', socket_type='NodeSocketShader', in_out='INPUT')
            if hasattr(input, 'attribute_domain'):
                input.attribute_domain = 'POINT'
            if hasattr(input, 'force_non_field'):
                input.force_non_field = False
            if hasattr(input, 'hide_in_modifier'):
                input.hide_in_modifier = False
            if hasattr(input, 'hide_value'):
                input.hide_value = False
            if hasattr(input, 'name'):
                input.name = 'Principled'
            if hasattr(input, 'socket_type'):
                input.socket_type = 'NodeSocketShader'
            input = node_tree2.interface.new_socket(name='Fac', socket_type='NodeSocketFloat', in_out='INPUT')
            if hasattr(input, 'attribute_domain'):
                input.attribute_domain = 'POINT'
            if hasattr(input, 'default_value'):
                input.default_value = 1.0
            if hasattr(input, 'force_non_field'):
                input.force_non_field = False
            if hasattr(input, 'hide_in_modifier'):
                input.hide_in_modifier = False
            if hasattr(input, 'hide_value'):
                input.hide_value = False
            if hasattr(input, 'max_value'):
                input.max_value = 1.0
            if hasattr(input, 'min_value'):
                input.min_value = 0.0
            if hasattr(input, 'name'):
                input.name = 'Fac'
            if hasattr(input, 'subtype'):
                input.subtype = 'FACTOR'
            # OUTPUTS
            output = node_tree2.interface.new_socket(name='Shader', socket_type='NodeSocketShader', in_out='OUTPUT')
            if hasattr(output, 'attribute_domain'):
                output.attribute_domain = 'POINT'
            if hasattr(output, 'force_non_field'):
                output.force_non_field = False
            if hasattr(output, 'hide_in_modifier'):
                output.hide_in_modifier = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Shader'
            if hasattr(output, 'socket_type'):
                output.socket_type = 'NodeSocketShader'
            # NODES
            invert_2 = node_tree2.nodes.new('ShaderNodeInvert')
            if hasattr(invert_2, 'color'):
                invert_2.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
            if hasattr(invert_2, 'hide'):
                invert_2.hide = False
            if hasattr(invert_2, 'location'):
                invert_2.location = (-380.0, -60.0)
            if hasattr(invert_2, 'mute'):
                invert_2.mute = False
            if hasattr(invert_2, 'name'):
                invert_2.name = 'Invert'
            if hasattr(invert_2, 'status'):
                invert_2.status = False
            if hasattr(invert_2, 'use_custom_color'):
                invert_2.use_custom_color = False
            if hasattr(invert_2, 'width'):
                invert_2.width = 140.0
            input_ = next((input_ for input_ in invert_2.inputs if input_.identifier=='Fac'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 1.0
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = True
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Fac'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in invert_2.inputs if input_.identifier=='Color'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = (0.0, 0.0, 0.0, 1.0)
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
            output = next((output for output in invert_2.outputs if output.identifier=='Color'), None)
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

            geometry_2 = node_tree2.nodes.new('ShaderNodeNewGeometry')
            if hasattr(geometry_2, 'color'):
                geometry_2.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
            if hasattr(geometry_2, 'hide'):
                geometry_2.hide = False
            if hasattr(geometry_2, 'location'):
                geometry_2.location = (-620.0, 200.0)
            if hasattr(geometry_2, 'mute'):
                geometry_2.mute = False
            if hasattr(geometry_2, 'name'):
                geometry_2.name = 'Geometry'
            if hasattr(geometry_2, 'status'):
                geometry_2.status = False
            if hasattr(geometry_2, 'use_custom_color'):
                geometry_2.use_custom_color = False
            if hasattr(geometry_2, 'width'):
                geometry_2.width = 140.0
            output = next((output for output in geometry_2.outputs if output.identifier=='Position'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = (0.0, 0.0, 0.0)
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Position'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False
            output = next((output for output in geometry_2.outputs if output.identifier=='Normal'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = (0.0, 0.0, 0.0)
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Normal'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False
            output = next((output for output in geometry_2.outputs if output.identifier=='Tangent'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = (0.0, 0.0, 0.0)
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Tangent'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False
            output = next((output for output in geometry_2.outputs if output.identifier=='True Normal'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = (0.0, 0.0, 0.0)
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'True Normal'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False
            output = next((output for output in geometry_2.outputs if output.identifier=='Incoming'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = (0.0, 0.0, 0.0)
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Incoming'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False
            output = next((output for output in geometry_2.outputs if output.identifier=='Parametric'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = (0.0, 0.0, 0.0)
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Parametric'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False
            output = next((output for output in geometry_2.outputs if output.identifier=='Backfacing'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = 0.0
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Backfacing'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False
            output = next((output for output in geometry_2.outputs if output.identifier=='Pointiness'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = 0.0
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Pointiness'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False
            output = next((output for output in geometry_2.outputs if output.identifier=='Random Per Island'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = 0.0
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Random Per Island'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False

            invert_001_2 = node_tree2.nodes.new('ShaderNodeInvert')
            if hasattr(invert_001_2, 'color'):
                invert_001_2.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
            if hasattr(invert_001_2, 'hide'):
                invert_001_2.hide = False
            if hasattr(invert_001_2, 'location'):
                invert_001_2.location = (-380.0, 80.0)
            if hasattr(invert_001_2, 'mute'):
                invert_001_2.mute = False
            if hasattr(invert_001_2, 'name'):
                invert_001_2.name = 'Invert.001'
            if hasattr(invert_001_2, 'status'):
                invert_001_2.status = False
            if hasattr(invert_001_2, 'use_custom_color'):
                invert_001_2.use_custom_color = False
            if hasattr(invert_001_2, 'width'):
                invert_001_2.width = 140.0
            input_ = next((input_ for input_ in invert_001_2.inputs if input_.identifier=='Fac'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 1.0
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = True
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Fac'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in invert_001_2.inputs if input_.identifier=='Color'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = (0.0, 0.0, 0.0, 1.0)
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
            output = next((output for output in invert_001_2.outputs if output.identifier=='Color'), None)
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

            math_2 = node_tree2.nodes.new('ShaderNodeMath')
            if hasattr(math_2, 'color'):
                math_2.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
            if hasattr(math_2, 'hide'):
                math_2.hide = False
            if hasattr(math_2, 'location'):
                math_2.location = (80.0, 100.0)
            if hasattr(math_2, 'mute'):
                math_2.mute = False
            if hasattr(math_2, 'name'):
                math_2.name = 'Math'
            if hasattr(math_2, 'operation'):
                math_2.operation = 'ADD'
            if hasattr(math_2, 'status'):
                math_2.status = False
            if hasattr(math_2, 'use_clamp'):
                math_2.use_clamp = False
            if hasattr(math_2, 'use_custom_color'):
                math_2.use_custom_color = False
            if hasattr(math_2, 'width'):
                math_2.width = 140.0
            input_ = next((input_ for input_ in math_2.inputs if input_.identifier=='Value'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 0.5
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = True
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Value'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in math_2.inputs if input_.identifier=='Value_001'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 0.5
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = True
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Value'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            input_ = next((input_ for input_ in math_2.inputs if input_.identifier=='Value_002'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 0.5
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = False
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Value'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False
            output = next((output for output in math_2.outputs if output.identifier=='Value'), None)
            if output:
                if hasattr(output, 'default_value'):
                    output.default_value = 0.0
                if hasattr(output, 'display_shape'):
                    output.display_shape = 'CIRCLE'
                if hasattr(output, 'enabled'):
                    output.enabled = True
                if hasattr(output, 'hide'):
                    output.hide = False
                if hasattr(output, 'hide_value'):
                    output.hide_value = False
                if hasattr(output, 'name'):
                    output.name = 'Value'
                if hasattr(output, 'show_expanded'):
                    output.show_expanded = False

            transparent_bsdf_2 = node_tree2.nodes.new('ShaderNodeBsdfTransparent')
            if hasattr(transparent_bsdf_2, 'color'):
                transparent_bsdf_2.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
            if hasattr(transparent_bsdf_2, 'hide'):
                transparent_bsdf_2.hide = False
            if hasattr(transparent_bsdf_2, 'location'):
                transparent_bsdf_2.location = (80.0, -100.0)
            if hasattr(transparent_bsdf_2, 'mute'):
                transparent_bsdf_2.mute = False
            if hasattr(transparent_bsdf_2, 'name'):
                transparent_bsdf_2.name = 'Transparent BSDF'
            if hasattr(transparent_bsdf_2, 'status'):
                transparent_bsdf_2.status = False
            if hasattr(transparent_bsdf_2, 'use_custom_color'):
                transparent_bsdf_2.use_custom_color = False
            if hasattr(transparent_bsdf_2, 'width'):
                transparent_bsdf_2.width = 140.0
            input_ = next((input_ for input_ in transparent_bsdf_2.inputs if input_.identifier=='Color'), None)
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
            input_ = next((input_ for input_ in transparent_bsdf_2.inputs if input_.identifier=='Weight'), None)
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

            mix_shader_2 = node_tree2.nodes.new('ShaderNodeMixShader')
            if hasattr(mix_shader_2, 'color'):
                mix_shader_2.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
            if hasattr(mix_shader_2, 'hide'):
                mix_shader_2.hide = False
            if hasattr(mix_shader_2, 'location'):
                mix_shader_2.location = (380.0, -120.0)
            if hasattr(mix_shader_2, 'mute'):
                mix_shader_2.mute = False
            if hasattr(mix_shader_2, 'name'):
                mix_shader_2.name = 'Mix Shader'
            if hasattr(mix_shader_2, 'status'):
                mix_shader_2.status = False
            if hasattr(mix_shader_2, 'use_custom_color'):
                mix_shader_2.use_custom_color = False
            if hasattr(mix_shader_2, 'width'):
                mix_shader_2.width = 140.0
            input_ = next((input_ for input_ in mix_shader_2.inputs if input_.identifier=='Fac'), None)
            if input_:
                if hasattr(input_, 'default_value'):
                    input_.default_value = 1.0
                if hasattr(input_, 'display_shape'):
                    input_.display_shape = 'CIRCLE'
                if hasattr(input_, 'enabled'):
                    input_.enabled = True
                if hasattr(input_, 'hide'):
                    input_.hide = False
                if hasattr(input_, 'hide_value'):
                    input_.hide_value = False
                if hasattr(input_, 'name'):
                    input_.name = 'Fac'
                if hasattr(input_, 'show_expanded'):
                    input_.show_expanded = False

            group_output_2 = node_tree2.nodes.new('NodeGroupOutput')
            if hasattr(group_output_2, 'color'):
                group_output_2.color = (0.0, 0.0, 0.3999914526939392)
            if hasattr(group_output_2, 'hide'):
                group_output_2.hide = False
            if hasattr(group_output_2, 'is_active_output'):
                group_output_2.is_active_output = True
            if hasattr(group_output_2, 'location'):
                group_output_2.location = (620.0, -0.0)
            if hasattr(group_output_2, 'mute'):
                group_output_2.mute = False
            if hasattr(group_output_2, 'name'):
                group_output_2.name = 'Group Output'
            if hasattr(group_output_2, 'status'):
                group_output_2.status = False
            if hasattr(group_output_2, 'use_custom_color'):
                group_output_2.use_custom_color = True
            if hasattr(group_output_2, 'width'):
                group_output_2.width = 140.0

            group_input_2 = node_tree2.nodes.new('NodeGroupInput')
            if hasattr(group_input_2, 'color'):
                group_input_2.color = (0.3999914526939392, 0.0, 0.0)
            if hasattr(group_input_2, 'hide'):
                group_input_2.hide = False
            if hasattr(group_input_2, 'location'):
                group_input_2.location = (-620.0, -180.0)
            if hasattr(group_input_2, 'mute'):
                group_input_2.mute = False
            if hasattr(group_input_2, 'name'):
                group_input_2.name = 'Group Input'
            if hasattr(group_input_2, 'status'):
                group_input_2.status = False
            if hasattr(group_input_2, 'use_custom_color'):
                group_input_2.use_custom_color = True
            if hasattr(group_input_2, 'width'):
                group_input_2.width = 140.0
            if hasattr(group_input_2.outputs[1], 'default_value'):
                group_input_2.outputs[1].default_value = 1.0
            if hasattr(group_input_2.outputs[1], 'display_shape'):
                group_input_2.outputs[1].display_shape = 'CIRCLE'
            if hasattr(group_input_2.outputs[1], 'enabled'):
                group_input_2.outputs[1].enabled = True
            if hasattr(group_input_2.outputs[1], 'hide'):
                group_input_2.outputs[1].hide = False
            if hasattr(group_input_2.outputs[1], 'hide_value'):
                group_input_2.outputs[1].hide_value = False
            if hasattr(group_input_2.outputs[1], 'name'):
                group_input_2.outputs[1].name = 'Fac'
            if hasattr(group_input_2.outputs[1], 'show_expanded'):
                group_input_2.outputs[1].show_expanded = False

            # LINKS
            node_tree2.links.new(group_input_2.outputs[0], mix_shader_2.inputs[2])
            node_tree2.links.new(mix_shader_2.outputs[0], group_output_2.inputs[0])
            node_tree2.links.new(geometry_2.outputs[6], invert_001_2.inputs[1])
            node_tree2.links.new(transparent_bsdf_2.outputs[0], mix_shader_2.inputs[1])
            node_tree2.links.new(invert_001_2.outputs[0], math_2.inputs[0])
            node_tree2.links.new(invert_2.outputs[0], math_2.inputs[1])
            node_tree2.links.new(math_2.outputs[0], mix_shader_2.inputs[0])
            node_tree2.links.new(group_input_2.outputs[1], invert_2.inputs[1])

        sw_aux_backface_culling_1 = node_tree1.nodes.new('ShaderNodeGroup')
        if hasattr(sw_aux_backface_culling_1, 'node_tree'):
            sw_aux_backface_culling_1.node_tree = bpy.data.node_groups.get('SW Aux - Backface Culling')
        if hasattr(sw_aux_backface_culling_1, 'color'):
            sw_aux_backface_culling_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(sw_aux_backface_culling_1, 'hide'):
            sw_aux_backface_culling_1.hide = False
        if hasattr(sw_aux_backface_culling_1, 'label'):
            sw_aux_backface_culling_1.label = 'SW Aux - Backface Culling'
        if hasattr(sw_aux_backface_culling_1, 'location'):
            sw_aux_backface_culling_1.location = (1000.0, 484.4059143066406)
        if hasattr(sw_aux_backface_culling_1, 'mute'):
            sw_aux_backface_culling_1.mute = False
        if hasattr(sw_aux_backface_culling_1, 'name'):
            sw_aux_backface_culling_1.name = 'SW Aux - Backface Culling'
        if hasattr(sw_aux_backface_culling_1, 'status'):
            sw_aux_backface_culling_1.status = False
        if hasattr(sw_aux_backface_culling_1, 'use_custom_color'):
            sw_aux_backface_culling_1.use_custom_color = False
        if hasattr(sw_aux_backface_culling_1, 'width'):
            sw_aux_backface_culling_1.width = 250.0
        if hasattr(sw_aux_backface_culling_1.inputs[1], 'default_value'):
            sw_aux_backface_culling_1.inputs[1].default_value = 1.0
        if hasattr(sw_aux_backface_culling_1.inputs[1], 'display_shape'):
            sw_aux_backface_culling_1.inputs[1].display_shape = 'CIRCLE'
        if hasattr(sw_aux_backface_culling_1.inputs[1], 'enabled'):
            sw_aux_backface_culling_1.inputs[1].enabled = True
        if hasattr(sw_aux_backface_culling_1.inputs[1], 'hide'):
            sw_aux_backface_culling_1.inputs[1].hide = False
        if hasattr(sw_aux_backface_culling_1.inputs[1], 'hide_value'):
            sw_aux_backface_culling_1.inputs[1].hide_value = False
        if hasattr(sw_aux_backface_culling_1.inputs[1], 'name'):
            sw_aux_backface_culling_1.inputs[1].name = 'Fac'
        if hasattr(sw_aux_backface_culling_1.inputs[1], 'show_expanded'):
            sw_aux_backface_culling_1.inputs[1].show_expanded = False

        mix_1 = node_tree1.nodes.new('ShaderNodeMix')
        if hasattr(mix_1, 'blend_type'):
            mix_1.blend_type = 'MIX'
        if hasattr(mix_1, 'clamp_factor'):
            mix_1.clamp_factor = False
        if hasattr(mix_1, 'clamp_result'):
            mix_1.clamp_result = False
        if hasattr(mix_1, 'color'):
            mix_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(mix_1, 'data_type'):
            mix_1.data_type = 'VECTOR'
        if hasattr(mix_1, 'factor_mode'):
            mix_1.factor_mode = 'UNIFORM'
        if hasattr(mix_1, 'hide'):
            mix_1.hide = False
        if hasattr(mix_1, 'location'):
            mix_1.location = (-60.0, 420.0)
        if hasattr(mix_1, 'mute'):
            mix_1.mute = False
        if hasattr(mix_1, 'name'):
            mix_1.name = 'Mix'
        if hasattr(mix_1, 'status'):
            mix_1.status = False
        if hasattr(mix_1, 'use_custom_color'):
            mix_1.use_custom_color = False
        if hasattr(mix_1, 'width'):
            mix_1.width = 140.0
        input_ = next((input_ for input_ in mix_1.inputs if input_.identifier=='Factor_Float'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Factor'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in mix_1.inputs if input_.identifier=='Factor_Vector'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.5, 0.5, 0.5)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Factor'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in mix_1.inputs if input_.identifier=='A_Float'), None)
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
                input_.name = 'A'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in mix_1.inputs if input_.identifier=='B_Float'), None)
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
                input_.name = 'B'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in mix_1.inputs if input_.identifier=='A_Vector'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'A'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in mix_1.inputs if input_.identifier=='B_Vector'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'B'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in mix_1.inputs if input_.identifier=='A_Color'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.5, 0.5, 0.5, 1.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'A'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in mix_1.inputs if input_.identifier=='B_Color'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.5, 0.5, 0.5, 1.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'B'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in mix_1.inputs if input_.identifier=='A_Rotation'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'A'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in mix_1.inputs if input_.identifier=='B_Rotation'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'B'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        output = next((output for output in mix_1.outputs if output.identifier=='Result_Float'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = False
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Result'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False
        output = next((output for output in mix_1.outputs if output.identifier=='Result_Vector'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0)
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Result'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False
        output = next((output for output in mix_1.outputs if output.identifier=='Result_Color'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0, 0.0)
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = False
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Result'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False
        output = next((output for output in mix_1.outputs if output.identifier=='Result_Rotation'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0)
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = False
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Result'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        reroute_1 = node_tree1.nodes.new('NodeReroute')
        if hasattr(reroute_1, 'color'):
            reroute_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(reroute_1, 'hide'):
            reroute_1.hide = False
        if hasattr(reroute_1, 'location'):
            reroute_1.location = (864.471435546875, 206.99977111816406)
        if hasattr(reroute_1, 'mute'):
            reroute_1.mute = False
        if hasattr(reroute_1, 'name'):
            reroute_1.name = 'Reroute'
        if hasattr(reroute_1, 'status'):
            reroute_1.status = False
        if hasattr(reroute_1, 'use_custom_color'):
            reroute_1.use_custom_color = False
        if hasattr(reroute_1, 'width'):
            reroute_1.width = 16.0

        separate_xyz_002_1 = node_tree1.nodes.new('ShaderNodeSeparateXYZ')
        if hasattr(separate_xyz_002_1, 'color'):
            separate_xyz_002_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(separate_xyz_002_1, 'hide'):
            separate_xyz_002_1.hide = False
        if hasattr(separate_xyz_002_1, 'location'):
            separate_xyz_002_1.location = (-880.9576416015625, 20.0)
        if hasattr(separate_xyz_002_1, 'mute'):
            separate_xyz_002_1.mute = False
        if hasattr(separate_xyz_002_1, 'name'):
            separate_xyz_002_1.name = 'Separate XYZ.002'
        if hasattr(separate_xyz_002_1, 'status'):
            separate_xyz_002_1.status = False
        if hasattr(separate_xyz_002_1, 'use_custom_color'):
            separate_xyz_002_1.use_custom_color = False
        if hasattr(separate_xyz_002_1, 'width'):
            separate_xyz_002_1.width = 100.0
        input_ = next((input_ for input_ in separate_xyz_002_1.inputs if input_.identifier=='Vector'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        output = next((output for output in separate_xyz_002_1.outputs if output.identifier=='X'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'X'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False
        output = next((output for output in separate_xyz_002_1.outputs if output.identifier=='Y'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Y'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False
        output = next((output for output in separate_xyz_002_1.outputs if output.identifier=='Z'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Z'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        animtexuvscrollspeed1_005_1 = node_tree1.nodes.new('ShaderNodeCombineXYZ')
        if hasattr(animtexuvscrollspeed1_005_1, 'color'):
            animtexuvscrollspeed1_005_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(animtexuvscrollspeed1_005_1, 'hide'):
            animtexuvscrollspeed1_005_1.hide = False
        if hasattr(animtexuvscrollspeed1_005_1, 'label'):
            animtexuvscrollspeed1_005_1.label = 'animTexTint2'
        if hasattr(animtexuvscrollspeed1_005_1, 'location'):
            animtexuvscrollspeed1_005_1.location = (-740.9576416015625, 20.0)
        if hasattr(animtexuvscrollspeed1_005_1, 'mute'):
            animtexuvscrollspeed1_005_1.mute = False
        if hasattr(animtexuvscrollspeed1_005_1, 'name'):
            animtexuvscrollspeed1_005_1.name = 'animTexUVScrollSpeed1.005'
        if hasattr(animtexuvscrollspeed1_005_1, 'status'):
            animtexuvscrollspeed1_005_1.status = False
        if hasattr(animtexuvscrollspeed1_005_1, 'use_custom_color'):
            animtexuvscrollspeed1_005_1.use_custom_color = False
        if hasattr(animtexuvscrollspeed1_005_1, 'width'):
            animtexuvscrollspeed1_005_1.width = 100.0
        input_ = next((input_ for input_ in animtexuvscrollspeed1_005_1.inputs if input_.identifier=='X'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.9647060036659241
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'X'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in animtexuvscrollspeed1_005_1.inputs if input_.identifier=='Y'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.3294120132923126
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Y'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in animtexuvscrollspeed1_005_1.inputs if input_.identifier=='Z'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.3294120132923126
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Z'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        output = next((output for output in animtexuvscrollspeed1_005_1.outputs if output.identifier=='Vector'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0)
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Vector'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        vector_math_002_1 = node_tree1.nodes.new('ShaderNodeVectorMath')
        if hasattr(vector_math_002_1, 'color'):
            vector_math_002_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(vector_math_002_1, 'hide'):
            vector_math_002_1.hide = False
        if hasattr(vector_math_002_1, 'location'):
            vector_math_002_1.location = (-740.9576416015625, 320.0)
        if hasattr(vector_math_002_1, 'mute'):
            vector_math_002_1.mute = False
        if hasattr(vector_math_002_1, 'name'):
            vector_math_002_1.name = 'Vector Math.002'
        if hasattr(vector_math_002_1, 'operation'):
            vector_math_002_1.operation = 'SCALE'
        if hasattr(vector_math_002_1, 'status'):
            vector_math_002_1.status = False
        if hasattr(vector_math_002_1, 'use_custom_color'):
            vector_math_002_1.use_custom_color = False
        if hasattr(vector_math_002_1, 'width'):
            vector_math_002_1.width = 140.0001220703125
        input_ = next((input_ for input_ in vector_math_002_1.inputs if input_.identifier=='Vector'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_002_1.inputs if input_.identifier=='Vector_001'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.5, 0.5, 0.5)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_002_1.inputs if input_.identifier=='Vector_002'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_002_1.inputs if input_.identifier=='Scale'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.5
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Scale'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        output = next((output for output in vector_math_002_1.outputs if output.identifier=='Vector'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0)
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Vector'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False
        output = next((output for output in vector_math_002_1.outputs if output.identifier=='Value'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = False
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Value'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        vector_math_001_1 = node_tree1.nodes.new('ShaderNodeVectorMath')
        if hasattr(vector_math_001_1, 'color'):
            vector_math_001_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(vector_math_001_1, 'hide'):
            vector_math_001_1.hide = False
        if hasattr(vector_math_001_1, 'location'):
            vector_math_001_1.location = (-920.9576416015625, 320.0)
        if hasattr(vector_math_001_1, 'mute'):
            vector_math_001_1.mute = False
        if hasattr(vector_math_001_1, 'name'):
            vector_math_001_1.name = 'Vector Math.001'
        if hasattr(vector_math_001_1, 'operation'):
            vector_math_001_1.operation = 'SUBTRACT'
        if hasattr(vector_math_001_1, 'status'):
            vector_math_001_1.status = False
        if hasattr(vector_math_001_1, 'use_custom_color'):
            vector_math_001_1.use_custom_color = False
        if hasattr(vector_math_001_1, 'width'):
            vector_math_001_1.width = 140.0
        input_ = next((input_ for input_ in vector_math_001_1.inputs if input_.identifier=='Vector'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_001_1.inputs if input_.identifier=='Vector_001'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.5, 0.5, 0.5)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_001_1.inputs if input_.identifier=='Vector_002'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_001_1.inputs if input_.identifier=='Scale'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.5
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Scale'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        output = next((output for output in vector_math_001_1.outputs if output.identifier=='Vector'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0)
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Vector'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False
        output = next((output for output in vector_math_001_1.outputs if output.identifier=='Value'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = False
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Value'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        animtexuvscrollspeed1_004_1 = node_tree1.nodes.new('ShaderNodeCombineXYZ')
        if hasattr(animtexuvscrollspeed1_004_1, 'color'):
            animtexuvscrollspeed1_004_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(animtexuvscrollspeed1_004_1, 'hide'):
            animtexuvscrollspeed1_004_1.hide = False
        if hasattr(animtexuvscrollspeed1_004_1, 'label'):
            animtexuvscrollspeed1_004_1.label = 'animTexTint1'
        if hasattr(animtexuvscrollspeed1_004_1, 'location'):
            animtexuvscrollspeed1_004_1.location = (-745.2055053710938, 480.0)
        if hasattr(animtexuvscrollspeed1_004_1, 'mute'):
            animtexuvscrollspeed1_004_1.mute = False
        if hasattr(animtexuvscrollspeed1_004_1, 'name'):
            animtexuvscrollspeed1_004_1.name = 'animTexUVScrollSpeed1.004'
        if hasattr(animtexuvscrollspeed1_004_1, 'status'):
            animtexuvscrollspeed1_004_1.status = False
        if hasattr(animtexuvscrollspeed1_004_1, 'use_custom_color'):
            animtexuvscrollspeed1_004_1.use_custom_color = False
        if hasattr(animtexuvscrollspeed1_004_1, 'width'):
            animtexuvscrollspeed1_004_1.width = 100.0
        input_ = next((input_ for input_ in animtexuvscrollspeed1_004_1.inputs if input_.identifier=='X'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.5
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'X'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in animtexuvscrollspeed1_004_1.inputs if input_.identifier=='Y'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.5
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Y'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in animtexuvscrollspeed1_004_1.inputs if input_.identifier=='Z'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.5
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Z'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        output = next((output for output in animtexuvscrollspeed1_004_1.outputs if output.identifier=='Vector'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0)
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Vector'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        separate_xyz_001_1 = node_tree1.nodes.new('ShaderNodeSeparateXYZ')
        if hasattr(separate_xyz_001_1, 'color'):
            separate_xyz_001_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(separate_xyz_001_1, 'hide'):
            separate_xyz_001_1.hide = False
        if hasattr(separate_xyz_001_1, 'location'):
            separate_xyz_001_1.location = (-885.2055053710938, 480.0)
        if hasattr(separate_xyz_001_1, 'mute'):
            separate_xyz_001_1.mute = False
        if hasattr(separate_xyz_001_1, 'name'):
            separate_xyz_001_1.name = 'Separate XYZ.001'
        if hasattr(separate_xyz_001_1, 'status'):
            separate_xyz_001_1.status = False
        if hasattr(separate_xyz_001_1, 'use_custom_color'):
            separate_xyz_001_1.use_custom_color = False
        if hasattr(separate_xyz_001_1, 'width'):
            separate_xyz_001_1.width = 100.0
        input_ = next((input_ for input_ in separate_xyz_001_1.inputs if input_.identifier=='Vector'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        output = next((output for output in separate_xyz_001_1.outputs if output.identifier=='X'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'X'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False
        output = next((output for output in separate_xyz_001_1.outputs if output.identifier=='Y'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Y'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False
        output = next((output for output in separate_xyz_001_1.outputs if output.identifier=='Z'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Z'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        group_input_1 = node_tree1.nodes.new('NodeGroupInput')
        if hasattr(group_input_1, 'color'):
            group_input_1.color = (0.3999914526939392, 0.0, 0.0)
        if hasattr(group_input_1, 'hide'):
            group_input_1.hide = False
        if hasattr(group_input_1, 'location'):
            group_input_1.location = (-1215.9871826171875, 360.0)
        if hasattr(group_input_1, 'mute'):
            group_input_1.mute = False
        if hasattr(group_input_1, 'name'):
            group_input_1.name = 'Group Input'
        if hasattr(group_input_1, 'status'):
            group_input_1.status = False
        if hasattr(group_input_1, 'use_custom_color'):
            group_input_1.use_custom_color = True
        if hasattr(group_input_1, 'width'):
            group_input_1.width = 201.4150390625
        if hasattr(group_input_1.outputs[0], 'default_value'):
            group_input_1.outputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_1.outputs[0], 'display_shape'):
            group_input_1.outputs[0].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[0], 'enabled'):
            group_input_1.outputs[0].enabled = True
        if hasattr(group_input_1.outputs[0], 'hide'):
            group_input_1.outputs[0].hide = True
        if hasattr(group_input_1.outputs[0], 'hide_value'):
            group_input_1.outputs[0].hide_value = True
        if hasattr(group_input_1.outputs[0], 'name'):
            group_input_1.outputs[0].name = '_d DiffuseMap Color'
        if hasattr(group_input_1.outputs[0], 'show_expanded'):
            group_input_1.outputs[0].show_expanded = False
        if hasattr(group_input_1.outputs[1], 'default_value'):
            group_input_1.outputs[1].default_value = 0.0
        if hasattr(group_input_1.outputs[1], 'display_shape'):
            group_input_1.outputs[1].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[1], 'enabled'):
            group_input_1.outputs[1].enabled = True
        if hasattr(group_input_1.outputs[1], 'hide'):
            group_input_1.outputs[1].hide = True
        if hasattr(group_input_1.outputs[1], 'hide_value'):
            group_input_1.outputs[1].hide_value = False
        if hasattr(group_input_1.outputs[1], 'name'):
            group_input_1.outputs[1].name = '_d DiffuseMap Alpha'
        if hasattr(group_input_1.outputs[1], 'show_expanded'):
            group_input_1.outputs[1].show_expanded = False
        if hasattr(group_input_1.outputs[2], 'default_value'):
            group_input_1.outputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_1.outputs[2], 'display_shape'):
            group_input_1.outputs[2].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[2], 'enabled'):
            group_input_1.outputs[2].enabled = True
        if hasattr(group_input_1.outputs[2], 'hide'):
            group_input_1.outputs[2].hide = False
        if hasattr(group_input_1.outputs[2], 'hide_value'):
            group_input_1.outputs[2].hide_value = False
        if hasattr(group_input_1.outputs[2], 'name'):
            group_input_1.outputs[2].name = 'AnimatedTexture1 Color'
        if hasattr(group_input_1.outputs[2], 'show_expanded'):
            group_input_1.outputs[2].show_expanded = False
        if hasattr(group_input_1.outputs[3], 'default_value'):
            group_input_1.outputs[3].default_value = 0.0
        if hasattr(group_input_1.outputs[3], 'display_shape'):
            group_input_1.outputs[3].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[3], 'enabled'):
            group_input_1.outputs[3].enabled = True
        if hasattr(group_input_1.outputs[3], 'hide'):
            group_input_1.outputs[3].hide = False
        if hasattr(group_input_1.outputs[3], 'hide_value'):
            group_input_1.outputs[3].hide_value = False
        if hasattr(group_input_1.outputs[3], 'name'):
            group_input_1.outputs[3].name = 'AnimatedTexture1 Alpha'
        if hasattr(group_input_1.outputs[3], 'show_expanded'):
            group_input_1.outputs[3].show_expanded = False
        if hasattr(group_input_1.outputs[4], 'default_value'):
            group_input_1.outputs[4].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_1.outputs[4], 'display_shape'):
            group_input_1.outputs[4].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[4], 'enabled'):
            group_input_1.outputs[4].enabled = True
        if hasattr(group_input_1.outputs[4], 'hide'):
            group_input_1.outputs[4].hide = True
        if hasattr(group_input_1.outputs[4], 'hide_value'):
            group_input_1.outputs[4].hide_value = False
        if hasattr(group_input_1.outputs[4], 'name'):
            group_input_1.outputs[4].name = 'AnimatedTexture2 Color'
        if hasattr(group_input_1.outputs[4], 'show_expanded'):
            group_input_1.outputs[4].show_expanded = False
        if hasattr(group_input_1.outputs[5], 'default_value'):
            group_input_1.outputs[5].default_value = 0.0
        if hasattr(group_input_1.outputs[5], 'display_shape'):
            group_input_1.outputs[5].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[5], 'enabled'):
            group_input_1.outputs[5].enabled = True
        if hasattr(group_input_1.outputs[5], 'hide'):
            group_input_1.outputs[5].hide = True
        if hasattr(group_input_1.outputs[5], 'hide_value'):
            group_input_1.outputs[5].hide_value = False
        if hasattr(group_input_1.outputs[5], 'name'):
            group_input_1.outputs[5].name = 'AnimatedTexture2 Alpha'
        if hasattr(group_input_1.outputs[5], 'show_expanded'):
            group_input_1.outputs[5].show_expanded = False
        if hasattr(group_input_1.outputs[6], 'default_value'):
            group_input_1.outputs[6].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_1.outputs[6], 'display_shape'):
            group_input_1.outputs[6].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[6], 'enabled'):
            group_input_1.outputs[6].enabled = True
        if hasattr(group_input_1.outputs[6], 'hide'):
            group_input_1.outputs[6].hide = True
        if hasattr(group_input_1.outputs[6], 'hide_value'):
            group_input_1.outputs[6].hide_value = False
        if hasattr(group_input_1.outputs[6], 'name'):
            group_input_1.outputs[6].name = 'animTexTint0'
        if hasattr(group_input_1.outputs[6], 'show_expanded'):
            group_input_1.outputs[6].show_expanded = False
        if hasattr(group_input_1.outputs[7], 'default_value'):
            group_input_1.outputs[7].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_1.outputs[7], 'display_shape'):
            group_input_1.outputs[7].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[7], 'enabled'):
            group_input_1.outputs[7].enabled = True
        if hasattr(group_input_1.outputs[7], 'hide'):
            group_input_1.outputs[7].hide = False
        if hasattr(group_input_1.outputs[7], 'hide_value'):
            group_input_1.outputs[7].hide_value = False
        if hasattr(group_input_1.outputs[7], 'name'):
            group_input_1.outputs[7].name = 'animTexTint1'
        if hasattr(group_input_1.outputs[7], 'show_expanded'):
            group_input_1.outputs[7].show_expanded = False
        if hasattr(group_input_1.outputs[8], 'default_value'):
            group_input_1.outputs[8].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_1.outputs[8], 'display_shape'):
            group_input_1.outputs[8].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[8], 'enabled'):
            group_input_1.outputs[8].enabled = True
        if hasattr(group_input_1.outputs[8], 'hide'):
            group_input_1.outputs[8].hide = True
        if hasattr(group_input_1.outputs[8], 'hide_value'):
            group_input_1.outputs[8].hide_value = False
        if hasattr(group_input_1.outputs[8], 'name'):
            group_input_1.outputs[8].name = 'animTexTint2'
        if hasattr(group_input_1.outputs[8], 'show_expanded'):
            group_input_1.outputs[8].show_expanded = False
        if hasattr(group_input_1.outputs[9], 'default_value'):
            group_input_1.outputs[9].default_value = 0.0
        if hasattr(group_input_1.outputs[9], 'display_shape'):
            group_input_1.outputs[9].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[9], 'enabled'):
            group_input_1.outputs[9].enabled = True
        if hasattr(group_input_1.outputs[9], 'hide'):
            group_input_1.outputs[9].hide = True
        if hasattr(group_input_1.outputs[9], 'hide_value'):
            group_input_1.outputs[9].hide_value = True
        if hasattr(group_input_1.outputs[9], 'name'):
            group_input_1.outputs[9].name = '—— EXTRAS ——'
        if hasattr(group_input_1.outputs[9], 'show_expanded'):
            group_input_1.outputs[9].show_expanded = False
        if hasattr(group_input_1.outputs[10], 'default_value'):
            group_input_1.outputs[10].default_value = 1.0
        if hasattr(group_input_1.outputs[10], 'display_shape'):
            group_input_1.outputs[10].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[10], 'enabled'):
            group_input_1.outputs[10].enabled = True
        if hasattr(group_input_1.outputs[10], 'hide'):
            group_input_1.outputs[10].hide = True
        if hasattr(group_input_1.outputs[10], 'hide_value'):
            group_input_1.outputs[10].hide_value = False
        if hasattr(group_input_1.outputs[10], 'name'):
            group_input_1.outputs[10].name = 'Roughness Factor'
        if hasattr(group_input_1.outputs[10], 'show_expanded'):
            group_input_1.outputs[10].show_expanded = False
        if hasattr(group_input_1.outputs[11], 'default_value'):
            group_input_1.outputs[11].default_value = 1.0
        if hasattr(group_input_1.outputs[11], 'display_shape'):
            group_input_1.outputs[11].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[11], 'enabled'):
            group_input_1.outputs[11].enabled = True
        if hasattr(group_input_1.outputs[11], 'hide'):
            group_input_1.outputs[11].hide = True
        if hasattr(group_input_1.outputs[11], 'hide_value'):
            group_input_1.outputs[11].hide_value = False
        if hasattr(group_input_1.outputs[11], 'name'):
            group_input_1.outputs[11].name = 'Emission Strength'
        if hasattr(group_input_1.outputs[11], 'show_expanded'):
            group_input_1.outputs[11].show_expanded = False
        if hasattr(group_input_1.outputs[12], 'default_value'):
            group_input_1.outputs[12].default_value = 1.0
        if hasattr(group_input_1.outputs[12], 'display_shape'):
            group_input_1.outputs[12].display_shape = 'CIRCLE'
        if hasattr(group_input_1.outputs[12], 'enabled'):
            group_input_1.outputs[12].enabled = True
        if hasattr(group_input_1.outputs[12], 'hide'):
            group_input_1.outputs[12].hide = True
        if hasattr(group_input_1.outputs[12], 'hide_value'):
            group_input_1.outputs[12].hide_value = False
        if hasattr(group_input_1.outputs[12], 'name'):
            group_input_1.outputs[12].name = 'Backface Culling Factor'
        if hasattr(group_input_1.outputs[12], 'show_expanded'):
            group_input_1.outputs[12].show_expanded = False

        vector_math_003_1 = node_tree1.nodes.new('ShaderNodeVectorMath')
        if hasattr(vector_math_003_1, 'color'):
            vector_math_003_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(vector_math_003_1, 'hide'):
            vector_math_003_1.hide = False
        if hasattr(vector_math_003_1, 'location'):
            vector_math_003_1.location = (-526.878662109375, 480.0)
        if hasattr(vector_math_003_1, 'mute'):
            vector_math_003_1.mute = False
        if hasattr(vector_math_003_1, 'name'):
            vector_math_003_1.name = 'Vector Math.003'
        if hasattr(vector_math_003_1, 'operation'):
            vector_math_003_1.operation = 'MULTIPLY'
        if hasattr(vector_math_003_1, 'status'):
            vector_math_003_1.status = False
        if hasattr(vector_math_003_1, 'use_custom_color'):
            vector_math_003_1.use_custom_color = False
        if hasattr(vector_math_003_1, 'width'):
            vector_math_003_1.width = 100.0
        input_ = next((input_ for input_ in vector_math_003_1.inputs if input_.identifier=='Vector'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_003_1.inputs if input_.identifier=='Vector_001'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_003_1.inputs if input_.identifier=='Vector_002'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_003_1.inputs if input_.identifier=='Scale'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 1.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Scale'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        output = next((output for output in vector_math_003_1.outputs if output.identifier=='Vector'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0)
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Vector'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False
        output = next((output for output in vector_math_003_1.outputs if output.identifier=='Value'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = False
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Value'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        group_input_001_1 = node_tree1.nodes.new('NodeGroupInput')
        if hasattr(group_input_001_1, 'color'):
            group_input_001_1.color = (0.3999914526939392, 0.0, 0.0)
        if hasattr(group_input_001_1, 'hide'):
            group_input_001_1.hide = False
        if hasattr(group_input_001_1, 'location'):
            group_input_001_1.location = (-1219.3504638671875, 101.3077163696289)
        if hasattr(group_input_001_1, 'mute'):
            group_input_001_1.mute = False
        if hasattr(group_input_001_1, 'name'):
            group_input_001_1.name = 'Group Input.001'
        if hasattr(group_input_001_1, 'status'):
            group_input_001_1.status = False
        if hasattr(group_input_001_1, 'use_custom_color'):
            group_input_001_1.use_custom_color = True
        if hasattr(group_input_001_1, 'width'):
            group_input_001_1.width = 207.8797607421875
        if hasattr(group_input_001_1.outputs[0], 'default_value'):
            group_input_001_1.outputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_001_1.outputs[0], 'display_shape'):
            group_input_001_1.outputs[0].display_shape = 'CIRCLE'
        if hasattr(group_input_001_1.outputs[0], 'enabled'):
            group_input_001_1.outputs[0].enabled = True
        if hasattr(group_input_001_1.outputs[0], 'hide'):
            group_input_001_1.outputs[0].hide = True
        if hasattr(group_input_001_1.outputs[0], 'hide_value'):
            group_input_001_1.outputs[0].hide_value = True
        if hasattr(group_input_001_1.outputs[0], 'name'):
            group_input_001_1.outputs[0].name = '_d DiffuseMap Color'
        if hasattr(group_input_001_1.outputs[0], 'show_expanded'):
            group_input_001_1.outputs[0].show_expanded = False
        if hasattr(group_input_001_1.outputs[1], 'default_value'):
            group_input_001_1.outputs[1].default_value = 0.0
        if hasattr(group_input_001_1.outputs[1], 'display_shape'):
            group_input_001_1.outputs[1].display_shape = 'CIRCLE'
        if hasattr(group_input_001_1.outputs[1], 'enabled'):
            group_input_001_1.outputs[1].enabled = True
        if hasattr(group_input_001_1.outputs[1], 'hide'):
            group_input_001_1.outputs[1].hide = True
        if hasattr(group_input_001_1.outputs[1], 'hide_value'):
            group_input_001_1.outputs[1].hide_value = False
        if hasattr(group_input_001_1.outputs[1], 'name'):
            group_input_001_1.outputs[1].name = '_d DiffuseMap Alpha'
        if hasattr(group_input_001_1.outputs[1], 'show_expanded'):
            group_input_001_1.outputs[1].show_expanded = False
        if hasattr(group_input_001_1.outputs[2], 'default_value'):
            group_input_001_1.outputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_001_1.outputs[2], 'display_shape'):
            group_input_001_1.outputs[2].display_shape = 'CIRCLE'
        if hasattr(group_input_001_1.outputs[2], 'enabled'):
            group_input_001_1.outputs[2].enabled = True
        if hasattr(group_input_001_1.outputs[2], 'hide'):
            group_input_001_1.outputs[2].hide = True
        if hasattr(group_input_001_1.outputs[2], 'hide_value'):
            group_input_001_1.outputs[2].hide_value = False
        if hasattr(group_input_001_1.outputs[2], 'name'):
            group_input_001_1.outputs[2].name = 'AnimatedTexture1 Color'
        if hasattr(group_input_001_1.outputs[2], 'show_expanded'):
            group_input_001_1.outputs[2].show_expanded = False
        if hasattr(group_input_001_1.outputs[3], 'default_value'):
            group_input_001_1.outputs[3].default_value = 0.0
        if hasattr(group_input_001_1.outputs[3], 'display_shape'):
            group_input_001_1.outputs[3].display_shape = 'CIRCLE'
        if hasattr(group_input_001_1.outputs[3], 'enabled'):
            group_input_001_1.outputs[3].enabled = True
        if hasattr(group_input_001_1.outputs[3], 'hide'):
            group_input_001_1.outputs[3].hide = False
        if hasattr(group_input_001_1.outputs[3], 'hide_value'):
            group_input_001_1.outputs[3].hide_value = False
        if hasattr(group_input_001_1.outputs[3], 'name'):
            group_input_001_1.outputs[3].name = 'AnimatedTexture1 Alpha'
        if hasattr(group_input_001_1.outputs[3], 'show_expanded'):
            group_input_001_1.outputs[3].show_expanded = False
        if hasattr(group_input_001_1.outputs[4], 'default_value'):
            group_input_001_1.outputs[4].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_001_1.outputs[4], 'display_shape'):
            group_input_001_1.outputs[4].display_shape = 'CIRCLE'
        if hasattr(group_input_001_1.outputs[4], 'enabled'):
            group_input_001_1.outputs[4].enabled = True
        if hasattr(group_input_001_1.outputs[4], 'hide'):
            group_input_001_1.outputs[4].hide = False
        if hasattr(group_input_001_1.outputs[4], 'hide_value'):
            group_input_001_1.outputs[4].hide_value = False
        if hasattr(group_input_001_1.outputs[4], 'name'):
            group_input_001_1.outputs[4].name = 'AnimatedTexture2 Color'
        if hasattr(group_input_001_1.outputs[4], 'show_expanded'):
            group_input_001_1.outputs[4].show_expanded = False
        if hasattr(group_input_001_1.outputs[5], 'default_value'):
            group_input_001_1.outputs[5].default_value = 0.0
        if hasattr(group_input_001_1.outputs[5], 'display_shape'):
            group_input_001_1.outputs[5].display_shape = 'CIRCLE'
        if hasattr(group_input_001_1.outputs[5], 'enabled'):
            group_input_001_1.outputs[5].enabled = True
        if hasattr(group_input_001_1.outputs[5], 'hide'):
            group_input_001_1.outputs[5].hide = True
        if hasattr(group_input_001_1.outputs[5], 'hide_value'):
            group_input_001_1.outputs[5].hide_value = False
        if hasattr(group_input_001_1.outputs[5], 'name'):
            group_input_001_1.outputs[5].name = 'AnimatedTexture2 Alpha'
        if hasattr(group_input_001_1.outputs[5], 'show_expanded'):
            group_input_001_1.outputs[5].show_expanded = False
        if hasattr(group_input_001_1.outputs[6], 'default_value'):
            group_input_001_1.outputs[6].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_001_1.outputs[6], 'display_shape'):
            group_input_001_1.outputs[6].display_shape = 'CIRCLE'
        if hasattr(group_input_001_1.outputs[6], 'enabled'):
            group_input_001_1.outputs[6].enabled = True
        if hasattr(group_input_001_1.outputs[6], 'hide'):
            group_input_001_1.outputs[6].hide = True
        if hasattr(group_input_001_1.outputs[6], 'hide_value'):
            group_input_001_1.outputs[6].hide_value = False
        if hasattr(group_input_001_1.outputs[6], 'name'):
            group_input_001_1.outputs[6].name = 'animTexTint0'
        if hasattr(group_input_001_1.outputs[6], 'show_expanded'):
            group_input_001_1.outputs[6].show_expanded = False
        if hasattr(group_input_001_1.outputs[7], 'default_value'):
            group_input_001_1.outputs[7].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_001_1.outputs[7], 'display_shape'):
            group_input_001_1.outputs[7].display_shape = 'CIRCLE'
        if hasattr(group_input_001_1.outputs[7], 'enabled'):
            group_input_001_1.outputs[7].enabled = True
        if hasattr(group_input_001_1.outputs[7], 'hide'):
            group_input_001_1.outputs[7].hide = True
        if hasattr(group_input_001_1.outputs[7], 'hide_value'):
            group_input_001_1.outputs[7].hide_value = False
        if hasattr(group_input_001_1.outputs[7], 'name'):
            group_input_001_1.outputs[7].name = 'animTexTint1'
        if hasattr(group_input_001_1.outputs[7], 'show_expanded'):
            group_input_001_1.outputs[7].show_expanded = False
        if hasattr(group_input_001_1.outputs[8], 'default_value'):
            group_input_001_1.outputs[8].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_001_1.outputs[8], 'display_shape'):
            group_input_001_1.outputs[8].display_shape = 'CIRCLE'
        if hasattr(group_input_001_1.outputs[8], 'enabled'):
            group_input_001_1.outputs[8].enabled = True
        if hasattr(group_input_001_1.outputs[8], 'hide'):
            group_input_001_1.outputs[8].hide = False
        if hasattr(group_input_001_1.outputs[8], 'hide_value'):
            group_input_001_1.outputs[8].hide_value = False
        if hasattr(group_input_001_1.outputs[8], 'name'):
            group_input_001_1.outputs[8].name = 'animTexTint2'
        if hasattr(group_input_001_1.outputs[8], 'show_expanded'):
            group_input_001_1.outputs[8].show_expanded = False
        if hasattr(group_input_001_1.outputs[9], 'default_value'):
            group_input_001_1.outputs[9].default_value = 0.0
        if hasattr(group_input_001_1.outputs[9], 'display_shape'):
            group_input_001_1.outputs[9].display_shape = 'CIRCLE'
        if hasattr(group_input_001_1.outputs[9], 'enabled'):
            group_input_001_1.outputs[9].enabled = True
        if hasattr(group_input_001_1.outputs[9], 'hide'):
            group_input_001_1.outputs[9].hide = True
        if hasattr(group_input_001_1.outputs[9], 'hide_value'):
            group_input_001_1.outputs[9].hide_value = True
        if hasattr(group_input_001_1.outputs[9], 'name'):
            group_input_001_1.outputs[9].name = '—— EXTRAS ——'
        if hasattr(group_input_001_1.outputs[9], 'show_expanded'):
            group_input_001_1.outputs[9].show_expanded = False
        if hasattr(group_input_001_1.outputs[10], 'default_value'):
            group_input_001_1.outputs[10].default_value = 1.0
        if hasattr(group_input_001_1.outputs[10], 'display_shape'):
            group_input_001_1.outputs[10].display_shape = 'CIRCLE'
        if hasattr(group_input_001_1.outputs[10], 'enabled'):
            group_input_001_1.outputs[10].enabled = True
        if hasattr(group_input_001_1.outputs[10], 'hide'):
            group_input_001_1.outputs[10].hide = True
        if hasattr(group_input_001_1.outputs[10], 'hide_value'):
            group_input_001_1.outputs[10].hide_value = False
        if hasattr(group_input_001_1.outputs[10], 'name'):
            group_input_001_1.outputs[10].name = 'Roughness Factor'
        if hasattr(group_input_001_1.outputs[10], 'show_expanded'):
            group_input_001_1.outputs[10].show_expanded = False
        if hasattr(group_input_001_1.outputs[11], 'default_value'):
            group_input_001_1.outputs[11].default_value = 1.0
        if hasattr(group_input_001_1.outputs[11], 'display_shape'):
            group_input_001_1.outputs[11].display_shape = 'CIRCLE'
        if hasattr(group_input_001_1.outputs[11], 'enabled'):
            group_input_001_1.outputs[11].enabled = True
        if hasattr(group_input_001_1.outputs[11], 'hide'):
            group_input_001_1.outputs[11].hide = True
        if hasattr(group_input_001_1.outputs[11], 'hide_value'):
            group_input_001_1.outputs[11].hide_value = False
        if hasattr(group_input_001_1.outputs[11], 'name'):
            group_input_001_1.outputs[11].name = 'Emission Strength'
        if hasattr(group_input_001_1.outputs[11], 'show_expanded'):
            group_input_001_1.outputs[11].show_expanded = False
        if hasattr(group_input_001_1.outputs[12], 'default_value'):
            group_input_001_1.outputs[12].default_value = 1.0
        if hasattr(group_input_001_1.outputs[12], 'display_shape'):
            group_input_001_1.outputs[12].display_shape = 'CIRCLE'
        if hasattr(group_input_001_1.outputs[12], 'enabled'):
            group_input_001_1.outputs[12].enabled = True
        if hasattr(group_input_001_1.outputs[12], 'hide'):
            group_input_001_1.outputs[12].hide = True
        if hasattr(group_input_001_1.outputs[12], 'hide_value'):
            group_input_001_1.outputs[12].hide_value = False
        if hasattr(group_input_001_1.outputs[12], 'name'):
            group_input_001_1.outputs[12].name = 'Backface Culling Factor'
        if hasattr(group_input_001_1.outputs[12], 'show_expanded'):
            group_input_001_1.outputs[12].show_expanded = False

        group_input_005_1 = node_tree1.nodes.new('NodeGroupInput')
        if hasattr(group_input_005_1, 'color'):
            group_input_005_1.color = (0.3999914526939392, 0.0, 0.0)
        if hasattr(group_input_005_1, 'hide'):
            group_input_005_1.hide = False
        if hasattr(group_input_005_1, 'location'):
            group_input_005_1.location = (-361.12109375, 339.8137512207031)
        if hasattr(group_input_005_1, 'mute'):
            group_input_005_1.mute = False
        if hasattr(group_input_005_1, 'name'):
            group_input_005_1.name = 'Group Input.005'
        if hasattr(group_input_005_1, 'status'):
            group_input_005_1.status = False
        if hasattr(group_input_005_1, 'use_custom_color'):
            group_input_005_1.use_custom_color = True
        if hasattr(group_input_005_1, 'width'):
            group_input_005_1.width = 169.3370361328125
        if hasattr(group_input_005_1.outputs[0], 'default_value'):
            group_input_005_1.outputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_005_1.outputs[0], 'display_shape'):
            group_input_005_1.outputs[0].display_shape = 'CIRCLE'
        if hasattr(group_input_005_1.outputs[0], 'enabled'):
            group_input_005_1.outputs[0].enabled = True
        if hasattr(group_input_005_1.outputs[0], 'hide'):
            group_input_005_1.outputs[0].hide = True
        if hasattr(group_input_005_1.outputs[0], 'hide_value'):
            group_input_005_1.outputs[0].hide_value = True
        if hasattr(group_input_005_1.outputs[0], 'name'):
            group_input_005_1.outputs[0].name = '_d DiffuseMap Color'
        if hasattr(group_input_005_1.outputs[0], 'show_expanded'):
            group_input_005_1.outputs[0].show_expanded = False
        if hasattr(group_input_005_1.outputs[1], 'default_value'):
            group_input_005_1.outputs[1].default_value = 0.0
        if hasattr(group_input_005_1.outputs[1], 'display_shape'):
            group_input_005_1.outputs[1].display_shape = 'CIRCLE'
        if hasattr(group_input_005_1.outputs[1], 'enabled'):
            group_input_005_1.outputs[1].enabled = True
        if hasattr(group_input_005_1.outputs[1], 'hide'):
            group_input_005_1.outputs[1].hide = True
        if hasattr(group_input_005_1.outputs[1], 'hide_value'):
            group_input_005_1.outputs[1].hide_value = False
        if hasattr(group_input_005_1.outputs[1], 'name'):
            group_input_005_1.outputs[1].name = '_d DiffuseMap Alpha'
        if hasattr(group_input_005_1.outputs[1], 'show_expanded'):
            group_input_005_1.outputs[1].show_expanded = False
        if hasattr(group_input_005_1.outputs[2], 'default_value'):
            group_input_005_1.outputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_005_1.outputs[2], 'display_shape'):
            group_input_005_1.outputs[2].display_shape = 'CIRCLE'
        if hasattr(group_input_005_1.outputs[2], 'enabled'):
            group_input_005_1.outputs[2].enabled = True
        if hasattr(group_input_005_1.outputs[2], 'hide'):
            group_input_005_1.outputs[2].hide = True
        if hasattr(group_input_005_1.outputs[2], 'hide_value'):
            group_input_005_1.outputs[2].hide_value = False
        if hasattr(group_input_005_1.outputs[2], 'name'):
            group_input_005_1.outputs[2].name = 'AnimatedTexture1 Color'
        if hasattr(group_input_005_1.outputs[2], 'show_expanded'):
            group_input_005_1.outputs[2].show_expanded = False
        if hasattr(group_input_005_1.outputs[3], 'default_value'):
            group_input_005_1.outputs[3].default_value = 0.0
        if hasattr(group_input_005_1.outputs[3], 'display_shape'):
            group_input_005_1.outputs[3].display_shape = 'CIRCLE'
        if hasattr(group_input_005_1.outputs[3], 'enabled'):
            group_input_005_1.outputs[3].enabled = True
        if hasattr(group_input_005_1.outputs[3], 'hide'):
            group_input_005_1.outputs[3].hide = False
        if hasattr(group_input_005_1.outputs[3], 'hide_value'):
            group_input_005_1.outputs[3].hide_value = False
        if hasattr(group_input_005_1.outputs[3], 'name'):
            group_input_005_1.outputs[3].name = 'AnimatedTexture1 Alpha'
        if hasattr(group_input_005_1.outputs[3], 'show_expanded'):
            group_input_005_1.outputs[3].show_expanded = False
        if hasattr(group_input_005_1.outputs[4], 'default_value'):
            group_input_005_1.outputs[4].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_005_1.outputs[4], 'display_shape'):
            group_input_005_1.outputs[4].display_shape = 'CIRCLE'
        if hasattr(group_input_005_1.outputs[4], 'enabled'):
            group_input_005_1.outputs[4].enabled = True
        if hasattr(group_input_005_1.outputs[4], 'hide'):
            group_input_005_1.outputs[4].hide = True
        if hasattr(group_input_005_1.outputs[4], 'hide_value'):
            group_input_005_1.outputs[4].hide_value = False
        if hasattr(group_input_005_1.outputs[4], 'name'):
            group_input_005_1.outputs[4].name = 'AnimatedTexture2 Color'
        if hasattr(group_input_005_1.outputs[4], 'show_expanded'):
            group_input_005_1.outputs[4].show_expanded = False
        if hasattr(group_input_005_1.outputs[5], 'default_value'):
            group_input_005_1.outputs[5].default_value = 0.0
        if hasattr(group_input_005_1.outputs[5], 'display_shape'):
            group_input_005_1.outputs[5].display_shape = 'CIRCLE'
        if hasattr(group_input_005_1.outputs[5], 'enabled'):
            group_input_005_1.outputs[5].enabled = True
        if hasattr(group_input_005_1.outputs[5], 'hide'):
            group_input_005_1.outputs[5].hide = False
        if hasattr(group_input_005_1.outputs[5], 'hide_value'):
            group_input_005_1.outputs[5].hide_value = False
        if hasattr(group_input_005_1.outputs[5], 'name'):
            group_input_005_1.outputs[5].name = 'AnimatedTexture2 Alpha'
        if hasattr(group_input_005_1.outputs[5], 'show_expanded'):
            group_input_005_1.outputs[5].show_expanded = False
        if hasattr(group_input_005_1.outputs[6], 'default_value'):
            group_input_005_1.outputs[6].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_005_1.outputs[6], 'display_shape'):
            group_input_005_1.outputs[6].display_shape = 'CIRCLE'
        if hasattr(group_input_005_1.outputs[6], 'enabled'):
            group_input_005_1.outputs[6].enabled = True
        if hasattr(group_input_005_1.outputs[6], 'hide'):
            group_input_005_1.outputs[6].hide = True
        if hasattr(group_input_005_1.outputs[6], 'hide_value'):
            group_input_005_1.outputs[6].hide_value = False
        if hasattr(group_input_005_1.outputs[6], 'name'):
            group_input_005_1.outputs[6].name = 'animTexTint0'
        if hasattr(group_input_005_1.outputs[6], 'show_expanded'):
            group_input_005_1.outputs[6].show_expanded = False
        if hasattr(group_input_005_1.outputs[7], 'default_value'):
            group_input_005_1.outputs[7].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_005_1.outputs[7], 'display_shape'):
            group_input_005_1.outputs[7].display_shape = 'CIRCLE'
        if hasattr(group_input_005_1.outputs[7], 'enabled'):
            group_input_005_1.outputs[7].enabled = True
        if hasattr(group_input_005_1.outputs[7], 'hide'):
            group_input_005_1.outputs[7].hide = True
        if hasattr(group_input_005_1.outputs[7], 'hide_value'):
            group_input_005_1.outputs[7].hide_value = False
        if hasattr(group_input_005_1.outputs[7], 'name'):
            group_input_005_1.outputs[7].name = 'animTexTint1'
        if hasattr(group_input_005_1.outputs[7], 'show_expanded'):
            group_input_005_1.outputs[7].show_expanded = False
        if hasattr(group_input_005_1.outputs[8], 'default_value'):
            group_input_005_1.outputs[8].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_005_1.outputs[8], 'display_shape'):
            group_input_005_1.outputs[8].display_shape = 'CIRCLE'
        if hasattr(group_input_005_1.outputs[8], 'enabled'):
            group_input_005_1.outputs[8].enabled = True
        if hasattr(group_input_005_1.outputs[8], 'hide'):
            group_input_005_1.outputs[8].hide = True
        if hasattr(group_input_005_1.outputs[8], 'hide_value'):
            group_input_005_1.outputs[8].hide_value = False
        if hasattr(group_input_005_1.outputs[8], 'name'):
            group_input_005_1.outputs[8].name = 'animTexTint2'
        if hasattr(group_input_005_1.outputs[8], 'show_expanded'):
            group_input_005_1.outputs[8].show_expanded = False
        if hasattr(group_input_005_1.outputs[9], 'default_value'):
            group_input_005_1.outputs[9].default_value = 0.0
        if hasattr(group_input_005_1.outputs[9], 'display_shape'):
            group_input_005_1.outputs[9].display_shape = 'CIRCLE'
        if hasattr(group_input_005_1.outputs[9], 'enabled'):
            group_input_005_1.outputs[9].enabled = True
        if hasattr(group_input_005_1.outputs[9], 'hide'):
            group_input_005_1.outputs[9].hide = True
        if hasattr(group_input_005_1.outputs[9], 'hide_value'):
            group_input_005_1.outputs[9].hide_value = True
        if hasattr(group_input_005_1.outputs[9], 'name'):
            group_input_005_1.outputs[9].name = '—— EXTRAS ——'
        if hasattr(group_input_005_1.outputs[9], 'show_expanded'):
            group_input_005_1.outputs[9].show_expanded = False
        if hasattr(group_input_005_1.outputs[10], 'default_value'):
            group_input_005_1.outputs[10].default_value = 1.0
        if hasattr(group_input_005_1.outputs[10], 'display_shape'):
            group_input_005_1.outputs[10].display_shape = 'CIRCLE'
        if hasattr(group_input_005_1.outputs[10], 'enabled'):
            group_input_005_1.outputs[10].enabled = True
        if hasattr(group_input_005_1.outputs[10], 'hide'):
            group_input_005_1.outputs[10].hide = True
        if hasattr(group_input_005_1.outputs[10], 'hide_value'):
            group_input_005_1.outputs[10].hide_value = False
        if hasattr(group_input_005_1.outputs[10], 'name'):
            group_input_005_1.outputs[10].name = 'Roughness Factor'
        if hasattr(group_input_005_1.outputs[10], 'show_expanded'):
            group_input_005_1.outputs[10].show_expanded = False
        if hasattr(group_input_005_1.outputs[11], 'default_value'):
            group_input_005_1.outputs[11].default_value = 1.0
        if hasattr(group_input_005_1.outputs[11], 'display_shape'):
            group_input_005_1.outputs[11].display_shape = 'CIRCLE'
        if hasattr(group_input_005_1.outputs[11], 'enabled'):
            group_input_005_1.outputs[11].enabled = True
        if hasattr(group_input_005_1.outputs[11], 'hide'):
            group_input_005_1.outputs[11].hide = True
        if hasattr(group_input_005_1.outputs[11], 'hide_value'):
            group_input_005_1.outputs[11].hide_value = False
        if hasattr(group_input_005_1.outputs[11], 'name'):
            group_input_005_1.outputs[11].name = 'Emission Strength'
        if hasattr(group_input_005_1.outputs[11], 'show_expanded'):
            group_input_005_1.outputs[11].show_expanded = False
        if hasattr(group_input_005_1.outputs[12], 'default_value'):
            group_input_005_1.outputs[12].default_value = 1.0
        if hasattr(group_input_005_1.outputs[12], 'display_shape'):
            group_input_005_1.outputs[12].display_shape = 'CIRCLE'
        if hasattr(group_input_005_1.outputs[12], 'enabled'):
            group_input_005_1.outputs[12].enabled = True
        if hasattr(group_input_005_1.outputs[12], 'hide'):
            group_input_005_1.outputs[12].hide = True
        if hasattr(group_input_005_1.outputs[12], 'hide_value'):
            group_input_005_1.outputs[12].hide_value = False
        if hasattr(group_input_005_1.outputs[12], 'name'):
            group_input_005_1.outputs[12].name = 'Backface Culling Factor'
        if hasattr(group_input_005_1.outputs[12], 'show_expanded'):
            group_input_005_1.outputs[12].show_expanded = False

        animtexuvscrollspeed1_003_1 = node_tree1.nodes.new('ShaderNodeCombineXYZ')
        if hasattr(animtexuvscrollspeed1_003_1, 'color'):
            animtexuvscrollspeed1_003_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(animtexuvscrollspeed1_003_1, 'hide'):
            animtexuvscrollspeed1_003_1.hide = False
        if hasattr(animtexuvscrollspeed1_003_1, 'label'):
            animtexuvscrollspeed1_003_1.label = 'animTexTint0'
        if hasattr(animtexuvscrollspeed1_003_1, 'location'):
            animtexuvscrollspeed1_003_1.location = (-740.9576416015625, 737.3845825195312)
        if hasattr(animtexuvscrollspeed1_003_1, 'mute'):
            animtexuvscrollspeed1_003_1.mute = False
        if hasattr(animtexuvscrollspeed1_003_1, 'name'):
            animtexuvscrollspeed1_003_1.name = 'animTexUVScrollSpeed1.003'
        if hasattr(animtexuvscrollspeed1_003_1, 'status'):
            animtexuvscrollspeed1_003_1.status = False
        if hasattr(animtexuvscrollspeed1_003_1, 'use_custom_color'):
            animtexuvscrollspeed1_003_1.use_custom_color = False
        if hasattr(animtexuvscrollspeed1_003_1, 'width'):
            animtexuvscrollspeed1_003_1.width = 100.0
        input_ = next((input_ for input_ in animtexuvscrollspeed1_003_1.inputs if input_.identifier=='X'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.6866850256919861
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'X'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in animtexuvscrollspeed1_003_1.inputs if input_.identifier=='Y'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.3324519991874695
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Y'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in animtexuvscrollspeed1_003_1.inputs if input_.identifier=='Z'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.10946200042963028
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Z'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        output = next((output for output in animtexuvscrollspeed1_003_1.outputs if output.identifier=='Vector'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0)
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Vector'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        separate_xyz_1 = node_tree1.nodes.new('ShaderNodeSeparateXYZ')
        if hasattr(separate_xyz_1, 'color'):
            separate_xyz_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(separate_xyz_1, 'hide'):
            separate_xyz_1.hide = False
        if hasattr(separate_xyz_1, 'location'):
            separate_xyz_1.location = (-880.9576416015625, 737.3845825195312)
        if hasattr(separate_xyz_1, 'mute'):
            separate_xyz_1.mute = False
        if hasattr(separate_xyz_1, 'name'):
            separate_xyz_1.name = 'Separate XYZ'
        if hasattr(separate_xyz_1, 'status'):
            separate_xyz_1.status = False
        if hasattr(separate_xyz_1, 'use_custom_color'):
            separate_xyz_1.use_custom_color = False
        if hasattr(separate_xyz_1, 'width'):
            separate_xyz_1.width = 100.0
        input_ = next((input_ for input_ in separate_xyz_1.inputs if input_.identifier=='Vector'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        output = next((output for output in separate_xyz_1.outputs if output.identifier=='X'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'X'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False
        output = next((output for output in separate_xyz_1.outputs if output.identifier=='Y'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Y'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False
        output = next((output for output in separate_xyz_1.outputs if output.identifier=='Z'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Z'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        vector_math_1 = node_tree1.nodes.new('ShaderNodeVectorMath')
        if hasattr(vector_math_1, 'color'):
            vector_math_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(vector_math_1, 'hide'):
            vector_math_1.hide = False
        if hasattr(vector_math_1, 'location'):
            vector_math_1.location = (-526.878662109375, 697.3845825195312)
        if hasattr(vector_math_1, 'mute'):
            vector_math_1.mute = False
        if hasattr(vector_math_1, 'name'):
            vector_math_1.name = 'Vector Math'
        if hasattr(vector_math_1, 'operation'):
            vector_math_1.operation = 'MULTIPLY'
        if hasattr(vector_math_1, 'status'):
            vector_math_1.status = False
        if hasattr(vector_math_1, 'use_custom_color'):
            vector_math_1.use_custom_color = False
        if hasattr(vector_math_1, 'width'):
            vector_math_1.width = 100.0
        input_ = next((input_ for input_ in vector_math_1.inputs if input_.identifier=='Vector'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_1.inputs if input_.identifier=='Vector_001'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_1.inputs if input_.identifier=='Vector_002'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_1.inputs if input_.identifier=='Scale'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 1.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Scale'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        output = next((output for output in vector_math_1.outputs if output.identifier=='Vector'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0)
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Vector'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False
        output = next((output for output in vector_math_1.outputs if output.identifier=='Value'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = False
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Value'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        group_input_002_1 = node_tree1.nodes.new('NodeGroupInput')
        if hasattr(group_input_002_1, 'color'):
            group_input_002_1.color = (0.3999914526939392, 0.0, 0.0)
        if hasattr(group_input_002_1, 'hide'):
            group_input_002_1.hide = False
        if hasattr(group_input_002_1, 'location'):
            group_input_002_1.location = (-1215.9871826171875, 622.9918823242188)
        if hasattr(group_input_002_1, 'mute'):
            group_input_002_1.mute = False
        if hasattr(group_input_002_1, 'name'):
            group_input_002_1.name = 'Group Input.002'
        if hasattr(group_input_002_1, 'status'):
            group_input_002_1.status = False
        if hasattr(group_input_002_1, 'use_custom_color'):
            group_input_002_1.use_custom_color = True
        if hasattr(group_input_002_1, 'width'):
            group_input_002_1.width = 201.4150390625
        if hasattr(group_input_002_1.outputs[0], 'default_value'):
            group_input_002_1.outputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_002_1.outputs[0], 'display_shape'):
            group_input_002_1.outputs[0].display_shape = 'CIRCLE'
        if hasattr(group_input_002_1.outputs[0], 'enabled'):
            group_input_002_1.outputs[0].enabled = True
        if hasattr(group_input_002_1.outputs[0], 'hide'):
            group_input_002_1.outputs[0].hide = False
        if hasattr(group_input_002_1.outputs[0], 'hide_value'):
            group_input_002_1.outputs[0].hide_value = True
        if hasattr(group_input_002_1.outputs[0], 'name'):
            group_input_002_1.outputs[0].name = '_d DiffuseMap Color'
        if hasattr(group_input_002_1.outputs[0], 'show_expanded'):
            group_input_002_1.outputs[0].show_expanded = False
        if hasattr(group_input_002_1.outputs[1], 'default_value'):
            group_input_002_1.outputs[1].default_value = 0.0
        if hasattr(group_input_002_1.outputs[1], 'display_shape'):
            group_input_002_1.outputs[1].display_shape = 'CIRCLE'
        if hasattr(group_input_002_1.outputs[1], 'enabled'):
            group_input_002_1.outputs[1].enabled = True
        if hasattr(group_input_002_1.outputs[1], 'hide'):
            group_input_002_1.outputs[1].hide = True
        if hasattr(group_input_002_1.outputs[1], 'hide_value'):
            group_input_002_1.outputs[1].hide_value = False
        if hasattr(group_input_002_1.outputs[1], 'name'):
            group_input_002_1.outputs[1].name = '_d DiffuseMap Alpha'
        if hasattr(group_input_002_1.outputs[1], 'show_expanded'):
            group_input_002_1.outputs[1].show_expanded = False
        if hasattr(group_input_002_1.outputs[2], 'default_value'):
            group_input_002_1.outputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_002_1.outputs[2], 'display_shape'):
            group_input_002_1.outputs[2].display_shape = 'CIRCLE'
        if hasattr(group_input_002_1.outputs[2], 'enabled'):
            group_input_002_1.outputs[2].enabled = True
        if hasattr(group_input_002_1.outputs[2], 'hide'):
            group_input_002_1.outputs[2].hide = True
        if hasattr(group_input_002_1.outputs[2], 'hide_value'):
            group_input_002_1.outputs[2].hide_value = False
        if hasattr(group_input_002_1.outputs[2], 'name'):
            group_input_002_1.outputs[2].name = 'AnimatedTexture1 Color'
        if hasattr(group_input_002_1.outputs[2], 'show_expanded'):
            group_input_002_1.outputs[2].show_expanded = False
        if hasattr(group_input_002_1.outputs[3], 'default_value'):
            group_input_002_1.outputs[3].default_value = 0.0
        if hasattr(group_input_002_1.outputs[3], 'display_shape'):
            group_input_002_1.outputs[3].display_shape = 'CIRCLE'
        if hasattr(group_input_002_1.outputs[3], 'enabled'):
            group_input_002_1.outputs[3].enabled = True
        if hasattr(group_input_002_1.outputs[3], 'hide'):
            group_input_002_1.outputs[3].hide = False
        if hasattr(group_input_002_1.outputs[3], 'hide_value'):
            group_input_002_1.outputs[3].hide_value = False
        if hasattr(group_input_002_1.outputs[3], 'name'):
            group_input_002_1.outputs[3].name = 'AnimatedTexture1 Alpha'
        if hasattr(group_input_002_1.outputs[3], 'show_expanded'):
            group_input_002_1.outputs[3].show_expanded = False
        if hasattr(group_input_002_1.outputs[4], 'default_value'):
            group_input_002_1.outputs[4].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_002_1.outputs[4], 'display_shape'):
            group_input_002_1.outputs[4].display_shape = 'CIRCLE'
        if hasattr(group_input_002_1.outputs[4], 'enabled'):
            group_input_002_1.outputs[4].enabled = True
        if hasattr(group_input_002_1.outputs[4], 'hide'):
            group_input_002_1.outputs[4].hide = True
        if hasattr(group_input_002_1.outputs[4], 'hide_value'):
            group_input_002_1.outputs[4].hide_value = False
        if hasattr(group_input_002_1.outputs[4], 'name'):
            group_input_002_1.outputs[4].name = 'AnimatedTexture2 Color'
        if hasattr(group_input_002_1.outputs[4], 'show_expanded'):
            group_input_002_1.outputs[4].show_expanded = False
        if hasattr(group_input_002_1.outputs[5], 'default_value'):
            group_input_002_1.outputs[5].default_value = 0.0
        if hasattr(group_input_002_1.outputs[5], 'display_shape'):
            group_input_002_1.outputs[5].display_shape = 'CIRCLE'
        if hasattr(group_input_002_1.outputs[5], 'enabled'):
            group_input_002_1.outputs[5].enabled = True
        if hasattr(group_input_002_1.outputs[5], 'hide'):
            group_input_002_1.outputs[5].hide = True
        if hasattr(group_input_002_1.outputs[5], 'hide_value'):
            group_input_002_1.outputs[5].hide_value = False
        if hasattr(group_input_002_1.outputs[5], 'name'):
            group_input_002_1.outputs[5].name = 'AnimatedTexture2 Alpha'
        if hasattr(group_input_002_1.outputs[5], 'show_expanded'):
            group_input_002_1.outputs[5].show_expanded = False
        if hasattr(group_input_002_1.outputs[6], 'default_value'):
            group_input_002_1.outputs[6].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_002_1.outputs[6], 'display_shape'):
            group_input_002_1.outputs[6].display_shape = 'CIRCLE'
        if hasattr(group_input_002_1.outputs[6], 'enabled'):
            group_input_002_1.outputs[6].enabled = True
        if hasattr(group_input_002_1.outputs[6], 'hide'):
            group_input_002_1.outputs[6].hide = False
        if hasattr(group_input_002_1.outputs[6], 'hide_value'):
            group_input_002_1.outputs[6].hide_value = False
        if hasattr(group_input_002_1.outputs[6], 'name'):
            group_input_002_1.outputs[6].name = 'animTexTint0'
        if hasattr(group_input_002_1.outputs[6], 'show_expanded'):
            group_input_002_1.outputs[6].show_expanded = False
        if hasattr(group_input_002_1.outputs[7], 'default_value'):
            group_input_002_1.outputs[7].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_002_1.outputs[7], 'display_shape'):
            group_input_002_1.outputs[7].display_shape = 'CIRCLE'
        if hasattr(group_input_002_1.outputs[7], 'enabled'):
            group_input_002_1.outputs[7].enabled = True
        if hasattr(group_input_002_1.outputs[7], 'hide'):
            group_input_002_1.outputs[7].hide = True
        if hasattr(group_input_002_1.outputs[7], 'hide_value'):
            group_input_002_1.outputs[7].hide_value = False
        if hasattr(group_input_002_1.outputs[7], 'name'):
            group_input_002_1.outputs[7].name = 'animTexTint1'
        if hasattr(group_input_002_1.outputs[7], 'show_expanded'):
            group_input_002_1.outputs[7].show_expanded = False
        if hasattr(group_input_002_1.outputs[8], 'default_value'):
            group_input_002_1.outputs[8].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_002_1.outputs[8], 'display_shape'):
            group_input_002_1.outputs[8].display_shape = 'CIRCLE'
        if hasattr(group_input_002_1.outputs[8], 'enabled'):
            group_input_002_1.outputs[8].enabled = True
        if hasattr(group_input_002_1.outputs[8], 'hide'):
            group_input_002_1.outputs[8].hide = True
        if hasattr(group_input_002_1.outputs[8], 'hide_value'):
            group_input_002_1.outputs[8].hide_value = False
        if hasattr(group_input_002_1.outputs[8], 'name'):
            group_input_002_1.outputs[8].name = 'animTexTint2'
        if hasattr(group_input_002_1.outputs[8], 'show_expanded'):
            group_input_002_1.outputs[8].show_expanded = False
        if hasattr(group_input_002_1.outputs[9], 'default_value'):
            group_input_002_1.outputs[9].default_value = 0.0
        if hasattr(group_input_002_1.outputs[9], 'display_shape'):
            group_input_002_1.outputs[9].display_shape = 'CIRCLE'
        if hasattr(group_input_002_1.outputs[9], 'enabled'):
            group_input_002_1.outputs[9].enabled = True
        if hasattr(group_input_002_1.outputs[9], 'hide'):
            group_input_002_1.outputs[9].hide = True
        if hasattr(group_input_002_1.outputs[9], 'hide_value'):
            group_input_002_1.outputs[9].hide_value = True
        if hasattr(group_input_002_1.outputs[9], 'name'):
            group_input_002_1.outputs[9].name = '—— EXTRAS ——'
        if hasattr(group_input_002_1.outputs[9], 'show_expanded'):
            group_input_002_1.outputs[9].show_expanded = False
        if hasattr(group_input_002_1.outputs[10], 'default_value'):
            group_input_002_1.outputs[10].default_value = 1.0
        if hasattr(group_input_002_1.outputs[10], 'display_shape'):
            group_input_002_1.outputs[10].display_shape = 'CIRCLE'
        if hasattr(group_input_002_1.outputs[10], 'enabled'):
            group_input_002_1.outputs[10].enabled = True
        if hasattr(group_input_002_1.outputs[10], 'hide'):
            group_input_002_1.outputs[10].hide = True
        if hasattr(group_input_002_1.outputs[10], 'hide_value'):
            group_input_002_1.outputs[10].hide_value = False
        if hasattr(group_input_002_1.outputs[10], 'name'):
            group_input_002_1.outputs[10].name = 'Roughness Factor'
        if hasattr(group_input_002_1.outputs[10], 'show_expanded'):
            group_input_002_1.outputs[10].show_expanded = False
        if hasattr(group_input_002_1.outputs[11], 'default_value'):
            group_input_002_1.outputs[11].default_value = 1.0
        if hasattr(group_input_002_1.outputs[11], 'display_shape'):
            group_input_002_1.outputs[11].display_shape = 'CIRCLE'
        if hasattr(group_input_002_1.outputs[11], 'enabled'):
            group_input_002_1.outputs[11].enabled = True
        if hasattr(group_input_002_1.outputs[11], 'hide'):
            group_input_002_1.outputs[11].hide = True
        if hasattr(group_input_002_1.outputs[11], 'hide_value'):
            group_input_002_1.outputs[11].hide_value = False
        if hasattr(group_input_002_1.outputs[11], 'name'):
            group_input_002_1.outputs[11].name = 'Emission Strength'
        if hasattr(group_input_002_1.outputs[11], 'show_expanded'):
            group_input_002_1.outputs[11].show_expanded = False
        if hasattr(group_input_002_1.outputs[12], 'default_value'):
            group_input_002_1.outputs[12].default_value = 1.0
        if hasattr(group_input_002_1.outputs[12], 'display_shape'):
            group_input_002_1.outputs[12].display_shape = 'CIRCLE'
        if hasattr(group_input_002_1.outputs[12], 'enabled'):
            group_input_002_1.outputs[12].enabled = True
        if hasattr(group_input_002_1.outputs[12], 'hide'):
            group_input_002_1.outputs[12].hide = True
        if hasattr(group_input_002_1.outputs[12], 'hide_value'):
            group_input_002_1.outputs[12].hide_value = False
        if hasattr(group_input_002_1.outputs[12], 'name'):
            group_input_002_1.outputs[12].name = 'Backface Culling Factor'
        if hasattr(group_input_002_1.outputs[12], 'show_expanded'):
            group_input_002_1.outputs[12].show_expanded = False

        vector_math_004_1 = node_tree1.nodes.new('ShaderNodeVectorMath')
        if hasattr(vector_math_004_1, 'color'):
            vector_math_004_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(vector_math_004_1, 'hide'):
            vector_math_004_1.hide = False
        if hasattr(vector_math_004_1, 'location'):
            vector_math_004_1.location = (-340.0, 639.813720703125)
        if hasattr(vector_math_004_1, 'mute'):
            vector_math_004_1.mute = False
        if hasattr(vector_math_004_1, 'name'):
            vector_math_004_1.name = 'Vector Math.004'
        if hasattr(vector_math_004_1, 'operation'):
            vector_math_004_1.operation = 'ADD'
        if hasattr(vector_math_004_1, 'status'):
            vector_math_004_1.status = False
        if hasattr(vector_math_004_1, 'use_custom_color'):
            vector_math_004_1.use_custom_color = False
        if hasattr(vector_math_004_1, 'width'):
            vector_math_004_1.width = 100.0
        input_ = next((input_ for input_ in vector_math_004_1.inputs if input_.identifier=='Vector'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_004_1.inputs if input_.identifier=='Vector_001'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_004_1.inputs if input_.identifier=='Vector_002'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Vector'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in vector_math_004_1.inputs if input_.identifier=='Scale'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 1.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = False
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Scale'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        output = next((output for output in vector_math_004_1.outputs if output.identifier=='Vector'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = (0.0, 0.0, 0.0)
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = True
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Vector'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False
        output = next((output for output in vector_math_004_1.outputs if output.identifier=='Value'), None)
        if output:
            if hasattr(output, 'default_value'):
                output.default_value = 0.0
            if hasattr(output, 'display_shape'):
                output.display_shape = 'CIRCLE'
            if hasattr(output, 'enabled'):
                output.enabled = False
            if hasattr(output, 'hide'):
                output.hide = False
            if hasattr(output, 'hide_value'):
                output.hide_value = False
            if hasattr(output, 'name'):
                output.name = 'Value'
            if hasattr(output, 'show_expanded'):
                output.show_expanded = False

        principled_bsdf_001_1 = node_tree1.nodes.new('ShaderNodeBsdfPrincipled')
        if hasattr(principled_bsdf_001_1, 'color'):
            principled_bsdf_001_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
        if hasattr(principled_bsdf_001_1, 'distribution'):
            principled_bsdf_001_1.distribution = 'GGX'
        if hasattr(principled_bsdf_001_1, 'hide'):
            principled_bsdf_001_1.hide = False
        if hasattr(principled_bsdf_001_1, 'location'):
            principled_bsdf_001_1.location = (687.1092529296875, 766.784912109375)
        if hasattr(principled_bsdf_001_1, 'mute'):
            principled_bsdf_001_1.mute = False
        if hasattr(principled_bsdf_001_1, 'name'):
            principled_bsdf_001_1.name = 'Principled BSDF.001'
        if hasattr(principled_bsdf_001_1, 'status'):
            principled_bsdf_001_1.status = False
        if hasattr(principled_bsdf_001_1, 'subsurface_method'):
            principled_bsdf_001_1.subsurface_method = 'RANDOM_WALK_SKIN'
        if hasattr(principled_bsdf_001_1, 'use_custom_color'):
            principled_bsdf_001_1.use_custom_color = False
        if hasattr(principled_bsdf_001_1, 'width'):
            principled_bsdf_001_1.width = 240.0
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Base Color'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0, 1.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Base Color'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Metallic'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Metallic'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Roughness'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 1.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Roughness'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='IOR'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 1.4500000476837158
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'IOR'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Alpha'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 1.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Alpha'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Normal'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = True
            if hasattr(input_, 'name'):
                input_.name = 'Normal'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Weight'), None)
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
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Subsurface Weight'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Subsurface Weight'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Subsurface Radius'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Subsurface Radius'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Subsurface Scale'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.05000000074505806
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Subsurface Scale'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Subsurface IOR'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 1.399999976158142
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Subsurface IOR'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Subsurface Anisotropy'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Subsurface Anisotropy'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Specular IOR Level'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.5
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Specular IOR Level'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Specular Tint'), None)
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
                input_.name = 'Specular Tint'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Anisotropic'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Anisotropic'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Anisotropic Rotation'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Anisotropic Rotation'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Tangent'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = True
            if hasattr(input_, 'name'):
                input_.name = 'Tangent'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Transmission Weight'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Transmission Weight'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Coat Weight'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Coat Weight'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Coat Roughness'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.029999999329447746
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Coat Roughness'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Coat IOR'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 1.5
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Coat IOR'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Coat Tint'), None)
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
                input_.name = 'Coat Tint'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Coat Normal'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = True
            if hasattr(input_, 'name'):
                input_.name = 'Coat Normal'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Sheen Weight'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Sheen Weight'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Sheen Roughness'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 0.5
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Sheen Roughness'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Sheen Tint'), None)
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
                input_.name = 'Sheen Tint'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Emission Color'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = (0.0, 0.0, 0.0, 1.0)
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Emission Color'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False
        input_ = next((input_ for input_ in principled_bsdf_001_1.inputs if input_.identifier=='Emission Strength'), None)
        if input_:
            if hasattr(input_, 'default_value'):
                input_.default_value = 1.0
            if hasattr(input_, 'display_shape'):
                input_.display_shape = 'CIRCLE'
            if hasattr(input_, 'enabled'):
                input_.enabled = True
            if hasattr(input_, 'hide'):
                input_.hide = False
            if hasattr(input_, 'hide_value'):
                input_.hide_value = False
            if hasattr(input_, 'name'):
                input_.name = 'Emission Strength'
            if hasattr(input_, 'show_expanded'):
                input_.show_expanded = False

        group_input_004_1 = node_tree1.nodes.new('NodeGroupInput')
        if hasattr(group_input_004_1, 'color'):
            group_input_004_1.color = (0.3999914526939392, 0.0, 0.0)
        if hasattr(group_input_004_1, 'hide'):
            group_input_004_1.hide = False
        if hasattr(group_input_004_1, 'location'):
            group_input_004_1.location = (805.8388671875, 380.9047546386719)
        if hasattr(group_input_004_1, 'mute'):
            group_input_004_1.mute = False
        if hasattr(group_input_004_1, 'name'):
            group_input_004_1.name = 'Group Input.004'
        if hasattr(group_input_004_1, 'status'):
            group_input_004_1.status = False
        if hasattr(group_input_004_1, 'use_custom_color'):
            group_input_004_1.use_custom_color = True
        if hasattr(group_input_004_1, 'width'):
            group_input_004_1.width = 153.34161376953125
        if hasattr(group_input_004_1.outputs[0], 'default_value'):
            group_input_004_1.outputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_004_1.outputs[0], 'display_shape'):
            group_input_004_1.outputs[0].display_shape = 'CIRCLE'
        if hasattr(group_input_004_1.outputs[0], 'enabled'):
            group_input_004_1.outputs[0].enabled = True
        if hasattr(group_input_004_1.outputs[0], 'hide'):
            group_input_004_1.outputs[0].hide = True
        if hasattr(group_input_004_1.outputs[0], 'hide_value'):
            group_input_004_1.outputs[0].hide_value = True
        if hasattr(group_input_004_1.outputs[0], 'name'):
            group_input_004_1.outputs[0].name = '_d DiffuseMap Color'
        if hasattr(group_input_004_1.outputs[0], 'show_expanded'):
            group_input_004_1.outputs[0].show_expanded = False
        if hasattr(group_input_004_1.outputs[1], 'default_value'):
            group_input_004_1.outputs[1].default_value = 0.0
        if hasattr(group_input_004_1.outputs[1], 'display_shape'):
            group_input_004_1.outputs[1].display_shape = 'CIRCLE'
        if hasattr(group_input_004_1.outputs[1], 'enabled'):
            group_input_004_1.outputs[1].enabled = True
        if hasattr(group_input_004_1.outputs[1], 'hide'):
            group_input_004_1.outputs[1].hide = True
        if hasattr(group_input_004_1.outputs[1], 'hide_value'):
            group_input_004_1.outputs[1].hide_value = False
        if hasattr(group_input_004_1.outputs[1], 'name'):
            group_input_004_1.outputs[1].name = '_d DiffuseMap Alpha'
        if hasattr(group_input_004_1.outputs[1], 'show_expanded'):
            group_input_004_1.outputs[1].show_expanded = False
        if hasattr(group_input_004_1.outputs[2], 'default_value'):
            group_input_004_1.outputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_004_1.outputs[2], 'display_shape'):
            group_input_004_1.outputs[2].display_shape = 'CIRCLE'
        if hasattr(group_input_004_1.outputs[2], 'enabled'):
            group_input_004_1.outputs[2].enabled = True
        if hasattr(group_input_004_1.outputs[2], 'hide'):
            group_input_004_1.outputs[2].hide = True
        if hasattr(group_input_004_1.outputs[2], 'hide_value'):
            group_input_004_1.outputs[2].hide_value = False
        if hasattr(group_input_004_1.outputs[2], 'name'):
            group_input_004_1.outputs[2].name = 'AnimatedTexture1 Color'
        if hasattr(group_input_004_1.outputs[2], 'show_expanded'):
            group_input_004_1.outputs[2].show_expanded = False
        if hasattr(group_input_004_1.outputs[3], 'default_value'):
            group_input_004_1.outputs[3].default_value = 0.0
        if hasattr(group_input_004_1.outputs[3], 'display_shape'):
            group_input_004_1.outputs[3].display_shape = 'CIRCLE'
        if hasattr(group_input_004_1.outputs[3], 'enabled'):
            group_input_004_1.outputs[3].enabled = True
        if hasattr(group_input_004_1.outputs[3], 'hide'):
            group_input_004_1.outputs[3].hide = False
        if hasattr(group_input_004_1.outputs[3], 'hide_value'):
            group_input_004_1.outputs[3].hide_value = False
        if hasattr(group_input_004_1.outputs[3], 'name'):
            group_input_004_1.outputs[3].name = 'AnimatedTexture1 Alpha'
        if hasattr(group_input_004_1.outputs[3], 'show_expanded'):
            group_input_004_1.outputs[3].show_expanded = False
        if hasattr(group_input_004_1.outputs[4], 'default_value'):
            group_input_004_1.outputs[4].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_004_1.outputs[4], 'display_shape'):
            group_input_004_1.outputs[4].display_shape = 'CIRCLE'
        if hasattr(group_input_004_1.outputs[4], 'enabled'):
            group_input_004_1.outputs[4].enabled = True
        if hasattr(group_input_004_1.outputs[4], 'hide'):
            group_input_004_1.outputs[4].hide = True
        if hasattr(group_input_004_1.outputs[4], 'hide_value'):
            group_input_004_1.outputs[4].hide_value = False
        if hasattr(group_input_004_1.outputs[4], 'name'):
            group_input_004_1.outputs[4].name = 'AnimatedTexture2 Color'
        if hasattr(group_input_004_1.outputs[4], 'show_expanded'):
            group_input_004_1.outputs[4].show_expanded = False
        if hasattr(group_input_004_1.outputs[5], 'default_value'):
            group_input_004_1.outputs[5].default_value = 0.0
        if hasattr(group_input_004_1.outputs[5], 'display_shape'):
            group_input_004_1.outputs[5].display_shape = 'CIRCLE'
        if hasattr(group_input_004_1.outputs[5], 'enabled'):
            group_input_004_1.outputs[5].enabled = True
        if hasattr(group_input_004_1.outputs[5], 'hide'):
            group_input_004_1.outputs[5].hide = True
        if hasattr(group_input_004_1.outputs[5], 'hide_value'):
            group_input_004_1.outputs[5].hide_value = False
        if hasattr(group_input_004_1.outputs[5], 'name'):
            group_input_004_1.outputs[5].name = 'AnimatedTexture2 Alpha'
        if hasattr(group_input_004_1.outputs[5], 'show_expanded'):
            group_input_004_1.outputs[5].show_expanded = False
        if hasattr(group_input_004_1.outputs[6], 'default_value'):
            group_input_004_1.outputs[6].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_004_1.outputs[6], 'display_shape'):
            group_input_004_1.outputs[6].display_shape = 'CIRCLE'
        if hasattr(group_input_004_1.outputs[6], 'enabled'):
            group_input_004_1.outputs[6].enabled = True
        if hasattr(group_input_004_1.outputs[6], 'hide'):
            group_input_004_1.outputs[6].hide = True
        if hasattr(group_input_004_1.outputs[6], 'hide_value'):
            group_input_004_1.outputs[6].hide_value = False
        if hasattr(group_input_004_1.outputs[6], 'name'):
            group_input_004_1.outputs[6].name = 'animTexTint0'
        if hasattr(group_input_004_1.outputs[6], 'show_expanded'):
            group_input_004_1.outputs[6].show_expanded = False
        if hasattr(group_input_004_1.outputs[7], 'default_value'):
            group_input_004_1.outputs[7].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_004_1.outputs[7], 'display_shape'):
            group_input_004_1.outputs[7].display_shape = 'CIRCLE'
        if hasattr(group_input_004_1.outputs[7], 'enabled'):
            group_input_004_1.outputs[7].enabled = True
        if hasattr(group_input_004_1.outputs[7], 'hide'):
            group_input_004_1.outputs[7].hide = False
        if hasattr(group_input_004_1.outputs[7], 'hide_value'):
            group_input_004_1.outputs[7].hide_value = False
        if hasattr(group_input_004_1.outputs[7], 'name'):
            group_input_004_1.outputs[7].name = 'animTexTint1'
        if hasattr(group_input_004_1.outputs[7], 'show_expanded'):
            group_input_004_1.outputs[7].show_expanded = False
        if hasattr(group_input_004_1.outputs[8], 'default_value'):
            group_input_004_1.outputs[8].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_004_1.outputs[8], 'display_shape'):
            group_input_004_1.outputs[8].display_shape = 'CIRCLE'
        if hasattr(group_input_004_1.outputs[8], 'enabled'):
            group_input_004_1.outputs[8].enabled = True
        if hasattr(group_input_004_1.outputs[8], 'hide'):
            group_input_004_1.outputs[8].hide = True
        if hasattr(group_input_004_1.outputs[8], 'hide_value'):
            group_input_004_1.outputs[8].hide_value = False
        if hasattr(group_input_004_1.outputs[8], 'name'):
            group_input_004_1.outputs[8].name = 'animTexTint2'
        if hasattr(group_input_004_1.outputs[8], 'show_expanded'):
            group_input_004_1.outputs[8].show_expanded = False
        if hasattr(group_input_004_1.outputs[9], 'default_value'):
            group_input_004_1.outputs[9].default_value = 0.0
        if hasattr(group_input_004_1.outputs[9], 'display_shape'):
            group_input_004_1.outputs[9].display_shape = 'CIRCLE'
        if hasattr(group_input_004_1.outputs[9], 'enabled'):
            group_input_004_1.outputs[9].enabled = True
        if hasattr(group_input_004_1.outputs[9], 'hide'):
            group_input_004_1.outputs[9].hide = True
        if hasattr(group_input_004_1.outputs[9], 'hide_value'):
            group_input_004_1.outputs[9].hide_value = True
        if hasattr(group_input_004_1.outputs[9], 'name'):
            group_input_004_1.outputs[9].name = '—— EXTRAS ——'
        if hasattr(group_input_004_1.outputs[9], 'show_expanded'):
            group_input_004_1.outputs[9].show_expanded = False
        if hasattr(group_input_004_1.outputs[10], 'default_value'):
            group_input_004_1.outputs[10].default_value = 1.0
        if hasattr(group_input_004_1.outputs[10], 'display_shape'):
            group_input_004_1.outputs[10].display_shape = 'CIRCLE'
        if hasattr(group_input_004_1.outputs[10], 'enabled'):
            group_input_004_1.outputs[10].enabled = True
        if hasattr(group_input_004_1.outputs[10], 'hide'):
            group_input_004_1.outputs[10].hide = True
        if hasattr(group_input_004_1.outputs[10], 'hide_value'):
            group_input_004_1.outputs[10].hide_value = False
        if hasattr(group_input_004_1.outputs[10], 'name'):
            group_input_004_1.outputs[10].name = 'Roughness Factor'
        if hasattr(group_input_004_1.outputs[10], 'show_expanded'):
            group_input_004_1.outputs[10].show_expanded = False
        if hasattr(group_input_004_1.outputs[11], 'default_value'):
            group_input_004_1.outputs[11].default_value = 1.0
        if hasattr(group_input_004_1.outputs[11], 'display_shape'):
            group_input_004_1.outputs[11].display_shape = 'CIRCLE'
        if hasattr(group_input_004_1.outputs[11], 'enabled'):
            group_input_004_1.outputs[11].enabled = True
        if hasattr(group_input_004_1.outputs[11], 'hide'):
            group_input_004_1.outputs[11].hide = True
        if hasattr(group_input_004_1.outputs[11], 'hide_value'):
            group_input_004_1.outputs[11].hide_value = False
        if hasattr(group_input_004_1.outputs[11], 'name'):
            group_input_004_1.outputs[11].name = 'Emission Strength'
        if hasattr(group_input_004_1.outputs[11], 'show_expanded'):
            group_input_004_1.outputs[11].show_expanded = False
        if hasattr(group_input_004_1.outputs[12], 'default_value'):
            group_input_004_1.outputs[12].default_value = 1.0
        if hasattr(group_input_004_1.outputs[12], 'display_shape'):
            group_input_004_1.outputs[12].display_shape = 'CIRCLE'
        if hasattr(group_input_004_1.outputs[12], 'enabled'):
            group_input_004_1.outputs[12].enabled = True
        if hasattr(group_input_004_1.outputs[12], 'hide'):
            group_input_004_1.outputs[12].hide = False
        if hasattr(group_input_004_1.outputs[12], 'hide_value'):
            group_input_004_1.outputs[12].hide_value = False
        if hasattr(group_input_004_1.outputs[12], 'name'):
            group_input_004_1.outputs[12].name = 'Backface Culling Factor'
        if hasattr(group_input_004_1.outputs[12], 'show_expanded'):
            group_input_004_1.outputs[12].show_expanded = False

        group_input_003_1 = node_tree1.nodes.new('NodeGroupInput')
        if hasattr(group_input_003_1, 'color'):
            group_input_003_1.color = (0.3999914526939392, 0.0, 0.0)
        if hasattr(group_input_003_1, 'hide'):
            group_input_003_1.hide = False
        if hasattr(group_input_003_1, 'location'):
            group_input_003_1.location = (458.5509033203125, 612.1364135742188)
        if hasattr(group_input_003_1, 'mute'):
            group_input_003_1.mute = False
        if hasattr(group_input_003_1, 'name'):
            group_input_003_1.name = 'Group Input.003'
        if hasattr(group_input_003_1, 'status'):
            group_input_003_1.status = False
        if hasattr(group_input_003_1, 'use_custom_color'):
            group_input_003_1.use_custom_color = True
        if hasattr(group_input_003_1, 'width'):
            group_input_003_1.width = 126.0262451171875
        if hasattr(group_input_003_1.outputs[0], 'default_value'):
            group_input_003_1.outputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_003_1.outputs[0], 'display_shape'):
            group_input_003_1.outputs[0].display_shape = 'CIRCLE'
        if hasattr(group_input_003_1.outputs[0], 'enabled'):
            group_input_003_1.outputs[0].enabled = True
        if hasattr(group_input_003_1.outputs[0], 'hide'):
            group_input_003_1.outputs[0].hide = True
        if hasattr(group_input_003_1.outputs[0], 'hide_value'):
            group_input_003_1.outputs[0].hide_value = True
        if hasattr(group_input_003_1.outputs[0], 'name'):
            group_input_003_1.outputs[0].name = '_d DiffuseMap Color'
        if hasattr(group_input_003_1.outputs[0], 'show_expanded'):
            group_input_003_1.outputs[0].show_expanded = False
        if hasattr(group_input_003_1.outputs[1], 'default_value'):
            group_input_003_1.outputs[1].default_value = 0.0
        if hasattr(group_input_003_1.outputs[1], 'display_shape'):
            group_input_003_1.outputs[1].display_shape = 'CIRCLE'
        if hasattr(group_input_003_1.outputs[1], 'enabled'):
            group_input_003_1.outputs[1].enabled = True
        if hasattr(group_input_003_1.outputs[1], 'hide'):
            group_input_003_1.outputs[1].hide = True
        if hasattr(group_input_003_1.outputs[1], 'hide_value'):
            group_input_003_1.outputs[1].hide_value = False
        if hasattr(group_input_003_1.outputs[1], 'name'):
            group_input_003_1.outputs[1].name = '_d DiffuseMap Alpha'
        if hasattr(group_input_003_1.outputs[1], 'show_expanded'):
            group_input_003_1.outputs[1].show_expanded = False
        if hasattr(group_input_003_1.outputs[2], 'default_value'):
            group_input_003_1.outputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_003_1.outputs[2], 'display_shape'):
            group_input_003_1.outputs[2].display_shape = 'CIRCLE'
        if hasattr(group_input_003_1.outputs[2], 'enabled'):
            group_input_003_1.outputs[2].enabled = True
        if hasattr(group_input_003_1.outputs[2], 'hide'):
            group_input_003_1.outputs[2].hide = True
        if hasattr(group_input_003_1.outputs[2], 'hide_value'):
            group_input_003_1.outputs[2].hide_value = False
        if hasattr(group_input_003_1.outputs[2], 'name'):
            group_input_003_1.outputs[2].name = 'AnimatedTexture1 Color'
        if hasattr(group_input_003_1.outputs[2], 'show_expanded'):
            group_input_003_1.outputs[2].show_expanded = False
        if hasattr(group_input_003_1.outputs[3], 'default_value'):
            group_input_003_1.outputs[3].default_value = 0.0
        if hasattr(group_input_003_1.outputs[3], 'display_shape'):
            group_input_003_1.outputs[3].display_shape = 'CIRCLE'
        if hasattr(group_input_003_1.outputs[3], 'enabled'):
            group_input_003_1.outputs[3].enabled = True
        if hasattr(group_input_003_1.outputs[3], 'hide'):
            group_input_003_1.outputs[3].hide = False
        if hasattr(group_input_003_1.outputs[3], 'hide_value'):
            group_input_003_1.outputs[3].hide_value = False
        if hasattr(group_input_003_1.outputs[3], 'name'):
            group_input_003_1.outputs[3].name = 'AnimatedTexture1 Alpha'
        if hasattr(group_input_003_1.outputs[3], 'show_expanded'):
            group_input_003_1.outputs[3].show_expanded = False
        if hasattr(group_input_003_1.outputs[4], 'default_value'):
            group_input_003_1.outputs[4].default_value = (0.0, 0.0, 0.0, 1.0)
        if hasattr(group_input_003_1.outputs[4], 'display_shape'):
            group_input_003_1.outputs[4].display_shape = 'CIRCLE'
        if hasattr(group_input_003_1.outputs[4], 'enabled'):
            group_input_003_1.outputs[4].enabled = True
        if hasattr(group_input_003_1.outputs[4], 'hide'):
            group_input_003_1.outputs[4].hide = True
        if hasattr(group_input_003_1.outputs[4], 'hide_value'):
            group_input_003_1.outputs[4].hide_value = False
        if hasattr(group_input_003_1.outputs[4], 'name'):
            group_input_003_1.outputs[4].name = 'AnimatedTexture2 Color'
        if hasattr(group_input_003_1.outputs[4], 'show_expanded'):
            group_input_003_1.outputs[4].show_expanded = False
        if hasattr(group_input_003_1.outputs[5], 'default_value'):
            group_input_003_1.outputs[5].default_value = 0.0
        if hasattr(group_input_003_1.outputs[5], 'display_shape'):
            group_input_003_1.outputs[5].display_shape = 'CIRCLE'
        if hasattr(group_input_003_1.outputs[5], 'enabled'):
            group_input_003_1.outputs[5].enabled = True
        if hasattr(group_input_003_1.outputs[5], 'hide'):
            group_input_003_1.outputs[5].hide = True
        if hasattr(group_input_003_1.outputs[5], 'hide_value'):
            group_input_003_1.outputs[5].hide_value = False
        if hasattr(group_input_003_1.outputs[5], 'name'):
            group_input_003_1.outputs[5].name = 'AnimatedTexture2 Alpha'
        if hasattr(group_input_003_1.outputs[5], 'show_expanded'):
            group_input_003_1.outputs[5].show_expanded = False
        if hasattr(group_input_003_1.outputs[6], 'default_value'):
            group_input_003_1.outputs[6].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_003_1.outputs[6], 'display_shape'):
            group_input_003_1.outputs[6].display_shape = 'CIRCLE'
        if hasattr(group_input_003_1.outputs[6], 'enabled'):
            group_input_003_1.outputs[6].enabled = True
        if hasattr(group_input_003_1.outputs[6], 'hide'):
            group_input_003_1.outputs[6].hide = True
        if hasattr(group_input_003_1.outputs[6], 'hide_value'):
            group_input_003_1.outputs[6].hide_value = False
        if hasattr(group_input_003_1.outputs[6], 'name'):
            group_input_003_1.outputs[6].name = 'animTexTint0'
        if hasattr(group_input_003_1.outputs[6], 'show_expanded'):
            group_input_003_1.outputs[6].show_expanded = False
        if hasattr(group_input_003_1.outputs[7], 'default_value'):
            group_input_003_1.outputs[7].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_003_1.outputs[7], 'display_shape'):
            group_input_003_1.outputs[7].display_shape = 'CIRCLE'
        if hasattr(group_input_003_1.outputs[7], 'enabled'):
            group_input_003_1.outputs[7].enabled = True
        if hasattr(group_input_003_1.outputs[7], 'hide'):
            group_input_003_1.outputs[7].hide = False
        if hasattr(group_input_003_1.outputs[7], 'hide_value'):
            group_input_003_1.outputs[7].hide_value = False
        if hasattr(group_input_003_1.outputs[7], 'name'):
            group_input_003_1.outputs[7].name = 'animTexTint1'
        if hasattr(group_input_003_1.outputs[7], 'show_expanded'):
            group_input_003_1.outputs[7].show_expanded = False
        if hasattr(group_input_003_1.outputs[8], 'default_value'):
            group_input_003_1.outputs[8].default_value = (0.0, 0.0, 0.0)
        if hasattr(group_input_003_1.outputs[8], 'display_shape'):
            group_input_003_1.outputs[8].display_shape = 'CIRCLE'
        if hasattr(group_input_003_1.outputs[8], 'enabled'):
            group_input_003_1.outputs[8].enabled = True
        if hasattr(group_input_003_1.outputs[8], 'hide'):
            group_input_003_1.outputs[8].hide = True
        if hasattr(group_input_003_1.outputs[8], 'hide_value'):
            group_input_003_1.outputs[8].hide_value = False
        if hasattr(group_input_003_1.outputs[8], 'name'):
            group_input_003_1.outputs[8].name = 'animTexTint2'
        if hasattr(group_input_003_1.outputs[8], 'show_expanded'):
            group_input_003_1.outputs[8].show_expanded = False
        if hasattr(group_input_003_1.outputs[9], 'default_value'):
            group_input_003_1.outputs[9].default_value = 0.0
        if hasattr(group_input_003_1.outputs[9], 'display_shape'):
            group_input_003_1.outputs[9].display_shape = 'CIRCLE'
        if hasattr(group_input_003_1.outputs[9], 'enabled'):
            group_input_003_1.outputs[9].enabled = True
        if hasattr(group_input_003_1.outputs[9], 'hide'):
            group_input_003_1.outputs[9].hide = True
        if hasattr(group_input_003_1.outputs[9], 'hide_value'):
            group_input_003_1.outputs[9].hide_value = True
        if hasattr(group_input_003_1.outputs[9], 'name'):
            group_input_003_1.outputs[9].name = '—— EXTRAS ——'
        if hasattr(group_input_003_1.outputs[9], 'show_expanded'):
            group_input_003_1.outputs[9].show_expanded = False
        if hasattr(group_input_003_1.outputs[10], 'default_value'):
            group_input_003_1.outputs[10].default_value = 1.0
        if hasattr(group_input_003_1.outputs[10], 'display_shape'):
            group_input_003_1.outputs[10].display_shape = 'CIRCLE'
        if hasattr(group_input_003_1.outputs[10], 'enabled'):
            group_input_003_1.outputs[10].enabled = True
        if hasattr(group_input_003_1.outputs[10], 'hide'):
            group_input_003_1.outputs[10].hide = False
        if hasattr(group_input_003_1.outputs[10], 'hide_value'):
            group_input_003_1.outputs[10].hide_value = False
        if hasattr(group_input_003_1.outputs[10], 'name'):
            group_input_003_1.outputs[10].name = 'Roughness Factor'
        if hasattr(group_input_003_1.outputs[10], 'show_expanded'):
            group_input_003_1.outputs[10].show_expanded = False
        if hasattr(group_input_003_1.outputs[11], 'default_value'):
            group_input_003_1.outputs[11].default_value = 1.0
        if hasattr(group_input_003_1.outputs[11], 'display_shape'):
            group_input_003_1.outputs[11].display_shape = 'CIRCLE'
        if hasattr(group_input_003_1.outputs[11], 'enabled'):
            group_input_003_1.outputs[11].enabled = True
        if hasattr(group_input_003_1.outputs[11], 'hide'):
            group_input_003_1.outputs[11].hide = False
        if hasattr(group_input_003_1.outputs[11], 'hide_value'):
            group_input_003_1.outputs[11].hide_value = False
        if hasattr(group_input_003_1.outputs[11], 'name'):
            group_input_003_1.outputs[11].name = 'Emission Strength'
        if hasattr(group_input_003_1.outputs[11], 'show_expanded'):
            group_input_003_1.outputs[11].show_expanded = False
        if hasattr(group_input_003_1.outputs[12], 'default_value'):
            group_input_003_1.outputs[12].default_value = 1.0
        if hasattr(group_input_003_1.outputs[12], 'display_shape'):
            group_input_003_1.outputs[12].display_shape = 'CIRCLE'
        if hasattr(group_input_003_1.outputs[12], 'enabled'):
            group_input_003_1.outputs[12].enabled = True
        if hasattr(group_input_003_1.outputs[12], 'hide'):
            group_input_003_1.outputs[12].hide = True
        if hasattr(group_input_003_1.outputs[12], 'hide_value'):
            group_input_003_1.outputs[12].hide_value = False
        if hasattr(group_input_003_1.outputs[12], 'name'):
            group_input_003_1.outputs[12].name = 'Backface Culling Factor'
        if hasattr(group_input_003_1.outputs[12], 'show_expanded'):
            group_input_003_1.outputs[12].show_expanded = False

        # LINKS
        node_tree1.links.new(group_input_1.outputs[2], vector_math_001_1.inputs[0])
        node_tree1.links.new(animtexuvscrollspeed1_003_1.outputs[0], vector_math_1.inputs[0])
        node_tree1.links.new(vector_math_001_1.outputs[0], vector_math_002_1.inputs[0])
        node_tree1.links.new(animtexuvscrollspeed1_004_1.outputs[0], vector_math_003_1.inputs[0])
        node_tree1.links.new(vector_math_002_1.outputs[0], vector_math_003_1.inputs[1])
        node_tree1.links.new(vector_math_1.outputs[0], vector_math_004_1.inputs[0])
        node_tree1.links.new(vector_math_003_1.outputs[0], vector_math_004_1.inputs[1])
        node_tree1.links.new(animtexuvscrollspeed1_005_1.outputs[0], vector_math_005_1.inputs[0])
        node_tree1.links.new(vector_math_005_1.outputs[0], mix_1.inputs[7])
        node_tree1.links.new(vector_math_004_1.outputs[0], mix_1.inputs[6])
        node_tree1.links.new(vector_math_004_1.outputs[0], mix_1.inputs[4])
        node_tree1.links.new(vector_math_005_1.outputs[0], mix_1.inputs[5])
        node_tree1.links.new(mix_1.outputs[1], vector_math_006_1.inputs[0])
        node_tree1.links.new(mix_1.outputs[1], principled_bsdf_001_1.inputs[0])
        node_tree1.links.new(mix_1.outputs[1], principled_bsdf_001_1.inputs[26])
        node_tree1.links.new(sw_aux_backface_culling_1.outputs[0], group_output_1.inputs[0])
        node_tree1.links.new(reroute_1.outputs[0], group_output_1.inputs[2])
        node_tree1.links.new(vector_math_006_1.outputs[1], math_1.inputs[0])
        node_tree1.links.new(math_1.outputs[0], group_output_1.inputs[3])
        node_tree1.links.new(math_1.outputs[0], principled_bsdf_001_1.inputs[4])
        node_tree1.links.new(separate_xyz_1.outputs[0], animtexuvscrollspeed1_003_1.inputs[0])
        node_tree1.links.new(separate_xyz_1.outputs[1], animtexuvscrollspeed1_003_1.inputs[1])
        node_tree1.links.new(separate_xyz_1.outputs[2], animtexuvscrollspeed1_003_1.inputs[2])
        node_tree1.links.new(separate_xyz_001_1.outputs[0], animtexuvscrollspeed1_004_1.inputs[0])
        node_tree1.links.new(separate_xyz_001_1.outputs[1], animtexuvscrollspeed1_004_1.inputs[1])
        node_tree1.links.new(separate_xyz_001_1.outputs[2], animtexuvscrollspeed1_004_1.inputs[2])
        node_tree1.links.new(separate_xyz_002_1.outputs[0], animtexuvscrollspeed1_005_1.inputs[0])
        node_tree1.links.new(separate_xyz_002_1.outputs[1], animtexuvscrollspeed1_005_1.inputs[1])
        node_tree1.links.new(separate_xyz_002_1.outputs[2], animtexuvscrollspeed1_005_1.inputs[2])
        node_tree1.links.new(principled_bsdf_001_1.outputs[0], sw_aux_backface_culling_1.inputs[0])
        node_tree1.links.new(group_input_001_1.outputs[8], separate_xyz_002_1.inputs[0])
        node_tree1.links.new(group_input_001_1.outputs[4], vector_math_005_1.inputs[1])
        node_tree1.links.new(group_input_002_1.outputs[6], separate_xyz_1.inputs[0])
        node_tree1.links.new(group_input_002_1.outputs[0], vector_math_1.inputs[1])
        node_tree1.links.new(group_input_003_1.outputs[11], principled_bsdf_001_1.inputs[27])
        node_tree1.links.new(group_input_003_1.outputs[10], principled_bsdf_001_1.inputs[2])
        node_tree1.links.new(group_input_004_1.outputs[12], sw_aux_backface_culling_1.inputs[1])
        node_tree1.links.new(group_input_005_1.outputs[5], mix_1.inputs[0])
        node_tree1.links.new(group_input_1.outputs[7], separate_xyz_001_1.inputs[0])
        node_tree1.links.new(mix_1.outputs[1], reroute_1.inputs[0])

    swtor_animateduv_shader_0 = node_tree0.nodes.new('ShaderNodeGroup')
    if hasattr(swtor_animateduv_shader_0, 'node_tree'):
        swtor_animateduv_shader_0.node_tree = bpy.data.node_groups.get('SWTOR - AnimatedUV Shader')
    if hasattr(swtor_animateduv_shader_0, 'color'):
        swtor_animateduv_shader_0.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(swtor_animateduv_shader_0, 'hide'):
        swtor_animateduv_shader_0.hide = False
    if hasattr(swtor_animateduv_shader_0, 'label'):
        swtor_animateduv_shader_0.label = 'C-3PO\'s & CaptnKoda\'s AnimatedUVs Group'
    if hasattr(swtor_animateduv_shader_0, 'location'):
        swtor_animateduv_shader_0.location = (260.0, 200.0)
    if hasattr(swtor_animateduv_shader_0, 'mute'):
        swtor_animateduv_shader_0.mute = False
    if hasattr(swtor_animateduv_shader_0, 'name'):
        swtor_animateduv_shader_0.name = 'SWTOR - AnimatedUV Shader'
    if hasattr(swtor_animateduv_shader_0, 'status'):
        swtor_animateduv_shader_0.status = False
    if hasattr(swtor_animateduv_shader_0, 'use_custom_color'):
        swtor_animateduv_shader_0.use_custom_color = False
    if hasattr(swtor_animateduv_shader_0, 'width'):
        swtor_animateduv_shader_0.width = 302.21063232421875
    if hasattr(swtor_animateduv_shader_0.inputs[0], 'default_value'):
        swtor_animateduv_shader_0.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
    if hasattr(swtor_animateduv_shader_0.inputs[0], 'display_shape'):
        swtor_animateduv_shader_0.inputs[0].display_shape = 'CIRCLE'
    if hasattr(swtor_animateduv_shader_0.inputs[0], 'enabled'):
        swtor_animateduv_shader_0.inputs[0].enabled = True
    if hasattr(swtor_animateduv_shader_0.inputs[0], 'hide'):
        swtor_animateduv_shader_0.inputs[0].hide = False
    if hasattr(swtor_animateduv_shader_0.inputs[0], 'hide_value'):
        swtor_animateduv_shader_0.inputs[0].hide_value = True
    if hasattr(swtor_animateduv_shader_0.inputs[0], 'name'):
        swtor_animateduv_shader_0.inputs[0].name = '_d DiffuseMap Color'
    if hasattr(swtor_animateduv_shader_0.inputs[0], 'show_expanded'):
        swtor_animateduv_shader_0.inputs[0].show_expanded = False
    if hasattr(swtor_animateduv_shader_0.inputs[1], 'default_value'):
        swtor_animateduv_shader_0.inputs[1].default_value = 0.0
    if hasattr(swtor_animateduv_shader_0.inputs[1], 'display_shape'):
        swtor_animateduv_shader_0.inputs[1].display_shape = 'CIRCLE'
    if hasattr(swtor_animateduv_shader_0.inputs[1], 'enabled'):
        swtor_animateduv_shader_0.inputs[1].enabled = True
    if hasattr(swtor_animateduv_shader_0.inputs[1], 'hide'):
        swtor_animateduv_shader_0.inputs[1].hide = False
    if hasattr(swtor_animateduv_shader_0.inputs[1], 'hide_value'):
        swtor_animateduv_shader_0.inputs[1].hide_value = False
    if hasattr(swtor_animateduv_shader_0.inputs[1], 'name'):
        swtor_animateduv_shader_0.inputs[1].name = '_d DiffuseMap Alpha'
    if hasattr(swtor_animateduv_shader_0.inputs[1], 'show_expanded'):
        swtor_animateduv_shader_0.inputs[1].show_expanded = False
    if hasattr(swtor_animateduv_shader_0.inputs[2], 'default_value'):
        swtor_animateduv_shader_0.inputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
    if hasattr(swtor_animateduv_shader_0.inputs[2], 'display_shape'):
        swtor_animateduv_shader_0.inputs[2].display_shape = 'CIRCLE'
    if hasattr(swtor_animateduv_shader_0.inputs[2], 'enabled'):
        swtor_animateduv_shader_0.inputs[2].enabled = True
    if hasattr(swtor_animateduv_shader_0.inputs[2], 'hide'):
        swtor_animateduv_shader_0.inputs[2].hide = False
    if hasattr(swtor_animateduv_shader_0.inputs[2], 'hide_value'):
        swtor_animateduv_shader_0.inputs[2].hide_value = False
    if hasattr(swtor_animateduv_shader_0.inputs[2], 'name'):
        swtor_animateduv_shader_0.inputs[2].name = 'AnimatedTexture1 Color'
    if hasattr(swtor_animateduv_shader_0.inputs[2], 'show_expanded'):
        swtor_animateduv_shader_0.inputs[2].show_expanded = False
    if hasattr(swtor_animateduv_shader_0.inputs[3], 'default_value'):
        swtor_animateduv_shader_0.inputs[3].default_value = 0.0
    if hasattr(swtor_animateduv_shader_0.inputs[3], 'display_shape'):
        swtor_animateduv_shader_0.inputs[3].display_shape = 'CIRCLE'
    if hasattr(swtor_animateduv_shader_0.inputs[3], 'enabled'):
        swtor_animateduv_shader_0.inputs[3].enabled = True
    if hasattr(swtor_animateduv_shader_0.inputs[3], 'hide'):
        swtor_animateduv_shader_0.inputs[3].hide = False
    if hasattr(swtor_animateduv_shader_0.inputs[3], 'hide_value'):
        swtor_animateduv_shader_0.inputs[3].hide_value = False
    if hasattr(swtor_animateduv_shader_0.inputs[3], 'name'):
        swtor_animateduv_shader_0.inputs[3].name = 'AnimatedTexture1 Alpha'
    if hasattr(swtor_animateduv_shader_0.inputs[3], 'show_expanded'):
        swtor_animateduv_shader_0.inputs[3].show_expanded = False
    if hasattr(swtor_animateduv_shader_0.inputs[4], 'default_value'):
        swtor_animateduv_shader_0.inputs[4].default_value = (0.0, 0.0, 0.0, 1.0)
    if hasattr(swtor_animateduv_shader_0.inputs[4], 'display_shape'):
        swtor_animateduv_shader_0.inputs[4].display_shape = 'CIRCLE'
    if hasattr(swtor_animateduv_shader_0.inputs[4], 'enabled'):
        swtor_animateduv_shader_0.inputs[4].enabled = True
    if hasattr(swtor_animateduv_shader_0.inputs[4], 'hide'):
        swtor_animateduv_shader_0.inputs[4].hide = False
    if hasattr(swtor_animateduv_shader_0.inputs[4], 'hide_value'):
        swtor_animateduv_shader_0.inputs[4].hide_value = False
    if hasattr(swtor_animateduv_shader_0.inputs[4], 'name'):
        swtor_animateduv_shader_0.inputs[4].name = 'AnimatedTexture2 Color'
    if hasattr(swtor_animateduv_shader_0.inputs[4], 'show_expanded'):
        swtor_animateduv_shader_0.inputs[4].show_expanded = False
    if hasattr(swtor_animateduv_shader_0.inputs[5], 'default_value'):
        swtor_animateduv_shader_0.inputs[5].default_value = 0.0
    if hasattr(swtor_animateduv_shader_0.inputs[5], 'display_shape'):
        swtor_animateduv_shader_0.inputs[5].display_shape = 'CIRCLE'
    if hasattr(swtor_animateduv_shader_0.inputs[5], 'enabled'):
        swtor_animateduv_shader_0.inputs[5].enabled = True
    if hasattr(swtor_animateduv_shader_0.inputs[5], 'hide'):
        swtor_animateduv_shader_0.inputs[5].hide = False
    if hasattr(swtor_animateduv_shader_0.inputs[5], 'hide_value'):
        swtor_animateduv_shader_0.inputs[5].hide_value = False
    if hasattr(swtor_animateduv_shader_0.inputs[5], 'name'):
        swtor_animateduv_shader_0.inputs[5].name = 'AnimatedTexture2 Alpha'
    if hasattr(swtor_animateduv_shader_0.inputs[5], 'show_expanded'):
        swtor_animateduv_shader_0.inputs[5].show_expanded = False
    if hasattr(swtor_animateduv_shader_0.inputs[6], 'default_value'):
        swtor_animateduv_shader_0.inputs[6].default_value = (0.0, 0.0, 0.0)
    if hasattr(swtor_animateduv_shader_0.inputs[6], 'display_shape'):
        swtor_animateduv_shader_0.inputs[6].display_shape = 'CIRCLE'
    if hasattr(swtor_animateduv_shader_0.inputs[6], 'enabled'):
        swtor_animateduv_shader_0.inputs[6].enabled = True
    if hasattr(swtor_animateduv_shader_0.inputs[6], 'hide'):
        swtor_animateduv_shader_0.inputs[6].hide = False
    if hasattr(swtor_animateduv_shader_0.inputs[6], 'hide_value'):
        swtor_animateduv_shader_0.inputs[6].hide_value = False
    if hasattr(swtor_animateduv_shader_0.inputs[6], 'name'):
        swtor_animateduv_shader_0.inputs[6].name = 'animTexTint0'
    if hasattr(swtor_animateduv_shader_0.inputs[6], 'show_expanded'):
        swtor_animateduv_shader_0.inputs[6].show_expanded = False
    if hasattr(swtor_animateduv_shader_0.inputs[7], 'default_value'):
        swtor_animateduv_shader_0.inputs[7].default_value = (0.0, 0.0, 0.0)
    if hasattr(swtor_animateduv_shader_0.inputs[7], 'display_shape'):
        swtor_animateduv_shader_0.inputs[7].display_shape = 'CIRCLE'
    if hasattr(swtor_animateduv_shader_0.inputs[7], 'enabled'):
        swtor_animateduv_shader_0.inputs[7].enabled = True
    if hasattr(swtor_animateduv_shader_0.inputs[7], 'hide'):
        swtor_animateduv_shader_0.inputs[7].hide = False
    if hasattr(swtor_animateduv_shader_0.inputs[7], 'hide_value'):
        swtor_animateduv_shader_0.inputs[7].hide_value = False
    if hasattr(swtor_animateduv_shader_0.inputs[7], 'name'):
        swtor_animateduv_shader_0.inputs[7].name = 'animTexTint1'
    if hasattr(swtor_animateduv_shader_0.inputs[7], 'show_expanded'):
        swtor_animateduv_shader_0.inputs[7].show_expanded = False
    if hasattr(swtor_animateduv_shader_0.inputs[8], 'default_value'):
        swtor_animateduv_shader_0.inputs[8].default_value = (0.0, 0.0, 0.0)
    if hasattr(swtor_animateduv_shader_0.inputs[8], 'display_shape'):
        swtor_animateduv_shader_0.inputs[8].display_shape = 'CIRCLE'
    if hasattr(swtor_animateduv_shader_0.inputs[8], 'enabled'):
        swtor_animateduv_shader_0.inputs[8].enabled = True
    if hasattr(swtor_animateduv_shader_0.inputs[8], 'hide'):
        swtor_animateduv_shader_0.inputs[8].hide = False
    if hasattr(swtor_animateduv_shader_0.inputs[8], 'hide_value'):
        swtor_animateduv_shader_0.inputs[8].hide_value = False
    if hasattr(swtor_animateduv_shader_0.inputs[8], 'name'):
        swtor_animateduv_shader_0.inputs[8].name = 'animTexTint2'
    if hasattr(swtor_animateduv_shader_0.inputs[8], 'show_expanded'):
        swtor_animateduv_shader_0.inputs[8].show_expanded = False
    if hasattr(swtor_animateduv_shader_0.inputs[9], 'default_value'):
        swtor_animateduv_shader_0.inputs[9].default_value = 0.0
    if hasattr(swtor_animateduv_shader_0.inputs[9], 'display_shape'):
        swtor_animateduv_shader_0.inputs[9].display_shape = 'CIRCLE'
    if hasattr(swtor_animateduv_shader_0.inputs[9], 'enabled'):
        swtor_animateduv_shader_0.inputs[9].enabled = True
    if hasattr(swtor_animateduv_shader_0.inputs[9], 'hide'):
        swtor_animateduv_shader_0.inputs[9].hide = False
    if hasattr(swtor_animateduv_shader_0.inputs[9], 'hide_value'):
        swtor_animateduv_shader_0.inputs[9].hide_value = True
    if hasattr(swtor_animateduv_shader_0.inputs[9], 'name'):
        swtor_animateduv_shader_0.inputs[9].name = '—— EXTRAS ——'
    if hasattr(swtor_animateduv_shader_0.inputs[9], 'show_expanded'):
        swtor_animateduv_shader_0.inputs[9].show_expanded = False
    if hasattr(swtor_animateduv_shader_0.inputs[10], 'default_value'):
        swtor_animateduv_shader_0.inputs[10].default_value = 0.0
    if hasattr(swtor_animateduv_shader_0.inputs[10], 'display_shape'):
        swtor_animateduv_shader_0.inputs[10].display_shape = 'CIRCLE'
    if hasattr(swtor_animateduv_shader_0.inputs[10], 'enabled'):
        swtor_animateduv_shader_0.inputs[10].enabled = True
    if hasattr(swtor_animateduv_shader_0.inputs[10], 'hide'):
        swtor_animateduv_shader_0.inputs[10].hide = False
    if hasattr(swtor_animateduv_shader_0.inputs[10], 'hide_value'):
        swtor_animateduv_shader_0.inputs[10].hide_value = False
    if hasattr(swtor_animateduv_shader_0.inputs[10], 'name'):
        swtor_animateduv_shader_0.inputs[10].name = 'Roughness Factor'
    if hasattr(swtor_animateduv_shader_0.inputs[10], 'show_expanded'):
        swtor_animateduv_shader_0.inputs[10].show_expanded = False
    if hasattr(swtor_animateduv_shader_0.inputs[11], 'default_value'):
        swtor_animateduv_shader_0.inputs[11].default_value = 1.0
    if hasattr(swtor_animateduv_shader_0.inputs[11], 'display_shape'):
        swtor_animateduv_shader_0.inputs[11].display_shape = 'CIRCLE'
    if hasattr(swtor_animateduv_shader_0.inputs[11], 'enabled'):
        swtor_animateduv_shader_0.inputs[11].enabled = True
    if hasattr(swtor_animateduv_shader_0.inputs[11], 'hide'):
        swtor_animateduv_shader_0.inputs[11].hide = False
    if hasattr(swtor_animateduv_shader_0.inputs[11], 'hide_value'):
        swtor_animateduv_shader_0.inputs[11].hide_value = False
    if hasattr(swtor_animateduv_shader_0.inputs[11], 'name'):
        swtor_animateduv_shader_0.inputs[11].name = 'Emission Strength'
    if hasattr(swtor_animateduv_shader_0.inputs[11], 'show_expanded'):
        swtor_animateduv_shader_0.inputs[11].show_expanded = False
    if hasattr(swtor_animateduv_shader_0.inputs[12], 'default_value'):
        swtor_animateduv_shader_0.inputs[12].default_value = 1.0
    if hasattr(swtor_animateduv_shader_0.inputs[12], 'display_shape'):
        swtor_animateduv_shader_0.inputs[12].display_shape = 'CIRCLE'
    if hasattr(swtor_animateduv_shader_0.inputs[12], 'enabled'):
        swtor_animateduv_shader_0.inputs[12].enabled = True
    if hasattr(swtor_animateduv_shader_0.inputs[12], 'hide'):
        swtor_animateduv_shader_0.inputs[12].hide = False
    if hasattr(swtor_animateduv_shader_0.inputs[12], 'hide_value'):
        swtor_animateduv_shader_0.inputs[12].hide_value = False
    if hasattr(swtor_animateduv_shader_0.inputs[12], 'name'):
        swtor_animateduv_shader_0.inputs[12].name = 'Backface Culling Factor'
    if hasattr(swtor_animateduv_shader_0.inputs[12], 'show_expanded'):
        swtor_animateduv_shader_0.inputs[12].show_expanded = False
    if hasattr(swtor_animateduv_shader_0.outputs[1], 'default_value'):
        swtor_animateduv_shader_0.outputs[1].default_value = 0.0
    if hasattr(swtor_animateduv_shader_0.outputs[1], 'display_shape'):
        swtor_animateduv_shader_0.outputs[1].display_shape = 'CIRCLE'
    if hasattr(swtor_animateduv_shader_0.outputs[1], 'enabled'):
        swtor_animateduv_shader_0.outputs[1].enabled = True
    if hasattr(swtor_animateduv_shader_0.outputs[1], 'hide'):
        swtor_animateduv_shader_0.outputs[1].hide = False
    if hasattr(swtor_animateduv_shader_0.outputs[1], 'hide_value'):
        swtor_animateduv_shader_0.outputs[1].hide_value = True
    if hasattr(swtor_animateduv_shader_0.outputs[1], 'name'):
        swtor_animateduv_shader_0.outputs[1].name = '—— EXTRAS ——'
    if hasattr(swtor_animateduv_shader_0.outputs[1], 'show_expanded'):
        swtor_animateduv_shader_0.outputs[1].show_expanded = False
    if hasattr(swtor_animateduv_shader_0.outputs[2], 'default_value'):
        swtor_animateduv_shader_0.outputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
    if hasattr(swtor_animateduv_shader_0.outputs[2], 'display_shape'):
        swtor_animateduv_shader_0.outputs[2].display_shape = 'CIRCLE'
    if hasattr(swtor_animateduv_shader_0.outputs[2], 'enabled'):
        swtor_animateduv_shader_0.outputs[2].enabled = True
    if hasattr(swtor_animateduv_shader_0.outputs[2], 'hide'):
        swtor_animateduv_shader_0.outputs[2].hide = False
    if hasattr(swtor_animateduv_shader_0.outputs[2], 'hide_value'):
        swtor_animateduv_shader_0.outputs[2].hide_value = False
    if hasattr(swtor_animateduv_shader_0.outputs[2], 'name'):
        swtor_animateduv_shader_0.outputs[2].name = 'Diffuse Color AUX'
    if hasattr(swtor_animateduv_shader_0.outputs[2], 'show_expanded'):
        swtor_animateduv_shader_0.outputs[2].show_expanded = False
    if hasattr(swtor_animateduv_shader_0.outputs[3], 'default_value'):
        swtor_animateduv_shader_0.outputs[3].default_value = 0.0
    if hasattr(swtor_animateduv_shader_0.outputs[3], 'display_shape'):
        swtor_animateduv_shader_0.outputs[3].display_shape = 'CIRCLE'
    if hasattr(swtor_animateduv_shader_0.outputs[3], 'enabled'):
        swtor_animateduv_shader_0.outputs[3].enabled = True
    if hasattr(swtor_animateduv_shader_0.outputs[3], 'hide'):
        swtor_animateduv_shader_0.outputs[3].hide = False
    if hasattr(swtor_animateduv_shader_0.outputs[3], 'hide_value'):
        swtor_animateduv_shader_0.outputs[3].hide_value = False
    if hasattr(swtor_animateduv_shader_0.outputs[3], 'name'):
        swtor_animateduv_shader_0.outputs[3].name = 'Alpha AUX'
    if hasattr(swtor_animateduv_shader_0.outputs[3], 'show_expanded'):
        swtor_animateduv_shader_0.outputs[3].show_expanded = False

    # LINKS
    node_tree0.links.new(animatedtexture1_0.outputs[0], swtor_animateduv_shader_0.inputs[2])
    node_tree0.links.new(animatedtexture2_0.outputs[0], swtor_animateduv_shader_0.inputs[4])
    node_tree0.links.new(sw_aux_transformalluv_0.outputs[0], _d_diffusemap_0.inputs[0])
    node_tree0.links.new(sw_aux_transformalluv_0.outputs[1], animatedtexture1_0.inputs[0])
    node_tree0.links.new(sw_aux_transformalluv_0.outputs[2], animatedtexture2_0.inputs[0])
    node_tree0.links.new(animatedtexture2_0.outputs[1], swtor_animateduv_shader_0.inputs[5])
    node_tree0.links.new(_d_diffusemap_0.outputs[0], swtor_animateduv_shader_0.inputs[0])
    node_tree0.links.new(swtor_animateduv_shader_0.outputs[0], material_output_0.inputs[0])
    node_tree0.links.new(animatedtexture1_0.outputs[1], swtor_animateduv_shader_0.inputs[3])
    node_tree0.links.new(_d_diffusemap_0.outputs[1], swtor_animateduv_shader_0.inputs[1])

    # DRIVERS
    driven_node = bpy.data.node_groups["SW Aux - TransformUV"].nodes["#frame-driven Value"]
    driven_property = driven_node.outputs["Value"].driver_add("default_value")
    driven_property.driver.expression = "frame"



    return material_datablock