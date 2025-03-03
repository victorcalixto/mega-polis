import bpy
import csv
import pandas as pd  # Corrected the import statement as per PEP8

# Megapolis Dependencies
from sverchok.node_tree import SverchCustomTreeNode


class SvMegapolisReadCsv(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Read CSV
    Tooltip: Read CSV file
    """
    bl_idname = 'SvMegapolisReadCsv'
    bl_label = 'Read CSV'
    bl_icon = 'FILE_TEXT'
    sv_dependencies = {'pandas'}

    def sv_init(self, context):
        """Initialize the inputs and outputs for the node."""
        # Inputs
        self.inputs.new('SvFilePathSocket', "Path")
        
        # Outputs
        self.outputs.new('SvStringsSocket', "CSV List")
        self.outputs.new('SvStringsSocket', "CSV Dict")
        self.outputs.new('SvStringsSocket', "CSV DF")

    def process(self):
        """Process the CSV file and set the outputs."""
        if not self.inputs["Path"].is_linked:
            return

        self.path = self.inputs["Path"].sv_get(deepcopy=False)
        file_name = self.path[0][0]

        csv_list = []
        csv_dict = []

        # Read CSV using the csv.reader and csv.DictReader
        with open(file_name, mode='r') as file:
            csv_file = csv.reader(file)
            csv_file_dict = csv.DictReader(file)
            
            # Populate csv_list and csv_dict
            for line in csv_file:
                csv_list.append(line)
            for row in csv_file_dict:
                csv_dict.append(row)

        # Using pandas to read the CSV file into a DataFrame
        df = pd.read_csv(file_name)

        # Set outputs
        self.outputs["CSV List"].sv_set(csv_list)
        self.outputs["CSV Dict"].sv_set(csv_dict)
        self.outputs["CSV DF"].sv_set(df)


def register():
    """Register the custom node class."""
    bpy.utils.register_class(SvMegapolisReadCsv)


def unregister():
    """Unregister the custom node class."""
    bpy.utils.unregister_class(SvMegapolisReadCsv)

