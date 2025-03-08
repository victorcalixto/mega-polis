import bpy
from bpy.props import IntProperty
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


class SvMegapolisDashboardMap(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Dashboard Map
    Tooltip: Dashboard Map
    """
    bl_idname = 'SvMegapolisDashboardMap'
    bl_label = 'Dashboard Map'
    bl_icon = 'SEQ_PREVIEW'

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """Need to do UX transformation before updating node."""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self, context)

    zoom: IntProperty(
        name="zoom",
        description="Zoom",
        default=10,
        update=update_sockets)

    # Blender Properties Buttons
    def sv_init(self, context):
        # Inputs
        self.inputs.new('SvStringsSocket', "Map Name")
        self.inputs.new('SvStringsSocket', "Latitude")
        self.inputs.new('SvStringsSocket', "Longitude")

        # Outputs
        self.outputs.new('SvStringsSocket', "Dashboard Map")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'zoom')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        if not self.inputs["Map Name"].is_linked or not self.inputs["Latitude"].is_linked or not self.inputs["Longitude"].is_linked:
            return

        self.mapname = self.inputs["Map Name"].sv_get(deepcopy=False)
        self.lat = self.inputs["Latitude"].sv_get(deepcopy=False)
        self.lon = self.inputs["Longitude"].sv_get(deepcopy=False)

        map_name = self.mapname[0][0]
        map_centre_lat = self.lat[0][0]
        map_centre_lon = self.lon[0][0]
        zoom = self.zoom

        map_ = f"""
{map_name} = kepler.Map(center=[{map_centre_lat}, {map_centre_lon}], zoom={zoom})\n\n
        """

        st_kepler_map_out = [map_]

        # Output
        self.outputs["Dashboard Map"].sv_set(st_kepler_map_out)


def register():
    bpy.utils.register_class(SvMegapolisDashboardMap)


def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardMap)

