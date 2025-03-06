import bpy
from bpy.props import IntProperty
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from megapolis.dependencies import pyproj


class SvMegapolisPointToLatLon(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: PointToLatLon
    Tooltip: Converts projected points to Latitude/Longitude
    """
    bl_idname = 'SvMegapolisPointToLatLon'
    bl_label = 'Point to Latitude/Longitude'
    bl_icon = 'LATTICE_DATA'

    def update_sockets(self, context):
        """ UX transformation before updating node """
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self, context)

    projection_in: IntProperty(
        name="Projection In",
        description="CSR Projection Number (input)",
        default=4236,
        update=update_sockets
    )

    projection_out: IntProperty(
        name="Projection Out",
        description="CSR Projection Number (output)",
        default=4326,
        update=update_sockets
    )

    def sv_init(self, context):
        """ Initialize inputs and outputs """
        self.inputs.new('SvVerticesSocket', "Vertices")
        self.outputs.new('SvStringsSocket', "Latitude")
        self.outputs.new('SvStringsSocket', "Longitude")

    def draw_buttons(self, context, layout):
        """ Draw buttons for input projections """
        layout.prop(self, 'projection_in')
        layout.prop(self, 'projection_out')

    def draw_buttons_ext(self, context, layout):
        """ Extend buttons layout """
        self.draw_buttons(context, layout)

    def process(self):
        """ Process the conversion from projected coordinates to lat/lon """
        if not self.inputs["Vertices"].is_linked:
            return

        vertices = self.inputs["Vertices"].sv_get(deepcopy=False)
        
        # Get input and output projections
        in_proj = self.projection_in
        out_proj = self.projection_out

        # Extract x, y coordinates from vertices
        x = vertices[0][0][0]
        y = vertices[0][0][1]

        # Initialize pyproj transformer
        transformer = pyproj.Transformer.from_proj(
            pyproj.Proj(init=f'epsg:{in_proj}'),
            pyproj.Proj(init=f'epsg:{out_proj}')
        )

        # Transform coordinates
        x2, y2 = transformer.transform(x, y)

        # Prepare latitude and longitude for output
        longitude = [[x2]]
        latitude = [[y2]]

        # Output latitude and longitude
        self.outputs["Latitude"].sv_set(latitude)
        self.outputs["Longitude"].sv_set(longitude)


def register():
    bpy.utils.register_class(SvMegapolisPointToLatLon)


def unregister():
    bpy.utils.unregister_class(SvMegapolisPointToLatLon)

