import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy


#Megapolis Dependencies
from megapolis.dependencies import pandas as pd
import csv


if pd is None:
    add_dummy('SvMegapolisReadCsv', 'Read CSV', 'pandas')
else:
    class SvMegapolisReadCsv(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: Read CSV
        Tooltip: Read CSV file
        """
        bl_idname = 'SvMegapolisReadCsv'
        bl_label = 'Read CSV'
        bl_icon = 'MESH_DATA'
        

        def sv_init(self, context):
            # inputs
            self.inputs.new('SvFilePathSocket', "Path")
           
            #outputs
            self.outputs.new('SvStringsSocket', "CSV List")
            self.outputs.new('SvStringsSocket', "CSV Dict")
            self.outputs.new('SvStringsSocket', "CSV DF")

        def process(self):
            if not self.inputs["Path"].is_linked:
                return
            self.path = self.inputs["Path"].sv_get(deepcopy = False)
          
            file_name = self.path[0][0]

            csv_list = []
            csv_dict  = []


            with open(file_name , mode ='r') as file:
                csvFile = csv.reader(file)
                csvFileDict = csv.DictReader(file)
                for lines in csvFile:
                    csv_list.append(lines)
                for i in csvFileDict:
                    csv_dict.append(i)

            with open(file_name , mode ='r') as file:
                csvFileDict = csv.DictReader(file)
                for i in csvFileDict:
                    csv_dict.append(i)



            df = pd.read_csv(file_name)

            csv_pandas_dataframe = df
            
            self.outputs["CSV List"].sv_set(csv_list)
            self.outputs["CSV Dict"].sv_set(csv_dict)
            self.outputs["CSV DF"].sv_set(df)

def register():
    if pd is not None:
        bpy.utils.register_class(SvMegapolisReadCsv)

def unregister():
    if pd is not None:
        bpy.utils.unregister_class(SvMegapolisReadCsv)
