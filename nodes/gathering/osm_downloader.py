import bpy
import re
from bpy.props import BoolProperty, EnumProperty
from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from megapolis.dependencies import osmnx as ox

DownloadMethod = namedtuple('DownloadMethod', ['Address', 'Place', 'Point', 'Bbox'])
DOWNLOAD_METHOD = DownloadMethod('Address', 'Place', 'Point', 'Bbox')
download_method_items = [(i, i, '') for i in DOWNLOAD_METHOD]

Features = namedtuple(
    'Features', [
        'aerialway', 'aeroway', 'amenity', 'barrier', 'boundary', 'building',
        'craft', 'emergency', 'geological', 'healthcare', 'highway', 'historic',
        'landuse', 'leisure', 'man_made', 'military', 'natural', 'office',
        'place', 'power', 'public_transport', 'railway', 'route', 'sport',
        'telecom', 'tourism', 'water', 'waterway', 'additional_properties',
        'annotations', 'name', 'properties', 'references', 'restrictions'
    ]
)
FEATURES = Features(*Features._fields)
features_items = [(i, i, '') for i in FEATURES]


def get_buildings_types(buildings):
    """Return a list of building types for OSM downloader."""
    return buildings.loc[:, buildings.columns.str.contains(
        'building|geometry|addr:|amenity|operator|name|historic|brand|cuisine|'
        'delivery|drive|internet|opening|outdoor|smoking|takeway|website|'
        'layer|source|shop|tourism|wheelchair|office|information|roof|'
        'emergency|man|access|parking|fixme|construction|toilets|denomination|'
        'religion|height|wikidata|leisure|area|healthcare|levels|diet|email|'
        'description|note|old_name|type'
    )]


class SvMegapolisOSMDownloader(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: OSM Downloader
    Tooltip: Download an OpenStreetMap file.
    """
    bl_idname = 'SvMegapolisOSMDownloader'
    bl_label = 'OSM Downloader'
    bl_icon = 'URL'
    sv_dependencies = {'osmnx'}

    def update_sockets(self, context):
        """Update node sockets based on the selected download method."""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        hide_map = {
            DOWNLOAD_METHOD.Address: ['Place', 'Coordinate_X', 'Coordinate_Y', 'North', 'South', 'East', 'West'],
            DOWNLOAD_METHOD.Place: ['Address', 'Distance', 'Coordinate_X', 'Coordinate_Y', 'North', 'South', 'East', 'West'],
            DOWNLOAD_METHOD.Point: ['Address', 'Place', 'North', 'South', 'East', 'West'],
            DOWNLOAD_METHOD.Bbox: ['Address', 'Place', 'Coordinate_X', 'Coordinate_Y', 'Distance']
        }

        for sock in self.inputs:
            set_hide(sock, sock.name in hide_map.get(self.download_method, []))

        updateNode(self, context)

    download: BoolProperty(
        name="download",
        description="Run the node to download",
        default=False,
        update=update_sockets
    )

    download_method: EnumProperty(
        name='download_method',
        items=download_method_items,
        default="Address",
        description='Choose an OSM Download Method',
        update=update_sockets
    )

    features: EnumProperty(
        name='features',
        items=features_items,
        default="building",
        description='Choose a feature to download',
        update=update_sockets
    )

    def sv_init(self, context):
        """Initialize node inputs and outputs."""
        inputs = [
            "Address", "Place", "Coordinate_X", "Coordinate_Y",
            "North", "South", "East", "West", "Distance", "Folder"
        ]

        for input_name in inputs:
            self.inputs.new('SvStringsSocket', input_name)
            self.inputs[input_name].hide_safe = True

        self.outputs.new('SvStringsSocket', "Output_Message")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'download')
        layout.prop(self, 'download_method', expand=True)
        layout.prop(self, 'features')

    def process(self):
        """Process node execution."""
        if self.download:
            folder = self.inputs["Folder"].sv_get(deepcopy=False)[0][0]
            query_param = None

            if self.download_method == DOWNLOAD_METHOD.Address:
                query_param = self.inputs["Address"].sv_get(deepcopy=False)[0][0]
                distance = self.inputs["Distance"].sv_get(deepcopy=False)[0][0]
                buildings = ox.features.features_from_address(query_param, {self.features: True}, distance)

            elif self.download_method == DOWNLOAD_METHOD.Place:
                query_param = self.inputs["Place"].sv_get(deepcopy=False)[0][0]
                buildings = ox.features.features_from_place(query_param, {self.features: True})

            elif self.download_method == DOWNLOAD_METHOD.Point:
                coord_x = float(self.inputs["Coordinate_X"].sv_get(deepcopy=False)[0][0])
                coord_y = float(self.inputs["Coordinate_Y"].sv_get(deepcopy=False)[0][0])
                distance = self.inputs["Distance"].sv_get(deepcopy=False)[0][0]
                buildings = ox.features.features_from_point((coord_x, coord_y), {self.features: True}, distance)

            else:
                north, south, east, west = [
                    float(self.inputs[dim].sv_get(deepcopy=False)[0][0])
                    for dim in ["North", "South", "East", "West"]
                ]
                buildings = ox.features.features_from_bbox(north, south, east, west, {self.features: True})

            buildings = get_buildings_types(buildings)
            filename = re.sub('[^A-Za-z0-9]+', ' ', f"{query_param}_{self.features}.geojson")
            buildings.to_file(f"{folder}{filename}", driver="GeoJSON")

        self.outputs["Output_Message"].sv_set(buildings)


def register():
    bpy.utils.register_class(SvMegapolisOSMDownloader)


def unregister():
    bpy.utils.unregister_class(SvMegapolisOSMDownloader)

