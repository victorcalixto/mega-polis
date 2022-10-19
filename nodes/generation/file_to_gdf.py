import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy


#Megapolis Dependencies
from megapolis.dependencies import geopandas as gpd



if gpd is None:
    add_dummy('SvMegapolisFileToGdf', 'File To Gdf', 'geopandas')
else:
    class SvMegapolisFileToGdf(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: FileToGdf
        Tooltip: File To Gdf
        """
        bl_idname = 'SvMegapolisFileToGdf'
        bl_label = 'File To Gdf'
        bl_icon = 'MESH_DATA'
        

        def sv_init(self, context):
            # inputs
            self.inputs.new('SvFilePathSocket', "File")

            #outputs
            self.outputs.new('SvStringsSocket', "GeoDataframe Output")

        def process(self):
            if not self.inputs["File"].is_linked:
                return
            self.file = self.inputs["File"].sv_get(deepcopy = False)

            file=self.file[0][0]

            df = gpd.read_file(file)  

            gdf_out = [df]

            #Output
            self.outputs["GeoDataframe Output"].sv_set(gdf_out)

def register():
    if gpd is not None:
        bpy.utils.register_class(SvMegapolisFileToGdf)

def unregister():
    if gpd is not None:
        bpy.utils.unregister_class(SvMegapolisFileToGdf)
