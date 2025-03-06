import bpy
from sverchok.node_tree import SverchCustomTreeNode


class SvMegapolisCreateDictionary(SverchCustomTreeNode, bpy.types.Node):
    """
    A Sverchok node that creates a dictionary from input keys and values.
    
    Inputs:
        - Dictionary Keys: Comma-separated keys.
        - Dictionary Values: Comma-separated values.
    
    Output:
        - Dictionary: A dictionary created from the given keys and values.
    """
    bl_idname = "SvMegapolisCreateDictionary"
    bl_label = "Create Dictionary"
    bl_icon = "SORTALPHA"

    def sv_init(self, context):
        """Initialize node inputs and outputs."""
        self.inputs.new("SvStringsSocket", "Dictionary Keys")
        self.inputs.new("SvStringsSocket", "Dictionary Values")
        self.outputs.new("SvStringsSocket", "Dictionary")

    def process(self):
        """Process input data and create a dictionary."""
        if not (self.inputs["Dictionary Keys"].is_linked and self.inputs["Dictionary Values"].is_linked):
            return

        dict_keys = self.inputs["Dictionary Keys"].sv_get(deepcopy=False)[0]
        dict_values = self.inputs["Dictionary Values"].sv_get(deepcopy=False)[0]

        dict_keys_list = dict_keys.split(",")
        dict_values_list = dict_values.split(",")

        # Ensure keys and values lists are of the same length
        if len(dict_keys_list) != len(dict_values_list):
            return

        dictionary = [{k: v for k, v in zip(dict_keys_list, dict_values_list)}]
        
        self.outputs["Dictionary"].sv_set(dictionary)


def register():
    bpy.utils.register_class(SvMegapolisCreateDictionary)


def unregister():
    bpy.utils.unregister_class(SvMegapolisCreateDictionary)
