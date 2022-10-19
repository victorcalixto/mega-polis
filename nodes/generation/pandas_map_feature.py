import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy


#Megapolis Dependencies
from megapolis.dependencies import pandas as pd
import json 


if pd is None:
    add_dummy('SvMegapolisPandasMapFeature', 'Pandas Map Feature', 'pandas')
else:
    class SvMegapolisPandasMapFeature(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: PandasMapFeature
        Tooltip: Pandas Map Feature
        """
        bl_idname = 'SvMegapolisPandasMapFeature'
        bl_label = 'Pandas Map Feature'
        bl_icon = 'MESH_DATA'
        

        def sv_init(self, context):
            # inputs
            self.inputs.new('SvStringsSocket', "Dataframe")
            self.inputs.new('SvStringsSocket', "Feature")
            self.inputs.new('SvStringsSocket', "Dict Map Values")

            #outputs
            self.outputs.new('SvStringsSocket', "Dataframe Output")

        def process(self):
            if not self.inputs["Dataframe"].is_linked or not self.inputs["Feature"].is_linked or not self.inputs["Dict Map Values"].is_linked:
                return
            self.df = self.inputs["Dataframe"].sv_get(deepcopy = False)
            self.feature = self.inputs["Feature"].sv_get(deepcopy = False)
            self.dict = self.inputs["Dict Map Values"].sv_get(deepcopy = False)

            feature = self.feature[0][0]

            dict_map_values = self.dict[0][0]

            dictionary = json.loads(dict_map_values)

            data = df[feature].map(dictionary)

            df_mapped = data


            #Output
            self.outputs["Dataframe Output"].sv_set(df_mapped)

def register():
    if pd is not None:
        bpy.utils.register_class(SvMegapolisPandasMapFeature)

def unregister():
    if pd is not None:
        bpy.utils.unregister_class(SvMegapolisPandasMapFeature)
