import bpy
from bpy.types import Operator


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
    was_corrected = False  # Set return flag 

    for face in mesh.polygons:
        if face.material_index == material_slot or material_slot == None:
            for loop_index in face.loop_indices:
                uv = uv_layer[loop_index].uv
                if uv.y <= 1:
                    return was_corrected
                uv.x += uv_offset[0]
                uv.y += uv_offset[1]
                was_corrected = True
                
    return was_corrected


class ZGSWTOR_PT_correct_twilek_uv(Operator):
    bl_idname = "zgswtor.correct_twilek_uv"
    bl_label = "Correct Twi'lek's UVs"
    bl_description = "Check for any Twi'lek character head object and, if needed,\nreposition their eyes' UVs inside their textures' area so that\nthey produce correct results in baking operations"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls,context):
        return bpy.data.objects != None


    def execute(self, context):

        heads_count = 0
        heads_corrected_count = 0
        heads_already_ok_count = 0
        
        for obj in bpy.data.objects:
            if "head_twilek" in obj.data.name:
                heads_count += 1
                result = translate_uv_coordinates(obj, 1, (0,-2) )
                if result is False:
                    heads_already_ok_count += 1
                else:
                    heads_corrected_count += 1

        if heads_count == 0:
            report_txt = "No twi'lek head objects detected."
        else:
            if heads_corrected_count == 0:
                report_txt = "All twi'lek heads had correct eye UVs already."
            elif heads_corrected_count == 1:
                report_txt = "1 twi'lek head's eye UVs corrected."
            else:
                report_txt = str(heads_corrected_count) + " twi'lek heads' eye UVs corrected."

        self.report({'INFO'}, report_txt)
        return {'FINISHED'}



# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_PT_correct_twilek_uv)
    
def unregister():
    bpy.utils.unregister_class(ZGSWTOR_PT_correct_twilek_uv)
    

if __name__ == "__main__":
    register()