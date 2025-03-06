import bpy
from bpy.props import IntProperty
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

try:
    from pyproj import CRS, Proj, transform
except ImportError:
    print("pyproj not found. Projection transformations will not work.")

class SvMegapolisLatLonToPoints(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: LatLonToPoints
    Tooltip: Converts Latitude and Longitude to projected points
    """
    bl_idname = 'SvMegapolisLatLonToPoints'
    bl_label = 'LatLonToPoints'
    bl_icon = 'WORLD'

    def update_sockets(self, context):
        """ UX transformation before updating node """
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self, context)


    projection: IntProperty(
        name="Projection",
        description="CSR Projection Number",
        default=4236,
        update=update_sockets)

    def sv_init(self, context):
        """ Initialize node inputs and outputs """
        # Inputs
        self.inputs.new('SvStringsSocket', "Latitude")
        self.inputs.new('SvStringsSocket', "Longitude")
        
        # Outputs
        self.outputs.new('SvStringsSocket', "Points")

    def draw_buttons(self, context, layout):
        """ Draw node interface buttons """
        layout.prop(self, 'projection')

    def draw_buttons_ext(self, context, layout):
        """ Extends buttons layout """
        self.draw_buttons(context, layout)

    def process(self):
        """ Process the input latitude and longitude and convert to points """
        if not self.inputs["Latitude"].is_linked or not self.inputs["Longitude"].is_linked:
            return

        lat = self.inputs["Latitude"].sv_get(deepcopy=False)
        lon = self.inputs["Longitude"].sv_get(deepcopy=False)

        lat_lon = []

        # Handle lat, lon as lists
        if len(lat[0]) > 1:
            lat_lon.extend([list(zip(lon[0][i], lat[0][i])) for i in range(len(lat[0]))])
        else:
            lat_lon.append([lon, lat])

        coords = []

        # Define CRS and projections
        in_latlon = CRS.from_proj4("+proj=latlon")
        out_proj = Proj(self.projection)

        if len(lat_lon) < 1:
            x, y = transform(in_latlon, out_proj, lon, lat)
            coords.append([x, y, 0])
        else:
            coords = [
                [transform(in_latlon, out_proj, i[1], i[0])[0], transform(in_latlon, out_proj, i[1], i[0])[1], 0]
                for i in lat_lon
            ]

        points = [coords]

        # Set output points
        self.outputs["Points"].sv_set(points)

def register():
    bpy.utils.register_class(SvMegapolisLatLonToPoints)

def unregister():
    bpy.utils.unregister_class(SvMegapolisLatLonToPoints)

