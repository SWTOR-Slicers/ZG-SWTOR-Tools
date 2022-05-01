import bpy
import addon_utils


class ZGSWTOR_OT_adjust_normals_emissives(bpy.types.Operator):

    bl_label = "SWTOR Tools"
    bl_idname = "zgswtor.adjust_normals_emissives"
    bl_description = "Sets the normals' strength in all SWTOR materials\nin the Scene"
    bl_options = {'REGISTER', 'UNDO'}


    # # Check that there are SWTOR shaders in the scene) 
    # @classmethod
    # def poll(cls,context):
    #     if bpy.data.node_groups["SWTOR"]:
    #         return True
    #     else:
    #         return False

    SetNormalsStrengthFloat: bpy.props.FloatProperty(
        name="SWTOR Normals Strength",
        default = 1.0
    )

    def execute(self, context):

        bpy.context.window.cursor_set("WAIT")

        # --------------------------------------------------------------
        # Check which version of the SWTOR shaders are available
        if addon_utils.check("io_scene_gr2_legacy")[1]:
            if "Uber Shader" in bpy.data.node_groups:
                gr2_addon_legacy = True
            else:
                self.report({"WARNING"}, "Although the Legacy version of the 'io_scene_gr2' add-on is enabled, no Uber Shader exists yet. Please import any arbitrary .gr2 object to produce an Uber Shader template.")
                return {"CANCELLED"}
        elif addon_utils.check("io_scene_gr2")[1]:
            gr2_addon_legacy = False
        else:
            self.report({"WARNING"}, "No version of the 'io_scene_gr2' add-on is enabled.")
            return {"CANCELLED"}


        for mat in bpy.data.materials:
            mat_nodes = mat.node_tree.nodes
            for node in mat_nodes:
                if node.name == "SWTOR":
                    print(mat.name)
                    subnodes=node.node_tree.nodes
                    for subnode in subnodes:
                        if subnode.name == "Normal Map":
                            subnode.inputs[0].default_value = self.SetNormalsStrengthFloat
                        
        bpy.context.window.cursor_set("DEFAULT")
        return {"FINISHED"}


# UI is set in ui.py


# ------------------------------------------------------------------
# Registrations

def register():
    bpy.types.Scene.uber_normals_fac = bpy.props.FloatProperty(
        name="Uber Materials", min=1.0, max=100.0, soft_min=1.0, soft_max=100.0, default= 1
        )
    bpy.types.Scene.creature_normals_fac = bpy.props.FloatProperty(
        name="Creature Materials", min=1.0, max=100.0, soft_min=1.0, soft_max=20.0, default= 1
        )
    bpy.types.Scene.garment_normals_fac = bpy.props.FloatProperty(
        name="Garment Materials", min=1.0, max=100.0, soft_min=1.0, soft_max=100.0, default= 1
        )
    bpy.types.Scene.skinb_normals_fac = bpy.props.FloatProperty(
        name="SkinB Materials", min=1.0, max=100.0, soft_min=1.0, soft_max=20.0, default= 1
        )
    bpy.types.Scene.hairc_normals_fac = bpy.props.FloatProperty(
        name="HairC Materials", min=1.0, max=100.0, soft_min=1.0, soft_max=20.0, default= 1
        )
    bpy.types.Scene.eye_normals_fac = bpy.props.FloatProperty(
        name="Eye Materials", min=1.0, max=100.0, soft_min=1.0, soft_max=100.0, default= 1
        )


    bpy.types.Scene.uber_emission_fac = bpy.props.FloatProperty(
        name="Uber Materials", min=0.0, max=100.0, soft_min=1.0, soft_max=100.0, default= 1
        )
    bpy.types.Scene.creature_emission_fac = bpy.props.FloatProperty(
        name="Creature Materials", min=0.0, max=100.0, soft_min=1.0, soft_max=100.0, default= 1
        )
    bpy.types.Scene.garment_emission_fac = bpy.props.FloatProperty(
        name="Garment Materials", min=0.0, max=100.0, soft_min=1.0, soft_max=100.0, default= 1
        )
    bpy.types.Scene.skinb_emission_fac = bpy.props.FloatProperty(
        name="SkinB Materials", min=0.0, max=100.0, soft_min=1.0, soft_max=100.0, default= 1
        )
    bpy.types.Scene.hairc_emission_fac = bpy.props.FloatProperty(
        name="HairC Materials", min=0.0, max=100.0, soft_min=1.0, soft_max=100.0, default= 1
        )
    bpy.types.Scene.eye_emission_fac = bpy.props.FloatProperty(
        name="Eye Materials", min=0.0, max=100.0, soft_min=1.0, soft_max=100.0, default= 1
        )

    bpy.utils.register_class(ZGSWTOR_OT_adjust_normals_emissives)

def unregister():
    del bpy.types.Scene.uber_normals_fac
    del bpy.types.Scene.creature_normals_fac
    del bpy.types.Scene.garment_normals_fac
    del bpy.types.Scene.skinb_normals_fac
    del bpy.types.Scene.hairc_normals_fac
    del bpy.types.Scene.eye_normals_fac

    bpy.utils.unregister_class(ZGSWTOR_OT_adjust_normals_emissives)

if __name__ == "__main__":
    register()