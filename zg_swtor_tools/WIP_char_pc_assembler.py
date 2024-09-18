import bpy
from bpy.props import IntProperty, EnumProperty
from bpy.types import PropertyGroup

import zipfile
from os import name

import json


# Functions

def replace_dict_keys(d, key_map):
    """
    Recursively replace keys in a dictionary based on a provided key mapping.

    Parameters:
    - d: The dictionary with keys to be replaced. Can be nested.
    - key_map: A dictionary that maps old keys to new keys.

    Returns:
    - A new dictionary with updated keys.
    """
    if isinstance(d, dict):
        new_dict = {}
        for k, v in d.items():
            # Replace the key if it exists in key_map, otherwise keep the original key
            new_key = key_map.get(k, k)
            # Recursively replace keys in nested dictionaries
            new_dict[new_key] = replace_dict_keys(v, key_map)
        return new_dict
    elif isinstance(d, list):
        # If the value is a list, recurse into any dictionaries within the list
        return [replace_dict_keys(item, key_map) for item in d]
    else:
        # If the value is not a dictionary or list, return it as is
        return d


def replace_dict_values(d, value_map):
    """
    Recursively replace values in a dictionary based on a provided value mapping.

    Parameters:
    - d: The dictionary with values to be replaced. Can be nested.
    - value_map: A dictionary that maps old values to new values.

    Returns:
    - A new dictionary with updated values.
    """
    if isinstance(d, dict):
        new_dict = {}
        for k, v in d.items():
            # Recursively replace values in nested dictionaries
            new_dict[k] = replace_dict_values(v, value_map)
        return new_dict
    elif isinstance(d, list):
        # If the value is a list, recurse into any dictionaries or lists within the list
        return [replace_dict_values(item, value_map) for item in d]
    else:
        # If the value is not a dictionary or list, replace it if it exists in value_map, otherwise return it as is
        return value_map.get(d, d)



# This Add-on's own modules
from .utils.addon_checks import requirements_checks

ADDON_ROOT = __file__.rsplit(__name__.rsplit(".")[0])[0] + __name__.rsplit(".")[0]


# Class for a PC Character's sliders data to be placed in context.screen
class PcSliders(PropertyGroup):

    # In node info:
    pc_species: EnumProperty(name="Species", default="human", items=[
        ("cathar",              "Cathar",               ""),
        ("chiss",               "Chiss",                ""),
        ("cyborg",              "Cyborg",               ""),
        ("human",               "Human",                ""),
        ("miralukan_legacy",    "Miralukan",            ""),
        ("mirialan_legacy",     "Mirialan",             ""),
        ("nautolan",            "nautolan",             ""),
        ("Cathar",              "Cathar",               ""),
        ("rattataki",           "Rattataki",            ""),
        ("sith_legacy",         "Sith Pureblood",       ""),
        ("twilek_legacy",       "Twi'lek",              ""),
        ("zabrak_rep_legacy",   "Zabrak (Republic)",    "Zabrak (Iridonian tattoos)"),
        ("zabrak_imp_legacy",   "Zabrak (Empire)",      "Zabrak (Sith tattoos)"),
    ])
    _pc_species_previous = None


    pc_class: EnumProperty(name="Class", default="jedi_knight", items=[
        ("jedi_knight",     "Jedi Knight",      ""),
        ("jedi_consular",   "Jedi Consular",    ""),
        ("trooper",         "Trooper",          ""),
        ("smuggler",        "Smuggler",         ""),
        ("sith_warrior",    "Sith Warrior",     ""),
        ("sith_inquisitor", "Sith Inquisitor",  ""),
        ("bounty_hunter",   "Bounty Hunter",    ""),
        ("imperial_agent",  "Imperial Agent",   ""),
    ])
    _pc_class_previous = None
    
    pc_gender: EnumProperty(name="Gender", default="male", items=[
        ("male",    "Male",   ""),
        ("female",  "Female", ""),
    ])
    _pc_gender_previous = None
    
    pc_bodytype: EnumProperty(name="Body", default="bt2", items=[
        ("bt1", "Body Type 1", ""),
        ("bt2", "Body Type 2", ""),
        ("bt3", "Body Type 3", ""),
        ("bt4", "Body Type 4", ""),
    ])
    _pc_bodytype_previous = None
    
    pc_head:        IntProperty( name="Head",           min=1, max=50, default=1)
    pc_age:         IntProperty( name="Scars/Age",      min=1, max=50, default=1)
    
    pc_complexion:  IntProperty( name="Complexion",     min=1, max=50, default=1)
    pc_eyecolor:    IntProperty( name="Eye Color",      min=1, max=50, default=1)
    pc_facehair:    IntProperty( name="Beard/Cyber/Mask/Jewelry",    min=1, max=50, default=1)
    pc_facepaint:   IntProperty( name="Tattoo/Makeup/Skin Pattern/Fur",        min=1, max=50, default=1)
    pc_hair:        IntProperty( name="Hair/Horns/Montrals/Band",           min=1, max=50, default=1)
    pc_haircolor:   IntProperty( name="Hair/Montral Pattern Color",     min=1, max=50, default=1)
    pc_skincolor:   IntProperty( name="Skin/Fur Color",     min=1, max=50, default=1)



    settings_descriptions = {
        "appPcsSkeletonDisplayList"     :  "Body Type",
        "appPcsHeadSkeletonMap"         :  "Head",
        
        "appSlotAge"                    :  "Scars",
        "appSlotComplexion"             :  "Complexion",
        "appSlotEyeColor"               :  "Eye Color",
        "appSlotFaceHair"               :  "Beard, Cybernetic Implant, Mask, or Jewelry",
        "appSlotFacePaint"              :  "Tattoo, Cosmetics, Skin Pattern, or Fur Pattern",
        "appSlotHair"                   :  "Hair, Horns, Montrals, or Headband",
        "appSlotHairColor"              :  "Hair Color, or Montrals Color Pattern",
        "appSlotSkinColor"              :  "Skin Color, or Fur Color"
    }



# -------------------------------------------------------------------------------------
# Operator


class ZGSWTOR_OT_pc_assembler(bpy.types.Operator):
    bl_label = "SWTOR Player Character Assembler"
    bl_idname = "zgswtor.pc_assembler"
    bl_description = "to fill"
    bl_options = {'REGISTER', 'UNDO'}




    def execute(self, context):
        bpy.context.window.cursor_set("WAIT")

        checks = requirements_checks()
        
        # if not checks["resources"]:
        #     bpy.context.window.cursor_set("DEFAULT")
        #     self.report({"WARNING"}, "No SWTOR 'resources' folder selected in this Add-on's Preferences.")
        #     return {"CANCELLED"}


        # Get the extracted SWTOR assets' "resources" folder from the add-on's preferences.
        # swtor_resources_folderpath = bpy.context.preferences.addons["zg_swtor_tools"].preferences.swtor_resources_folderpath
        swtor_resources_folderpath = "D:/3D SWTOR/SWTOR ASSETS/SWTOR EXTRACTION 64/resources/"


        # OPENING CHARACTER DATA (zipped nodes and related resources):
        
        # PCS strings (shown in the Appearance Booth's UI).
        if not zipfile.is_zipfile(f"{ADDON_ROOT}/rsrc/pcs_str.zip"):
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, "pcs_str.zip file not found.")
            return {"CANCELLED"}
        with zipfile.ZipFile(f"{ADDON_ROOT}/rsrc/pcs_str.zip") as pcs_str_zip:
            pcs_str_file = pcs_str_zip.open("pcs_str.json", "r")
        pcs_str = json.load(pcs_str_file)


        # GOM strings (for identifying the PCS nodes' fields).
        if not zipfile.is_zipfile(f"{ADDON_ROOT}/rsrc/gom_str.zip"):
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, "gom_str.zip file not found.")
            return {"CANCELLED"}
        with zipfile.ZipFile(f"{ADDON_ROOT}/rsrc/gom_str.zip") as gom_str_zip:
            gom_file = gom_str_zip.open("gom_str.json", "r")
        gom = json.load(gom_file)


        # # Types strings (for identifying the PCS nodes' data types).
        # if not zipfile.is_zipfile(f"{ADDON_ROOT}/rsrc/types.zip"):
        #     bpy.context.window.cursor_set("DEFAULT")
        #     self.report({"WARNING"}, "types.zip file not found.")
        #     return {"CANCELLED"}
        # types_zip = zipfile.ZipFile(f"{ADDON_ROOT}/rsrc/types.zip")
        # types_file = types_zip.open("types.json", "r")
        # types = json.load(types_file)


        # DYNAMIC strings (for identifying the PCS nodes' data types).
        if not zipfile.is_zipfile(f"{ADDON_ROOT}/rsrc/dynamic.zip"):
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, "dynamic.zip file not found.")
            return {"CANCELLED"}
        with zipfile.ZipFile(f"{ADDON_ROOT}/rsrc/dynamic.zip") as dynamic_zip:
            dynamic_file = dynamic_zip.open("dynamic.json", "r")
        dynamic = json.load(dynamic_file)
        # Turn it into a dict that indexes the data by FQN
        dynamic = {elem["node"]["fqn"]:elem["obj"] for elem in dynamic}
        dynamic = replace_dict_values(dynamic, gom)


        # PCS nodes (the actual sliders-to-character data).
        if not zipfile.is_zipfile(f"{ADDON_ROOT}/rsrc/pcs.zip"):
            bpy.context.window.cursor_set("DEFAULT")
            self.report({"WARNING"}, "pcs.zip file not found.")
            return {"CANCELLED"}
        with zipfile.ZipFile(f"{ADDON_ROOT}/rsrc/pcs.zip") as pcs_zip:
            pass

        # Read the character's sliders data
        swpc = bpy.context.scene.swtor_pc_sliders
        
        # Build path to specific PCS node, catering to
        # some oddities in Zabrak nomenclature per faction:
        # * When in the Empire faction, plain "zabrak" equals "zabrak_imp_legacy".
        # * When in the Republic faction, plain "zabrak" equals "zabrak_rep_legacy".
        if "zabrak" in swpc.pc_species:
            if swpc.pc_class in ["sith_warrior", "sith_inquisitor", "bounty_hunter", "imperial_agent"]:
                if "_imp_" in swpc.pc_species:
                    species = "zabrak"
            else:
                if "_rep_" in swpc.pc_species:
                    species = "zabrak"
        else:
            species = swpc.pc_species
        
        
        # Get the specific node for the combination of character traits
        node_path = f"pcs/{swpc.pc_class}/{swpc.pc_gender}/{species}.json"
        node_file = pcs_zip.open(node_path, "r")
        
        # As we are going to preprocess the data to replace IDs' values
        # with human-readable GOM names, we are reading the text file
        # instead of directly parsing its .json data.
        node = json.load(node_file)
        
        print("replacing")
        node = replace_dict_keys(node, gom)
        # node = replace_dict_keys(node, types)
        # node = replace_dict_keys(node, pcs_str) # Leave for pass to update UI names
        
        print("replaced")


        # Some "constants"
        
        base_bodies = {
            "male bt1":    "bma",
            "male bt2":    "bmn",
            "male bt3":    "bms",
            "male bt4":    "bmf",
            "female bt1":  "bfa",
            "female bt2":  "bfn",
            "female bt3":  "bfs",
            "female bt4":  "bfb",
            }

        # This is the sliders' order
        # in which they appear in
        # appPcsCustomizationSlotNameIds.
        slot_types = {
            "1":  "appSlotAge",
            "2":  "appSlotBoot",
            "3":  "appSlotBracer",
            "4":  "appSlotChest",
            "5":  "appSlotComplexion",
            "6":  "appSlotCreature",
            "7":  "appSlotEyeColor",
            "8":  "appSlotFace",
            "9":  "appSlotFaceHair",
            "10": "appSlotFacePaint",
            "11": "appSlotHair",
            "12": "appSlotHairColor",
            "13": "appSlotHand",
            "14": "appSlotHead",
            "15": "appSlotLeg",
            "16": "appSlotSkinColor",
            "17": "appSlotWaist",
            "18": "appSlotUnknown",
            "19": "appSlotGarmentHue",
            "20": "appSlotColorScheme",
            "21": "appSlotMainHand",
            "22": "appSlotOffHand"
            }

        mesh_types = {
            "2":  "appSlotBoot",
            "3":  "appSlotBracer",
            "4":  "appSlotChest",
            "6":  "appSlotCreature", # For sure?
            "8":  "appSlotFace",
            "9":  "appSlotFaceHair",
            "11": "appSlotHair",
            "13": "appSlotHand",
            "14": "appSlotHead",
            "15": "appSlotLeg",
            "17": "appSlotWaist",
        }
        
        
        # Build dict relating appPcsCustomizationSlotNameIds' keys with
        # the locTextRetrieverMap data saying what slider they are
        # and what name they use in the Character Creator's UI.
        node_slots = {}
        
        for x, slot_type in zip( node["appPcsCustomizationSlotNameIds"], slot_types ):
            slot_value = node["appPcsCustomizationSlotNameIds"][x]
            slot_name = pcs_str[ node["locTextRetrieverMap"][slot_value]["strLocalizedTextRetrieverStringID"] ]
            
            node_slots[x] = {"slot_type":slot_type, "slot_name":slot_name, "slot_value_id":slot_value}

        
        base_body = base_bodies[f"{swpc.pc_gender} {swpc.pc_bodytype}"]
        body_type = int(swpc.pc_bodytype[2:])
        

        # Assign slider names from pcs.stb strings
        # in_order_slots_types = {i:slot for (i, slot) in enumerate(slot_types)}
        # in_order_slots_texts = {i:pcs_str[SlotName] for i, SlotName in enumerate(node["appPcsCustomizationSlotNameIds"])}

        # Body type (1 to 4) to appPcsSkeletonDisplayList
        appPcsSkeletonDisplayList = node["appPcsSkeletonDisplayList"][body_type - 1]

        # HEAD
        # List of appPcsCustomizationSlots for each body type's Head slider
        appPcsHeadSkeletonMap = node["appPcsHeadSkeletonMap"][appPcsSkeletonDisplayList]
        head_id = appPcsHeadSkeletonMap[swpc.pc_head - 1]
        head_data = node["appPcsCustomizationSlots"][head_id]
        
        head_ModelID = head_data["appAppearanceSlotModelID"]
        head_MaterialIndex = head_data["appAppearanceSlotMaterialIndex"]
        head_Attachments = head_data["appAppearanceSlotAttachments"]

        # SLIDERS SLOTS (can be less than the usual for certain PCS path combinations)
        slots_data = node["appPcsSliderMap"][head_id]

        # Final ModelID/MaterialIndex/etc per slot
        final_data = []
        
        # Add the head data we just got
        final_data.append( {
            "Type":          "appSlotHead",
            "ModelID":       head_ModelID,
            "MaterialIndex": head_MaterialIndex,
            "Attachments":   head_Attachments,
        } )
        
        for slot in node_slots:  # cycle through all possible slots
            
            # Does it exist for this specific character type?
            if not slot in slots_data:
                continue
            
            # Get slider position
            pc_prop_name = f'pc_{slot_types[slot].replace("appSlot", "").lower()}'
            if not hasattr(swpc, pc_prop_name):
                continue
            
            slider_pos = getattr(swpc, pc_prop_name)
            if not slider_pos:
                continue
            
            # slider_pos = str(slider_pos)
            
            appPcsCustomizationSlots_id = slots_data[slot][slider_pos - 1]
            appPcsCustomizationSlots_values = node["appPcsCustomizationSlots"][appPcsCustomizationSlots_id]            
            
            final_data.append( {
                "Type":          slot_types[slot],
                "ModelID":       appPcsCustomizationSlots_values.get("appAppearanceSlotModelID"      , None),
                "MaterialIndex": appPcsCustomizationSlots_values.get("appAppearanceSlotMaterialIndex", None),
                "Attachments":   appPcsCustomizationSlots_values.get("appAppearanceSlotAttachments"  , None),
            } )
                        
            
        body_defaults = [
            {
                "Type":          "appSlotBoot",
                "ModelID":       "1142744",
                "MaterialIndex": "",
            },
            {
                "Type":         "appSlotChest",
                "ModelID":       "",
                "MaterialIndex": "",
            },
            {
                "Type":         "appSlotHand",
                "ModelID":       "",
                "MaterialIndex": "",
            },
            {
                "Type":          "appSlotLeg",
                "ModelID":       "1142836",
                "MaterialIndex": "2777271", # I'm choosing the dyeable one instead of 1143851
            },
        ]
            
        final_data += body_defaults
            
        # Materials for the body parts will depend on the head's, as there is such things
        # as boot_naked_african_young_a01c01_[bt].mat
            
            
            
        
        
        bpy.context.window.cursor_set("DEFAULT")
        return {"FINISHED"}
    







# -------------------------------------------------------------------------------------
# Panel (provisional)


class ZGSWTOR_PT_test(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ZG TEST"
    bl_label = "SWTOR PC Assembler"

    def draw(self, context):
        
        layout = self.layout
        
        swtor_pc_sliders = bpy.context.scene.swtor_pc_sliders
        
        col = layout.column()
        col.prop(swtor_pc_sliders, "pc_class",      text="Class")
        col.prop(swtor_pc_sliders, "pc_species",    text="Species")
        col.prop(swtor_pc_sliders, "pc_gender",     text="Gender")
        col.prop(swtor_pc_sliders, "pc_bodytype",   text="Body")
        
        col.separator()
        
        # col.prop(swtor_pc_sliders, "pc_head",       text="Head")
        # col.prop(swtor_pc_sliders, "pc_age",        text="Scars")
        # col.prop(swtor_pc_sliders, "pc_complexion", text="Complexion")
        # col.prop(swtor_pc_sliders, "pc_eyecolor",   text="Eye Color")
        # col.prop(swtor_pc_sliders, "pc_facehair",   text="Facial Hair")
        # col.prop(swtor_pc_sliders, "pc_hair",       text="Hair")
        # col.prop(swtor_pc_sliders, "pc_haircolor",  text="Hair Color")
        # col.prop(swtor_pc_sliders, "pc_skincolor",  text="Skin Color")

        col.prop(swtor_pc_sliders, "pc_head",       )
        col.prop(swtor_pc_sliders, "pc_age",        )
        col.prop(swtor_pc_sliders, "pc_complexion", )
        col.prop(swtor_pc_sliders, "pc_eyecolor",   )
        col.prop(swtor_pc_sliders, "pc_facehair",   )
        col.prop(swtor_pc_sliders, "pc_hair",       )
        col.prop(swtor_pc_sliders, "pc_haircolor",  )
        col.prop(swtor_pc_sliders, "pc_skincolor",  )
        
        col.separator()
        
        col.operator("zgswtor.pc_assembler", text="Build Player Character")
        



# REGISTRATIONS ---------------------------------------------

classes = [
    PcSliders,
    ZGSWTOR_OT_pc_assembler,
    ZGSWTOR_PT_test,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.swtor_pc_sliders = bpy.props.PointerProperty(type=PcSliders)

def unregister():
    del bpy.types.Scene.swtor_pc_sliders

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()