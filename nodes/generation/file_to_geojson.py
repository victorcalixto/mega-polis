import bpy
import json
from sverchok.node_tree import SverchCustomTreeNode
from megapolis.dependencies import geopandas as gpd


class SvMegapolisFileToGeoJson(SverchCustomTreeNode, bpy.types.Node):
    
    """
    Triggers: FileToGeoJson
    Tooltip: File To GeoJson
    """
    
    bl_idname = "SvMegapolisFileToGeoJson"
    bl_label = "File To GeoJson"
    bl_icon = "KEY_MENU"
    sv_dependencies = {"geopandas"}

    def sv_init(self, context):
        """Initialize node inputs and outputs."""
        self.inputs.new("SvFilePathSocket", "File")
        self.outputs.new("SvStringsSocket", "GeoDataframe Output")

    def process(self):
        """Process the input file and convert it to GeoJSON."""
        if not self.inputs["File"].is_linked:
            return

        file_path = self.inputs["File"].sv_get(deepcopy=False)[0][0]
        df = gpd.read_file(file_path)
        
        geojson = json.dumps(df.to_json()).replace("null", "None")
        
        self.outputs["GeoDataframe Output"].sv_set(geojson)


def register():
    bpy.utils.register_class(SvMegapolisFileToGeoJson)


def unregister():
    bpy.utils.unregister_class(SvMegapolisFileToGeoJson)

