import bpy
import bmesh
from .utils.addon_checks import requirements_checks
from pathlib import Path


# Utility functions for Blender 4.1 and higher
# See: https://projects.blender.org/blender/blender/issues/117399#issuecomment-1167467

def get_internal_asset_path():
    for path_type in ("LOCAL", "SYSTEM", "USER"):
        path = Path(bpy.utils.resource_path(path_type)) / "datafiles" / "assets"
        if path.exists():
            return path
    assert False

SMOOTH_BY_ANGLE_ASSET_PATH = str(
    get_internal_asset_path() / "geometry_nodes" / "smooth_by_angle.blend"
)

SMOOTH_BY_ANGLE_NODE_GROUP_NAME = "Smooth by Angle"

def add_smooth_by_angle_modifier(obj):
    global SMOOTH_BY_ANGLE_NODE_GROUP_NAME

    smooth_by_angle_node_group = bpy.data.node_groups.get(SMOOTH_BY_ANGLE_NODE_GROUP_NAME)
    if not smooth_by_angle_node_group or smooth_by_angle_node_group.type != "GEOMETRY":
        with bpy.data.libraries.load(SMOOTH_BY_ANGLE_ASSET_PATH) as (data_from, data_to):
            data_to.node_groups = [SMOOTH_BY_ANGLE_NODE_GROUP_NAME]
        smooth_by_angle_node_group = data_to.node_groups[0]
        SMOOTH_BY_ANGLE_NODE_GROUP_NAME = smooth_by_angle_node_group.name

    modifier = obj.modifiers.new("Smooth by Angle", "NODES")
    modifier.node_group = smooth_by_angle_node_group




class ZGSWTOR_OT_clear_splitnormals_layers(bpy.types.Operator):
    bl_idname = "zgswtor.clear_splitnormals_layers"
    bl_label = "ZG Clear Split Normals Layers"
    bl_description = "Clears split normals layers in selected or all objects to solve some shading artifacts"
    bl_options = {'REGISTER', "UNDO"}


    # Check that there is a selection of objects and that we are in Object mode
    # (greys-out the UI button otherwise) 
    @classmethod
    def poll(cls,context):
        if bpy.data.objects:
            return True
        else:
            return False
    

    use_selection_only : bpy.props.BoolProperty(
        name="Apply To Selected Objects Only",
        description="Apply to selected objects only.",
        default=True,
        options={'HIDDEN'},
    )

    def execute(self, context):

        context.window.cursor_set("WAIT")  # Show wait cursor icon

        print("--------------------------")
        print("CLEAR CUSTOM SPLIT NORMALS")
        print("--------------------------")
        print()

        checks = requirements_checks()
        
        if self.use_selection_only == True:
            objs = [obj for obj in bpy.context.selected_objects if obj.type == "MESH"]
        else:
            objs = [obj for obj in bpy.data.objects if obj.type == "MESH"]
            
        if not objs:
            self.report({"WARNING"}, "No mesh objects were selected.")
            return {"CANCELLED"}

        for obj in objs:
            mesh = obj.data
            
            # Check if custom split normals are present
            if not mesh.has_custom_normals:
                print(f"{obj.name}: No custom split normals found.")
            else:
                # Remove custom split normals
                
                # Access the bmesh data of the object
                bm = bmesh.new()
                bm.from_mesh(mesh)

                # Remove custom normal layer if it exists
                if bm.loops.layers.float_vector.get("normals_split_custom"):
                    layer = bm.loops.layers.float_vector["normals_split_custom"]
                    bmesh.ops.remove_customdata_layer(bm, type='LOOP', layer=layer)

                # Update the mesh and free the bmesh
                bm.to_mesh(mesh)
                bm.free()                
                # Set Auto Smooth
                if checks["blender_version"] < 4.1:
                    # For Blender 4.0.x and lower.
                    
                    mesh.use_auto_smooth = True
                    
                    # Update mesh to apply changes
                    mesh.update()

                else:
                    # For Blender 4.1 and higher.

                    # Update mesh to apply changes
                    mesh.update()
                    
                    add_smooth_by_angle_modifier(obj)
                
                # Update mesh to apply changes
                mesh.update()

                print(f"{obj.name}: Custom split normals deleted.")

        print("\nDONE!")

        bpy.context.window.cursor_set("DEFAULT")  # Show normal cursor icon
        
        return {"FINISHED"}

    
    
    
    
# UI is set in addon_ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_clear_splitnormals_layers)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_clear_splitnormals_layers)

if __name__ == "__main__":
    register()