import bpy
import addon_utils
from pathlib import Path
import os


class zg_props(bpy.types.PropertyGroup):
    
    check_gr2:                           bpy.props.BoolProperty()
    check_gr2_status:                    bpy.props.StringProperty()
    check_gr2_status_verbose:            bpy.props.StringProperty()
    
    check_resources:                     bpy.props.BoolProperty()
    check_resources_status:              bpy.props.StringProperty()
    check_resources_status_verbose:      bpy.props.StringProperty()
    
    check_custom_shaders:                bpy.props.BoolProperty()
    check_custom_shaders_status:         bpy.props.StringProperty()
    check_custom_shaders_status_verbose: bpy.props.StringProperty()




def register():
    bpy.utils.register_class(zg_props)
    bpy.types.Scene.zg_props = bpy.props.PointerProperty(type=zg_props)


def unregister():
    bpy.utils.unregister_class(zg_props)
    del bpy.types.Scene.zg_props