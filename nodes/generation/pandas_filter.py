import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import pandas as pd


class SvMegapolisPandasFilter(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Pandas Filter
    Tooltip: Creates a Pandas Filter
    """
    bl_idname = 'SvMegapolisPandasFilter'
    bl_label = 'Pandas Filter'
    bl_icon = 'MESH_DATA'
    

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Dataframe")
        self.inputs.new('SvStringsSocket', "Filter")
        self.inputs.new('SvStringsSocket', "Value")

        #outputs
        self.outputs.new('SvStringsSocket', "Dataframe Output")

    def process(self):
        if not self.inputs["Dataframe"].is_linked or not self.inputs["Filter"].is_linked or not self.inputs["Value"].is_linked  :
            return
        self.df = self.inputs["Dataframe"].sv_get(deepcopy = False)
        self.filter = self.inputs["Filter"].sv_get(deepcopy = False)
        self.value = self.inputs["Value"].sv_get(deepcopy = False)
      
        filter = self.filter[0][0]
        value = self.value[0][0]

        data = df[df[filter] == value] 

        df_out = data

        #Output
        self.outputs["Pandas Series"].sv_set(df_out)

def register():
    if pd is not None:
        bpy.utils.register_class(SvMegapolisPandasFilter)

def unregister():
    if pd is not None:
        bpy.utils.unregister_class(SvMegapolisPandasFilter)
