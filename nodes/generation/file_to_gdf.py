import bpy
from sverchok.node_tree import SverchCustomTreeNode

# Megapolis Dependencies
from megapolis.dependencies import geopandas as gpd


class SvMegapolisFileToGdf(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: FileToGdf
    Tooltip: File To Gdf
    """
    bl_idname = 'SvMegapolisFileToGdf'
    bl_label = 'File To Gdf'
    bl_icon = 'WORDWRAP_ON'
    sv_dependencies = {'geopandas'}

    def sv_init(self, context):
        """ Initialize inputs and outputs """
        # Inputs
        self.inputs.new('SvFilePathSocket', "File")

        # Outputs
        self.outputs.new('SvStringsSocket', "GeoDataframe Output")

    def process(self):
        """ Process the file and convert it to a GeoDataFrame """
        if not self.inputs["File"].is_linked:
            return

        # Get the input file path
        self.file = self.inputs["File"].sv_get(deepcopy=False)
        file = self.file[0][0]

        # Read the file as a GeoDataFrame
        gdf = gpd.read_file(file)

        # Output the GeoDataFrame
        self.outputs["GeoDataframe Output"].sv_set([gdf])


def register():
    bpy.utils.register_class(SvMegapolisFileToGdf)


def unregister():
    bpy.utils.unregister_class(SvMegapolisFileToGdf)

