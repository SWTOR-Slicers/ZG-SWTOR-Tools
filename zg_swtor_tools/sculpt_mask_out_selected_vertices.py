# based on: https://blender.stackexchange.com/questions/251597/how-can-i-create-a-sculpt-mask-based-purely-on-face-vertex-selection-instead-of

import bpy
import bmesh
try:
    import numpy
except:
    pass

# Main

class ZGSWTOR_OT_selected_vertices_to_sculpt_mask(bpy.types.Operator):
    bl_idname = "zgswtor.selected_vertices_to_sculpt_mask"
    bl_label = "ZG Set Selected Vertices as a Sculpt Mode Mask"
    bl_options = {'REGISTER', "UNDO"}
    bl_description = "Sets the active object's selected vertices to a masked out state for Sculpt Mode\n(it masks everything but those) protecting the vertices from sculpting actions.\n\nUsage:\n1. Select the vertices in Edit Mode, leaving them so (Vertex selections\n    done in Edit Mode persist across modes).\n\n2. Use the tool while in Sculpt Mode to protect them: they'll turn darker to\n    show that they are excluded from the sculpting tools' influence"

    # Check that there is an active object 
    @classmethod
    def poll(cls,context):
        if bpy.context.active_object:
            return True
        else:
            return False


    def execute(self, context):

        bpy.context.window.cursor_set("WAIT")  # Show wait cursor icon

        obj = context.active_object
        bm = bmesh.new()

        if obj.mode == "EDIT":
            bm = bmesh.from_edit_mesh(obj.data)
        else:
            bm.from_mesh(obj.data)

        #get selected verts
        v_sel = numpy.empty(len(obj.data.vertices), dtype=bool)
        obj.data.vertices.foreach_get('select', v_sel)
        sel_idx, = numpy.where(v_sel)
        report_verts = len(sel_idx)


        #get custom data layer paint_mask
        mask_layer= bm.verts.layers.paint_mask.verify() #strange way, but that gets you custom data layer
        bm.verts.ensure_lookup_table()
        #set every selected vert to mask_value

        mask_value = 1.0
        for idx in sel_idx:
            bm.verts[idx][mask_layer]=mask_value

        if obj.mode == "EDIT":
            # bmesh.update_edit_mesh(obj.data)
            pass
        else:
            bm.to_mesh(obj.data)




        if report_verts > 0:
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
            self.report({'INFO'}, obj.name + "'s " + str(report_verts) + " selected vertices set as a sculpting mask")
        else:
            self.report({"WARNING"}, obj.name + " has no selected vertices")

        bpy.context.window.cursor_set("DEFAULT")  # Show normal cursor icon

        return {"FINISHED"}


# UI is set in addon_ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_selected_vertices_to_sculpt_mask)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_selected_vertices_to_sculpt_mask)

if __name__ == "__main__":
    register()