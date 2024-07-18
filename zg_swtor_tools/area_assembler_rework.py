import bpy
import bmesh
import json
from math import degrees, radians
from mathutils import Matrix
from pathlib import Path
from zipfile import ZipFile
import copy
import os
import time
import datetime


# ImportHelper is a helper class, defines filename and an
# implicit invoke() function which calls the file selector.
# We might use invoke() for that, though, if we have to
# make some kind of initialization stuff there.
from bpy_extras.io_utils import ImportHelper

from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       CollectionProperty
                       )
from bpy.types import Operator


# These imports are for a "hide console output" fn
import contextlib
import io
import sys


from .utils.addon_checks import requirements_checks


ADDON_ROOT = __file__.rsplit(__name__.rsplit(".")[0])[0] + __name__.rsplit(".")[0]


# SWTOR Objects, Meshes, Materials, and Shaders types
# that denote SWTOR Engine Objects.

# All these are single mesh ones
ENGINE_OBJECTS = {
    "spawner_crefac_quest",
    "spawner_encounter",
    "spawner_encounter_d_1",
    "spawner_encounter_z_2",
    "spawner_group",
    "spawner_letter_a",
    "spawner_movepoint_1",
    "spawner_number_max_1",
    "spawner_number_max_2",
    "spawner_number_max_3",
    "spawner_number_max_4",
    "spawner_placeable",
    "spawner_rallypoint",
    "spawner_seed_point",
    "util_cube_hidden",
    "utility_box_white01",
    "00_test_area01",
    "cover_left",
    "cover_right",
    "cover_top",
    "coverpoint_auto_left",
    "coverpoint_auto_right",
    "coverpoint_crouching_auto",
    "coverpoint_crouching_exclusion",
    "coverpoint_crouching_manual",
    "coverpoint_crouching_questionable",
    "coverpoint_exclusion_left",
    "coverpoint_exclusion_right",
    "coverpoint_manual_left",
    "coverpoint_manual_right",
    "coverpoint_questionable_left",
    "coverpoint_questionable_right",
    "engine_map_mapnode",
    "engine_map_mapnode_exit",
    "engine_staging_camera",
    "engine_staging_human_01",
    "engine_staging_human_02",
    "engine_staging_human_03",
    "engine_staging_human_04",
    "engine_staging_human_05",
    "engine_staging_pointlight",
    "spawner_creature",
    "spawner_creature_quest",
}



# Many Hero Engine utility object types can't be determined by
# their names, but oftentimes their materials'names are a good
# criteria (these are all the invisible-type ones in .mat files).
ENGINE_MATERIALS = {
    "collision",
    "dbo_universal_superexclusion_test",
    "mote_mote_a01_v01",
    "occluder",
    "occluder_terrain",
    "occluder_wall",
    "portal",
    "util_blue_hidden",
    "util_collision_hidden",
    "util_collision_none",
    "util_green_hidden",
    "util_red_hidden",
    "util_white_hidden",
    "util_yellow_hidden",
    "white_utility_hidden",
}

# More filters to apply, by <derived> type:
ENGINE_SHADERS = {
    "OpacityFade",
}







# region

# -------------------------------------------------------------------------------
# START WINDOW IMPORT -----------------------------------------------------------
# -------------------------------------------------------------------------------







class ZGSWTOR_OT_area_assembler(Operator):
    bl_idname = "zgswtor.area_assembler"
    bl_label = "Import Area .json files"
    bl_description = "Import SWTOR Area data files (json) from Jedipedia.net's File Viewer.\n\nRequires:\n• Setting the path to an assets 'resources' folder in SWTOR Area Assembler's Addon Preferences.\n• An active Modern .gr2 importer Addon"
    bl_options = {'REGISTER', 'UNDO'}


    # Checks that the 'resources' folder set in Preferences is valid
    # and that the .gr2 importer addon's operator is available.
    # Greys-out the Import sub-menu otherwise.
    @classmethod
    def poll(cls,context):       
        swtor_resources_folderpath = context.preferences.addons["zg_swtor_tools"].preferences.swtor_resources_folderpath
        
        if Path(swtor_resources_folderpath).exists() and ("gr2" in dir(bpy.ops.import_mesh)):
            return True
        else:
            return False


    # List of operator properties. Their attributes are assigned
    # to the class instance from the operator settings before calling.
    ApplyFinalRotation: BoolProperty(
        name="Apply Final Rotation",
        description="Disable to skip final rotation. All objects will need to be rotated X Axis 90 Degrees",
        default=True,
    )
    ApplyMaterials: BoolProperty(
        name="Apply Materials",
        description="Apply materials to the objects based on matching .mat files info in Resources",
        default=True,
    )
    ApplySceneScale: BoolProperty(
        name="Apply Scene Scale",
        description="Scale the entire scene by a factor (x10, typically)",
        default=False,
    )
    SceneScaleFactor: FloatProperty(
        name="Scene Scale Factor",
        description="Scale Factor If Applying Scene Scale",
        default=1.0,
    )
    SkipDBOObjects: BoolProperty(
        name="Skip dbo Objects",
        description="Don't import design blockout (DBO) objects such as blockers, portals, etc",
        default=True,
    )
    CreateSceneLights: BoolProperty(
        name="Create Scene Lights",
        description="Automatically create basic scene lighting based on in game lighting nodes.\nIf they exceed the amount of 100, they will be created\nas Excluded From The View Layer for performance reasons",
        default=False,
    )
    CollectionObjects: BoolProperty(
        name="Separate Object Types in Collections",
        description="Separates objects, terrains and lights in per-Area children Collections",
        default=False,
    )
    MergeMultiMeshObjects: BoolProperty(
        name="Merge Multi-Mesh Objects",
        description="Joins single .gr2 file-originated multi-mesh objects\ninto single objects",
        default=False,
    )
    ShowFullReport: BoolProperty(
        name="Show Full Report In Terminal",
        description="If checked, a full length report will be produced, including not just errors but importing successes, too.\n\nFull length reports may exceed the Console's default capacity and become truncated.\nTo avoid that, increase that setting accordingly, around 500 lines per expected .json file,\nin your Operating System's Terminal app or in your IDE (Integrated Development Environment)",
        default=False,
    )
    HideAfterImport: BoolProperty(
        name="Hide Objects After Importing",
        description="Imported Area objects are hidden ('eye' icon in Outliner, 'h' shortcut) to keep Blender\nmore responsive when having massive amounts of objects per individual Collections.\n\nLag could persist if the Outliner is overloaded, but it should be far more tolerable.\n\nRecommended when importing .json files weighting several MegaBytes each",
        default=False,
    )
    ExcludeAfterImport: BoolProperty(
        name="Exclude Collections After Importing",
        description="Resulting Collections are excluded (checkbox in Outliner, 'e' shortcut')\nto keep Blender fully responsive and be able to manage them without lag.\n\nExcluded Collections won't list their objects in the Outliner: that's normal.\n\nRecommended when importing a massive number of areas, such as whole worlds.\n\n(Excluding Collections resets the hide/show state of the Collections' contents.\nHide Objects After Importing won't have an effect if this option is on)",
        default=False,
    )

    
    # Register some custom properties in the object class for
    # storing helpful info for diagnosing and stuff
    bpy.types.Object.swtor_type = bpy.props.StringProperty()
    bpy.types.Object.swtor_id = bpy.props.StringProperty()
    bpy.types.Object.swtor_parent_id = bpy.props.StringProperty()
    bpy.types.Object.swtor_json = bpy.props.StringProperty()
    
    
    # Define some methods to accept changing some properties
    # and some related scene properties.
    
    # @classmethod
    # def modify_ApplySceneScale(self, context, apply_scene_scale = False):
    #     context.scene.ZGSAA_ApplySceneScale = apply_scene_scale
    
    # @classmethod
    # def modify_SceneScaleFactor(self, context, scene_scale_factor = 1.0):
    #     context.scene.ZGSAA_SceneScaleFactor = scene_scale_factor
    


    def invoke(self, context, event):
        # File Browser for selecting paths.json file.
        # Apply the UI panel's settings to the class' properties
        # before opening the File Browser, so that they match.
        self.ApplyFinalRotation = context.scene.ZGSAA_ApplyFinalRotation
        self.ApplyMaterials = context.scene.ZGSAA_ApplyMaterials
        
        checks = requirements_checks()
        # Check if we are dealing with the latest version of the
        # .gr2 importer add-on and its scaling settings to use them
        # in ApplySceneScale.
        # Axis conversion isn't considered given how this tool works
        # (it's alwasys as if it was applied).
        if checks['gr2HasParams'] and not context.scene.ZGSAA_ApplySceneScale:
            prefs = context.preferences.addons["io_scene_gr2"].preferences
            self.ApplySceneScale = getattr(prefs, 'gr2_scale_object')
            self.SceneScaleFactor = getattr(prefs, 'gr2_scale_factor')
        else:
            self.ApplySceneScale = context.scene.ZGSAA_ApplySceneScale
            self.SceneScaleFactor = context.scene.ZGSAA_SceneScaleFactor

        self.SkipDBOObjects = context.scene.ZGSAA_SkipDBOObjects
        self.CreateSceneLights = context.scene.ZGSAA_CreateSceneLights
        self.CollectionObjects = context.scene.ZGSAA_CollectionObjects
        self.MergeMultiMeshObjects = context.scene.ZGSAA_MergeMultiMeshObjects
        self.HideAfterImport = context.scene.ZGSAA_HideAfterImport
        self.ExcludeAfterImport = context.scene.ZGSAA_ExcludeAfterImport
        self.ShowFullReport = context.scene.ZGSAA_ShowFullReport


        # Open File Browser.
        context.window_manager.fileselect_add(self)
        
        return {'RUNNING_MODAL'}

    # ImportHelper and invoke() mixin class' properties
    # (pay attention to their types):

    # Filetype filter
    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    
    # Selected files
    files: CollectionProperty(type=bpy.types.PropertyGroup)
    
    # Filepath property
    # Always a single one even when selecting multiple files.
    # If none selected, it gets the directory, with a trailing final separator
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    # Filename property
    filename: bpy.props.StringProperty()

    # Directory property
    directory: bpy.props.StringProperty()

# endregion

# region


    def execute(self, context):
                
        if self.filepath == self.directory:
            # When nothing is selected, self.filepath gets the directory too, so…
            self.report({'ERROR'}, "No files selected")
            return {'CANCELLED'}


        # Blender version check for 3.x/4.x API differences
        # (.obj import so far, which affects terrains import)
        checks = requirements_checks()
        
        blender_version = checks['blender_version']
        
        # Check if we are dealing with the latest version of the
        # .gr2 importer add-on and its scaling settings to use them
        # in ApplySceneScale.
        # Axis conversion isn't considered given how this tool works
        # (it's alwasys as if it was applied).
        # This also affects how the add-on detects new imported objects.
        
        if checks['gr2HasParams']:
            gr2HasParams = True
        else:
            gr2HasParams = False


        # Terminal's VT100 escape codes (most terminals understand them).
        # See: http://www.climagic.org/mirrors/VT100_Escape_Codes.html
        # (replacing ^[ in terminal codes with \033)
        CLEAR_TERMINAL = '\033[2J'      # Clear entire screen.
        CURSOR_HOME = '\033[H'          # Move cursor to upper left corner.
        CLEAR_EOL = '\r\033[K'          # Erase to end of current line.
        LINE_BACK_1ST_COL = '\033[F'    # Move cursor one line up, 1st column.

        # If Full Reports in Terminal are selected,
        # don't use the terminal code for backtracking a line
        if self.ShowFullReport is True:
            LINEBACK = ""
        else:
            LINEBACK = LINE_BACK_1ST_COL + CLEAR_EOL

        # For timing stats
        start_time = time.time()



        print(CLEAR_TERMINAL + CURSOR_HOME)
        print("####################")
        print("SWTOR AREA ASSEMBLER")
        print("####################")
        print()        
        bpy.context.window.cursor_set("WAIT")

        # Open all the folders and files necessary for the addon's workings
        spn_table_available = False
        dyn_nodes__available = False


        # get the folder
        # We derive it from the filepath because when called as an
        # operator we don't get a directory from ImportHelper.
        # (os.path.dirname omits the separator after the directory)
        folder = (os.path.dirname(self.filepath))

        # Get the extracted SWTOR assets' "resources" folder from the add-on's preferences. 
        swtor_resources_folderpath = context.preferences.addons["zg_swtor_tools"].preferences.swtor_resources_folderpath

        # Check that there is a terrain maps subfolder in the resources folder
        terrain_folderpath = Path(swtor_resources_folderpath) / "world" / "heightmaps"
        if not terrain_folderpath.exists():
            terrain_folderpath = None


        # Open the auxiliary files (zipped nodes and relationship tables)
        
        # Open zipped dyn nodes folder
        try:
            dyn_zip = ZipFile(str(Path(ADDON_ROOT) / "rsrc" / "dyn.zip"), "r")
            dyn_nodes__available = True
        except FileNotFoundError:
            print(" -- No dyn.zip file found inside the addon. Some objects will be omitted")  # Console.


        # Open spn to pcl or dyn correspondence table
        try:
            with open(str(Path(ADDON_ROOT) / "rsrc" / "spn_table.txt"), "r") as spn_to_gr2_or_dyn:
                print()
                print("BUILDING TABLE OF INDIRECT OBJECT REFERENCES:")
                print("---------------------------------------------")
                print()
                                    
                spn_table_available = True
                spn_table = {}
                for dyn_obj in spn_to_gr2_or_dyn:
                    key, value = dyn_obj.split(",")
                    spn_table[key] = value.replace("\n", "")

                print(LINEBACK + "DONE!")
        except FileNotFoundError:
            print(" -- No spn_table file found inside the addon. Some objects will be omitted")  # Console.

        
        plc_nodes_folder = str(Path(ADDON_ROOT) / Path("rsrc") / Path("plc.zip"))
        dyn_nodes_folder = str(Path(ADDON_ROOT) / Path("rsrc") / Path("dyn.zip"))


# endregion

        # -------------------------------------------------------------------------------
        # PER-JSON FILE PREPROCESSING ---------------------------------------------------
        # -------------------------------------------------------------------------------

# region

        # Iterate through the selected files and build a full location data list
        # plus a list of location names out of the .json filenames
        # and appropriate Collections

        swtor_location_data = []
        json_filenames = []
        dyn_file_data = []
        DBOObjects = []

        # For console output formatting stuff
        max_json_filename_length = 0
        max_swtor_name_length = 0


# endregion
# region


        print("\n\nMERGING DATA FROM .JSON FILES:\n------------------------------\n")

        # When being called as an operator, take care of filepaths
        # being fed through ImportHelper's self.filepath or self.files
        if not self.files:
            # Make sure a single object works as a list for the loop.
            filepaths = [Path(self.filepath)]
        else:
            filepaths = self.files


        for filepath in filepaths:

            # generate full path to file
            json_filepath = (os.path.join(folder, filepath.name))
            print(LINEBACK + filepath.name, end="")

            # Load .json file as a list of dictionary elements.
            try:
                with open(json_filepath, "r") as read_file:
                    try:
                        json_location_data = json.load(read_file)
                        print()  # adds line feed to previous print()
                    except:
                        print(" -- EMPTY OR BADLY WRITTEN .JSON FILE. OMITTED.")
                        continue
            except FileNotFoundError:
                print(" -- .json file not found")  # Console.
                self.report( {"WARNING"}, (".json file '" + json_filepath + "' wasn't found.") )
                return {"CANCELLED"}
            
            # Add the name of the .json file to this list.
            json_filename = Path(json_filepath).stem
            json_filenames.append(json_filename)

            # For console output formatting stuff
            if len(json_filename) > max_json_filename_length:
                max_json_filename_length = len(json_filename)


            # Flag to decide to create a terrain Collection for this .json area
            # if the user has selected to have sub-Collections.
            has_terrain = False

# endregion


            # -------------------------------------------------------------------------------
            # PER-ELEMENT FILE PREPROCESSING ------------------------------------------------
            # -------------------------------------------------------------------------------
            # Loop through the .json file's elements,
            # filter out some obvious discardables,
            # and pre-process indirect object references
            
# region
            
            indirect_object_elements = []
            
            for element in json_location_data:
                if "assetName" in element:
                    element["make_dyn_empty"] = False
                    swtor_filepath = element["assetName"]
                    # delete preceding directory separator if it exists. It shouldn't vary so much
                    # but SWTOR is a mess, separator types-wise.
                    if swtor_filepath.startswith("/") or swtor_filepath.startswith("\\"):
                        swtor_filepath = swtor_filepath[1:]
                    element["assetName"] = swtor_filepath
                    
                    # Add json_filename to element
                    element["json_filename"] = json_filename


                    # Filter in object types we know how to handle.
                    # DON'T FILTER OUT DBOs OR OTHER OBJECTS THAT
                    # MIGHT HAVE TO BECOME PARENTS. 
                    if any( (
                            ".gr2" in swtor_filepath and not "_fadeportal_" in swtor_filepath,
                            ".hms" in swtor_filepath,
                            ".lit" in swtor_filepath,
                            ".mag" in swtor_filepath,
                            ".spn_p" in swtor_filepath,
                            ) ):
                    
                        
                        # Calculate max name length For console output formatting
                        swtor_name_length = len(Path(element["assetName"]).stem) + 2
                        if swtor_name_length > max_swtor_name_length:
                            max_swtor_name_length = swtor_name_length

                        if ".hms" in swtor_filepath:
                            has_terrain = True



                        # Pre-process item for indirect object types
                        # (.mag, .spn to plc, .spn to .plc to .dyn, etc.)
                        # Use the most indirect first so that their results
                        # are processed by the least indirect afterwards
                        # as a temporary solution for their lack of
                        # recursivity.
                        
                        swtor_id = element["id"]
                        swtor_parent_id = element["parent"]
                                                    
                        if swtor_filepath.endswith(".spn_p"):
                            # .SPN_P OBJECT REFERENCE (non-NPC .SPN)
                            
                            if swtor_filepath in spn_table:
                                if spn_table[swtor_filepath][-3:] == "dyn":
                                    
                                    # pre-process dyn objects
                                    # WARNING: ZIP files internally use forward slashes as separators.
                                    # We have to cater to that when defining paths inside them.
                                    try:
                                        zipped_filepath = spn_table[swtor_filepath].replace(".dyn", ".json").replace("\\", "/")
                                        with dyn_zip.open(zipped_filepath, "r" ) as read_dyn_file:
                                            dyn_file_data = json.load(read_dyn_file)
                                    except FileNotFoundError:
                                        print(".json file not found")  # Console.
                                        continue

                                    dyn_element = copy.deepcopy(element)

                                    for idx, dyn_obj in enumerate(dyn_file_data["dynPlaceable"]["dynVisualList"]["value"]["list"]):
                                        if "dynVisualFqn" in dyn_obj:
                                            dyn_element["assetName"] = dyn_obj["dynVisualFqn"]["value"]
                                            if ".gr2" in dyn_element["assetName"] or ".mag" in dyn_element["assetName"]:
                                                dyn_element["parent"] = swtor_id
                                                dyn_element["id"] = f"{swtor_id}-{str(idx)}"
                                                
                                                if "dynPosition" in dyn_obj:
                                                    dyn_element["position"][0] = dyn_obj["dynPosition"]["value"]["x"]
                                                    dyn_element["position"][1] = dyn_obj["dynPosition"]["value"]["y"]
                                                    dyn_element["position"][2] = dyn_obj["dynPosition"]["value"]["z"]
                                                else:
                                                    dyn_element["position"] = [0,0,0]
                                
                                                if "dynRotation" in dyn_obj:
                                                    dyn_element["rotation"][0] = dyn_obj["dynRotation"]["value"]["x"]
                                                    dyn_element["rotation"][1] = dyn_obj["dynRotation"]["value"]["y"]
                                                    dyn_element["rotation"][2] = dyn_obj["dynRotation"]["value"]["z"]
                                                else:
                                                    dyn_element["rotation"] = [0,0,0]

                                                if "dynScale" in dyn_obj:
                                                    dyn_element["scale"][0] = dyn_obj["dynScale"]["value"]["x"]
                                                    dyn_element["scale"][1] = dyn_obj["dynScale"]["value"]["y"]
                                                    dyn_element["scale"][2] = dyn_obj["dynScale"]["value"]["z"]
                                                else:
                                                    dyn_element["scale"] = [1,1,1]

                                                dyn_element["make_dyn_empty"] = False
                                                
                                                indirect_object_elements.append(dyn_element)
                                            else:
                                                continue
                                        
                                    element["make_dyn_empty"] = True

                            
                                elif ".gr2" in spn_table[swtor_filepath] or ".mag" in spn_table[swtor_filepath]:
                                    element["make_dyn_empty"] = False
                                    swtor_filepath = spn_table[swtor_filepath]
                                    
                                if swtor_filepath.startswith("/") or swtor_filepath.startswith("\\"):
                                    swtor_filepath = swtor_filepath[1:]
                                element["assetName"] = swtor_filepath
                                swtor_name = Path(swtor_filepath).stem
                                
                            else:
                                continue
                            
            json_location_data += indirect_object_elements
            
            swtor_location_data += (json_location_data)



            # Create Collections.

            # Main location collection inside the Scene's root "Scene Collection".
            if not json_filename in bpy.data.collections:
                location_collection = bpy.data.collections.new(json_filename)
                bpy.context.collection.children.link(location_collection)
            else:
                location_collection = bpy.data.collections[json_filename]

            if self.CollectionObjects == True:
                # Location's lights if the user wants them (yes by default)
                if self.CreateSceneLights == True:
                    if not (json_filename + " - Lights") in bpy.data.collections:
                        location_lights_collection  = bpy.data.collections.new(json_filename + " - Lights")
                        location_collection.children.link(location_lights_collection)
                    else:
                        location_lights_collection  = bpy.data.collections[json_filename + " - Lights"]

                # Location's terrain.
                if has_terrain == True:
                    if not (json_filename + " - Terrain") in bpy.data.collections:
                        location_terrains_collection = bpy.data.collections.new(json_filename + " - Terrain")
                        location_collection.children.link(location_terrains_collection)
                    else:
                        location_terrains_collection = bpy.data.collections[json_filename + " - Terrain"]

                # Location's objects.
                if not (json_filename + " - Objects") in bpy.data.collections:
                    location_objects_collection = bpy.data.collections.new(json_filename + " - Objects")
                    location_collection.children.link(location_objects_collection)
                else:
                    location_objects_collection = bpy.data.collections[json_filename + " - Objects"]



            # Create a Light data block to base Light objects on. Having one per .json file instead of
            # a single one for all the Addon's run is a bit arbitrary, but it might be interesting for,
            # say, setting a common light intensity and color per room and the like.

            if self.CreateSceneLights == True:
                light_data = bpy.data.lights.new(name= json_filename, type= "POINT")
                light_data.energy = 2

                Lights_count = 0

        print(LINEBACK + "DONE!")



        # Weird case of all empty or invalid .json, but hey, could happen.
        if len(swtor_location_data) == 0:
            self.report({"WARNING"}, "The selected .json files contain no data.")
            return {"CANCELLED"}

# endregion




        # -------------------------------------------------------------------------------
        # ACTUAL PROCESSING OF THE ELEMENTS IN THE AREA DATA ----------------------------
        # -------------------------------------------------------------------------------
        
# region

        # Deduplication dict to keep track of already imported objects
        # and avoid reimporting thorugh timewasting .gr2 importer.
        # Key: value is:
        # object's filepath: imported object's mesh data
        # or
        # multi-object's filepath: [parent object's name]
        already_existing_objects = {}

        # List to hold the terrain objects being imported
        terrains = []


        # Percentage of progress stuff. It's based on number
        # of elements, although most will be discarded (non-objects). 
        amount_to_process = len(swtor_location_data)
        amount_processed = 0


        # LOOP THROUGH ELEMENTS STARTS HERE ----------------------------------------


        print("\n\nPROCESSING AREA OBJECTS' DATA:\n------------------------------\n")

        for element in swtor_location_data:
            amount_processed += 1

            # For .json file elements with transforms but no assetName at all.
            # Last time it happened it was a bug in Jedipedia. Just in case…
            if not "assetName" in element:
                print("WARNING: item with id "+ element["id"] + " lacks assetName")
                continue

            # Set some variables that will be used per element constantly.
            swtor_filepath = element["assetName"]
            
            # Skip any of the entry types we don't know how to handle.
            # DON'T FILTER OUT ANY DBOs OR OTHER OBJECTS THAT
            # MIGHT HAVE TO BECOME PARENTS. 
            if not any((swtor_filepath.endswith(".gr2"),
                        swtor_filepath.endswith(".lit"),
                        swtor_filepath.endswith(".hms"),
                        swtor_filepath.endswith(".mag"),
                        swtor_filepath.endswith(".spn_p"),
                        )):
                continue
            
            # delete preceding directory separator if it exists. It shouldn't vary
            # so often, but SWTOR is a mess, separator types-wise.
            if swtor_filepath.startswith("/") or swtor_filepath.startswith("\\"):
                swtor_filepath = swtor_filepath[1:]

            # More variables.
            swtor_id = element["id"]
            swtor_parent_id = element["parent"]
            swtor_name = Path(swtor_filepath).stem

            json_filename = element["json_filename"]


            # Unlikely to happen, but…
            if swtor_id in bpy.data.objects:
                continue

            


            if swtor_filepath.endswith(".lit"):

                # LIGHT OBJECT. ----------------------------------

                if self.CreateSceneLights == True:
                    # Collection where the light object will be moved to
                    if self.CollectionObjects == True:
                        location_lights_collection  = bpy.data.collections[json_filename + " - Lights"]
                    else:
                        location_lights_collection  = bpy.data.collections[json_filename]

                    light_data = bpy.data.lights[json_filename]
                    blender_object = bpy.data.objects.new(name=swtor_id, object_data = light_data)

                    link_objects_to_collection(blender_object, location_lights_collection, move = True)

                    Lights_count += 1
                else:
                    continue


            elif swtor_filepath.endswith(".hms"):

                # TERRAIN OBJECT. ---------------------------------

                print(f'{LINEBACK}{amount_processed * 100 / amount_to_process:6.2f} %   AREA: {json_filename:<{max_json_filename_length}}   ID: {swtor_id}   -- TERRAIN OBJECT --   ', end="")

                if terrain_folderpath is None:
                    print("WARNING: NO RESOURCES\\WORLD\\HEIGHTMAPS FOLDER AVAILABLE")
                    continue

                # Collection where the terrain object will be moved to
                if self.CollectionObjects == True:
                    location_terrains_collection  = bpy.data.collections[json_filename + " - Terrain"]
                else:
                    location_terrains_collection  = bpy.data.collections[json_filename]

                terrain_path = str(terrain_folderpath / Path(swtor_id + ".obj") )

                # ACTUAL IMPORTING:
                # …through Blender's bpy.ops.import_scene.obj addon.
                # Does a after-minus-before bpy.data.objects check to determine
                # the objects resulting from the importing, as the addon doesn't
                # return that information.

                objects_before_importing = list(bpy.data.objects)
                try:
                    with suppress_stdout():  # To silence .obj importing outputs
                        if blender_version < 4.0:
                            # BLENDER 3.X-SPECIFIC .OBJ IMPORT:
                            result = bpy.ops.import_scene.obj(
                                filepath=terrain_path,
                                use_image_search=False)
                        else:
                            # BLENDER 4.X-SPECIFIC .OBJ IMPORT:
                            result = bpy.ops.wm.obj_import(filepath=terrain_path)

                    if result == "CANCELLED":
                        print(f"\n           WARNING: Blender's .obj importer failed to import {swtor_id} - {str( Path(swtor_resources_folderpath) / Path(swtor_filepath) )}\n")
                        continue
                    else:
                        print("IMPORTED")
                        objects_after_importing = list(bpy.data.objects)
                        imported_objects_amount = 1
                        blender_object = list(set(objects_after_importing) - set(objects_before_importing))[0]
                        blender_object.name = swtor_id
                        link_objects_to_collection(blender_object, location_terrains_collection, move = True)
                except:
                    print(f"\n\n           WARNING: Blender's .obj Importer CRASHED while trying to import it.")
                    print("           Despite that, the Area Importer addon will keep on importing the rest of the objects.\n")
                    continue

                
            elif element["make_dyn_empty"] == True:
                
                # DYN PARENT. ---------------------------------
                
                # As some indirect objects result into multiple .gr2, .mag, etc.
                # an Empty is necessary to parent them and pass them transforms.
                # .dyn are the only case so far, but there could be more.

                blender_object = bpy.data.objects.new(swtor_id, None)
                blender_object.empty_display_size = 0.1
                blender_object.empty_display_type = 'CUBE'
                
                # Collection where the Empty will be moved to
                if self.CollectionObjects == True:
                    location_objects_collection = bpy.data.collections[json_filename + " - Objects"]
                else:
                    location_objects_collection = bpy.data.collections[json_filename]

                link_objects_to_collection(blender_object, location_objects_collection, move = True)

            else:

                # MESH OBJECT  ----------------------------------

                print(f'{LINEBACK}{amount_processed * 100 / amount_to_process:6.2f} %   AREA: {json_filename:<{max_json_filename_length}}   ID: {swtor_id}   NAME: {swtor_name:{max_swtor_name_length}}', end="")


                if swtor_filepath.endswith(".mag"):
                    # .MAG OBJECT REFERENCE
                    # .mag files describe placeable, armature-animated objects (mag = Morpheme Animated Granny).
                    # They are stored in resources/art/dynamic/spec. This block reads those and gets the
                    # .gr2 objects they refer to, so that they are processed as such.
                    try:
                        with open( str( Path(swtor_resources_folderpath) / Path(swtor_filepath) ), "r") as read_mag_file:
                            if ".gr2" in read_mag_file:
                                for dyn_obj in read_mag_file:
                                    if ".gr2" in dyn_obj:
                                        swtor_filepath = dyn_obj.split("Mesh=")[1]
                                        if swtor_filepath.startswith("/") or swtor_filepath.startswith("\\"):
                                            swtor_filepath = swtor_filepath[1:]
                                        element["assetName"] = swtor_filepath
                                        break
                            else:
                                print("  WARNING: NO .GR2 OBJECT REFERENCED IN FILE")
                                continue
                    except FileNotFoundError:
                        print(" -- file not found")  # Console.
                        continue


                # Collection where the objects will be moved to
                if self.CollectionObjects == True:
                    location_objects_collection = bpy.data.collections[json_filename + " - Objects"]
                else:
                    location_objects_collection = bpy.data.collections[json_filename]


                if swtor_filepath not in already_existing_objects:

                    # IMPORTING NEW OBJECTS:
                    # …through Darth Atroxa's bpy.ops.import_mesh.gr2.
                    if not gr2HasParams:
                        # IF WORKING WITH OLDER VERSIONS OF THE .GR2 ADD-ON:
                        # makes a copy of bpy.data. objects to be able to do
                        # an after-minus-before check to determine the objects
                        # resulting from the importing.
                        objects_before_importing = list(bpy.data.objects)
                        
                    gr2_filepath = str( Path(swtor_resources_folderpath) / Path(swtor_filepath) )
                    if os.path.isfile(gr2_filepath):
                        try:
                            with suppress_stdout():  # To silence Darth Atroxa's print() outputs
                                result = bpy.ops.import_mesh.gr2(filepath=gr2_filepath, enforce_neutral_settings=True)
                            if result == "CANCELLED":
                                print(f"\n\nWARNING: .gr2 importer addon failed to import {swtor_id} - {str( Path(swtor_resources_folderpath) / Path(swtor_filepath) )}\n")
                                continue
                            else:
                                print("IMPORTED    ", end="")
                        except:
                            print(f"\n\nWARNING: the .gr2 Importer addon CRASHED while importing:\n{swtor_id} - {str( Path(swtor_resources_folderpath) / Path(swtor_filepath) )}\n")
                            print("Despite that, the Area Importer addon will keep on importing the rest of the objects")
                            continue
                        
                        if not gr2HasParams:
                            # IF WORKING WITH OLDER VERSIONS OF THE .GR2 ADD-ON:
                            # does the after-minus-before diff.
                            objects_after_importing = list(bpy.data.objects)
                            imported_objects = list(set(objects_after_importing) - set(objects_before_importing))
                        else:
                            # IF WORKING WITH NEWER VERSIONS OF THE .GR2 ADD-ON:
                            # reads the new objects report that the .gr2 importer placed in a scene property.
                            objs_names = json.loads(bpy.context.scene.io_scene_gr2_last_job)['objs_names']
                            imported_objects = [bpy.data.objects[obj_name] for obj_name in objs_names]
                            
                        # Delete polys in use by materials_to_exclude_objects_by
                        for i, obj_to_clean in enumerate(imported_objects[:]):
                            # if len(obj_to_clean.material_slots) > 1:  # a bit of CYA against unintended consequences.
                            separate_by_specific_materials(obj_to_clean, ENGINE_MATERIALS, separate = False)
                            if obj_to_clean.material_slots == 0: # in case the obj is purely made of mats. to exclude
                                imported_objects.pop(i)
                        
                        imported_objects_amount = len(imported_objects)

                        link_objects_to_collection(imported_objects, location_objects_collection, move = True)
                    else:
                        print("FILE NOT FOUND. DISCARDED")
                        continue

                else:
                    
                    # DUPLICATING ALREADY IMPORTED OBJECTS AS INSTANCES:
                    # …To make the importing faster. If object's path is in the already_existing_objects dict,
                    # don't import through the .gr2 Addon and just duplicate from mesh data.

                    # If the mesh data is None that means that the original object was made of discardables
                    # (colliders, etc.) that the user decided to exclude, so, we don't duplicate it. 
                    if already_existing_objects[swtor_filepath] == "":
                        print("DISCARDED")
                        continue


                    print("DUPLICATED  ", end="")

                    imported_objects = [ bpy.data.objects.new(name= swtor_id, object_data= already_existing_objects[swtor_filepath][0]) ]
                    imported_objects_amount = 1

                    link_objects_to_collection(imported_objects, location_objects_collection, move = True)

                    # If the already existing object was a multi-object (the dict's value lists more than a single mesh data block)
                    # create children objects out of them using the meshes' names as their names, and parent them to the first object
                    # created just before. In this way, the parent can be processed as a single object by the rest of the code and
                    # the children objects go along for the ride.
                    if len(already_existing_objects[swtor_filepath]) > 1:
                        for i in range( 1, len(already_existing_objects[swtor_filepath]) ):
                            multi_object_child = bpy.data.objects.new(
                                name= already_existing_objects[swtor_filepath][i].name,
                                object_data= already_existing_objects[swtor_filepath][i]
                                )

                            link_objects_to_collection(multi_object_child, location_objects_collection, move = True)

                            parent_with_transformations(multi_object_child, imported_objects[0], inherit_transformations = False)

                        print("MULTI-OBJECT", end="")



                # Single object vs. multi-object processing ---------------------------------------------

                if imported_objects_amount == 0:  # collider objects, depending on .gr2 importer settings
                    print()  # adds line feed to previous print()
                    continue


                if imported_objects_amount == 1:

                    # SINGLE OBJECT (OR ALREADY EXISTING MULTI-OBJECT) -------

                    blender_object = imported_objects[0]
                    # Add imported object's path and mesh data to dedupe dict.
                    already_existing_objects[swtor_filepath] = [blender_object.data]

                    # If object is a dbo, replace it with an Empty to
                    # cover for it being a parent object
                    if swtor_name.startswith("dbo"):
                        DBOObjects.append(blender_object)
                        print("DBO ", end="")

                    blender_object.name = swtor_id
                    print()  # adds line feed to previous print()
                else:

                    # IMPORTED MULTI-OBJECT ----------------------------------

                    print("MULTI-OBJECT ", end="")

                    # imported_objects_meshnames_and_names will store:
                    # Key = object's mesh's name.
                    # Value = object's name.
                    # to help determine which object will act as parent by
                    # finding the one whose mesh data name (which spares us
                    # the usual .00x suffixes) is closest to the filename.
                    imported_objects_meshnames_and_names = {}


                    # List to fill with objects to discard
                    # if set so in the relevant checkbox
                    discardables = []

                    for imported_object in imported_objects:

                        # Check object's name and materials to detect discardable ones.
                        is_discardable = False
                        
                        # if self.SkipDBOObjects == True:
                        #     # Test by file's name
                        #     if imported_object.name.startswith("dbo"):
                        #         is_discardable = True
                        #     else:
                        #         # Test by material slot's names
                        #         if imported_object.material_slots:
                        #             for material_slot in imported_object.material_slots:
                        #                 if material_slot.name in materials_to_exclude_objects_by:
                        #                     is_discardable = True
                        #                     break

                        # Add object to list of discardables if checkbox is true,
                        # otherwise rename them with their meshes' names (which could produce .00x suffixes)
                        if is_discardable == True:
                            discardables.append(imported_object)
                            continue
                        else:
                            imported_objects_meshnames_and_names[imported_object.data.name] = imported_object.name

                    # Delete discardables from imported_objects and from bpy.data.objects
                    if discardables:
                        for discardable in discardables:
                            bpy.data.objects.remove(discardable, do_unlink=True)
                            imported_objects.remove(discardable)

                            print("DBO to EMPTY ", end="")
                    


                    # It can happen that a multi-object is entirely composed of non-renderable
                    # objects, so, objects_to_group might be actually empty after discarding them.
                    # In such case, replace the multi-object with an Empty.
                    if len(imported_objects) == 0:
                        blender_object = bpy.data.objects.new(swtor_id, None)
                        blender_object.empty_display_size = 0.1
                        blender_object.empty_display_type = 'CUBE'
                        blender_object.name = swtor_id

                        already_existing_objects[swtor_filepath] = ""
                        print("DISCARDED")
                        continue

                    # There could be a single object left.
                    if len(imported_objects) == 1:
                        blender_object = imported_objects[0]
                        blender_object.name = swtor_id
                        already_existing_objects[swtor_filepath] = [blender_object.data]
                        print()  # adds line feed to previous print()




                    # If there are more than one, and we've chosen not to
                    # merge them into a single object, we need to select
                    # a main one to parent the rest to. We go for the one
                    # whose name is closest to the .gr2 filename.
                    if len(imported_objects) > 1:
                        if self.MergeMultiMeshObjects == False:
                            multi_object_data_list = []

                            parent_name = imported_objects_meshnames_and_names[ find_closest_match(list(imported_objects_meshnames_and_names), swtor_name) ]
                            
                            blender_object = bpy.data.objects[parent_name]
                            multi_object_data_list.append(blender_object.data)

                            for imported_object in imported_objects:
                                if imported_object.name != parent_name:
                                    parent_with_transformations(imported_object, blender_object, inherit_transformations = False)
                                    multi_object_data_list.append(imported_object.data)

                            already_existing_objects[swtor_filepath] = multi_object_data_list


                        else:
                            # Join objects into a single one (using bpy.ops because
                            # the alternative is sisyphean: meshes, materials…).
                            deselectall()
                            for imported_object in imported_objects:
                                imported_object.select_set(state= True)
                            bpy.context.view_layer.objects.active = imported_objects[0]
                            bpy.ops.object.join()
                            blender_object = bpy.context.view_layer.objects.active
                            deselectall()
                            already_existing_objects[swtor_filepath] = [blender_object.data]


                        blender_object.name = swtor_id
                        
                        print()  # adds line feed to previous print()






            # After all this processing, there's only one object,
            # to transform, no matter if imported, duplicated, and
            # parenting the rest of a multi-object.
            #
            # Position, Rotate and Scale the object.
            # we are delaying the usual 90º rotation in the X axis
            # to the very end of the whole process, as doing it now
            # would lead to extra nested rotations after the general
            # parenting stage that we don't know how to correct.

            if not swtor_name.endswith(".hms"):
                position = [element["position"][0], 
                            element["position"][1],
                            element["position"][2]]
            
                rotation = [radians( element["rotation"][0]), 
                            radians( element["rotation"][1]),
                            radians( element["rotation"][2])]

                scale =    [element["scale"][0], 
                            element["scale"][1],
                            element["scale"][2]]
            else:
                scale = [0.001, 0.001, 0.001]
            blender_object.location = position
            blender_object.rotation_mode = 'ZXY'
            blender_object.rotation_euler = rotation
            blender_object.scale = scale

            # Resize lights to something more reasonable
            if swtor_name.endswith(".lit"):
                scale = scale / 10

            # Fill custom properties to the object to facilitate
            # other processes.
            blender_object["swtor_id"] = swtor_id
            blender_object["swtor_parent_id"] = swtor_parent_id
            blender_object["swtor_json"] = json_filename
            if gr2HasParams:
                blender_object["gr2_scale"] = self.SceneScaleFactor
                blender_object["gr2_axis_conversion"] = True

            # Props that no longer seem necessary once transforms were nailed down
            # blender_object["swtor_positionX"] = str(item["position"][0])
            # blender_object["swtor_positionY"] = str(item["position"][1])
            # blender_object["swtor_positionZ"] = str(item["position"][2])
            # blender_object["swtor_rotationX"] = str(item["rotation"][0])
            # blender_object["swtor_rotationY"] = str(item["rotation"][1])
            # blender_object["swtor_rotationZ"] = str(item["rotation"][2])
            # blender_object["swtor_finalPositionX"] = str(item["finalPosition"]["0"])
            # blender_object["swtor_finalPositionY"] = str(item["finalPosition"]["1"])
            # blender_object["swtor_finalPositionZ"] = str(item["finalPosition"]["2"])


        print(LINEBACK + "DONE!")

# endregion


        # -------------------------------------------------------------------------------
        # FINAL PROCESSING PASSES -------------------------------------------------------
        # -------------------------------------------------------------------------------

# region

        # Parenting pass

        print("\n\nPARENTING OBJECTS:\n------------------\n")

        amount_processed = 0
        for element in swtor_location_data:
            amount_processed += 1
            swtor_id = element["id"]
            if swtor_id in bpy.data.objects:
                swtor_parent_id = element["parent"]
                if swtor_parent_id != "0":
                    if swtor_parent_id in bpy.data.objects:
                        print(f"{LINEBACK}{amount_processed * 100 / amount_to_process:6.2f} %  Parenting  {swtor_id}  to  {swtor_parent_id}")
                        
                        parent_with_transformations(bpy.data.objects[swtor_id], bpy.data.objects[swtor_parent_id], inherit_transformations = True)
                    else:
                        print(f"{LINEBACK}{amount_processed * 100 / amount_to_process:6.2f} %  Parenting  {swtor_id}  to  {swtor_parent_id}  FAILED!!! Parent doesn't exist")
                        print(f"          AREA: {element['json_filename']:<{max_json_filename_length}}   ORPHANED OBJECT: {str(Path(element['assetName']).stem):{max_swtor_name_length}}")
                        print()
        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = None
        
        print(LINEBACK + "DONE!")



        # Renaming pass

        print("\n\nRENAMING OBJECTS:\n-----------------\n")

        amount_processed = 0
        for element in swtor_location_data:
            amount_processed += 1
            swtor_id = element["id"]
            if swtor_id in bpy.data.objects:
                swtor_name = Path(element["assetName"]).stem
                if swtor_name != "heightmap":
                    bpy.data.objects[swtor_id].name = swtor_name
                    print(f"{LINEBACK}{amount_processed * 100 / amount_to_process:6.2f} %  Renaming  {swtor_id}  {swtor_name}")

        print(LINEBACK + "DONE!")



        # Processing DBOs pass
        
        if self.SkipDBOObjects:
            amount_processed = 0
            print("\n\nCONVERTING DBO OBJECTS TO EMPTIES:\n-----------------\n")
            for obj in bpy.data.objects[:]:
                if obj.data:  # Empties have no object data
                    if obj.name.startswith("dbo") or obj.data.name.startswith("dbo"):
                        empty = replace_with_empty( bpy.data.objects[obj.name])
                        amount_processed += 1
                        print(f"{LINEBACK}Converting DBO #{amount_processed} : {empty.name}")

            print(LINEBACK + "DONE!")
            
            

        # Non-parenting Empties clean-up pass

        print("\n\nDELETING UNUSED EMPTIES:\n------------------------\n")
        scene = bpy.context.scene

        # Create a list to store empties that should be deleted
        empties_to_delete = []

        # Iterate through all objects in the scene
        for obj in scene.objects:
            if obj.type == 'EMPTY':
                # Check if the empty is a parent or child of other objects
                # if not obj.parent and not obj.children:
                if not obj.children:
                    empties_to_delete.append(obj)

        # Delete the unused empties
        for obj in empties_to_delete:
            bpy.data.objects.remove(obj, do_unlink=True)     
        
        print(LINEBACK + "DONE!")
        


    # -------------------------------------------------------------------------------
    # FINAL ROTATION OF THE WHOLE AREA ----------------------------------------------
    # -------------------------------------------------------------------------------

        selectparents()

        if self.ApplyFinalRotation is True:
            print("\n\nFINAL SCENE ROTATION:\n---------------------\n")
            finalrotation()
            # finalrotationbymethod()
            print(LINEBACK + "DONE!")

        if self.ApplySceneScale is True:
            print("\n\nFINAL SCENE SCALING:\n--------------------\n")
            scalescene(scale_factor=self.SceneScaleFactor)
            print(LINEBACK + "DONE!")

        deselectall()


    # -------------------------------------------------------------------------------
    # APPLYING MATERIALS ------------------------------------------------------------
    # -------------------------------------------------------------------------------

        if self.ApplyMaterials is True:
            print("\n\nAPPLYING MATERIALS:\n-------------------\n")
            bpy.ops.zgswtor.process_named_mats(use_selection_only=False)


    # -------------------------------------------------------------------------------
    # some final housekeeping -------------------------------------------------------
    # -------------------------------------------------------------------------------

        # If number of "imported" lights exceeds 100, exclude their collections from view
        if self.CreateSceneLights and Lights_count > 100:
            view_layer = bpy.context.view_layer
            for collection in view_layer.layer_collection.children:
                iterate_collections(collection, exclude_collection_lights)
                # exclude_collection_lights DOESN'T WORK!!!
                # Collections have no .exclude method, which that fn tries


        # If Hide after Import is on, hide area objects from view
        if self.HideAfterImport:
            print("\n\nHIDING OBJECTS FROM VIEW\n------------------------\n")
            view_layer = bpy.context.view_layer
            for collection in bpy.data.collections:
                if collection.name.split(" ")[0] in json_filenames:
                    if collection.objects:
                        for obj in collection.objects:
                            obj.hide_set(True)


        # If Exclude after Import is on, exclude area Collections from view
        # (but not its Objects and Terrains' sub-Collections)
        if self.ExcludeAfterImport:
            print("\n\nEXCLUDING COLLECTIONS FROM VIEWLAYER\n------------------------------------\n")
            view_layer = bpy.context.view_layer
            for collection in view_layer.layer_collection.children:
                if (collection.name in json_filenames
                    and " - Objects" not in collection.name
                    and " - Terrain" not in collection.name
                    and " - Lights" not in collection.name):
                    
                    collection.exclude = True




    # -------------------------------------------------------------------------------
    # THE END. FINIS.  --------------------------------------------------------------
    # -------------------------------------------------------------------------------
        
        print("\n\n")
        print("SETTINGS USED:\n")
        print("SKIP DBO OBJECTS: ", str(self.SkipDBOObjects))
        print("ADD PLACEHOLDER LIGHTS: ", str(self.CreateSceneLights))
        print("MERGE MULTI-MESH OBJECTS ", str(self.MergeMultiMeshObjects))
        print("APPLY FINAL ROTATION: ", str(self.ApplyFinalRotation))
        print("APPLY MATERIALS: ", str(self.ApplyMaterials))
        print("APPLY SCENE SCALE: ", str(self.ApplySceneScale))
        print("HIDE OBJECTS AFTER IMPORT: ", str(self.HideAfterImport))
        print("EXCLUDE COLLECTIONS AFTER IMPORT: ", str(self.ExcludeAfterImport))
        print("------------------------------------------")
        if self.CreateSceneLights and Lights_count > 100:
            print("Number of lights in the area exceeds 100.")
            print("Their Collections have been hidden to help")
            print("Blender's responsiveness.")
            print("------------------------------------------")

        end_time = time.time()
        total_time = end_time - start_time

        print(f"Task executed in hh:mm:ss.ms = {str(datetime.timedelta(seconds=total_time))[:-3]}")
        print("------------------------------------------")
        print("\nALL DONE!\n\nHAVE A NICE DAY.\n\nBYE <3!")
    
    
    
        return {'FINISHED'}
    








# Register and add to the "file selector" menu (required to use F3 search "Text Import Operator" for quick access).
def register():

    bpy.types.Scene.ZGSAA_ApplyFinalRotation = bpy.props.BoolProperty(
        description="Disable to skip final rotation. All objects will need to be rotated X Axis 90 Degrees",
        default=True,
    )
    bpy.types.Scene.ZGSAA_ApplyMaterials = bpy.props.BoolProperty(
        description="Apply materials to the objects based on matching .mat files info in Resources",
        default=True,
    )
    bpy.types.Scene.ZGSAA_ApplySceneScale = bpy.props.BoolProperty(
        description="Scale the entire scene by a factor (x10, typically)",
        default=False,
    )
    bpy.types.Scene.ZGSAA_SceneScaleFactor = bpy.props.FloatProperty(
        description="Scale Factor If Applying Scene Scale",
        default=10.0,
    )
    bpy.types.Scene.ZGSAA_SkipDBOObjects = bpy.props.BoolProperty(
        description="Don't import design blockout (DBO) objects such as blockers, portals, etc",
        default=True,
    )
    bpy.types.Scene.ZGSAA_CreateSceneLights = bpy.props.BoolProperty(
        description="Automatically create basic scene lighting based on in game lighting nodes.\nIf they exceed the amount of 100, they will be created\nas Excluded From The View Layer for performance reasons",
        default=False,
    )
    bpy.types.Scene.ZGSAA_CollectionObjects = bpy.props.BoolProperty(
        description="Separates objects, terrains and lights in per-Area children Collections",
        default=False,
    )
    bpy.types.Scene.ZGSAA_MergeMultiMeshObjects = bpy.props.BoolProperty(
        description="Joins single .gr2 file-originated multi-mesh objects\ninto single objects",
        default=False,
    )
    bpy.types.Scene.ZGSAA_HideAfterImport = bpy.props.BoolProperty(
        description="Imported Area objects are hidden ('eye' icon in Outliner, 'h' shortcut) to keep Blender\nmore responsive when having massive amounts of objects per individual Collections.\n\nLag could persist if the Outliner is overloaded, but it should be far more tolerable.\n\nRecommended when importing .json files weighting several MegaBytes each",
        default=False,
    )
    bpy.types.Scene.ZGSAA_ExcludeAfterImport = bpy.props.BoolProperty(
        description="Resulting Collections are excluded (checkbox in Outliner, 'e' shortcut')\nto keep Blender fully responsive and be able to manage them without lag.\n\nExcluded Collections won't list their objects in the Outliner: that's normal.\n\nRecommended when importing a massive number of areas, such as whole worlds.\n\n(Excluding Collections resets the hide/show state of the Collections' contents.\nHide Objects After Importing won't have an effect if this option is on)",
        default=False,
    )
    bpy.types.Scene.ZGSAA_ShowFullReport = bpy.props.BoolProperty(
        description="If checked, a full length report will be produced, including not just errors but importing successes, too.\n\nFull length reports may exceed the Console's default capacity and become truncated.\nTo avoid that, increase that setting accordingly, around 500 lines per expected .json file,\nin your Operating System's Terminal app or in your IDE (Integrated Development Environment)",
        default=False,
    )

    bpy.utils.register_class(ZGSWTOR_OT_area_assembler)
    


def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_area_assembler)
    
    del bpy.types.Scene.ZGSAA_ApplyFinalRotation
    del bpy.types.Scene.ZGSAA_ApplyMaterials
    del bpy.types.Scene.ZGSAA_ApplySceneScale
    del bpy.types.Scene.ZGSAA_SceneScaleFactor
    del bpy.types.Scene.ZGSAA_SkipDBOObjects
    del bpy.types.Scene.ZGSAA_CreateSceneLights
    del bpy.types.Scene.ZGSAA_CollectionObjects
    del bpy.types.Scene.ZGSAA_MergeMultiMeshObjects
    del bpy.types.Scene.ZGSAA_HideAfterImport
    del bpy.types.Scene.ZGSAA_ExcludeAfterImport
    del bpy.types.Scene.ZGSAA_ShowFullReport



if __name__ == "__main__":
    register()

    # Test Call
    #bpy.ops.import_area.area_json('INVOKE_DEFAULT')

# endregion








































# -------------------------------------------------------------------------------
# UTLITY FUNCTIONS --------------------------------------------------------------
# -------------------------------------------------------------------------------
# region




# MINOR UTILITY CONSOLE FUNCTIONS -----------------------------------------------

@contextlib.contextmanager
def suppress_stdout(suppress=True):
    # Console output supressor for hiding the .gr2 addon's output.
    # Use suppress=False to allow for specific outputs
    # in the middle of a suppressed block of code.
    # Usage is:
    # with suppress_stdout():
    #     <code to be suppressed here>
    #     Use suppress=False to allow for specific outputs
    #     in the middle of a suppressed block of code.

    # (No need to explicitly stop suppression).
    if suppress:
        with io.StringIO() as buffer:
            old_stdout = sys.stdout
            sys.stdout = buffer
            try:
                yield
            finally:
                sys.stdout = old_stdout
    else:
        yield


# Create objects-fitting Empties (not in use yet)
def encase_objects_with_empty(objects, empty_name = "Empty", collection_name = ""):
    # Create a new Empty object
    empty = bpy.data.objects.new(empty_name, None)
    if collection_name == "":
        bpy.context.collection.objects.link(empty)
    else:
        if collection_name not in bpy.data.collections:
            bpy.data.collections.new(collection_name)
        bpy.data.collections[collection_name].objects.link(empty)
        
    # Set the Empty object's display type to 'CUBE'
    empty.empty_display_type = 'CUBE'

    # Set the Empty object's origin to the center of its base
    empty.matrix_world = calculate_base_center_matrix(objects)

    # Parent objects to the Empty object
    for obj in objects:
        obj.parent = empty
        
    return empty
    
def calculate_base_center_matrix(objects):
    # Find the minimum and maximum coordinates of all objects' bounding boxes
    min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
    max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')

    for obj in objects:
        bbox = obj.bound_box
        for vertex in bbox:
            min_x = min(min_x, vertex[0])
            min_y = min(min_y, vertex[1])
            min_z = min(min_z, vertex[2])
            max_x = max(max_x, vertex[0])
            max_y = max(max_y, vertex[1])
            max_z = max(max_z, vertex[2])

    # Calculate the center of the base
    base_center = (
        (min_x + max_x) / 2,
        (min_y + max_y) / 2,
        min_z
    )

    # Calculate the translation vector to move the origin
    translation_vector = -base_center

    # Create a translation matrix
    translation_matrix = Matrix.Translation(translation_vector)

    return translation_matrix




# Functions for managing Collections in the Outliner

# THIS IS PROBABLY NOT WORKING
def iterate_collections(collection, function):
    # (its only use in this operator is passing it
    # exclude_collection_lights, which excludes
    # the collection from the view_layer, but that
    # fn is known not to be working)
    #
    # Define a function to recursively iterate over
    # all collections in a hierarchy and apply
    # a function to them.

    function(collection)
    
    # Recursively iterate over all child collections
    for child_collection in collection.children:
        iterate_collections(child_collection, function)

def exclude_collection_lights(collection):
    # DOESN'T WORK (collections don't
    # have an .exclude method)
    if " - Lights" in collection.name:
        collection.exclude = True
        

def hide_collection_children(collection):
    for child in collection.children:
        child.hide_viewport = True

def link_objects_to_collection (objects, collection, move = False):
    """
    Links objects to a Collection. If move == True,
    it unlinks the objects from their current Collections first.
    Accepts a single object or a list of objects. 
    """

    # Make sure objects works as a list for the loop.
    if not isinstance(objects, list):
        objects = [objects]

    for object in objects:
        # First, unlink from any collections it is in.
        if object.users_collection and move == True:
            for current_collections in object.users_collection:
                current_collections.objects.unlink(object)

        # Then link to collection.
        collection.objects.link(object)

    return


def parent_with_transformations(obj_to_parent, parent_obj, inherit_transformations=True):
    """
    Parents an object to another, inheriting its transformations
    (plain .parent method-style) or not (imitating bpy.ops).
    Args:
        obj_to_parent (_type_): bpy.data.object.
        parent_obj (_type_): bpy.data.object.
        inherit_transformations (bool, optional): defaults to True.
    """
    # Clear any existing parent-child relationship
    obj_to_parent.parent = None
    
    # Set new parent-child relationship
    obj_to_parent.parent = parent_obj
    
    # Inherit transformations
    if inherit_transformations:
        # Get parent's world matrix
        parent_matrix = parent_obj.matrix_world
        
        # Apply parent's world matrix to child's local matrix
        obj_to_parent.matrix_local = parent_matrix @ obj_to_parent.matrix_local
    
    # Clear child's transformation if not inheriting transformations
    else:
        obj_to_parent.location = (0,0,0)
        obj_to_parent.rotation_euler = (0,0,0)
        obj_to_parent.scale = (1,1,1)

    return


def find_closest_match(strings_list, reference_string):
    
    # Finds the closest match to a reference string
    # among the strings in a list.
    # Meant to find which sub-object in a multi-object
    # is the main one (name closest to the file's one).
    # CHECK IF IT'S JUST THE FIRST ONE CONSISTENTLY (ALTHOUGH
    # BPY.DATA.OBJECTS MIGHT DISORDER THEM) OR IF
    # THERE IS SOME SIMPLE HEURISTIC (UNDERLINES?)
    closest_match = strings_list[0] # a default winner if all are equally bad
    highest_closeness = 0
    for candidate_string in strings_list:
        closeness = count_matching_characters(reference_string, candidate_string)
        if closeness > highest_closeness:
            highest_closeness = closeness
            closest_match = candidate_string
    return closest_match

# UNUSED DISCARDED
def count_matching_characters(string1, string2):
    # A gross and cheap approach to calculating
    # the "distance" between two strings
    # by checking how many characters match.

    """
    Counts the number of matching characters between two strings.

    Args:
        string1 (str): The first string.
        string2 (str): The second string.

    Returns:
        int: The number of matching characters.
    """
    # Initialize a counter for the number of matching characters.
    count = 0

    # Iterate over the characters in the first string.
    for char in string1:
        # If the character is also in the second string, increment the counter.
        if char in string2:
            count += 1

    # Return the number of matching characters.
    return count


def replace_with_empty(obj):
    """
    ChatGPT-generated code (like pulling teeth).
    Preserves the object's original name
    (and its parent, children and Collections state).

    Args:
        obj (bpy.types.Object): object to be replaced.

    Returns:
        obj (bpy.types.Object): replacement Empty object.
    """    

    # No checks to force exception if wrongly fed.
    # if obj is None:
    #     print("Object is None. Exiting.")
    #     return
    
    
    # Save the object's name and world transformation matrix
    obj_name = obj.name
    obj_matrix_world = obj.matrix_world.copy()
    
    # Save the parent
    parent = obj.parent
    
    # Save the children and their world matrices
    children = [(child, child.matrix_world.copy()) for child in obj.children]
    
    # Save the collections the object is in
    collections = [coll for coll in obj.users_collection]
    
    # Create a new empty object
    empty = bpy.data.objects.new(f"{obj.name}_empty", None)
    bpy.context.collection.objects.link(empty)
    
    # Set the empty's world transformation to match the original object
    empty.matrix_world = obj_matrix_world
    
    # Set the parent of the empty to be the same as the original object's parent
    if parent is not None:
        empty.parent = parent
        empty.matrix_parent_inverse = obj.matrix_parent_inverse
    
    # Add the empty to the same collections as the original object
    for coll in collections:
        coll.objects.link(empty)

    # Re-parent the children to the empty and restore their world transformations
    for child, world_matrix in children:
        child.parent = empty
        child.matrix_world = world_matrix
    
    # Optionally, transfer custom properties, constraints, etc. from the original object to the empty
    for prop in obj.keys():
        if prop not in "_RNA_UI":
            empty[prop] = obj[prop]
    
    # Store the object's name
    obj_name = obj.name
    
    # Remove the empty from the default collection (where it was originally linked)
    bpy.context.collection.objects.unlink(empty)
    
    # Delete the original object
    bpy.data.objects.remove(obj)

    # Make sure empty's name is correct after original object
    # is no more and its name has been freed, to avoid .001s
    # (BF intends to make collisions control stricter in the future).
    empty.name = obj_name

    return empty


def separate_by_specific_materials(obj_or_obj_name, materials_names, separate = True):

    """
    Separates an object's polys associated to specified materials
    into separate objects per those materials. By default it
    deletes those polys and materials from the original object.
    
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



def selectparents():
    deselectall()
    if bpy.data.objects:
        for obj in bpy.data.objects:
            if "swtor_parent_id" in obj.keys():
                obj.select_set( obj["swtor_parent_id"] == "0" )

    return


def selectall():
    bpy.ops.object.select_all(action='SELECT')

    for obj in bpy.data.objects:
       if obj.type == 'MESH':
           obj.select_set(True)
    return


# WHY NOT OPS-BASED?
def deselectall():
    for obj in bpy.data.objects:
        obj.select_set(False)
    return


def finalrotation():        
    # Final Rotation correction pass to the whole construction
    bpy.ops.transform.rotate(value=radians(90),
                            orient_axis='X',
                            orient_type='GLOBAL',
                            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                            orient_matrix_type='GLOBAL',
                            constraint_axis=(True, False, False),
                            mirror=False,
                            use_proportional_edit=False,
                            proportional_edit_falloff='SMOOTH',
                            proportional_size=1,
                            use_proportional_connected=False,
                            use_proportional_projected=False,
                            release_confirm=True)
            
    return

# UNUSED. MOST PROBABLY IT WILL BE DELETED
def finalrotationbymethod():
    if bpy.data.objects:
        for obj in bpy.data.objects:
            if "swtor_parent_id" in obj.keys():
                if obj["swtor_parent_id"] == "0":
                    obj_x_rotation = obj.rotation_euler[0]
                    obj.rotation_euler[0] = obj_x_rotation + radians(90)
# def transform_rotate(obj_list, axis=(1, 0, 0), angle=0):
#     # Calculate the rotation matrix
#     rotation_matrix = Matrix.Rotation(angle, 4, axis)
    
#     # Loop through each object in the list
#     for obj in obj_list:
#         # Set the object's rotation mode to 'AXIS_ANGLE'
#         obj.rotation_mode = 'AXIS_ANGLE'
        
#         # Convert the matrix to an axis-angle representation
#         axis_angle = rotation_matrix.to_axis_angle()
        
#         # Set the object's axis-angle rotation
#         obj.rotation_axis_angle = axis_angle.axis + (axis_angle.angle,)


    return


    
def scalescene(scale_factor=10.0):
    print("----------------------------------------------------")
    print("\n\nAPPLY SCENE SCALE\n\n") 
    print("----------------------------------------------------")
        
    # Final Size correction pass to the whole construction
    bpy.ops.transform.resize(value=(scale_factor, scale_factor, scale_factor),
                            orient_type='GLOBAL',
                            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                            orient_matrix_type='GLOBAL',
                            constraint_axis=(True, True, True),
                            mirror=False,
                            use_proportional_edit=False,
                            proportional_edit_falloff='SMOOTH',
                            proportional_size=1,
                            use_proportional_connected=False,
                            use_proportional_projected=False,
                            snap=False,
                            snap_elements={'INCREMENT'},
                            use_snap_project=False,
                            snap_target='CLOSEST',
                            use_snap_self=False,
                            use_snap_edit=True,
                            use_snap_nonedit=True,
                            use_snap_selectable=False,
                            release_confirm=True)
        
    return
    
    # endregion