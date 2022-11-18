import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import pandas as pd
import json


class SvMegapolisReadJson(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Read JSON
    Tooltip: Read JSON file
    """
    bl_idname = 'SvMegapolisReadJson'
    bl_label = 'Read JSON'
    bl_icon = 'MESH_DATA'
    

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvFilePathSocket', "Path")
       
        #outputs
        self.outputs.new('SvStringsSocket', "JSON Data")
        self.outputs.new('SvStringsSocket', "JSON DF")

    def process(self):
        if not self.inputs["Path"].is_linked:
            return
        self.path = self.inputs["Path"].sv_get(deepcopy = False)
      
        file_name = self.path[0][0]
        
        # Opening JSON file

        with open(file_name) as f:
           data = json.load(f)



        df = pd.read_json(file_name)


        json_pandas_dataframe = df


        json_data = data

        self.outputs["JSON Data"].sv_set(data)
        self.outputs["JSON DF"].sv_set(df)

def register():
    if pd is not None:
        bpy.utils.register_class(SvMegapolisReadJson)

def unregister():
    if pd is not None:
        bpy.utils.unregister_class(SvMegapolisReadJson)
