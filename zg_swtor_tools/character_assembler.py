import bpy
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator

import os
from pathlib import Path
import shutil

import json
import xml.etree.ElementTree as ET



# Aux Functions

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

def black_dds(swtor_resources_folderpath):
    addon_directory = os.path.dirname(__file__)

    black_dds_origin = Path(addon_directory) / "black.dds"
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
                for scene_collection in list(bpy.context.scene.collection.children):
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


# Class

class ZGSWTOR_OT_character_assembler(Operator):
    bl_label = "SWTOR Character Assembler"
    bl_idname = "zgswtor.character_assembler"
    bl_description = "Processes the 'path.json' file in a Player Character/NPC folder\nexported by TORCommunity.com, filling its subfolders with all\nrelated objects and textures, then importing the Character\n\n• Requires setting the path to a 'resources' folder in this addon's Preferences"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: StringProperty(subtype='FILE_PATH')


    # Some properties
    
    gather_only: bpy.props.BoolProperty(
        name="Gather Assets Only",
        description="Don't Import The Character, and just copy the required assets\nto the Character's folder",
        default = False,
        options={'HIDDEN'}
    )

    dont_overwrite: bpy.props.BoolProperty(
        name="Don't overwrite Existing assets",
        description="If the character's folder contains some assets already, don't overwrite those.\nThat will preserve any changes done to them, such as manual retouchings",
        default = True,
        options={'HIDDEN'}
    )

    collect: bpy.props.BoolProperty(
        name="Collect By In-game Names",
        description="Organize the Character's Objects in Collections named after their in-game names.\nThe Collections will be set inside the currently Active Collection in the Outliner.",
        default = True,
        options={'HIDDEN'}
    )
    
    import_armor_only: bpy.props.BoolProperty(
        name="Import Armor Gear Only",
        description="Import only the armor gear elements and omit the rest of the body.",
        default = False,
        options={'HIDDEN'}
    )

    import_skeleton: bpy.props.BoolProperty(
        name="Import Rigging Skeleton",
        description="Import the character's Skeleton Object if available.",
        default = True,
        options={'HIDDEN'}
    )

    bind_to_skeleton: bpy.props.BoolProperty(
        name="Bind Objects To Skeleton",
        description="Bind all objects to the skeleton, if imported.",
        default = True,
        options={'HIDDEN'}
    )

    prefix_everything: bpy.props.BoolProperty(
        name="Prefix All Names With:",
        description="Prefix all objects, their Materials, and the Collections they are in\nwith the text in the following field.",
        default = True,
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


        # Sync properties with their UI matches
        self.gather_only = context.scene.swca_gather_only_bool
        self.dont_overwrite = context.scene.swca_dont_overwrite_bool
        self.collect = context.scene.swca_collect_bool
        self.import_armor_only = context.scene.swca_import_armor_only
        self.import_skeleton = context.scene.swca_import_skeleton_bool
        self.bind_to_skeleton = context.scene.swca_bind_to_skeleton_bool

        # Get the extracted SWTOR assets' "resources" folder from the add-on's preferences. 
        swtor_resources_folderpath = bpy.context.preferences.addons[__package__].preferences.swtor_resources_folderpath
        swtor_shaders_path = swtor_resources_folderpath + "/art/shaders/materials"
        # Test the existence of the shaders subfolder to validate the SWTOR "resources" folder
        if Path(swtor_shaders_path).exists() == False:
            self.report({"WARNING"}, "Please check this add-on's preferences' path to the extracted assets 'resources' folder.")
            return {"CANCELLED"}


        print(CLEAR_TERMINAL + CURSOR_HOME)
        print("=================================")
        print("CHARACTER FOLDER'S ASSETS LOCATOR")
        print("=================================")
        print()
        print()

        # Check for the existence of a "black.dds" file in resources/art/defaultassets and add one if missing
        black_dds(swtor_resources_folderpath)


        if self.filepath.endswith("paths.json") == False:
            self.report({"WARNING"}, "The selected file isn't a 'path.json' file. Please select a correct one.")
            return {"CANCELLED"}
        
        character_folder_name = Path(self.filepath).parent.parent.name

        body_coll_name_in_outliner = "BODY"
        gear_coll_name_in_outliner = "GEAR"

        # list of origins and destinations for copying. Each element is:
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
            with open(skeleton_filepath, 'r') as skeleton_file:
                json_data = json.load(skeleton_file)
                if "path" in json_data:
                    skeleton_model = json_data["path"]
                    if skeleton_model:
                        origin = str( Path(swtor_resources_folderpath) / Path(skeleton_model[1:]) )
                        destination = str( Path(character_skeleton_folderpath) / Path(skeleton_model).name )
                        files_to_copy.append(["Skeleton", "model", origin, destination, ""])
                        skeleton_exists = True



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
                            Path(destination).parent.mkdir(parents=False, exist_ok=True)
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
                if result == "CANCELLED":
                    print(f"\n\nWARNING: .gr2 Importer Addon failed to import {skeleton_filepath}")
                else:
                    print("CHARACTER IMPORTING DONE!")
            except:
                print(f"WARNING: the .gr2 Importer addon CRASHED while importing:\n{skeleton_filepath}")

            objects_after_importing = list(bpy.data.objects)
            
            character_objects = list(set(objects_after_importing) - set(objects_before_importing))



            # Importing skeleton, if any, using Atroxa's .gr2 Importer Addon.
            if skeleton_exists and self.import_skeleton:
                objects_before_importing = list(bpy.data.objects)

                skeleton_filepath = str( Path(character_skeleton_folderpath) / Path(skeleton_model).name )
                try:
                    result = bpy.ops.import_mesh.gr2(filepath=skeleton_filepath)
                    if result == "CANCELLED":
                        print(f"\n\nWARNING: .gr2 Importer Addon failed to import {skeleton_filepath}")
                        skeleton_exists = False
                        skeleton_object = []
                    else:
                        print("\nSkeleton Object Imported\n")
                        
                        objects_after_importing = list(bpy.data.objects)
                        
                        skeleton_object = list(set(objects_after_importing) - set(objects_before_importing))[0]

                        # Binding character's objects to skeleton
                        if character_objects and self.bind_to_skeleton:
                            for obj in character_objects:
                                obj.parent = skeleton_object
                                obj.parent_type = "ARMATURE"
                                obj.matrix_parent_inverse = skeleton_object.matrix_world.inverted()
                                skeleton_object.show_in_front = True
                                
                            print("Character's Objects Bound To Skeleton")
                    
                except:
                    print(f"WARNING: the .gr2 Importer addon CRASHED while importing:\n{skeleton_filepath}")
                    skeleton_exists = False
                
            
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
            
            if skeleton_exists and self.import_skeleton:
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


    # File Browser for selecting paths.json file
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}






# REGISTRATIONS ---------------------------------------------

classes = [
    ZGSWTOR_OT_character_assembler,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.swca_gather_only_bool = bpy.props.BoolProperty(
        name="Gather Assets Only",
        description="Don't import the character, just copy the required assets\nto the Character's folder",
        default = False,
    )
    bpy.types.Scene.swca_dont_overwrite_bool = bpy.props.BoolProperty(
        name="Don't overwrite Existing assets",
        description="If the character's folder contains some assets already, don't overwrite those.\nThat will preserve any changes done to them, such as manual retouchings",
        default = True,
    )

    bpy.types.Scene.swca_collect_bool = bpy.props.BoolProperty(
        name="Collect By In-Game Names",
        description="Organizes the Character's Objects in Collections named after their in-game names.\nThe Collections will be set inside the currently Active Collection in the Outliner.",
        default = True,
    )

    bpy.types.Scene.swca_import_armor_only = bpy.props.BoolProperty(
        name="Import Armor Gear Only",
        description="Import only the armor gear elements and omit the rest of the body.",
        default = False,
    )

    bpy.types.Scene.swca_import_skeleton_bool = bpy.props.BoolProperty(
        name="Import Rigging Skeleton",
        description="Import the character's Skeleton Object if available.",
        default = False,
    )

    bpy.types.Scene.swca_bind_to_skeleton_bool = bpy.props.BoolProperty(
        name="Bind Objects To Skeleton",
        description="Bind all objects to the skeleton, if imported.",
        default = False,
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls) 
        
    del bpy.types.Scene.swca_gather_only_bool
    del bpy.types.Scene.swca_dont_overwrite_bool
    del bpy.types.Scene.swca_collect_bool
    del bpy.types.Scene.swca_import_skeleton_bool
    del bpy.types.Scene.swca_bind_to_skeleton_bool


if __name__ == "__main__":
    register()