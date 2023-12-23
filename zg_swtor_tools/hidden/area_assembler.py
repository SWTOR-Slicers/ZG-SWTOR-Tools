import bpy
import json
from math import degrees, radians
from mathutils import Matrix
from pathlib import Path
from zipfile import ZipFile
import copy
import os
import time
import datetime

# These imports are for a "hide console output" fn
import contextlib
import io
import sys






# -------------------------------------------------------------------------------
# START WINDOW IMPORT -----------------------------------------------------------
# -------------------------------------------------------------------------------


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import (BoolProperty,
                       StringProperty,
                       CollectionProperty
                       )
from bpy.types import Operator




class ZGSWTOR_OT_area_assembler(Operator):
    bl_idname = "zgswtor.area_assembler"
    bl_label = "Import Area .json files"
    bl_description = "Import SWTOR Area data files (json) from Jedipedia.net's File Viewer.\n\nRequires:\n• Setting the path to an assets 'resources' folder in SWTOR Area Assembler's Addon Preferences.\n• An active Modern .gr2 importer Addon"
    bl_options = {'REGISTER', 'UNDO'}




    # File Browser for selecting paths.json file
    
    def invoke(self, context, event):
        # Match properties to UI's checkboxes
        self.ApplyFinalRotation = context.scene.ZGSAA_ApplyFinalRotation
        self.ApplyMaterials = context.scene.ZGSAA_ApplyMaterials
        self.ApplySceneScale = context.scene.ZGSAA_ApplySceneScale
        self.SkipDBOObjects = context.scene.ZGSAA_SkipDBOObjects
        self.CreateSceneLights = context.scene.ZGSAA_CreateSceneLights
        self.CollectionObjects = context.scene.ZGSAA_CollectionObjects
        self.MergeMultiMeshObjects = context.scene.ZGSAA_MergeMultiMeshObjects
        self.HideAfterImport = context.scene.ZGSAA_HideAfterImport
        self.ExcludeAfterImport = context.scene.ZGSAA_ExcludeAfterImport
        self.ShowFullReport = context.scene.ZGSAA_ShowFullReport

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


    # Checks that the 'resources' folder set in Preferences is valid
    # and that the .gr2 importer addon's operator is available.
    # Greys-out the Import sub-menu otherwise.
    @classmethod
    def poll(cls,context):
        swtor_resources_folderpath = context.preferences.addons
        
        swtor_resources_folderpath = context.preferences.addons[__package__].preferences.swtor_resources_folderpath
        
        if Path(swtor_resources_folderpath).exists() and ("gr2" in dir(bpy.ops.import_mesh)):
            return True
        else:
            return False

    


    # ImportHelper mixin class' properties
    # (pay attention to their types)

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



    # List of operator properties, the attributes will be assigned
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
        description="Automatically scale the entire scene after import by 10x to better match Blender Units",
        default=False,
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

    
    # Register some properties in the object class for helping
    # dealing with them in certain phases of the process
    bpy.types.Object.swtor_type = bpy.props.StringProperty()
    bpy.types.Object.swtor_id = bpy.props.StringProperty()
    bpy.types.Object.swtor_parent_id = bpy.props.StringProperty()
    bpy.types.Object.swtor_json = bpy.props.StringProperty()
    





    def execute(self, context):
        
        if self.filepath == self.directory:
            # When nothing is selected, self.filepath gets the directory too, so…
            self.report({'ERROR'}, "No files selected")
            return {'CANCELLED'}



        # if this is in invoke() already it isn't necessary here
        
        # # Match properties to UI's checkboxes
        # self.ApplyFinalRotation = context.scene.ZGSAA_ApplyFinalRotation
        # self.ApplyMaterials = context.scene.ZGSAA_ApplyMaterials
        # self.ApplySceneScale = context.scene.ZGSAA_ApplySceneScale
        # self.SkipDBOObjects = context.scene.ZGSAA_SkipDBOObjects
        # self.CreateSceneLights = context.scene.ZGSAA_CreateSceneLights
        # self.CollectionObjects = context.scene.ZGSAA_CollectionObjects
        # self.MergeMultiMeshObjects = context.scene.ZGSAA_MergeMultiMeshObjects
        # self.HideAfterImport = context.scene.ZGSAA_HideAfterImport
        # self.ExcludeAfterImport = context.scene.ZGSAA_ExcludeAfterImport
        # self.ShowFullReport = context.scene.ZGSAA_ShowFullReport





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
        swtor_resources_folderpath = context.preferences.addons[__package__].preferences.swtor_resources_folderpath

        # Check that there is a terrain maps subfolder in the resources folder
        terrain_folderpath = Path(swtor_resources_folderpath) / "world" / "heightmaps"
        if not terrain_folderpath.exists():
            terrain_folderpath = None


        # Open the auxiliary files (zipped nodes and relationship tables)

        addon_pathfolder = os.path.dirname(__file__)
        
        # Open zipped dyn nodes folder
        try:
            dyn_zip = ZipFile(str(Path(addon_pathfolder) / "resources" / "dyn.zip"), "r")
            dyn_nodes__available = True
        except FileNotFoundError:
            print(" -- No dyn.zip file found inside the addon. Some objects will be omitted")  # Console.


        # Open spn to pcl or dyn correspondence table
        try:
            with open(str(Path(addon_pathfolder) / "resources" / "spn_table.txt"), "r") as spn_to_gr2_or_dyn:
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

        
        plc_nodes_folder = str(Path(addon_pathfolder) / Path("resources") / Path("plc.zip"))
        dyn_nodes_folder = str(Path(addon_pathfolder) / Path("resources") / Path("dyn.zip"))


        # -------------------------------------------------------------------------------
        # PER-JSON FILE PREPROCESSING ---------------------------------------------------
        # -------------------------------------------------------------------------------

        # Iterate through the selected files and build a full location data list
        # plus a list of location names out of the .json filenames
        # and appropriate Collections

        swtor_location_data = []
        json_names = []
        dyn_file_data = []

        # For console output formatting stuff
        max_json_name_length = 0
        max_swtor_name_length = 0


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
            json_name = Path(json_filepath).stem
            json_names.append(json_name)

            # For console output formatting stuff
            if len(json_name) > max_json_name_length:
                max_json_name_length = len(json_name)


            # Flag to decide to create a terrain Collection for this .json area
            # if the user has selected to have sub-Collections.
            has_terrain = False


            # -------------------------------------------------------------------------------
            # PER-ELEMENT FILE PREPROCESSING ------------------------------------------------
            # -------------------------------------------------------------------------------
            # Loop through the .json file's elements,
            # filter out some obvious discardables,
            # and pre-process indirect object references
            
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
                    
                    # Add json_name to element
                    element["json_name"] = json_name


                    if (
                        (".gr2" in swtor_filepath or
                         ".hms" in swtor_filepath or
                         ".lit" in swtor_filepath or
                         ".mag" in swtor_filepath or
                         ".spn_p" in swtor_filepath or
                         ("dbo" in swtor_filepath and self.SkipDBOObjects == False) )
                         and not "_fadeportal_" in swtor_filepath
                        ):
                    
                        
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
                                                dyn_element["id"] = swtor_id + "-" + str(idx)
                                                
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
            if not json_name in bpy.data.collections:
                location_collection = bpy.data.collections.new(json_name)
                bpy.context.collection.children.link(location_collection)
            else:
                location_collection = bpy.data.collections[json_name]

            if self.CollectionObjects == True:
                # Location's lights if the user wants them (yes by default)
                if self.CreateSceneLights == True:
                    if not (json_name + " - Lights") in bpy.data.collections:
                        location_lights_collection  = bpy.data.collections.new(json_name + " - Lights")
                        location_collection.children.link(location_lights_collection)
                    else:
                        location_lights_collection  = bpy.data.collections[json_name + " - Lights"]

                # Location's terrain.
                if has_terrain == True:
                    if not (json_name + " - Terrain") in bpy.data.collections:
                        location_terrains_collection = bpy.data.collections.new(json_name + " - Terrain")
                        location_collection.children.link(location_terrains_collection)
                    else:
                        location_terrains_collection = bpy.data.collections[json_name + " - Terrain"]

                # Location's objects.
                if not (json_name + " - Objects") in bpy.data.collections:
                    location_objects_collection = bpy.data.collections.new(json_name + " - Objects")
                    location_collection.children.link(location_objects_collection)
                else:
                    location_objects_collection = bpy.data.collections[json_name + " - Objects"]



            # Create a Light data block to base Light objects on. Having one per .json file instead of
            # a single one for all the Addon's run is a bit arbitrary, but it might be interesting for,
            # say, setting a common light intensity and color per room and the like.

            if self.CreateSceneLights == True:
                light_data = bpy.data.lights.new(name= json_name, type= "POINT")
                light_data.energy = 2

                Lights_count = 0

        print(LINEBACK + "DONE!")



        # Weird case of all empty or invalid .json, but hey, could happen.
        if len(swtor_location_data) == 0:
            self.report({"WARNING"}, "The selected .json files contain no data.")
            return {"CANCELLED"}






        # -------------------------------------------------------------------------------
        # ACTUAL PROCESSING OF THE ELEMENTS IN THE AREA DATA ----------------------------
        # -------------------------------------------------------------------------------

        # SOME VARIABLES:

        # Many Hero Engine utility object types can't be determined by
        # their names, but oftentimes their materials'names are a good
        # criteria (these are all the invisible-type ones in .mat files).
        materials_to_exclude_objects_by = [
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
        ]

        # More filters to apply, by <derived> type:
        shaders_to_exclude_objects_by = [
            "OpacityFade",
        ]

        # Deduplication dict to keep track of already imported objects
        # and avoid reimporting thorugh timewasting .gr2 importer.
        # Key: value is:
        # object's filepath: imported object's mesh data
        # or
        # multi-object's filepath: [parent object's name]: 
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
            if not (swtor_filepath.endswith(".gr2") or
                    swtor_filepath.endswith(".lit") or
                    swtor_filepath.endswith(".hms") or
                    swtor_filepath.endswith(".mag") or
                    swtor_filepath.endswith(".spn_p") or
                    ("dbo" in swtor_filepath and self.SkipDBOObjects == False)
                    ):
                continue
            # delete preceding directory separator if it exists. It shouldn't vary so much
            # but SWTOR is a mess, separator types-wise.
            if swtor_filepath.startswith("/") or swtor_filepath.startswith("\\"):
                swtor_filepath = swtor_filepath[1:]

            swtor_id = element["id"]
            swtor_parent_id = element["parent"]
            swtor_name = Path(swtor_filepath).stem

            json_name = element["json_name"]


            # Unlikely to happen, but…
            if swtor_id in bpy.data.objects:
                continue

            


            if swtor_filepath.endswith(".lit"):

                # LIGHT OBJECT. ----------------------------------

                if self.CreateSceneLights == True:
                    # Collection where the light object will be moved to
                    if self.CollectionObjects == True:
                        location_lights_collection  = bpy.data.collections[json_name + " - Lights"]
                    else:
                        location_lights_collection  = bpy.data.collections[json_name]

                    light_data = bpy.data.lights[json_name]
                    blender_object = bpy.data.objects.new(name=swtor_id, object_data = light_data)

                    link_objects_to_collection(blender_object, location_lights_collection, move = True)

                    Lights_count += 1
                else:
                    continue


            elif swtor_filepath.endswith(".hms"):

                # TERRAIN OBJECT. ---------------------------------

                print(f'{LINEBACK}{amount_processed * 100 / amount_to_process:6.2f} %   AREA: {json_name:<{max_json_name_length}}   ID: {swtor_id}   -- TERRAIN OBJECT --   ', end="")

                if terrain_folderpath is None:
                    print("WARNING: NO RESOURCES\\WORLD\\HEIGHTMAPS FOLDER AVAILABLE")
                    continue

                # Collection where the terrain object will be moved to
                if self.CollectionObjects == True:
                    location_terrains_collection  = bpy.data.collections[json_name + " - Terrain"]
                else:
                    location_terrains_collection  = bpy.data.collections[json_name]

                terrain_path = str(terrain_folderpath / Path(swtor_id + ".obj") )

                # ACTUAL IMPORTING:
                # …through Blender's bpy.ops.import_scene.obj addon.
                # Does a after-minus-before bpy.data.objects check to determine
                # the objects resulting from the importing, as the addon doesn't
                # return that information.

                objects_before_importing = list(bpy.data.objects)
                try:
                    with suppress_stdout():  # To silence .obj importing outputs
                        result = bpy.ops.import_scene.obj(
                            filepath=terrain_path,
                            use_image_search=False)  # .obj importer
                    if result == "CANCELLED":
                        print(f"\n           WARNING: Blender's .obj importer failed to import {swtor_id} - {str( Path(swtor_resources_folderpath) / Path(swtor_filepath) )}\n")
                        continue
                    else:
                        print("IMPORTED")
                except:
                    print(f"\n\n           WARNING: Blender's .obj Importer CRASHED while trying to import it.")
                    print("           Despite that, the Area Importer addon will keep on importing the rest of the objects.\n")
                    continue
                objects_after_importing = list(bpy.data.objects)
                imported_objects_amount = 1
                blender_object = list(set(objects_after_importing) - set(objects_before_importing))[0]
                blender_object.name = swtor_id

                link_objects_to_collection(blender_object, location_terrains_collection, move = True)
                

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
                    location_objects_collection = bpy.data.collections[json_name + " - Objects"]
                else:
                    location_objects_collection = bpy.data.collections[json_name]

                link_objects_to_collection(blender_object, location_objects_collection, move = True)

            else:

                # MESH OBJECT  ----------------------------------

                print(f'{LINEBACK}{amount_processed * 100 / amount_to_process:6.2f} %   AREA: {json_name:<{max_json_name_length}}   ID: {swtor_id}   NAME: {swtor_name:{max_swtor_name_length}}', end="")


                if swtor_filepath.endswith(".mag"):
                    # .MAG OBJECT REFERENCE
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
                    location_objects_collection = bpy.data.collections[json_name + " - Objects"]
                else:
                    location_objects_collection = bpy.data.collections[json_name]

                if swtor_filepath not in already_existing_objects:

                    # IMPORTING NEW OBJECTS:
                    # …through Darth Atroxa's bpy.ops.import_mesh.gr2.
                    # Does a after-minus-before bpy.data.objects check to determine
                    # the objects resulting from the importing, as the addon doesn't
                    # return that information.
                    
                    objects_before_importing = list(bpy.data.objects)
                    gr2_filepath = str( Path(swtor_resources_folderpath) / Path(swtor_filepath) )
                    if os.path.isfile(gr2_filepath):
                        try:
                            with suppress_stdout():  # To silence Darth Atroxa's print() outputs
                                result = bpy.ops.import_mesh.gr2(filepath=gr2_filepath)
                            if result == "CANCELLED":
                                print(f"\n\nWARNING: .gr2 importer addon failed to import {swtor_id} - {str( Path(swtor_resources_folderpath) / Path(swtor_filepath) )}\n")
                                continue
                            else:
                                print("IMPORTED    ", end="")
                        except:
                            print(f"\n\nWARNING: the .gr2 Importer addon CRASHED while importing:\n{swtor_id} - {str( Path(swtor_resources_folderpath) / Path(swtor_filepath) )}\n")
                            print("Despite that, the Area Importer addon will keep on importing the rest of the objects")
                            continue
                        objects_after_importing = list(bpy.data.objects)
                        imported_objects = list(set(objects_after_importing) - set(objects_before_importing))
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
                    # the children objects go a long for the ride.
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
                        if self.SkipDBOObjects == True:
                            blender_object = replace_with_empty(blender_object)

                            link_objects_to_collection(blender_object, location_objects_collection, move = True)

                            print("DBO to EMPTY ", end="")
                        else:
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
                        if self.SkipDBOObjects == True:
                            if imported_object.name.startswith("dbo"):
                                is_discardable = True
                            else:
                                if imported_object.material_slots:
                                    for material_slot in imported_object.material_slots:
                                        if material_slot.name in materials_to_exclude_objects_by:
                                            is_discardable = True

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
                    


                    # It can happen that a multi-object is entirely composed of non-renderable
                    # objects, so, objects_to_group might be actually empty after discarding them.
                    if len(imported_objects) == 0:
                        already_existing_objects[swtor_filepath] = ""
                        print("DISCARDED")
                        continue

                    # Also, there could be a single object left.
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
            blender_object["swtor_json"] = json_name
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

        # -------------------------------------------------------------------------------
        # FINAL PROCESSING PASSES -------------------------------------------------------
        # -------------------------------------------------------------------------------


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
                        print(f"          AREA: {element['json_name']:<{max_json_name_length}}   ORPHANED OBJECT: {str(Path(element['assetName']).stem):{max_swtor_name_length}}")
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



        # Non-parenting Empties clean-up pass

        print("\n\nDELETING UNUSED EMPTIES:\n------------------------\n")
        scene = bpy.context.scene

        # Create a list to store empties that should be deleted
        empties_to_delete = []

        # Iterate through all objects in the scene
        for obj in scene.objects:
            if obj.type == 'EMPTY':
                # Check if the empty is a parent or child of other objects
                if not obj.parent and not obj.children:
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
            scalescene()
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


        # If Hide after Import is on, hide area objects from view
        if self.HideAfterImport:
            print("\n\nHIDING OBJECTS FROM VIEW\n------------------------\n")
            view_layer = bpy.context.view_layer
            for collection in bpy.data.collections:
                if collection.name.split(" ")[0] in json_names:
                    if collection.objects:
                        for obj in collection.objects:
                            obj.hide_set(True)


        # If Exclude after Import is on, exclude area Collections from view
        # (but not its Objects and Terrains' sub-Collections)
        if self.ExcludeAfterImport:
            print("\n\nEXCLUDING COLLECTIONS FROM VIEWLAYER\n------------------------------------\n")
            view_layer = bpy.context.view_layer
            for collection in view_layer.layer_collection.children:
                if (collection.name in json_names
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
        description="Automatically scale the entire scene after import by 10x to better match Blender Units",
        default=False,
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










































# -------------------------------------------------------------------------------
# UTLITY FUNCTIONS --------------------------------------------------------------
# -------------------------------------------------------------------------------





# MINOR UTILITY CONSOLE FUNCTIONS -----------------------------------------------

@contextlib.contextmanager
def suppress_stdout(suppress=True):
    # Console output supressor for hiding the .gr2 addon's output.
    # Use suppress=False to allow for specific outputs
    # in the middle of a suppressed block of code.
    # Usage is:
    # with suppress_stdout():
    #     <code to be suppressed here>
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


# Cre

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




# UNUSED: THE OPS ISN'T WORKING
def hide_outliner_one_level():

    # Select overriding method depending on Blender's version.
    # Starting in 3.2 context overrides are deprecated in favor of temp_override
    # https://docs.blender.org/api/3.2/bpy.types.Context.html#bpy.types.Context.temp_override
    #
    # They are scheduled to be removed in 3.3

    version = bpy.app.version
    major = version[0]
    minor = version[1]
    if major < 3 or (major == 3 and minor < 2):
        use_temp_override = False
    else:
        use_temp_override = True

    # window = current Blender app's window in focus
    window = bpy.context.window
    # screen = current Workspace
    screen = window.screen
    # areas = editors and others. There can be several areas of a same type
    areas  = [area for area in screen.areas if area.type == 'OUTLINER']

    for area in areas:
        
        outliner_area = area.spaces.active
        
        display_mode = outliner_area.display_mode
        
        if display_mode == "VIEW_LAYER":

            # Regions refer to "physical" regions inside an area: HEADER, WINDOW… (messy terminology)
            region = [region for region in area.regions if region.type == 'WINDOW'][0]
            
            override = {
                'window': window,
                'screen': screen,
                'area': area,
                'region': region,
            }

            if use_temp_override:
                with bpy.context.temp_override(window=window,
                                            screen=screen,
                                            area=area,
                                            region=region
                                            ):
                    bpy.ops.outliner.show_one_level(override, open=False)
                    outliner_area.tag_redraw()
            else:
                bpy.ops.outliner.show_one_level(override, open=False)
                outliner_area.tag_redraw()

    return



# Functions for managing Collections in the Outliner

def iterate_collections(collection, function):
    # Define a function to recursively iterate over
    # all collections in a hierarchy and apply
    # a function to them.

    function(collection)
    
    # Recursively iterate over all child collections
    for child_collection in collection.children:
        iterate_collections(child_collection, function)

def exclude_collection_lights(collection):
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
    closest_match = strings_list[0] # a default winner if all are equally bad
    highest_closeness = 0
    for candidate_string in strings_list:
        closeness = count_matching_characters(reference_string, candidate_string)
        if closeness > highest_closeness:
            highest_closeness = closeness
            closest_match = candidate_string
    return closest_match

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


def replace_with_empty(blender_object):
    # ChatGPT-generated code. Needs checking.
    # Preserves the object's original name (and its parent and children relationships,
    # just in case it's necessary): if the object has a parent, its parent relationship
    # is preserved by setting the new empty's parent to the original parent
    # and calculating the inverse transform matrix. Each child of the original object
    # is also updated to have the new empty as its parent.
    
    # Store object properties
    obj_name = blender_object.name

    obj_parent = blender_object.parent
    obj_children = blender_object.children[:]
    obj_matrix_local = blender_object.matrix_local.copy()
    obj_matrix_world = blender_object.matrix_world.copy()

    # Create empty object
    empty = bpy.data.objects.new(obj_name, None)
    empty.empty_display_size = 1.0
    empty.empty_display_type = 'CUBE'
    bpy.context.collection.objects.link(empty)

    # Set empty object properties
    empty.matrix_local = obj_matrix_local
    empty.matrix_world = obj_matrix_world

    # Set parent relationship
    if obj_parent:
        empty.parent = obj_parent
        empty.matrix_parent_inverse.copy_from(blender_object.matrix_parent_inverse)
        empty.parent_type = blender_object.parent_type
        empty.parent_space = blender_object.parent_space
        empty.parent_inverse = blender_object.parent_inverse
        
    # Set children relationships
    for child in obj_children:
        child.parent = empty


    # Delete original object
    bpy.data.objects.remove(blender_object, do_unlink=True)

    # Make sure empty's name is correct after original object
    # is no more and its name has been freed, to avoid .001s
    empty.name = obj_name

    return empty



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


def finalrotationbymethod(): # MOST PROBABLY IT WILL BE DELETED
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


    
def scalescene():
    print("----------------------------------------------------")
    print("\n\nAPPLY SCENE SCALE\n\n") 
    print("----------------------------------------------------")
        
    # Final Size correction pass to the whole construction
    bpy.ops.transform.resize(value=(10, 10, 10),
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
    