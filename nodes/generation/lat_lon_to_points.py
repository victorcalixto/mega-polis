import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

#Megapolis Dependencies
from megapolis.dependencies import pyproj

try:
    from pyproj import CRS, Proj, transform
except:
    pass



class SvMegapolisLatLonToPoints(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: LatLonToPoints
    Tooltip: Lat-Lon To Points
    """
    bl_idname = 'SvMegapolisLatLonToPoints'
    bl_label = 'LatLonToPoints'
    bl_icon = 'MESH_DATA'
    
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self,context)
        
    projection: IntProperty(
        name="projection",
        description="CSR Projection Number",
        default=4236,
        update=update_sockets)
    

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Latitude")
        self.inputs.new('SvStringsSocket', "Longitude")
       

        #outputs
        self.outputs.new('SvStringsSocket', "Points")


    def draw_buttons(self,context, layout):
        layout.prop(self, 'projection')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        if not self.inputs["Latitude"].is_linked or not self.inputs["Longitude"].is_linked:
            return
        self.lat = self.inputs["Latitude"].sv_get(deepcopy = False)
        self.long = self.inputs["Longitude"].sv_get(deepcopy = False)
    

        lat = self.lat[0][0]
        lon = self.long[0][0]

        latlon = []

        if len(lat[0]) > 1:
            for i in range(0,len(lat[0])):
                latlon.append(list(zip(lon[0][i],lat[0][i])))
        else:
            latlon.append([lon,lat])

        coords = []

        in_latlon = CRS.from_proj4("+proj=latlon")
        out_proj = Proj(self.projection)

        if len(latlon) < 1:
            for i in latlon:
               x = i[0]
               y = i[1]
               x,y = transform(in_latlon,out_proj, y,x)
               z = 0
               coords.append([x,y,z])
        else:
            x,y = transform(in_latlon,out_proj, lon,lat)
            z = 0
            coords.append([x,y,z])

        points = [coords]

        #Outputs
        self.outputs["Points"].sv_set(points)

def register():
    bpy.utils.register_class(SvMegapolisLatLonToPoints)

def unregister():
    bpy.utils.unregister_class(SvMegapolisLatLonToPoints)

