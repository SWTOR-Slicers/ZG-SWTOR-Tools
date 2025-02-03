import bpy

import bmesh
from mathutils import Vector, Matrix
import numpy as np
import time


# ImportHelper is a helper class, defines filename and an
# implicit invoke() function which calls the file selector.
# The string properties ‘filepath’, ‘filename’, ‘directory’
# and a ‘files’ collection
# are assigned when present in the operator
from bpy_extras.io_utils import ImportHelper


import os
from pathlib import Path
import shutil

import json
import xml.etree.ElementTree as ET

# This Add-on's own modules
from .utils.addon_checks import requirements_checks


ADDON_ROOT = __file__.rsplit(__name__.rsplit(".")[0])[0] + __name__.rsplit(".")[0]


# Aux Functions
# region


def extract_mat_texture_data(mat_file_abs_path):
    with open(mat_file_abs_path, 'r') as mat_file:
        tree = ET.parse(mat_file)
        root = tree.getroot()
        texture_data = {}
        
        # List of maps to update, to avoid affecting maps that aren't in the .mat
        # info, such as complexion, make-up, etc.
        modernizables = ["DiffuseMap", "RotationMap1", "GlossMap", "PaletteMap", "PaletteMaskMap"]
        
        for input_element in root.findall('input'):
            semantic = input_element.find('semantic')
            type_element = input_element.find('type')
            value = input_element.find('value')
            
            if type_element is not None and type_element.text == 'texture':
                if semantic is not None and semantic.text in modernizables and value is not None:
                    if semantic.text == "RotationMap1":
                        semantic_text = "rotationMap"
                    else:
                        semantic_text = semantic.text[0:1].lower() + semantic.text[1:]
                    texture_data[semantic_text] = value.text.replace("\\", "/") + ".dds"
    
        return texture_data

def replace_json_data_texturepaths_with_mat_data_ones(json_data, swtor_resources_folderpath):
    for elem in json_data:
        if "slotName" in elem:
            slotName = elem["slotName"]
            if slotName != "skinMats":
                matPath = elem["materialInfo"]["matPath"]
                ddsPaths =  elem["materialInfo"]["ddsPaths"]

                if matPath[0:1] == "\\" or matPath[0:1] == "/":
                    matPath = matPath[1:]

                mat_file_abs_path = Path(swtor_resources_folderpath) / Path(matPath)
                modern_textures = extract_mat_texture_data(mat_file_abs_path)                
        
                for ddsPath_key in ddsPaths.keys():
                    if ddsPath_key in modern_textures.keys():
                        ddsPaths[ddsPath_key] = modern_textures[ddsPath_key]
            else:
                for skin_elem in elem["materialInfo"]["mats"]:
                    if "slotName" in skin_elem:
                        slotName = skin_elem["slotName"]
                        if slotName != "skinMats":
                            matPath = skin_elem["materialInfo"]["matPath"]
                            ddsPaths =  skin_elem["ddsPaths"]
                    
                            if matPath[0:1] == "\\" or matPath[0:1] == "/":
                                matPath = matPath[1:]

                            mat_file_abs_path = Path(swtor_resources_folderpath) / Path(matPath)
                            modern_textures = extract_mat_texture_data(mat_file_abs_path)                
                    
                            for ddsPath_key in ddsPaths.keys():
                                if ddsPath_key in modern_textures.keys():
                                    ddsPaths[ddsPath_key] = modern_textures[ddsPath_key]








def bind_objects_to_armature(objects, armature, single_armature_only=True):
    """
    Bind a set of objects to an armature, producing Armature Modifiers in the process.

    :param objects: A list of objects to be bound to the armature
    :param armature: The armature object
    :param single_armature_only: prevents from adding armatures when there are any already
    """
    for obj in objects:
        # Ensure the object has a mesh data type
        if obj.type == 'MESH':
            # Add an Armature modifier if it doesn't already exist
            # or if it does but we allow multiple ones
            if not ( single_armature_only and any(mod.type == 'ARMATURE' for mod in obj.modifiers) ):
                mod = obj.modifiers.new(name="Armature", type='ARMATURE')
                mod.object = armature
                
                # Create a parent relationship
                # DON'T USE A PARENT_TYPE OF 'ARMATURE'. THE MODIFIER IS DOING THAT ALREADY
                obj.parent = armature
                obj.matrix_parent_inverse = armature.matrix_world.inverted() # Is this necessary?

                # Automatic weight assignment is more complex and would usually require the operator,
                # so here we assume weights have been assigned manually or by another method. For
                # implementing it, it would be bpy.ops.object.parent_set(type='ARMATURE_AUTO')

# THIS VARIANT IS NOT IN USE
def bind_objects_to_armature_ops_version(objects, armature, automatic_weights=False):
    """
    Bind a set of objects to an armature, producing Armature Modifiers in the process.

    :param objects: A list of objects to be bound to the armature
    :param armature: The armature object
    :param automatic_weights: calculate automatic weights while parenting the objects
    """
    # Make sure the armature is in Object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Loop through each object in the list
    for obj in objects:
        # Ensure we are in Object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Select the object
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        # Add an Armature modifier to the object
        mod = obj.modifiers.new(name="Armature", type='ARMATURE')
        mod.object = armature

        # THIS MIGHT HAVE ISSUES DONE AT THIS STEP, BECAUSE 'ARMATURE'
        # DOUBLE-DIPS ON WHAT THE MODIFIER IS DOING ALREADY. MAYBE BETTER
        # TO PARENT FIRST FOR 'ARMATURE-AUTO', THEN UNPARENT, THEN
        # ADD THE MODIFIER, THEN PARENT NORMALLY.
        if automatic_weights:
            # Parent the object to the armature with automatic weights
            bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        else:
            bpy.ops.object.parent_set(type='ARMATURE')

        # Deselect the object
        obj.select_set(False)

    # Select the armature at the end
    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)

def get_wrinkles_and_directionmaps(mat_file_abs_path):
    '''Reads a shader .mat file and returns any DirectionMap
    and WrinkleMap paths in an "as is" basis
    (slashes, backslashes, initial ones or not…)'''
    
    relative_paths = []
    with open(mat_file_abs_path, 'r') as mat_file:
        tree = ET.parse(mat_file)
        root = tree.getroot()

        # The diverse camelCases are as per BioWare's horrific inconsistency.
        # Same goes for initial backslash. For consistency, we add it if missing.
        # backslash vs. slash is solved vía pathlib later on.

        DirectionMap = root.find("./input/[semantic='DirectionMap']")
        if DirectionMap != None:
            texturemap_path = DirectionMap.find("value").text + ".dds"
            if texturemap_path[0] != "\\":
                texturemap_path = "\\" + texturemap_path
            relative_paths.append(texturemap_path)

        animatedWrinkleMap = root.find("./input/[semantic='animatedWrinkleMap']")
        if animatedWrinkleMap != None:
            texturemap_path = animatedWrinkleMap.find("value").text + ".dds"
            if texturemap_path[0] != "\\":
                texturemap_path = "\\" + texturemap_path
            relative_paths.append(texturemap_path)

        animatedWrinkleMask = root.find("./input/[semantic='animatedWrinkleMask']")
        if animatedWrinkleMask != None:
            texturemap_path = animatedWrinkleMask.find("value").text + ".dds"
            if texturemap_path[0] != "\\":
                texturemap_path = "\\" + texturemap_path
            relative_paths.append(texturemap_path)

    return(relative_paths)

def place_black_dds(swtor_resources_folderpath):

    black_dds_origin = Path(ADDON_ROOT) / "rsrc" / "black.dds"
    black_dds_destination = Path(swtor_resources_folderpath) / "art/defaultassets/black.dds"
    
    if black_dds_destination.exists() == False:
        print ("'black.dds' file missing in 'resources\\art\\defaultassets'. Placing a copy of the file \(included in this Addon\) there.")
        print()
        print()
        try:
            shutil.copy2( str(black_dds_origin), str(black_dds_destination) )
        except Exception as e:
            print("ERROR: Copying the 'black.dds' file to the resources folder failed:")
            print(e)
            print()

    return

def link_objects_to_collection(objects, destination_collection, create = True, move = False):
    """
    Links objects to a Collection.
    Accepts both data-blocks and ID strings.
    Accepts a single object or a list of objects. 
    If create == True, creates destination_collection if doesn't exists.
    If move == True,
    it unlinks the objects from their current Collections first.
    """

    if objects:
        # Make sure a single object works as a list for the loop.
        if not isinstance(objects, list):
            objects = [objects]
            
        # if destination_collection is a string, turn it into a data-block.
        if type(destination_collection) == str:
            if destination_collection not in bpy.data.collections:
                if create == True:
                    destination_collection = bpy.data.collections.new(destination_collection)
                else:
                    return False
            else:
                destination_collection = bpy.data.collections[destination_collection]           
                
        for object in objects:
            # if object is a string, turn it into a data-block.
            if type(object) == str:
                object = bpy.data.objects.get(object)
                if object == None:
                    return False
            
            # If move == True, unlink from any collections it is in.
            if object.users_collection and move == True:
                for current_collections in object.users_collection:
                    current_collections.objects.unlink(object)
            # Then link to assigned collection.
            destination_collection.objects.link(object)
            
        # If destination_collection isn't linked to any other Collection
        # including the Scene Collection, link it to the Scene Collection.
        if not bpy.context.scene.user_of_id(destination_collection):
            bpy.context.collection.children.link(destination_collection)

        return
    else:
        return False

def link_collections_to_collection(collections, destination_collection, create = True, move = True):
    """
    Links collections to a Collection.
    Accepts both data-blocks and ID strings.
    Accepts a single collection or a list of collections. 
    If create == True, creates destination_collection if it doesn't exists.
    If move == True, unlink from any collections it is in before placing in destination.

    """

    if collections:
        # Make sure a single collection works as a list for the loop.
        if not isinstance(collections, list):
            collections = [collections]
            
        # if destination_collection is a string, turn it into a data-block.
        if type(destination_collection) == str:
            if destination_collection not in bpy.data.collections:
                if create == True:
                    destination_collection = bpy.data.collections.new(destination_collection)
                else:
                    return False
            else:
                destination_collection = bpy.data.collections[destination_collection]           
                
        for collection in collections:
            # if collection is string turn it into a data-block.
            if type(collection) == str:
                collection = bpy.data.collections.get(collection)
                if collection == None:
                    return False
            
            # If move == True, unlink from any collections it is in.
            if move == True:
                # Unlink from all collections in the scene.
                for scene_collection in list(bpy.context.scene.collection.children_recursive):
                    if collection in list(scene_collection.children):
                        scene_collection.children.unlink(collection)
                # Also unlink from the Scene Collection
                if collection in list(bpy.context.scene.collection.children):
                    bpy.context.scene.collection.children.unlink(collection)
            # Then link to assigned collection.
            destination_collection.children.link(collection)
            
        # If destination_collection isn't linked to any other Collection
        # including the Scene Collection, link it to the Scene Collection.
        if not bpy.context.scene.user_of_id(destination_collection):
            bpy.context.collection.children.link(destination_collection)

        return
    else:
        return False

def translate_uv_coordinates(mesh_object, material_slot = None, uv_offset = (0,0) ):
    # uv_offset's default is needed because there can't be args without defaults
    # after an arg with one
    
    '''
    Offset an object's polys' UVs, either all or those
    associated to a material. Motivated by Twi'lek's
    off-image coordinates eye UVs producing black bakes.
    '''
    
    # Ensure the object is a mesh
    if mesh_object.type != 'MESH':
        print("Selected object is not a mesh.")
        return

    # Get the mesh data
    mesh = mesh_object.data

    # Ensure the mesh has UV coordinates
    if not mesh.uv_layers.active:
        print("Mesh has no UV coordinates.")
        return

    # Get the active UV layer
    uv_layer = mesh.uv_layers.active.data

    # Translate UV coordinates
    for face in mesh.polygons:
        if face.material_index == material_slot or material_slot == None:
            for loop_index in face.loop_indices:
                uv = uv_layer[loop_index].uv
                if uv.y <= 1:
                    return
                uv.x += uv_offset[0]
                uv.y += uv_offset[1]

    return False

def duplicate_obj(obj_or_obj_name):
    
    if type(obj_or_obj_name) == str:
        obj = bpy.data.objects[obj_or_obj_name]
    else:
        obj = obj_or_obj_name
        
    # Create a new object data-block that is a copy of the original object's data
    # including transforms, modifiers, constraints, parents and Collections.
    new_data = obj.data.copy()
    
    # Create a new object with the copied data
    new_obj = bpy.data.objects.new(obj.name + ".copy", new_data)
    
    # Link the new object to the same collection(s) as the original object
    for col in obj.users_collection:
        col.objects.link(new_obj)
    
    # Copy all properties from the original object to the new object
    new_obj.location = obj.location.copy()
    new_obj.rotation_euler = obj.rotation_euler.copy()
    new_obj.rotation_quaternion = obj.rotation_quaternion.copy()
    new_obj.scale = obj.scale.copy()
    new_obj.data = new_data
    
    # Copy custom properties
    for prop in obj.keys():
        if prop != "_RNA_UI":  # Ignore the RNA UI property
            new_obj[prop] = obj[prop]
    
# Copy all modifiers
    for mod in obj.modifiers:
        new_mod = new_obj.modifiers.new(name=mod.name, type=mod.type)
        for attr in dir(mod):
            if not attr.startswith("_") and attr not in {"type", "name", "rna_type"}:
                try:
                    setattr(new_mod, attr, getattr(mod, attr))
                except AttributeError:
                    pass
        
        # Special handling for Armature modifiers
        if mod.type == 'ARMATURE':
            new_mod.object = mod.object
        
    # Copy animation data
    if obj.animation_data:
        new_obj.animation_data_create()
        new_obj.animation_data.action = obj.animation_data.action
        new_obj.animation_data.action = obj.animation_data.action.copy()
    
    # Copy constraints
    for constr in obj.constraints:
        new_constr = new_obj.constraints.new(type=constr.type)
        for attr in dir(constr):
            if not attr.startswith("_") and attr not in {"type", "name", "rna_type"}:
                try:
                    setattr(new_constr, attr, getattr(constr, attr))
                except AttributeError:
                    pass
    
    return new_obj

def separate_obj_by_specific_materials(obj_or_obj_name, materials_names, separate = True):

    """
    Separates an object's polys associated to specified materials
    into separate objects per those materials. By default it
    deletes those polys AND materials from the original object.
    
    Args:
        obj_or_obj_name (bpy.types.object or string): object to be separated.
        materials_names (list): list of materials names.
        separate (bool, optional): If False, no separate objects are produced and the polys are just deleted.
    Returns:
        list of bpy.types.object: list of separated objects, empty if there were no materials matches.
    """

    if type(obj_or_obj_name) == str:
        original_obj = bpy.data.objects[obj_or_obj_name]
    else:
        original_obj = obj_or_obj_name
        
    original_mesh = original_obj.data
    new_objs = []
    
    # Get material indices to separate
    mat_indices = [i for i, mat in enumerate(original_mesh.materials) if mat.name in materials_names]
    
    if separate:
        for mat_index in mat_indices:
            # Create a duplicate object
            new_obj = original_obj.copy()
            new_obj.data = original_obj.data.copy()
            bpy.context.collection.objects.link(new_obj)
            new_obj.name = f"{original_obj.name}_{original_mesh.materials[mat_index].name}"
            
            # Create a new bmesh to work with
            bm = bmesh.new()
            bm.from_mesh(new_obj.data)
            
            # Iterate through all faces and hide those that don't use the current material
            faces_to_delete = [f for f in bm.faces if f.material_index != mat_index]
            bmesh.ops.delete(bm, geom=faces_to_delete, context='FACES')
            
            # Update the mesh
            bm.to_mesh(new_obj.data)
            bm.free()
            
            new_objs.append(new_obj)
    
    # Update original object to remove specified materials' polys
    bm = bmesh.new()
    bm.from_mesh(original_mesh)
    faces_to_delete = [f for f in bm.faces if f.material_index in mat_indices]
    bmesh.ops.delete(bm, geom=faces_to_delete, context='FACES')
    bm.to_mesh(original_mesh)
    bm.free()

    # Update original object to remove specified materials' material slots
    for i, slot in enumerate(original_obj.material_slots[:]):  # Use a copy of the list to modify it safely
        if slot.material and slot.material.name in materials_names:
            # Remove the material slot by removing
            # the object.data.materials' element
            original_obj.data.materials.pop(index=i)

    return new_objs

def delete_polygons_on_side(obj_or_obj_name, side='LEFT'):
    
    if type(obj_or_obj_name) == str:
        obj = bpy.data.objects[obj_or_obj_name]
    else:
        obj = obj_or_obj_name

    # Ensure we're in object mode
    if obj.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Get the mesh data
    mesh = obj.data

    # Create a BMesh from the mesh data
    bm = bmesh.new()
    bm.from_mesh(mesh)

    # Select polygons based on the side parameter
    for face in bm.faces:
        center = face.calc_center_median()
        if side == 'LEFT' and center.x < 0:
            face.select_set(True)
        elif side == 'RIGHT' and center.x >= 0:
            face.select_set(True)
        else:
            face.select_set(False)

    # Remove the selected faces
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.select], context='FACES')

    # Update the mesh with the BMesh data
    bm.to_mesh(mesh)
    bm.free()

    # Update the scene to reflect changes. NECESSARY???
    # mesh.update()  # This refreshes the mesh data
    # obj.data.update()  # Ensure that the object data is up-to-date
    # bpy.context.view_layer.update()  # Refresh the view layer to reflect changes

    print(f"Polygons on the {side} side have been deleted.")

def find_highest_lowest_vertices(obj_or_obj_name):
    
    if type(obj_or_obj_name) == str:
        obj = bpy.data.objects[obj_or_obj_name]
    else:
        obj = obj_or_obj_name

    # Get the mesh data from the object
    mesh = obj.data
    
    # Initialize variables to store highest and lowest vertices
    highest_vertex = None
    lowest_vertex = None
    
    # Initialize variables to store maximum and minimum Z coordinates
    max_z = -float('inf')
    min_z = float('inf')
    
    # Iterate through all vertices in the mesh
    for vert in mesh.vertices:
        # Get the world coordinates of the vertex
        world_vert = obj.matrix_world @ vert.co
        
        # Update highest and lowest vertices based on Z coordinate
        if world_vert.z > max_z:
            max_z = world_vert.z
            highest_vertex = world_vert
        
        if world_vert.z < min_z:
            min_z = world_vert.z
            lowest_vertex = world_vert
    
    return highest_vertex, lowest_vertex

def get_highest_and_lowest_vertices(obj_or_obj_name):
    
    if type(obj_or_obj_name) == str:
        obj = bpy.data.objects[obj_or_obj_name]
    else:
        obj = obj_or_obj_name

    # Ensure we are in object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create a bmesh from the object's mesh data
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    
    # Transform matrix to convert local coordinates to global
    global_matrix = obj.matrix_world
    
    highest_vertex = None
    lowest_vertex = None
    
    for v in bm.verts:
        global_coord = global_matrix @ v.co
        if highest_vertex is None or global_coord.z > highest_vertex.z:
            highest_vertex = global_coord
        if lowest_vertex is None or global_coord.z < lowest_vertex.z:
            lowest_vertex = global_coord
    
    bm.free()
    
    return highest_vertex, lowest_vertex

def set_obj_origin(obj_or_obj_name, new_origin):

    if type(obj_or_obj_name) == str:
        obj = bpy.data.objects[obj_or_obj_name]
    else:
        obj = obj_or_obj_name

    new_origin = Vector(new_origin)
    
    # Get the object's world matrix
    obj_matrix = obj.matrix_world
    
    # Calculate the current origin in world space
    current_origin_world = obj_matrix @ Vector((0, 0, 0))
    
    # Calculate the delta vector from current origin to new origin in world space
    delta_world = new_origin - current_origin_world
    
    # Apply the inverse world matrix to get delta in object space
    delta_object_space = obj_matrix.inverted() @ delta_world
    
    # Move the object's location to compensate for the delta
    obj.location += delta_world
    
    # Transform the mesh data to correct for the origin adjustment
    # Note: Applying the inverse translation in object space
    obj.data.transform(Matrix.Translation(-delta_object_space))
    
    # Update the mesh data to apply the changes
    obj.data.update()

# endregion




# Operator

class ZGSWTOR_OT_character_assembler(bpy.types.Operator):
    bl_label = "SWTOR Character Assembler"
    bl_idname = "zgswtor.character_assembler"
    bl_description = "Processes the 'path.json' file in a Player Character/NPC folder\nexported by TORCommunity.com, filling its subfolders with all\nrelated objects and textures, then importing the Character\n\n• Requires setting the path to a 'resources' folder in this addon's Preferences.\n• Requires an enabled modern .gr2 Importer Addon (not the Legacy version)"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')


    # Properties
    
    gather_only: bpy.props.BoolProperty(
        name="Gather Assets Only",
        description="Don't Import The Character, and just copy the required assets\nto the Character's folder",
        default = False,
        # options={'HIDDEN'}
    )

    dont_overwrite: bpy.props.BoolProperty(
        name="Don't overwrite Existing assets",
        description="If the character's folder contains some assets already, don't overwrite those.\nThat will preserve any changes done to them, such as manual retouchings",
        default = False,
        # options={'HIDDEN'}
    )

    collect: bpy.props.BoolProperty(
        name="Collect By In-game Names",
        description="Organize the Character's Objects in Collections named after their in-game names.\nThe Collections will be set inside the currently Active Collection in the Outliner.",
        default = True,
        # options={'HIDDEN'}
    )
    
    import_armor_only: bpy.props.BoolProperty(
        name="Import Armor Gear Only",
        description="Import only the armor gear elements and omit the rest of the body.",
        default = False,
        # options={'HIDDEN'}
    )

    import_skeleton: bpy.props.BoolProperty(
        name="Import Rigging Skeleton",
        description="Import the character's Skeleton Object if available.",
        default = True,
        # options={'HIDDEN'}
    )

    bind_to_skeleton: bpy.props.BoolProperty(
        name="Bind Objects To Skeleton",
        description="Bind all objects to the skeleton, if imported.",
        default = True,
        # options={'HIDDEN'}
    )

    separate_eyes: bpy.props.BoolProperty(
        name="Separate Eyes From Head Object",
        description="Separates the eyes from the character's head object to make them\neasier to rig and animate (certain rigging systems require that).\nNeeds them to be using a material with 'eye' in its name, as separating criteria.\n\nThe result is a single object with both eyes.\n\nTo further separate them into individual eyes,\nuse the 'Separate Eyes From Each Other' option, too",
        default = False,
        # options={'HIDDEN'}
    )
    
    separate_each_eye: bpy.props.BoolProperty(
        name="   Separate Eyes From Each Other",
        description="When separating the eyes from the character's head object\nmake each eye its own object and set their origin points\nso that they can also be posed via simple rotations",
        default = False,
        # options={'HIDDEN'}
    )

    correct_twilek_eyes_uv: bpy.props.BoolProperty(
        name="Correct Twi'lek's Eyes' UVs",
        description="When importing a Twi'lek character, reposition their eyes' UVs\ninside their textures' area so that they produce correct results\nin baking operations\n\n(This doesn't affect renderings)",
        default = True,
        # options={'HIDDEN'}
    )

    npc_uses_skin: bpy.props.BoolProperty(
        name="NPC Gear's Mat #2 is Skin",
        description="When importing a Non-Creature-type NPC, assume that any 2nd. Material Slots\nin armor or clothes are skin. If unticked, use a garment material instead.\n\nMOST NPC GEAR LACK SECOND MATERIALS, ANYWAY.\nTypical case actually using this checkbox: cantina dancers.\n\nIn mixed use cases, the Material Slots' assignments can be easily corrected\nmanually. Skin materials are always created, no matter if not in use.\n\n(TORCommunity.com's non-Creature NPC database exports don't include\n'materialSkinIndex' data indicating whether a piece of garment with\ntwo material slots uses skin or garment for the 2nd one. Hence this\ncheckbox)",
        default = True,
        # options={'HIDDEN'}
    )


    # File Browser for selecting paths.json file
    def invoke(self, context, event):

        # Sync properties with their UI matches
        self.gather_only = context.scene.zg_swca_gather_only_bool
        # self.assemble_only = context.scene.zg_swca_assemble_only_bool
        self.dont_overwrite = context.scene.zg_swca_dont_overwrite_bool
        self.collect = context.scene.zg_swca_collect_bool
        self.import_armor_only = context.scene.zg_swca_import_armor_only
        self.import_skeleton = context.scene.zg_swca_import_skeleton_bool
        self.bind_to_skeleton = context.scene.zg_swca_bind_to_skeleton_bool
        self.separate_eyes = context.scene.zg_swca_separate_eyes
        self.separate_each_eye = context.scene.zg_swca_separate_each_eye
        self.correct_twilek_eyes_uv = context.scene.zg_correct_twilek_eyes_uv
        self.npc_uses_skin = context.scene.zg_npc_uses_skin

        # Open File Browser.
        context.window_manager.fileselect_add(self)
        
        return {'RUNNING_MODAL'}



    # File Browsing properties

    filter_glob: bpy.props.StringProperty(
        default='*.json;',  # file wildcards separated by semicolons
        options={'HIDDEN'}
    )






    def execute(self, context):
        start_time = time.time()
        # Terminal's VT100 escape codes (most terminals understand them).
        # See: http://www.climagic.org/mirrors/VT100_Escape_Codes.html
        # (replacing ^[ in terminal codes with \033)
        CLEAR_TERMINAL = '\033[2J'      # Clear entire screen.
        CURSOR_HOME = '\033[H'          # Move cursor to upper left corner.
        CLEAR_EOL = '\r\033[K'          # Erase to end of current line.
        LINE_BACK_1ST_COL = '\033[F'    # Move cursor one line up, 1st column.


        # Sync properties with their UI matches (MOVED TO AN INVOKE FN)
        # self.gather_only = context.scene.zg_swca_gather_only_bool
        # # self.assemble_only = context.scene.zg_swca_assemble_only_bool
        # self.dont_overwrite = context.scene.zg_swca_dont_overwrite_bool
        # self.collect = context.scene.zg_swca_collect_bool
        # self.import_armor_only = context.scene.zg_swca_import_armor_only
        # self.import_skeleton = context.scene.zg_swca_import_skeleton_bool
        # self.bind_to_skeleton = context.scene.zg_swca_bind_to_skeleton_bool
        # self.separate_eyes = context.scene.zg_swca_separate_eyes
        # self.separate_each_eye = context.scene.zg_swca_separate_each_eye
        # self.correct_twilek_eyes_uv = context.scene.zg_correct_twilek_eyes_uv


        # Get the extracted SWTOR assets' "resources" folder from the add-on's preferences. 
        swtor_resources_folderpath = bpy.context.preferences.addons["zg_swtor_tools"].preferences.swtor_resources_folderpath
        swtor_shaders_path = swtor_resources_folderpath + "/art/shaders/materials"
        # Test the existence of the shaders subfolder to validate the SWTOR "resources" folder
        if Path(swtor_shaders_path).exists() == False:
            # self.report({"WARNING"}, "Please check this add-on's preferences' path to the extracted assets 'resources' folder.")
            # return {"CANCELLED"}
            swtor_resources_folderpath = None


        print(CLEAR_TERMINAL + CURSOR_HOME)
        print("========================================")
        print("COPYING ASSETS TO THE CHARACTER'S FOLDER")
        print("========================================")
        print()
        if self.dont_overwrite:
            print("Already existing assets won't be overwritten")
        else:
            print("Already existing assets will be overwritten")
        print()
        print()

        # Check for the existence of a "black.dds" file in resources/art/defaultassets and add one if missing
        if swtor_resources_folderpath:
            place_black_dds(swtor_resources_folderpath)


        if self.filepath.endswith("paths.json") == False:
            self.report({"WARNING"}, "The selected file isn't a 'path.json' file. Please select a correct one.")
            return {"CANCELLED"}
        
        character_folder_name = Path(self.filepath).parent.parent.name

        body_coll_name_in_outliner = "BODY"
        gear_coll_name_in_outliner = "GEAR"


        if swtor_resources_folderpath:

            # Building list of origins and destinations for copying. Each element is:
            # [slotName, type of asset, origin, destination, some report text if needed]
            
            files_to_copy = []
            
            with open(self.filepath, 'r') as file:
                json_data = json.load(file)
                
                # Fill list of files to copy to character folder
                
                character_models_folderpath = str( Path(self.filepath).parent / "models" )
                character_materials_folderpath = str( Path(self.filepath).parent / "materials" )
                character_skeleton_folderpath = str( Path(self.filepath).parent / "skeleton" )
                
                replace_json_data_texturepaths_with_mat_data_ones(json_data, swtor_resources_folderpath)
                
                
                # Save corrected .json info
                corrected_json_data_filepath = str(self.filepath).replace("paths.json", "paths_corrected.json")

                with open(corrected_json_data_filepath, 'w', encoding='utf-8') as json_file:
                    json.dump(json_data, json_file, indent=4)



                for element in json_data:
                    
                    slotName = element["slotName"]
                    
                    if slotName != "skinMats":
                        
                        # NOT SKIN MATERIALS
                        
                        if "models" in element:
                            models =  element["models"]
                            if models:
                                for model in models:
                                    if model[0:1] == "\\" or model[0:1] == "/":
                                        model = model[1:]
                                    origin = str( Path(swtor_resources_folderpath) / Path(model) )
                                    destination = str( Path(character_models_folderpath) / slotName / Path(model).name )
                                    files_to_copy.append([slotName, "model", origin, destination, ""])
                                
                        if "materialInfo" in element:
                            materialInfo = element["materialInfo"]
                            
                            if "matPath" in materialInfo:
                                matPath = materialInfo["matPath"]
                                if matPath[0:1] == "\\" or matPath[0:1] == "/":
                                    matPath = matPath[1:]
                                origin = str( Path(swtor_resources_folderpath) / Path(matPath) )
                                destination = str( Path(character_materials_folderpath) / slotName / Path(matPath).name )
                                files_to_copy.append([slotName, "material definition", origin, destination, ""])
                                
                                additional_texturemaps = get_wrinkles_and_directionmaps(origin)
                                if additional_texturemaps:
                                    for additional_texturemap in additional_texturemaps:
                                        if additional_texturemap[0:1] == "\\" or additional_texturemap[0:1] == "/":
                                            additional_texturemap = additional_texturemap[1:]
                                        origin = str( Path(swtor_resources_folderpath) / Path(additional_texturemap) )
                                        destination = str( Path(character_materials_folderpath) / slotName / Path(additional_texturemap).name )
                                        files_to_copy.append([slotName, "texture map", origin, destination, ""])

                            if "ddsPaths" in materialInfo:
                                ddsPaths = materialInfo["ddsPaths"]
                                if ddsPaths:
                                    for ddsPath in ddsPaths:
                                        if ddsPaths[ddsPath].endswith(".dds"):
                                            ddsPath = ddsPaths[ddsPath]
                                            if ddsPath[0:1] == "\\" or ddsPath[0:1] == "/":
                                                ddsPath = ddsPath[1:]
                                            origin = str( Path(swtor_resources_folderpath) / Path(ddsPath) )
                                            destination = str( Path(character_materials_folderpath) / slotName / Path(ddsPath).name )
                                            files_to_copy.append([slotName, "texture map", origin, destination, ""])

                            if "eyeMatInfo" in materialInfo:
                                if "ddsPaths" in materialInfo["eyeMatInfo"]:
                                    ddsPaths = materialInfo["eyeMatInfo"]["ddsPaths"]
                                    if ddsPaths:
                                        for ddsPath in ddsPaths:
                                            if ddsPaths[ddsPath].endswith(".dds"):
                                                ddsPath = ddsPaths[ddsPath]
                                                if ddsPath[0:1] == "\\" or ddsPath[0:1] == "/":
                                                    ddsPath = ddsPath[1:]
                                                origin = str( Path(swtor_resources_folderpath) / Path(ddsPath) )
                                                destination = str( Path(character_materials_folderpath) / "eye" / Path(ddsPath).name )
                                                files_to_copy.append(["eye", "texture map", origin, destination, ""])


                    else:

                        # SKIN MATERIALS (the dict hierarchy gets deeper and more confusing)
                        
                        if "materialInfo" in element:
                            if "mats" in element["materialInfo"]:
                                mats = element["materialInfo"]["mats"]
                                for mat in mats:
                                    mat_slotName = mat["slotName"]
                                    
                                    if "materialInfo" in mat:
                                        mat_materialInfo = mat["materialInfo"]

                                        if "matPath" in mat_materialInfo:
                                            matPath = materialInfo["matPath"]
                                            if matPath[0:1] == "\\" or matPath[0:1] == "/":
                                                matPath = matPath[1:]
                                            origin = str( Path(swtor_resources_folderpath) / Path(matPath) )
                                            destination = str( Path(character_materials_folderpath) / slotName / mat_slotName / Path(mat_materialInfo["matPath"]).name )
                                            files_to_copy.append([slotName + ": " + mat_slotName, "material definition", origin, destination, ""])

                                    if "ddsPaths" in mat:
                                        mat_ddsPaths = mat["ddsPaths"]
                                        if mat_ddsPaths:
                                            for ddsPath in mat_ddsPaths:
                                                if mat_ddsPaths[ddsPath].endswith(".dds"):
                                                    mat_ddsPath = mat_ddsPaths[ddsPath]
                                                    if mat_ddsPath[0:1] == "\\" or mat_ddsPath[0:1] == "/":
                                                        mat_ddsPath = mat_ddsPath[1:]
                                                    origin = str( Path(swtor_resources_folderpath) / Path(mat_ddsPath) )
                                                    destination = str( Path(character_materials_folderpath) / slotName / mat_slotName / Path(mat_ddsPath).name )
                                                    files_to_copy.append([slotName + ": " + mat_slotName, "texture map", origin, destination, ""])


                # If there is a companion "skeleton.json" file, process it too.
                skeleton_exists = False
                skeleton_filepath = Path(self.filepath).parent / "skeleton.json"
                try:
                    with open(skeleton_filepath, 'r') as skeleton_file:
                        json_data = json.load(skeleton_file)
                        if "path" in json_data:
                            skeleton_model = json_data["path"]
                            if skeleton_model:
                                # Creature-type NPCs might have wrong info from TORC, having a "new" bit
                                # in their names that normally exists only in the eight basic humanoid skeletons.
                                origin = str( Path(swtor_resources_folderpath) / Path(skeleton_model[1:]) )
                                if not Path(origin).exists():
                                    skeleton_model = str(Path(skeleton_model).parent / Path( str( Path(skeleton_model).name ).replace("new", "") ))
                                    origin = str( Path(swtor_resources_folderpath) / Path(skeleton_model[1:]) )
                                    
                                    json_data["path"] = skeleton_model.replace("\\", "/")
                                    skeleton_corrected_filepath = Path(self.filepath).parent / "skeleton_corrected.json"
                                    with open(skeleton_corrected_filepath, 'w') as skeleton_corrected_file:
                                        json.dump(json_data, skeleton_corrected_file)
                                    
                                destination = str( Path(character_skeleton_folderpath) / Path(skeleton_model).name )
                                files_to_copy.append(["Skeleton", "model", origin, destination, ""])
                                skeleton_exists = True
                except Exception as error:
                    pass
                



                # Process list of files to copy to character folder
                
                errors_report = []
                body_part_heading = ""
                
                if files_to_copy:
                    for element in files_to_copy:
                        body_part = element[0]
                        asset_type = element[1]
                        origin = element[2]
                        destination = element[3]
                        report = element[4]
                        
                        if body_part != body_part_heading:
                            print()
                            print(f"{body_part.upper()} ASSETS")
                            print("-" * 80)
                            body_part_heading = body_part
                            
                        print(f"{asset_type.upper()}\nFROM: {origin}\nTO  : {destination}")

                        # If any of the destination folders doesn't exist, create it
                        # ('eye', typically, plus any new one such as 'skeleton')
                        if Path(destination).parent.exists() == False:
                            try:
                                os.makedirs(Path(destination).parent, mode=0o777, exist_ok=True) # mode required to make folders user-accessible
                                # Path(destination).parent.makedirs(parents=False, exist_ok=True)
                                print("Creating " + str(Path(destination).parent) + "folder.\n")
                            except Exception as e:
                                print("ERROR!!!--------: The folder ",destination," didn't exist and when trying to create it an error occurred:\n",e,"\n")
                        
                        if Path(destination).exists() == True and self.dont_overwrite == True:
                            print("FILE ALREADY EXISTS IN DESTINATION. PRESERVED")
                        else:
                            # File copy as such:
                            if not ( destination.endswith('\\.dds') or destination.endswith('/.dds') ):
                                try:
                                    shutil.copy2(origin, destination)
                                    print("COPIED")
                                except Exception as e:
                                    print("ERROR!!!-------- ", str(e))
                                    print()
                                    errors_report.append(body_part + " - " + asset_type + " - " + str(origin))
                        
                        print()
                            
            print("ASSETS COPYING DONE!")
            print()
            if errors_report:
                print("Some files failed to be copied:\n")
                for error_report in errors_report:
                    print("     " + error_report)
                print("\nPlease check the console for their related error messages, and their entries in the 'paths.json' and/or related .mat files.")
                
                self.report({'INFO'}, "Character's Assets copied to its folder. SOME FILES FAILED TO BE COPIED! Check the console's output." )
            else:
                self.report({'INFO'}, "Character's Assets copied to its folder" )
            
            
        
        # Importing objects if set so
        
        if self.gather_only == False:
            print("=============================================")
            print("IMPORTING CHARACTER")
            print("Importing and assembling the character assets")
            print("via the .gr2 Add-on's .json importer feature.")
            print("Its own progress reports follow now:")
            print("=============================================")
            print()

            # We do a after-minus-before bpy.data.objects check to determine
            # the objects resulting from the importing, as the addon doesn't
            # return that information.
            objects_before_importing = list(bpy.data.objects)
            
            # Calling Darth Atroxa's Character Importer in his .gr2 Importer Addon.
            try:
                result = bpy.ops.import_mesh.gr2_json(filepath = corrected_json_data_filepath, npc_uses_skin = self.npc_uses_skin)
                print(result)
                if result == {"CANCELLED"}:
                    print(f"\n\nWARNING: .gr2 Importer Addon failed to import {self.filepath}\n\n")
                else:
                    print("\n\nCharacter's Path File successfully processed by the .gr2 Importer Add-on!\n\n")
            except Exception as e:
                print(f"\n\nWARNING: the .gr2 Importer addon CRASHED while importing:\n{self.filepath}\n\n")
                print("Its error report was:")
                print("-" * 80)
                print(e)
                print("-" * 80)
                print()
                print("CANCELLING CHARACTER IMPORT")
                report_text = "The .gr2 Importer Add-on crashed while processing this character's Path file. \nPlease check if any of its assets is missing. "
                if swtor_resources_folderpath == None:
                    report_text += "\nIf a SWTOR assets extraction's 'resources' folder is available, set it in this Add-on's Preferences and try again."
                self.report({"WARNING"}, report_text)
                return {"CANCELLED"}

            print("==========================================")
            print("TIDYING THINGS UP")
            print("Organizing the results, importing skeleton")
            print("if chosen so, etc.")
            print("==========================================")
            print()

            objects_after_importing = list(bpy.data.objects)
            
            character_objects = list(set(objects_after_importing) - set(objects_before_importing))

            
            # Check for Twi'lek heads to correct their eyes' UVs
            # (do it before separating eye objects just in case)
            if self.correct_twilek_eyes_uv:
                for obj in character_objects:
                    if "head_twilek" in obj.name:
                        translate_uv_coordinates(obj, 1, (0, -2) )
                        break
            
            
            # Separate character's eye objects
            if self.separate_eyes:
                has_eyes = False
                for obj in character_objects:
                    if "head" in obj.name.lower():
                        if len(obj.material_slots) > 1:
                            if "eye" in obj.material_slots[1].name.lower():
                                has_eyes = True
                                
                                # Duplicate head object
                                eyes_obj = duplicate_obj(obj)
                                
                                # Delete eyes' polys and material from head object
                                separate_obj_by_specific_materials(obj, obj.material_slots[1].name, separate = False)
                                
                                # Delete head's polys and material from eyes object (the duplicate head object)
                                separate_obj_by_specific_materials(eyes_obj, eyes_obj.material_slots[0].name, separate = False)
                                
                                if not self.separate_each_eye:
                                    # Rename eyes object
                                    eyes_obj.name = f"{obj.name}.eyes"
                                    character_objects.append(eyes_obj)
                                else:
                                    eyes_obj_right = eyes_obj
                                    eyes_obj_left  = duplicate_obj(eyes_obj)
                                    
                                    delete_polygons_on_side(eyes_obj_right, side='LEFT')
                                    highest_vertex, lowest_vertex = get_highest_and_lowest_vertices(eyes_obj_right)
                                    new_origin_location = (highest_vertex.x, highest_vertex.y, (highest_vertex.z + lowest_vertex.z) / 2)
                                    set_obj_origin(eyes_obj_right, new_origin_location)
                                    
                                    eyes_obj_right.name = f"{obj.name}.eyes.right"
                                    character_objects.append(eyes_obj_right)

                                    delete_polygons_on_side(eyes_obj_left, side='RIGHT')
                                    highest_vertex, lowest_vertex = get_highest_and_lowest_vertices(eyes_obj_left)
                                    new_origin_location = (highest_vertex.x, highest_vertex.y, (highest_vertex.z + lowest_vertex.z) / 2)
                                    set_obj_origin(eyes_obj_left, new_origin_location)
                                    
                                    eyes_obj_left.name = f"{obj.name}.eyes.left"
                                    character_objects.append(eyes_obj_left)
                                    
                                
                                # eyes_obj, eye_r_obj, eye_l_obj, head_obj = separate_eyes(self, obj)
                        
                                if eyes_obj:
                                    character_objects.append(eyes_obj)
                                        
                                # if eye_r_obj:
                                #     character_objects.extend( [eye_r_obj, eye_l_obj, head_obj] )
                        else:
                            print("NO MATERIAL TO SEPARATE EYES BY:\nThis character's head object has no multiple materials that we could use\nto separate eye objects by.")
                        break
                if not has_eyes:
                    print("NO OBJECT WITH FACIAL FEATURES TO SEPARATE EYES FROM.\n")

            # Importing skeleton, if any, using Atroxa's .gr2 Importer Addon.
            if self.import_skeleton:
                objects_before_importing = list(bpy.data.objects)

                skeleton_filepath = str( Path(character_skeleton_folderpath) / Path(skeleton_model).name )
                try:
                    result = bpy.ops.import_mesh.gr2(filepath=skeleton_filepath)
                    if result == "CANCELLED":
                        print(f"\n\nWARNING: .gr2 Importer Addon failed to import {skeleton_filepath}\n\n")
                        skeleton_exists = False
                        skeleton_object = []
                    else:
                        print("\nSkeleton Object Imported\n")
                                                
                        skeleton_object = list( set(bpy.data.objects).difference(objects_before_importing) )[0]
                        skeleton_object.show_in_front = True

                        # Binding character's objects to skeleton
                        if character_objects and self.bind_to_skeleton:
                            bind_objects_to_armature(character_objects, skeleton_object)
                            print("Character's Objects Bound To Skeleton")
                    
                except:
                    print(f"\n\nWARNING: the .gr2 Importer addon CRASHED while importing:\n{skeleton_filepath}\n\n")
                    skeleton_exists = False
                    skeleton_object = []
                
            
            # identify what's armor and what's body parts
            armor_slots = ["face", "chest", "bracer", "hand", "waist", "leg", "boot"]
            armor_gear_objects = []
            body_parts_objects = []
            for obj in character_objects:
                if (
                    "underwear" in obj.name
                    or "naked" in obj.name
                    or (obj.name.split("_")[0] not in armor_slots)
                    ):
                    body_parts_objects.append(obj)
                else:
                    armor_gear_objects.append(obj)


            # COLLECTIONING
            
            # if skeleton_exists and self.import_skeleton:
            if self.import_skeleton:
                if skeleton_object:
                    link_objects_to_collection(skeleton_object, character_folder_name, create = True, move = True)


            if armor_gear_objects:
                if self.collect:
                    # Parsing "preset.json" to get the in-game names for the armor, if any,
                    # and creating Collections with their names
                    # and moving the armor objects to them
                    character_preset_filepath = str( Path(self.filepath).parent / "preset.json" )
                    if Path(character_preset_filepath).exists():
                        with open(character_preset_filepath, 'r') as preset_file:
                            json_data = json.load(preset_file)
                            armor_gear_collections = []
                            for element in json_data:
                                if "Gear" in element:
                                    if json_data[element] != None:
                                        in_game_name = json_data[element]["name"]
                                        objects_for_this_slot = []
                                        for obj in armor_gear_objects:
                                            if json_data[element]["slot"] in obj.name:
                                                objects_for_this_slot.append(obj)
                                        if objects_for_this_slot:
                                            link_objects_to_collection(objects_for_this_slot, in_game_name, create = True, move = True)
                                            link_collections_to_collection (in_game_name, gear_coll_name_in_outliner, create = True, move = True)
                                            armor_gear_collections.append(bpy.data.collections[in_game_name])

                            # Collect armor parts in collections, and collect those in G
                            if armor_gear_collections:
                                link_collections_to_collection(gear_coll_name_in_outliner, character_folder_name, create = True, move = True)
                else:
                    link_objects_to_collection(armor_gear_objects, character_folder_name, create = True, move = True)
            else:
                print("\nThis character has no armor gear.\n")
                

            if body_parts_objects:
                if self.import_armor_only:
                    for obj in body_parts_objects:
                        bpy.data.objects.remove(obj)
                else:
                    if self.collect:
                        link_objects_to_collection(body_parts_objects, body_coll_name_in_outliner, create = True, move = True)
                        link_collections_to_collection(body_coll_name_in_outliner, character_folder_name, create = True, move = True)
                    else:
                        link_objects_to_collection(body_parts_objects, character_folder_name, create = True, move = True)
            else:
                print("\nThis character has no naked or default underwear body parts\n")
                
            print()
            print("DONE!")
            print()
            print(f"TOTAL TIME ELAPSED: {(time.time() - start_time):.3f} s.")
            print()
            
        return {'FINISHED'}




# REGISTRATIONS ---------------------------------------------

classes = [
    ZGSWTOR_OT_character_assembler,
]

def register():
    bpy.utils.register_class(ZGSWTOR_OT_character_assembler)

    bpy.types.Scene.zg_swca_gather_only_bool = bpy.props.BoolProperty(
        name="Gather Assets Only",
        description="Don't import the character, just copy the required assets\nto the Character's folder",
        default = False,
    )
    
    bpy.types.Scene.zg_swca_dont_overwrite_bool = bpy.props.BoolProperty(
        name="Don't overwrite Existing assets",
        description="If the character's folder contains some assets already, don't overwrite those.\nThat will preserve any changes done to them, such as manual retouchings",
        default = False,
    )

    bpy.types.Scene.zg_swca_collect_bool = bpy.props.BoolProperty(
        name="Collect By In-Game Names",
        description="Organizes the Character's Objects in Collections named after their in-game names.\nThe Collections will be set inside the currently Active Collection in the Outliner",
        default = True,
    )

    bpy.types.Scene.zg_swca_import_armor_only = bpy.props.BoolProperty(
        name="Import Armor Gear Only",
        description="Import only the armor gear elements and omit the rest of the body",
        default = False,
    )

    bpy.types.Scene.zg_swca_import_skeleton_bool = bpy.props.BoolProperty(
        name="Import Rigging Skeleton",
        description="Import the character's Skeleton Object if available",
        default = True,
    )

    bpy.types.Scene.zg_swca_bind_to_skeleton_bool = bpy.props.BoolProperty(
        name="Bind Objects To Skeleton",
        description="Bind all objects to the skeleton, if imported",
        default = True,
    )

    bpy.types.Scene.zg_swca_separate_eyes = bpy.props.BoolProperty(
        name="Separate Eyes From Head Object",
        description="Separates the eyes from the character's head object to make them\neasier to rig and animate (certain rigging systems require that).\nNeeds them to be using a material with 'eye' in its name, as separating criteria.\n\nThe result is a single object with both eyes.\nTo further separate them into individual eyes,\nuse the 'As Two Eye Objects' option, too.\n\nThis doesn't affect the ability to keep using\nSWTOR skeletons with the model's eyes",
        default = False,
    )

    bpy.types.Scene.zg_swca_separate_each_eye = bpy.props.BoolProperty(
        name="As Two Eye Objects",
        description="When separating the eyes from the character's head object\nmake each eye its own object and set their origin points\nso that they can also be posed via simple rotations.\n\nThis doesn't affect the ability to keep using\nSWTOR skeletons with the model's eyes",
        default = False,
        # options={'HIDDEN'}
    )

    bpy.types.Scene.zg_correct_twilek_eyes_uv = bpy.props.BoolProperty(
        name="Correct Twi'lek's Eyes' UVs",
        description="When importing a Twi'lek character, reposition their eyes' UVs\ninside their textures' area so that they produce correct results\nin baking operations.\n\n(This doesn't affect renderings)",
        default = True,
    )

    bpy.types.Scene.zg_npc_uses_skin = bpy.props.BoolProperty(
        name="NPC Gear's Mat #2 is Skin",
        description="When importing a non-Creature-type NPC, assume that any 2nd. Material Slots\nin armor or clothes are skin. If unticked, use a garment material instead.\n\nMOST NPC GEAR LACK SECOND MATERIALS, ANYWAY.\nTypical case actually using this checkbox: cantina dancers.\n\nIn mixed use cases, the Material Slots' assignments can be easily corrected\nmanually. Skin materials are always created, no matter if not in use.\n\n(TORCommunity.com's non-Creature NPC database exports don't include\n'materialSkinIndex' data indicating whether a piece of garment with two\nmaterial slots uses skin or garment for the 2nd one. Hence this checkbox)",
        default = True,
        # options={'HIDDEN'}
    )



def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_character_assembler) 
        
    del bpy.types.Scene.zg_swca_gather_only_bool
    del bpy.types.Scene.zg_swca_dont_overwrite_bool
    del bpy.types.Scene.zg_swca_collect_bool
    del bpy.types.Scene.zg_swca_import_skeleton_bool
    del bpy.types.Scene.zg_swca_bind_to_skeleton_bool
    del bpy.types.Scene.zg_swca_separate_eyes
    del bpy.types.Scene.zg_correct_twilek_eyes_uv
    del bpy.types.Scene.zg_npc_uses_skin


if __name__ == "__main__":
    register()