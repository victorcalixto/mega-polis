import bpy
from bpy.props import IntProperty, EnumProperty
from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

# Megapolis Dependencies
try:
    from megapolis.dependencies import osmnx as ox
except ImportError:
    ox = None  

try:
    from shapely.geometry import mapping
except ImportError:
    mapping = None

import itertools

# Define network types
NetworkType = namedtuple("NetworkType", ["all", "bike", "drive", "drive_service", "walk"])
NETWORK_TYPE = NetworkType("all", "bike", "drive", "drive_service", "walk")
network_type_items = [(i, i, "") for i in NETWORK_TYPE]

##### Utility Functions #####

def chunk(iterable, size):
    """Splits an iterable into fixed-size chunks."""
    iterator = iter(iterable)
    return iter(lambda: tuple(itertools.islice(iterator, size)), ())

def shift(seq, n=0):
    """Shifts a sequence cyclically by n places."""
    a = n % len(seq)
    return seq[-a:] + seq[:-a]

def get_gdf_geometry(gdf_geometry, gdf_mapping, geometry_type):
    """Extracts geometries of a specific type from a GeoDataFrame."""
    return [
        gdf_mapping["features"][i]["geometry"]["coordinates"]
        for i in range(len(gdf_geometry))
        if gdf_mapping["features"][i]["geometry"]["type"] == geometry_type
    ]

def get_gdf_features(gdf_geometry, gdf_mapping, features, geometry_type):
    """Extracts feature properties for a specific geometry type."""
    return [
        features["features"][i]
        for i in range(len(gdf_geometry))
        if gdf_mapping["features"][i]["geometry"]["type"] == geometry_type
    ]


##### Main Node Class #####

class SvMegapolisLoadStreetNetwork(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Load Street Network
    Tooltip: Loads a street network based on an address.
    """
    bl_idname = "SvMegapolisLoadStreetNetwork"
    bl_label = "Load Street Network"
    bl_icon = "MOD_MULTIRES"
    sv_dependencies = {"osmnx"}

    def update_sockets(self, context):
        """Handles UX updates before updating node."""
        updateNode(self, context)

    # Blender Properties Buttons
    projection: IntProperty(
        name="Projection",
        description="CRS Projection Number",
        default=4236,
        update=update_sockets
    )
    
    network_type: EnumProperty(
        name="Network Type",
        items=network_type_items,
        default="drive",
        description="Choose Network Type",
        update=update_sockets
    )
    
    distance: IntProperty(
        name="Distance",
        description="Search radius (in meters)",
        default=1000,
        update=update_sockets
    )

    def sv_init(self, context):
        """Initializes input and output sockets."""
        self.inputs.new("SvStringsSocket", "Address")

        self.outputs.new("SvVerticesSocket", "Nodes")
        self.outputs.new("SvStringsSocket", "Nodes_ID")
        self.outputs.new("SvStringsSocket", "Nodes_Keys")
        self.outputs.new("SvStringsSocket", "Nodes_Values")

        self.outputs.new("SvVerticesSocket", "Edges_Verts")
        self.outputs.new("SvStringsSocket", "Edges")
        self.outputs.new("SvStringsSocket", "Edges_ID")
        self.outputs.new("SvStringsSocket", "Edges_Keys")
        self.outputs.new("SvStringsSocket", "Edges_Values")

        self.outputs.new("SvStringsSocket", "DF")
        self.outputs.new("SvStringsSocket", "Network")

    def draw_buttons(self, context, layout):
        """Draws UI buttons in the Blender panel."""
        layout.prop(self, "projection")
        layout.prop(self, "network_type", expand=True)
        layout.prop(self, "distance")

    def draw_buttons_ext(self, context, layout):
        """Extends UI layout."""
        self.draw_buttons(context, layout)

    def process(self):
        """Processes the node and retrieves OSM street network data."""
        if not self.inputs["Address"].is_linked or ox is None:
            return
        
        address = str(self.inputs["Address"].sv_get(deepcopy=False)[0][0])
        distance = self.distance

        # Load street network
        G = ox.graph_from_address(address, dist=distance, network_type=self.network_type)
        G = ox.projection.project_graph(G, to_crs=self.projection)

        # Convert to GeoDataFrames
        gdf_nodes, gdf_edges = ox.convert.graph_to_gdfs(G, nodes=True, edges=True, node_geometry=True, fill_edge_geometry=True)

        # Process nodes
        gdf_mapping_nodes = mapping(gdf_nodes)
        points = get_gdf_geometry(gdf_nodes["geometry"], gdf_mapping_nodes, "Point")
        points_features = get_gdf_features(gdf_nodes["geometry"], gdf_mapping_nodes, mapping(gdf_nodes), "Point")

        points_verts = [[i + (0,)] for i in points]
        points_id = [i["id"] for i in points_features]
        points_keys = [list(i["properties"].keys()) for i in points_features]
        points_values = [list(i["properties"].values()) for i in points_features]

        # Process edges
        gdf_mapping_edges = mapping(gdf_edges)
        linestrings = get_gdf_geometry(gdf_edges["geometry"], gdf_mapping_edges, "LineString")
        linestrings_features = get_gdf_features(gdf_edges["geometry"], gdf_mapping_edges, mapping(gdf_edges), "LineString")

        edges_verts = [[tuple(i) + (0,) for i in line] for line in linestrings]
        edges_id = [i["id"] for i in linestrings_features]
        edges_keys = [list(i["properties"].keys()) for i in linestrings_features]
        edges_values = [list(i["properties"].values()) for i in linestrings_features]

        edges = [list(zip(verts[:-1], verts[1:])) for verts in edges_verts]

        # Output results
        self.outputs["Nodes"].sv_set(points_verts)
        self.outputs["Nodes_ID"].sv_set(points_id)
        self.outputs["Nodes_Keys"].sv_set(points_keys)
        self.outputs["Nodes_Values"].sv_set(points_values)

        self.outputs["Edges_Verts"].sv_set(edges_verts)
        self.outputs["Edges"].sv_set(edges)
        self.outputs["Edges_ID"].sv_set(edges_id)
        self.outputs["Edges_Keys"].sv_set(edges_keys)
        self.outputs["Edges_Values"].sv_set(edges_values)

        self.outputs["DF"].sv_set((gdf_nodes, gdf_edges))
        self.outputs["Network"].sv_set(G)


def register():
    bpy.utils.register_class(SvMegapolisLoadStreetNetwork)


def unregister():
    bpy.utils.unregister_class(SvMegapolisLoadStreetNetwork)

