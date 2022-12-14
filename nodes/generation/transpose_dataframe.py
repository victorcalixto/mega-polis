import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import pandas as pd
 

class SvMegapolisTransposeDataframe(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Transpose Dataframe
    Tooltip: Transpose a Dataframe
    """
    bl_idname = 'SvMegapolisTransposeDataframe'
    bl_label = 'Transpose Dataframe'
    bl_icon = 'MESH_DATA'
    sv_dependencies = {'pandas'}

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Dataframe")

        #outputs
        self.outputs.new('SvStringsSocket', "Dataframe Output")

    def process(self):
        if not self.inputs["Dataframe"].is_linked:
            return
        self.df = self.inputs["Dataframe"].sv_get(deepcopy = False)

        data = self.df.T

        df_transposed = data

        #Output
        self.outputs["Dataframe Output"].sv_set(df_transposed)


def register():
    bpy.utils.register_class(SvMegapolisTransposeDataframe)


def unregister():
    bpy.utils.unregister_class(SvMegapolisTransposeDataframe)
