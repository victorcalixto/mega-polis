import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy

#Megapolis Dependencies

class SvMegapolisCreateDictionary(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Create Dictionary
    Tooltip: Create Dictionary
    """
    bl_idname = 'SvMegapolisCreateDictionary'
    bl_label = 'Create Dictionary'
    bl_icon = 'MESH_DATA'
    

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Dictionary Keys")
        self.inputs.new('SvStringsSocket', "Dictionary Values")

        #outputs
        self.outputs.new('SvStringsSocket', "Dictionary")

    def process(self):
        if not self.inputs["Dictionary Keys"].is_linked or not self.inputs["Dictionary Keys"].is_linked :
            return
        self.dict_keys = self.inputs["Dictionary Keys"].sv_get(deepcopy = False)
        self.dict_values = self.inputs["Dictionary Values"].sv_get(deepcopy = False)
        
        dict_keys = self.dict_keys[0]
        dict_values = self.dict_values[0]

        dict_keys_list = dict_keys.split(",")
        dict_values_list = dict_values.split(",")

        dictio = {}
        for i in range(0,len(dict_keys_list)):
            dictio[dict_keys_list[i]] = dict_values_list[i]

        dictionary = [dictio]   

        #Output
        self.outputs["Dictionary"].sv_set(dictionary)

def register():
    bpy.utils.register_class(SvMegapolisCreateDictionary)

def unregister():
    bpy.utils.unregister_class(SvMegapolisCreateDictionary)

