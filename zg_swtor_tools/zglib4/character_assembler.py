import bpy

import bmesh
import mathutils
from mathutils import Vector, Matrix
import numpy as np


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
from ..utils.addon_checks import requirements_checks


ADDON_ROOT = __file__.rsplit(__name__.rsplit(".")[0])[0] + __name__.rsplit(".")[0]


# Aux Functions

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

def separate_eyes(self, obj_to_separate):
    
    # SEPARATE BY MATERIAL ----------------
    
    objs_before_separating = list(bpy.data.objects)
    
    # Make object Active
    bpy.context.view_layer.objects.active = obj_to_separate
    # Switch object to edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Separate by material
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='MATERIAL')
    
    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
        
    separated_obj = list( set(bpy.data.objects).difference(objs_before_separating) )[0]
    
    
    # Determine which object is the eyes: the remainder of the original,
    # which still exists in bpy.data.objects, modified by the operator,
    # or the new one resulting from separating by material.
    # Uses polycount as eye detector (eyes' polycount < head's polycount).
    if len(separated_obj.data.polygons) < len(obj_to_separate.data.polygons):
        eyes_obj = separated_obj
        head_obj = obj_to_separate
    else:
        eyes_obj = obj_to_separate
        head_obj = separated_obj
    
    # Some renaming to avoid ".00x" suffixes.
    # (this could be smarter but I can't be bothered)
    if head_obj.name[-3:].isdigit():
        head_obj.name = head_obj.name[:-4]
    head_obj.data.name = head_obj.name
        
    if eyes_obj.name[-3:].isdigit():
        eyes_obj.name = eyes_obj.name[:-4] + ".eyes"
    else:
        eyes_obj.name = eyes_obj.name + ".eyes"
    eyes_obj.data.name = eyes_obj.name
    
    if not self.separate_each_eye:
        return eyes_obj, None, None, head_obj


    # SEPARATE BY SIDE OF YZ ----------------
    
    objs_before_separating = list(bpy.data.objects)
    
    # Separate by selection
    select_faces_right_of_plane(eyes_obj, threshold=0.0)
    bpy.ops.mesh.separate(type="SELECTED")

    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    objs_after_separating_by_yz = list(bpy.data.objects)
    
    separated_objs = list( set(objs_after_separating_by_yz).difference(objs_before_separating) )
    
    eye_l_obj = eyes_obj
    eye_r_obj = separated_objs[0]
    
    eye_l_obj.name = eye_l_obj.name + ".l"
    eye_l_obj.data.name = eye_l_obj.name
    
    eye_r_obj.name = eye_r_obj.name[:-4] + ".r"
    eye_r_obj.data.name = eye_r_obj.name


    # REPOSITION EYES' ORIGINS ----------------

    highest_vertex, lowest_vertex = find_highest_lowest_vertices(eye_l_obj)
    new_origin_location = (highest_vertex + lowest_vertex) / 2
    set_mesh_origin(eye_l_obj, new_origin_location)
    
    highest_vertex, lowest_vertex = find_highest_lowest_vertices(eye_r_obj)
    new_origin_location = (highest_vertex + lowest_vertex) / 2
    set_mesh_origin(eye_r_obj, new_origin_location)

    return None, eye_r_obj, eye_l_obj, head_obj

def select_faces_right_of_plane(obj, threshold=0.0):
    # Make object Active
    bpy.context.view_layer.objects.active = obj
    # Switch object to edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    # Deselect all
    bpy.ops.mesh.select_all(action='DESELECT')

    bm = bmesh.from_edit_mesh(obj.data)

    # Define the YZ plane
    plane_normal = Vector((1, 0, 0))  # Normal vector of the YZ plane
    plane_origin = Vector((0, 0, 0))  # Origin point of the YZ plane

    for face in bm.faces:
        # Calculate the center of the face
        face_center = sum((v.co for v in face.verts), Vector()) / len(face.verts)
        
        # Calculate the vector from the origin to the face center
        vec_to_center = face_center - plane_origin

        # Calculate the dot product between the vector to the center and the plane normal
        dot_product = vec_to_center.dot(plane_normal)

        # If dot product is greater than the threshold, select the face
        if dot_product > threshold:
            face.select = True

    bmesh.update_edit_mesh(obj.data)

def find_highest_lowest_vertices(obj):
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

def set_mesh_origin(obj, pos):
    '''Given a mesh object set it's origin to a given position.'''
    # Casting pos to vector so you can pass in tuples or lists
    pos = Vector(pos)
    mat = Matrix.Translation(pos - obj.location)
    obj.location = pos
    obj.data.transform(mat.inverted())
    # obj.data.update()



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
        default = True,
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

        # Open File Browser.
        context.window_manager.fileselect_add(self)
        
        return {'RUNNING_MODAL'}



    # File Browsing properties

    filter_glob: bpy.props.StringProperty(
        default='*.json;',  # file wildcards separated by semicolons
        options={'HIDDEN'}
    )






    def execute(self, context):
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
        print("=================================")
        print("CHARACTER FOLDER'S ASSETS LOCATOR")
        print("=================================")
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
                
                for element in json_data:
                    
                    slotName = element["slotName"]
                    
                    if slotName != "skinMats":
                        
                        # NOT SKIN MATERIALS
                        
                        if "models" in element:
                            models =  element["models"]
                            if models:
                                for model in models:
                                    origin = str( Path(swtor_resources_folderpath) / Path(model[1:]) )
                                    destination = str( Path(character_models_folderpath) / slotName / Path(model).name )
                                    files_to_copy.append([slotName, "model", origin, destination, ""])
                                
                        if "materialInfo" in element:
                            materialInfo = element["materialInfo"]
                            
                            if "matPath" in materialInfo:
                                origin = str( Path(swtor_resources_folderpath) / Path(materialInfo["matPath"][1:]) )
                                destination = str( Path(character_materials_folderpath) / slotName / Path(materialInfo["matPath"]).name )
                                files_to_copy.append([slotName, "material definition", origin, destination, ""])
                                
                                additional_texturemaps = get_wrinkles_and_directionmaps(origin)
                                if additional_texturemaps:
                                    for additional_texturemap in additional_texturemaps:
                                        origin = str( Path(swtor_resources_folderpath) / Path(additional_texturemap[1:]) )
                                        destination = str( Path(character_materials_folderpath) / slotName / Path(additional_texturemap).name )
                                        files_to_copy.append([slotName, "material definition", origin, destination, ""])

                            if "ddsPaths" in materialInfo:
                                ddsPaths = materialInfo["ddsPaths"]
                                if ddsPaths:
                                    for ddsPath in ddsPaths:
                                        if ddsPaths[ddsPath].endswith(".dds"):
                                            origin = str( Path(swtor_resources_folderpath) / Path(ddsPaths[ddsPath][1:]) )
                                            destination = str( Path(character_materials_folderpath) / slotName / Path(ddsPaths[ddsPath]).name )
                                            files_to_copy.append([slotName, "texture map", origin, destination, ""])

                            if "eyeMatInfo" in materialInfo:
                                if "ddsPaths" in materialInfo["eyeMatInfo"]:
                                    ddsPaths = materialInfo["eyeMatInfo"]["ddsPaths"]
                                    if ddsPaths:
                                        for ddsPath in ddsPaths:
                                            if ddsPaths[ddsPath].endswith(".dds"):
                                                origin = str( Path(swtor_resources_folderpath) / Path(ddsPaths[ddsPath][1:]) )
                                                destination = str( Path(character_materials_folderpath) / "eye" / Path(ddsPaths[ddsPath]).name )
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
                                            origin = str( Path(swtor_resources_folderpath) / Path(mat_materialInfo["matPath"][1:]) )
                                            destination = str( Path(character_materials_folderpath) / slotName / mat_slotName / Path(mat_materialInfo["matPath"]).name )
                                            files_to_copy.append([slotName + ": " + mat_slotName, "material definition", origin, destination, ""])
                                
                                            additional_texturemaps = get_wrinkles_and_directionmaps(origin)
                                            if additional_texturemaps:
                                                for additional_texturemap in additional_texturemaps:
                                                    origin = str( Path(swtor_resources_folderpath) / Path(additional_texturemap[1:]) )
                                                    destination = str( Path(character_materials_folderpath) / slotName / Path(additional_texturemap).name )
                                                    files_to_copy.append([slotName, "material definition", origin, destination, ""])

                                    if "ddsPaths" in mat:
                                        mat_ddsPaths = mat["ddsPaths"]
                                        if mat_ddsPaths:
                                            for ddsPath in mat_ddsPaths:
                                                if mat_ddsPaths[ddsPath].endswith(".dds"):
                                                    origin = str( Path(swtor_resources_folderpath) / Path(mat_ddsPaths[ddsPath][1:]) )
                                                    destination = str( Path(character_materials_folderpath) / slotName / mat_slotName / Path(mat_ddsPaths[ddsPath]).name )
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
                                origin = str( Path(swtor_resources_folderpath) / Path(skeleton_model[1:]) )
                                destination = str( Path(character_skeleton_folderpath) / Path(skeleton_model).name )
                                files_to_copy.append(["Skeleton", "model", origin, destination, ""])
                                skeleton_exists = True
                except Exception as error:
                    pass
                



                # Process list of files to copy to character folder
                
                errors_report = []
                
                if files_to_copy:
                    for element in files_to_copy:
                        body_part = element[0]
                        asset_type = element[1]
                        origin = element[2]
                        destination = element[3]
                        report = element[4]
                        
                        print(body_part, "-", asset_type, "\n",origin, "\n",destination)

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
                            try:
                                shutil.copy2(origin, destination)
                                print("COPIED")
                            except Exception as e:
                                print("ERROR!!!-------- ", str(e))
                                print()
                                errors_report.append(body_part + " - " + asset_type + " - " + str(origin))
                        
                        print()
                            
            print("ASSETS GATHERING DONE!")
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
            print("IMPORTING CHARACTER")
            print("Importing and assembling the character assets")
            print()

            # We do a after-minus-before bpy.data.objects check to determine
            # the objects resulting from the importing, as the addon doesn't
            # return that information.
            objects_before_importing = list(bpy.data.objects)
            
            # Calling Darth Atroxa's Character Importer in his .gr2 Importer Addon.
            try:
                result = bpy.ops.import_mesh.gr2_json(filepath = str( self.filepath ))
                print(result)
                if result == {"CANCELLED"}:
                    print(f"\n\nWARNING: .gr2 Importer Addon failed to import {self.filepath}\n\n")
                else:
                    print("\n\nCharacter's Path File successfully processed by the .gr2 Importer Add-on!\n\n")
            except:
                print(f"\n\nWARNING: the .gr2 Importer addon CRASHED while importing:\n{self.filepath}\n\n")
                print("CANCELLING CHARACTER IMPORT")
                report_text = "The .gr2 Importer Add-on crashed while processing this character's Path file. \nPlease check if any of its assets is missing. "
                if swtor_resources_folderpath == None:
                    report_text += "\nIf a SWTOR assets extraction's 'resources' folder is available, set it in this Add-on's Preferences and try again."
                self.report({"WARNING"}, report_text)
                return {"CANCELLED"}

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
                for obj in character_objects:
                    if "head" in obj.name:
                        eyes_obj, eye_r_obj, eye_l_obj, head_obj = separate_eyes(self, obj)
                        break
                
                if eyes_obj:
                        character_objects.append(head_obj)
                        
                if eye_r_obj:
                        character_objects.extend( [eye_r_obj, eye_l_obj, head_obj] )


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
        default = True,
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
        description="Separates the eyes from the character's head object to make them\neasier to rig and animate (certain rigging systems require that).\nNeeds them to be using a material with 'eye' in its name, as separating criteria.\n\nThe result is a single object with both eyes.\n\nTo further separate them into individual eyes,\nuse the 'As Two Eye Objects' option, too",
        default = False,
    )

    bpy.types.Scene.zg_swca_separate_each_eye = bpy.props.BoolProperty(
        name="As Two Eye Objects",
        description="When separating the eyes from the character's head object\nmake each eye its own object and set their origin points\nso that they can also be posed via simple rotations",
        default = False,
        # options={'HIDDEN'}
    )

    bpy.types.Scene.zg_correct_twilek_eyes_uv = bpy.props.BoolProperty(
        name="Correct Twi'lek's Eyes' UVs",
        description="When importing a Twi'lek character, reposition their eyes' UVs\ninside their textures' area so that they produce correct results\nin baking operations.\n\n(This doesn't affect renderings)",
        default = True,
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


if __name__ == "__main__":
    register()