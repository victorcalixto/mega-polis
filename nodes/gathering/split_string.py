import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


class SvMegapolisSplitString(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Split String
    Tooltip: Splits a string into a list
    """
    bl_idname = 'SvMegapolisSplitString'
    bl_label = 'Split String'
    bl_icon = 'MESH_DATA'

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "String")
        self.inputs.new('SvStringsSocket', "Separator")

        #outputs
        self.outputs.new('SvStringsSocket', "List")

    def process(self):
        if not self.inputs["String"].is_linked or not self.inputs["Separator"].is_linked:
            return
        self.string = self.inputs["String"].sv_get(deepcopy = False)
        self.separator = self.inputs["Separator"].sv_get(deepcopy = False)
        
        string = self.string[0][0]
        separator = self.separator[0][0]

        str_list = string.split(separator)

        self.outputs["List"].sv_set(str_list)

def register():
    bpy.utils.register_class(SvMegapolisSplitString)

def unregister():
    bpy.utils.unregister_class(SvMegapolisSplitString)
