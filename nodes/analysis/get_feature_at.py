import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import pandas as pd

class SvMegapolisGetFeatureAt(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Correlation Matrix
    Tooltip: Get a Feture From a Dataframe at X and y features 
    """
    bl_idname = 'SvMegapolisGetFeatureAt'
    bl_label = 'Get Feature At'
    bl_icon = 'MESH_DATA'
    sv_dependencies = {'pandas'}

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Dataframe")
        self.inputs.new('SvStringsSocket', "Feature X")
        self.inputs.new('SvStringsSocket', "Feature y")
       
        #outputs
        self.outputs.new('SvStringsSocket', "Feature Out")

    def process(self):
        if not self.inputs["Dataframe"].is_linked or not self.inputs["Feature X"].is_linked or not self.inputs["Feature y"].is_linked:
            return
        self.dataframe = self.inputs["Dataframe"].sv_get(deepcopy = False)
        self.feature_x = self.inputs["Feature X"].sv_get(deepcopy = False)
        self.feature_y = self.inputs["Feature y"].sv_get(deepcopy = False)
      
        df = self.dataframe
        index_feature_x= self.feature_x[0][0]
        index_feature_y = self.feature_y[0][0]

        at = df.at[index_feature_x,index_feature_y]

        corr_at  = [at]
        
        #Outputs

        self.outputs["Feature Out"].sv_set(corr_at)


def register():
    bpy.utils.register_class(SvMegapolisGetFeatureAt)


def unregister():
    bpy.utils.unregister_class(SvMegapolisGetFeatureAt)
