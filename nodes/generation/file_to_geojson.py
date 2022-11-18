import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import geopandas as gpd
import json

class SvMegapolisFileToGeoJson(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: FileToGeoJson
    Tooltip: File To GeoJson
    """
    bl_idname = 'SvMegapolisFileToGeoJson'
    bl_label = 'File To GeoJson'
    bl_icon = 'MESH_DATA'
    sv_dependencies = {'geopandas'}

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
    bpy.utils.register_class(SvMegapolisFileToGeoJson)


def unregister():
    bpy.utils.unregister_class(SvMegapolisFileToGeoJson)
