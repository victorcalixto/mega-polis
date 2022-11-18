import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies


class SvMegapolisDashboardMap(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Dashboard Map
    Tooltip: Dashboard Map
    """
    bl_idname = 'SvMegapolisDashboardMap'
    bl_label = 'Dashboard Map'
    bl_icon = 'MESH_DATA'

    
    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self,context)
    
    zoom: IntProperty(
        name="zoom",
        description="Zoom",
        default=10 ,
        update=update_sockets)
    
    #Blender Properties Buttons
    
    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Map Name")
        self.inputs.new('SvStringsSocket', "Map Coordinate X")
        self.inputs.new('SvStringsSocket', "Map Coordinate Y")

        #Outputs
        self.outputs.new('SvStringsSocket',"Dashboard Map")

    def draw_buttons(self,context, layout):
        layout.prop(self, 'zoom')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
    
        if not self.inputs["Map Name"].is_linked or not self.inputs["Map Coordinate X"].is_linked or not self.inputs["Map Coordinate Y"].is_linked :
            return
        self.mapname = self.inputs["Map Name"].sv_get(deepcopy = False)
        self.x = self.inputs["Map Coordinate X"].sv_get(deepcopy = False)
        self.y = self.inputs["Map Coordinate Y"].sv_get(deepcopy = False)


        map_name = self.mapname[0][0]
        map_centre_x = self.x[0][0]
        map_centre_y = self.y[0][0]
        zoom = self.zoom
        
        
        map_ = f"""
{map_name} = kepler.Map(center=[{map_centre_x}, {map_centre_y}], zoom={zoom}) \n\n
            """

        st_kepler_map_out = [map_] 

        ## Output

        self.outputs["Dashboard Map"].sv_set(st_kepler_map_out)


def register():
    bpy.utils.register_class(SvMegapolisDashboardMap)

def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardMap)
