import bpy
import json
from bpy.props import StringProperty
from bpy.types import Operator
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET



# Functions

def get_wrinkles_and_directionmaps(mat_file_abs_path):
    '''Reads a shader .mat file and returns any DirectionMap
    and WrinkleMap paths in an as is basis
    (slashes, backslashes, initial ones…)'''
    
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



class ZGSWTOR_OT_locate_character_assets(Operator):
    bl_label = "ZG Locate Character's Assets"
    bl_idname = "zgswtor.locate_character_assets"
    bl_description = "Processes the 'path.json' file in a Player Character/NPC folder\nexported by TORCommunity.com, filling its subfolders\nwith all related objects and textures.\n\n• Requires setting the path to a 'resources' folder in this addon's Preferences"
    filepath: StringProperty(subtype='FILE_PATH')

    def execute(self, context):
        # Terminal's VT100 escape codes (most terminals understand them).
        # See: http://www.climagic.org/mirrors/VT100_Escape_Codes.html
        # (replacing ^[ in terminal codes with \033)
        CLEAR_TERMINAL = '\033[2J'      # Clear entire screen.
        CURSOR_HOME = '\033[H'          # Move cursor to upper left corner.
        CLEAR_EOL = '\r\033[K'          # Erase to end of current line.
        LINE_BACK_1ST_COL = '\033[F'    # Move cursor one line up, 1st column.


        # Get the extracted SWTOR assets' "resources" folder from the add-on's preferences. 
        swtor_resources_folderpath = bpy.context.preferences.addons[__package__].preferences.swtor_resources_folderpath
        swtor_shaders_path = swtor_resources_folderpath + "/art/shaders/materials"
        # Test the existence of the shaders subfolder to validate the SWTOR "resources" folder
        if Path(swtor_shaders_path).exists() == False:
            self.report({"WARNING"}, "Please check this add-on's preferences' path to the extracted assets 'resources' folder.")
            return {"CANCELLED"}


        if self.filepath.endswith("paths.json") == False:
            self.report({"WARNING"}, "The selected file isn't a 'path.json' file. Please select a correct one.")
            return {"CANCELLED"}

        # Process .json file
        print(CLEAR_TERMINAL + CURSOR_HOME)
        print("=================================")
        print("CHARACTER FOLDER'S ASSETS LOCATOR")
        print("=================================")
        print()
        print("Processing JSON file:\n" + self.filepath)
        print()
        print()
        
        # list of origins and destinations for copying. Each element is:
        # [slotName, type of asset, origin, destination, report if any]
        
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
            skeleton_filepath = Path(self.filepath).parent / "skeleton.json"
            with open(skeleton_filepath, 'r') as skeleton_file:
                json_data = json.load(skeleton_file)
                if "path" in json_data:
                    skeleton_model = json_data["path"]
                    if skeleton_model:
                        origin = str( Path(swtor_resources_folderpath) / Path(skeleton_model[1:]) )
                        destination = str( Path(character_skeleton_folderpath) / Path(skeleton_model).name )
                        files_to_copy.append(["Skeleton", "model", origin, destination, ""])


            # Process list of files to copy to character folder
            
            if files_to_copy:
                for element in files_to_copy:
                    body_part = element[0]
                    asset_type = element[1]
                    origin = element[2]
                    destination = element[3]
                    report = element[4]

                    print(body_part, "-", asset_type, "\n",origin, "\n",destination)
                    
                    if Path(destination).parent.exists() == False:
                        try:
                            Path(destination).parent.mkdir(parents=False, exist_ok=True)
                            print("Creating " + str(Path(destination).parent) + "folder.\n")
                        except Exception as e:
                            print("--------ERROR: The folder ",destination," didn't exist.\nWhen trying to create it an error occurred:\n",e,"\n")
                    
                    try:
                        shutil.copy2(origin, destination)
                    except Exception as e:
                        print("--------ERROR!!!\n", str(e))
                        print()
                    
                    print()
                        
        print("DONE!")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}



def register():
    bpy.utils.register_class(ZGSWTOR_OT_locate_character_assets)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_locate_character_assets)

if __name__ == "__main__":
    register()