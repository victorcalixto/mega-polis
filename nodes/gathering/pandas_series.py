import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import pandas as pd


class SvMegapolisPandasSeries(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Pandas Series
    Tooltip: Creates a Pandas Series from a list
    """
    bl_idname = 'SvMegapolisPandasSeries'
    bl_label = 'Pandas Series'
    bl_icon = 'MESH_DATA'
    sv_dependencies = {'pandas'}

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "List")
       
        #outputs
        self.outputs.new('SvStringsSocket', "Pandas Series")

    def process(self):
        if not self.inputs["List"].is_linked:
            return
        self.list = self.inputs["List"].sv_get(deepcopy = False)
      
        list_p = self.list[0]
        pd_list = pd.Series(list_p)
        pd_series = [pd_list] 
        
        self.outputs["Pandas Series"].sv_set(pd_series)


def register():
    bpy.utils.register_class(SvMegapolisPandasSeries)


def unregister():
    bpy.utils.unregister_class(SvMegapolisPandasSeries)
