import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
import os


class SvMegapolisGetFilePath(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: GetFilePath
    Tooltip: Get File Path
    """
    bl_idname = 'SvMegapolisGetFilePath'
    bl_label = 'Get File path'
    bl_icon = 'MESH_DATA'
    

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvFilePathSocket', "File")

        #outputs
        self.outputs.new('SvStringsSocket', "File Path")

    def process(self):
        if not self.inputs["File"].is_linked:
            return
        self.file = self.inputs["File"].sv_get(deepcopy = False)

        file=self.file[0][0]

        file_out = [os.path.dirname(os.path.abspath(file))]

        #Output
        self.outputs["File Path"].sv_set(file_out)

def register():
    bpy.utils.register_class(SvMegapolisGetFilePath)

def unregister():
    bpy.utils.unregister_class(SvMegapolisGetFilePath)
