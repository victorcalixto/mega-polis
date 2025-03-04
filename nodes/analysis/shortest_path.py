import bpy
from bpy.props import IntProperty, EnumProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

# Megapolis Dependencies
from megapolis.dependencies import osmnx as ox


def sum_of_list(lst, size):
    if size == 0:
        return 0
    else:
        return lst[size - 1] + sum_of_list(lst, size - 1)


PathType = namedtuple('PathType', ['length', 'travel_time'])
PATHTYPE = PathType('length', 'travel_time')
pathtype_items = [(i, i, '') for i in PATHTYPE]


class SvMegapolisShortestPath(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Shortest Path
    Tooltip: Provides shortest path between two points based on length or time travel
    """
    bl_idname = 'SvMegapolisShortestPath'
    bl_label = 'Shortest Path'
    bl_icon = 'TRACKING'
    sv_dependencies = {'osmnx', 'networkx'}

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """Need to do UX transformation before updating node."""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status
        updateNode(self, context)

    # Blender Properties Buttons
    pathtype: EnumProperty(
        name='Method', items=pathtype_items,
        default="length",
        description='Choose the method to calculate the shortest path', 
        update=update_sockets
    )

    residential: IntProperty(
        name='Residential St. max. Speed',
        default=35,
        description='Choose a max speed for residential streets', 
        update=update_sockets
    )

    secondary: IntProperty(
        name='Secondary St. max. Speed',
        default=50,
        description='Choose a max speed for secondary streets', 
        update=update_sockets
    )

    tertiary: IntProperty(
        name='Tertiary St. max. Speed',
        default=60,
        description='Choose a max speed for tertiary streets', 
        update=update_sockets
    )

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Nx Graph")
        self.inputs.new('SvVerticesSocket', "Origin")
        self.inputs.new('SvVerticesSocket', "Destination")

        # outputs
        self.outputs.new('SvStringsSocket', "Path ID")
        self.outputs.new('SvVerticesSocket', "Path")
        self.outputs.new('SvStringsSocket', "Path Edges")
        self.outputs.new('SvStringsSocket', "Time")
        self.outputs.new('SvStringsSocket', "Distance")
        self.outputs.new('SvStringsSocket', "Features")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'pathtype', expand=False)
        layout.prop(self, 'residential')
        layout.prop(self, 'secondary')
        layout.prop(self, 'tertiary')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        if not self.inputs["Origin"].is_linked or not self.inputs["Destination"].is_linked or not self.inputs["Nx Graph"].is_linked:
            return

        self.origin = self.inputs["Origin"].sv_get(deepcopy=False)
        self.destination = self.inputs["Destination"].sv_get(deepcopy=False)
        self.graph = self.inputs["Nx Graph"].sv_get(deepcopy=False)

        origin = self.origin[0][0]
        origin_x = origin[0]
        origin_y = origin[1]

        destination = self.destination[0][0]
        destination_x = destination[0]
        destination_y = destination[1]

        G = self.graph

        G = ox.add_edge_speeds(G)
        G = ox.add_edge_travel_times(G)
        hwy_speeds = {"residential": self.residential, "secondary": self.secondary, "tertiary": self.tertiary}
        G = ox.add_edge_speeds(G, hwy_speeds)
        G = ox.add_edge_travel_times(G)

        node_origin = ox.nearest_nodes(G, origin_x, origin_y)
        node_destination = ox.nearest_nodes(G, destination_x, destination_y)

        route = ox.shortest_path(G, node_origin, node_destination, weight=self.pathtype)

        attributes = ox.utils_graph.get_route_edge_attributes(G, route, attribute=None, minimize_key=self.pathtype, retrieve_default=None)
        travel_time = ox.utils_graph.get_route_edge_attributes(G, route, attribute='travel_time', minimize_key='travel_time', retrieve_default=None)
        edges_lengths = ox.utils_graph.get_route_edge_attributes(G, route, attribute='length', minimize_key='length', retrieve_default=None)

        total_time = sum_of_list(travel_time, len(travel_time))
        total_dist = sum_of_list(edges_lengths, len(edges_lengths))

        geometry_path = []

        for i in range(0, len(attributes)):
            try:
                geometry_path.append(attributes[i]['geometry'])
            except:
                continue

        geometries = [list(zip([i.coords[0][0]], [i.coords[0][1]], [0])) for i in geometry_path]
        geometries_f = [j for i in geometries for j in i]
        geometries_f.append(destination)

        edges_list = [i for i in range(0, len(geometries_f))]
        edges_list_shift = edges_list[1:] + edges_list[:1]
        edges_list_shift = edges_list_shift[:-1]

        edges = list(zip(edges_list, edges_list_shift))

        path_id = [route]
        path = [geometries_f]
        path_edges = [edges]
        features = [attributes]
        time = [total_time / 60, 'min']
        distance = [total_dist / 1000, 'km']

        # Output
        self.outputs["Path ID"].sv_set(path_id)
        self.outputs["Path"].sv_set(path)
        self.outputs["Path Edges"].sv_set(path_edges)
        self.outputs["Time"].sv_set(time)
        self.outputs["Distance"].sv_set(distance)
        self.outputs["Features"].sv_set(features)


def register():
    bpy.utils.register_class(SvMegapolisShortestPath)


def unregister():
    bpy.utils.unregister_class(SvMegapolisShortestPath)

