import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
import json

class SvMegapolisDashboardGeojsonToMap(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Dashboard Geojson To Map
    Tooltip: Dashboard Geojson to Map
    """
    bl_idname = 'SvMegapolisDashboardGeojsonToMap'
    bl_label = 'Dashboard Geojson To Map'
    bl_icon = 'MESH_DATA'

    
    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self,context)
    
   
    #Blender Properties Buttons
    
    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Map Name")
        self.inputs.new('SvStringsSocket', "GeoJson")


        #Outputs
        self.outputs.new('SvStringsSocket',"Dashboard GeoJson")

    def process(self):
    
        if not self.inputs["Map Name"].is_linked or not self.inputs["GeoJson"].is_linked: 
            return
        self.mapname = self.inputs["Map Name"].sv_get(deepcopy = False)
        self.geojson = self.inputs["GeoJson"].sv_get(deepcopy = False)
        
        map_name=self.mapname[0][0]
        geojson_in =self.geojson
        geomap = json.loads(geojson_in)

        load = f"""
{map_name}.add_geojson({geomap})\n
            """

        load_geo=load

        ## Output

        self.outputs["Dashboard GeoJson"].sv_set(load_geo)

def register():
    bpy.utils.register_class(SvMegapolisDashboardGeojsonToMap)

def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardGeojsonToMap)
