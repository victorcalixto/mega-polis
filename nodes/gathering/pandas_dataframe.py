import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy

#Megapolis Dependencies
from megapolis.dependencies import pandas as pd


if pd is None:
    add_dummy('SvMegapolisPandasDataframe', 'Pandas Dataframe', 'pandas')
else:
    class SvMegapolisPandasDataframe(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: Pandas Series
        Tooltip: Creates a Pandas Dataframe from a Pandas Series
        """
        bl_idname = 'SvMegapolisPandasDataframe'
        bl_label = 'Pandas Dataframe'
        bl_icon = 'MESH_DATA'

        def sv_init(self, context):
            # inputs
            self.inputs.new('SvStringsSocket', "Pandas Series")
            self.inputs.new('SvStringsSocket', "Features Names")

            #outputs
            self.outputs.new('SvStringsSocket', "Pandas Dataframe")

        def process(self):
            if not self.inputs["Pandas Series"].is_linked or not self.inputs["Features Names"].is_linked:
                return
            self.series = self.inputs["Pandas Series"].sv_get(deepcopy = False)
            self.features = self.inputs["Features Names"].sv_get(deepcopy = False)
            
            dataframe = pd.DataFrame()
            dataframe = pd.concat(self.series, axis=1)
            dataframe.columns = self.features

            df = dataframe
         
            self.outputs["Pandas Dataframe"].sv_set(df)

def register():
    if pd is not None:
        bpy.utils.register_class(SvMegapolisPandasDataframe)

def unregister():
    if pd is not None:
        bpy.utils.unregister_class(SvMegapolisPandasDataframe)
