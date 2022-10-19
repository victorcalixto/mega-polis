import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy


#Megapolis Dependencies
from megapolis.dependencies import pandas as pd


if pd is None:
    add_dummy('SvMegapolisGetPandasFeature', 'Get Pandas Feature', 'pandas')
else:
    class SvMegapolisGetPandasFeature(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: Get Pandas Feature
        Tooltip: Gets a feature from a pandas series
        """
        bl_idname = 'SvMegapolisGetPandasFeature'
        bl_label = 'Get Pandas Feature'
        bl_icon = 'MESH_DATA'
        

        def sv_init(self, context):
            # inputs
            self.inputs.new('SvStringsSocket', "Dataframe")
            self.inputs.new('SvStringsSocket', "Feature")

            #outputs
            self.outputs.new('SvStringsSocket', "Dataframe Out")

        def process(self):
            if not self.inputs["Dataframe"].is_linked or not self.inputs["Feature"].is_linked:
                return
            self.df = self.inputs["Dataframe"].sv_get(deepcopy = False)
            self.feature = self.inputs["Feature"].sv_get(deepcopy = False)
          
            feature = self.feature[0][0]
            data = self.df[feature]

            df_out = data

            self.outputs["Dataframe Out"].sv_set(data)

def register():
    if pd is not None:
        bpy.utils.register_class(SvMegapolisGetPandasFeature)

def unregister():
    if pd is not None:
        bpy.utils.unregister_class(SvMegapolisGetPandasFeature)
