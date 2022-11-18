import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import pandas as pd


class SvMegapolisCsvToDataframe(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: CsvToDataframe
    Tooltip: Creates a Dataframe from Csv File
    """
    bl_idname = 'SvMegapolisCsvToDataframe'
    bl_label = 'CsvToDataframe'
    bl_icon = 'MESH_DATA'
    
    def sv_init(self, context):
        # inputs
        self.inputs.new('SvFilePathSocket', "File")

        #outputs
        self.outputs.new('SvStringsSocket', "Dataframe Output")

    def process(self):
        if not self.inputs["File"].is_linked:
            return
        self.file = self.inputs["File"].sv_get(deepcopy = False)



        csv = self.file[0][0]

        data = pd.read_csv(csv)

        df = data

        #Output
        self.outputs["Dataframe Output"].sv_set(df)

def register():
    if pd is not None:
        bpy.utils.register_class(SvMegapolisCsvToDataframe)

def unregister():
    if pd is not None:
        bpy.utils.unregister_class(SvMegapolisCsvToDataframe)
