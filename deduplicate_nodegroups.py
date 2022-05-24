# For references to approaches to the subject, see:
# https://blender.stackexchange.com/questions/45992/how-to-remove-duplicated-node-groups
# https://gist.github.com/IPv6/0886731e6e98b6968cb1ffa0b8d5900e (the one used here)
# https://meshlogic.github.io/posts/blender/scripting/eliminate-material-duplicates/


import bpy

def eliminateNG(node):
    node_groups = bpy.data.node_groups
                
    # Get the node group name as 3-tuple (base, separator, extension)
    (base, sep, ext) = node.node_tree.name.rpartition('.')

    # Replace the numeric duplicate
    if ext.isnumeric():
        if base in node_groups:
            print("- Replace nodegroup '%s' with '%s'" % (node.node_tree.name, base))
            node.node_tree.use_fake_user = False
            node.node_tree = node_groups.get(base)


class ZGSWTOR_OT_deduplicate_nodegroups(bpy.types.Operator):

    bl_idname = "zgswtor.deduplicate_nodegroups"
    bl_label = "ZG Deduplicate Nodegroups"
    bl_description = "Replaces all Nodegroups with numbered suffixes (.001, .002, etc.)\nwith instances of the non-suffixed original Nodegroups.\n\nThis operator affects all Nodegroups in the current Scene\nand doesn't require a selection"
    bl_options = {'REGISTER', "UNDO"}



    def execute(self, context):
        bpy.context.window.cursor_set("WAIT")

        #--- Search for duplicates in actual node groups
        ng_counter = 0
        node_groups = bpy.data.node_groups
        for group in node_groups:
            for node in group.nodes:
                if node.type == 'GROUP':
                    eliminateNG(node)
                    ng_counter += 1

        #--- Search for duplicates in materials
        mats = list(bpy.data.materials)
        worlds = list(bpy.data.worlds)

        for mat in mats + worlds:
            if mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type == 'GROUP':
                        eliminateNG(node)
                        ng_counter += 1

        bpy.context.window.cursor_set("DEFAULT")
        self.report({'INFO'}, str(ng_counter) + " duplicate Nodegroups deduped and set to zero users" )
        return {'FINISHED'}


# UI is set in ui.py


# Registrations

def register():
    bpy.utils.register_class(ZGSWTOR_OT_deduplicate_nodegroups)

def unregister():
    bpy.utils.unregister_class(ZGSWTOR_OT_deduplicate_nodegroups)

if __name__ == "__main__":
    register()