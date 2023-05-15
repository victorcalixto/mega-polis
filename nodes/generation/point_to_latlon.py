import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

from megapolis.dependencies import pyproj

class SvMegapolisPointToLatLon(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: PointToLatLon
    Tooltip: Point to Lan/Lon
    """
    bl_idname = 'SvMegapolisPointToLatLon'
    bl_label = 'Point to Latitude/Longitude'
    bl_icon = 'MESH_DATA'
    
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self,context)
        
    projection_in: IntProperty(
        name="projectionIn",
        description="CSR Projection Number",
        default=4236,
        update=update_sockets)
    
    projection_out: IntProperty(
        name="projectionOut",
        description="CSR Projection Number",
        default=4236,
        update=update_sockets)

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvVerticesSocket', "Vertices")

        #outputs
        self.outputs.new('SvStringsSocket', "Latitude")
        self.outputs.new('SvStringsSocket', "Longitude")
     
    def draw_buttons(self,context, layout):
        layout.prop(self, 'projection_in')
        layout.prop(self, 'projection_out')


    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)


    def process(self):
        if not self.inputs["Vertices"].is_linked:
            return
        self.vertices = self.inputs["Vertices"].sv_get(deepcopy = False)
      
        in_proj= self.projection_in 

        out_proj= self.projection_out

        x = self.vertices[0][0][0]
        y = self.vertices[0][0][1] 

        inProj = pyproj.Proj(init=f'epsg:{in_proj}')
        outProj = pyproj.Proj(init=f'epsg:{out_proj}')

        x2,y2 = pyproj.transform(inProj,outProj,x,y)

        longitude = [[x2]]
        latitude = [[y2]]

        #Outputs       
        self.outputs["Latitude"].sv_set(latitude)
        self.outputs["Longitude"].sv_set(latitude)


def register():
    bpy.utils.register_class(SvMegapolisPointToLatLon)

def unregister():
    bpy.utils.unregister_class(SvMegapolisPointToLatLon)
