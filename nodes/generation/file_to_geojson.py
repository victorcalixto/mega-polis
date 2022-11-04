import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy


#Megapolis Dependencies
from megapolis.dependencies import geopandas as gpd
import json

if gpd is None:
    add_dummy('SvMegapolisFileToGeoJson', 'File To GeoJson', 'geopandas')
else:
    class SvMegapolisFileToGeoJson(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: FileToGeoJson
        Tooltip: File To GeoJson
        """
        bl_idname = 'SvMegapolisFileToGeoJson'
        bl_label = 'File To GeoJson'
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

            geojson= df.to_json()

            geojson=json.dumps(geojson).replace("null", "None")

            geojson_out = geojson

            #Output
            self.outputs["GeoDataframe Output"].sv_set(geojson_out)

def register():
    if gpd is not None:
        bpy.utils.register_class(SvMegapolisFileToGeoJson)

def unregister():
    if gpd is not None:
        bpy.utils.unregister_class(SvMegapolisFileToGeoJson)
