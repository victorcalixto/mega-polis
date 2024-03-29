import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import pandas as pd


class SvMegapolisGetPandasFeature(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Get Pandas Feature
    Tooltip: Gets a feature from a pandas series
    """
    bl_idname = 'SvMegapolisGetPandasFeature'
    bl_label = 'Get Pandas Feature'
    bl_icon = 'MESH_DATA'
    sv_dependencies = {'pandas'}

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Dataframe")
        self.inputs.new('SvStringsSocket', "Feature")

        #outputs
        self.outputs.new('SvStringsSocket', "Dataframe Out")
        self.outputs.new('SvStringsSocket', "List Out")


    def process(self):
        if not self.inputs["Dataframe"].is_linked or not self.inputs["Feature"].is_linked:
            return
        self.df = self.inputs["Dataframe"].sv_get(deepcopy = False)
        self.feature = self.inputs["Feature"].sv_get(deepcopy = False)
      
        feature = self.feature[0][0]
        data = self.df[feature]

        df_out = data
        list_out = df_out.tolist()

        self.outputs["Dataframe Out"].sv_set(data)
        self.outputs["List Out"].sv_set(list_out)



def register():
    bpy.utils.register_class(SvMegapolisGetPandasFeature)


def unregister():
    bpy.utils.unregister_class(SvMegapolisGetPandasFeature)
