import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy


#Megapolis Dependencies
from megapolis.dependencies import pandas as pd


if pd is None:
    add_dummy('SvMegapolisPandasSeries', 'Pandas Series', 'pandas')
else:
    class SvMegapolisPandasSeries(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: Pandas Series
        Tooltip: Creates a Pandas Series from a list
        """
        bl_idname = 'SvMegapolisPandasSeries'
        bl_label = 'Pandas Series'
        bl_icon = 'MESH_DATA'
        

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
    if pd is not None:
        bpy.utils.register_class(SvMegapolisPandasSeries)

def unregister():
    if pd is not None:
        bpy.utils.unregister_class(SvMegapolisPandasSeries)
