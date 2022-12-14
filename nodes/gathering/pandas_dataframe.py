import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

#Megapolis Dependencies
from megapolis.dependencies import pandas as pd


class SvMegapolisPandasDataframe(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Pandas Series
    Tooltip: Creates a Pandas Dataframe from a Pandas Series
    """
    bl_idname = 'SvMegapolisPandasDataframe'
    bl_label = 'Pandas Dataframe'
    bl_icon = 'MESH_DATA'
    sv_dependencies = {'pandas'}

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
    bpy.utils.register_class(SvMegapolisPandasDataframe)


def unregister():
    bpy.utils.unregister_class(SvMegapolisPandasDataframe)
