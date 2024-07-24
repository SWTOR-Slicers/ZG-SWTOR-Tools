import bpy


#############################
# MATERIALS-RELATED FUNCTIONS
#############################

# -------------------------------------------------------------------------------------------------
def merge_materials_node_trees(source_material_name,
                                destination_material_name,
                                offset_x = 0.0,
                                offset_y = 0.0,
                                delete_source_output_nodes = False,
                                delete_destination_output_nodes = False):
    """
    Adds the entire node tree of a source material to the node tree of a
    destination material, resulting in both sets of nodes inside the
    destination material's node tree.
    
    It lets us offset the source's nodes in Shader Editor space coordinate units
    to keep them from overlapping.
    
    It doesn't delete any Output Node by default (which can be actually useful
    in certain situations, as Blender lets us select which Output Node among many
    is the one currently producing the material's output).
    
    Args:
        source_material_name (string): material with node tree to copy.
        destination_material_name (string): material receiving the nodes.

        offset_x (float, optional): displace the source's nodes in Shader Editor space. Defaults to 0.0.
        offset_y (float, optional): displace the source's nodes in Shader Editor space. Defaults to 0.0.
        
        delete_source_output_node (bool, optional): omits the Output Node from the source material. Defaults to False.
        delete_destination_output_node (bool, optional): deletes the Output Node from the source material. Defaults to False.
        (WARNING: in case of multiple Output Nodes in the source material or in the destination one, these options will omit
        or delete all applicable Output Nodes)

    Returns:
        Bool: True if successful, False if any of the materials doesn't exist.
    """
    
    # Get the source and destination materials
    source_material = bpy.data.materials.get(source_material_name)
    destination_material = bpy.data.materials.get(destination_material_name)

    # Check if both materials exist
    if not source_material:
        print(f"Error: the '{source_material_name}' Material does not exist.")
        return False
    
    if not destination_material:
        print(f"Error: the '{destination_material_name}' Material does not exist.")
        return False

    # Get the node trees of the materials
    source_node_tree = source_material.node_tree
    destination_node_tree = destination_material.node_tree
    
    
    # Delete destination material's Outputs Nodes if set so in args
    if delete_destination_output_nodes:
        for node in destination_node_tree.nodes:
            if node.bl_idname == 'ShaderNodeOutputMaterial':
                destination_node_tree.nodes.remove(node)


    # Create a dict relating the source's nodes
    # and their copies created into the destination.
    # It will be used for reading the source ones' linkings
    # and apply them to the copied ones.
    node_mapping = {}

    # Add nodes to the destination node tree
    for source_node in source_node_tree.nodes:
        
        # Omit processing the source material's Output Node if set so in args
        if source_node.bl_idname == 'ShaderNodeOutputMaterial' and delete_source_output_nodes:
            continue
        
        # Create copy of source node in the destination node tree
        new_node = destination_node_tree.nodes.new(type=source_node.bl_idname)
        
        # Add the mapping between source and destination nodes
        node_mapping[source_node] = new_node
        
        new_node.name = source_node.name
        new_node.label = source_node.label
        new_node.location[0] = source_node.location + offset_x
        new_node.location[1] = source_node.location + offset_y
        new_node.hide = source_node.hide
        new_node.use_custom_color = source_node.use_custom_color
        new_node.color = source_node.color


    # Add links to the destination node tree
    for source_link in source_node_tree.links:
        source_socket = node_mapping.get(source_link.from_node).outputs[source_link.from_socket.name]
        destination_socket = node_mapping.get(source_link.to_node).inputs[source_link.to_socket.name]
        
        # Omit processing the source material's links to their Output Nodes if set so in args
        # as those nodes won't exist
        if source_link.to_node.bl_idname == 'ShaderNodeOutputMaterial' and delete_source_output_nodes:
            continue

        destination_node_tree.links.new(source_socket, destination_socket)
    
    return True
        
# -------------------------------------------------------------------------------------------------
