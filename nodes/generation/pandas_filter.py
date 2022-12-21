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
    sv_dependencies = {'pandas'}

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Dataframe")
        self.inputs.new('SvStringsSocket', "Filter")

        #outputs
        self.outputs.new('SvStringsSocket', "Dataframe Output")

    def process(self):
        if not self.inputs["Dataframe"].is_linked or not self.inputs["Filter"].is_linked:
            return
        self.df = self.inputs["Dataframe"].sv_get(deepcopy = False)
        self.filter = self.inputs["Filter"].sv_get(deepcopy = False)
        
        filters = self.filter[0][0].split(',')
        df_out = self.df.filter(items=filters)

        #Output
        self.outputs["Dataframe Output"].sv_set(df_out)


def register():
    bpy.utils.register_class(SvMegapolisPandasFilter)


def unregister():
    bpy.utils.unregister_class(SvMegapolisPandasFilter)
