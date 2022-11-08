import bpy
from bpy.props import IntProperty, EnumProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import geopandas as gpd
from megapolis.dependencies import osmnx as ox
from shapely.geometry import shape, Polygon, Point, LineString, mapping
from itertools import islice 
import itertools


Network_type = namedtuple('NetworkType', ['all', 'bike','drive','drive_service','walk'])
NETWORKTYPE = Network_type('all', 'bike','drive','drive_service','walk')
networktype_items = [(i, i, '') for i in NETWORKTYPE]

class SvMegapolisLoadStreetNetwork(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Load Street Network
    Tooltip: Load Street Network
    """
    bl_idname = 'SvMegapolisLoadStreetNetwork'
    bl_label = 'Load Street Network'
    bl_icon = 'MESH_DATA'

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status
        updateNode(self,context)

    #Blender Properties Buttons

    projection: IntProperty(
        name="projection",
        description="CSR Projection Number",
        default=4236,
        update=update_sockets)
    
    networktype: EnumProperty(
        name='networktype', items=networktype_items,
        default="drive",
        description='Choose Network Type', 
        update=update_sockets)
    
    distance: IntProperty(
        name="distance",
        description="Distance",
        default=1000,
        update=update_sockets)
    


    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Address")
        
        # outputs
        
        self.outputs.new('SvVerticesSocket', "Nodes")
        self.outputs.new('SvStringsSocket', "Nodes_ID")
        self.outputs.new('SvStringsSocket', "Nodes_Keys")
        self.outputs.new('SvStringsSocket', "Nodes_Values")
        
        self.outputs.new('SvVerticesSocket', "Edges_Verts")
        self.outputs.new('SvStringsSocket', "Edges")
        self.outputs.new('SvStringsSocket', "Edges_ID")
        self.outputs.new('SvStringsSocket', "Edges_Keys")
        self.outputs.new('SvStringsSocket', "Edges_Values")
        
        self.outputs.new('SvStringsSocket', "DF")
        self.outputs.new('SvStringsSocket', "Network")


    def draw_buttons(self,context, layout):
        layout.prop(self, 'projection')
        layout.prop(self, 'networktype', expand=True)
        layout.prop(self, 'distance')


    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
         
        if not self.inputs["Address"].is_linked:
            return
        self.address = self.inputs["Address"].sv_get(deepcopy = False)
        distance = self.distance 

        address = str(self.address[0][0])

        G = ox.graph_from_address(address,dist=distance,network_type=self.networktype)

        G = ox.projection.project_graph(G, to_crs=self.projection)

        gdf = ox.utils_graph.graph_to_gdfs(G, nodes=True, edges=True, node_geometry=True, fill_edge_geometry=True)


        poly=gdf[0]["geometry"]


        test = mapping(poly)

        all_features= mapping(gdf[0])

        poly_edges=gdf[1]["geometry"]
        test_edges = mapping(poly_edges)

        all_features_edges= mapping(gdf[1])


        #print(gdf)
        #geometry = gdf[0]["geometry"]
        #geometry = gdf[1]["geometry"]

        #print(geometry)
        #al_features= mapping(gdf)

        linestrings = []
        linestrings_features = []


        points = []
        points_features = []


        ###### Functions #######

        def chunk(it, size):
            it = iter(it)
            return iter(lambda: tuple(itertools.islice(it, size)), ())

        def unequal_divide(iterable, chunks):
            it = iter(iterable)
            return [list(itertools.islice(it, c)) for c in chunks]

        def removeLastElement(givenlist):
            # using pop() function
            givenlist.pop()
            # return the result list
            return givenlist

        def shift(seq, n=0):
            a = n % len(seq)
            return seq[-a:] + seq[:-a]

        #####-------------------------------#####

        # Points

        for i in range(0,len(poly)):
            if test["features"][i]["geometry"]["type"] == "Point":
                points.append(test["features"][i]["geometry"]["coordinates"])
                points_features.append(all_features["features"][i])

        ###########################################################################################

        # Edges

        for i in range(0,len(poly_edges)):
            if test_edges["features"][i]["geometry"]["type"] == "LineString":
                linestrings.append(test_edges["features"][i]["geometry"]["coordinates"])
                linestrings_features.append(all_features_edges["features"][i])
        ###########################################################################################



        # Points

        points_verts = [[i + (0,)] for i in points]


        # Points Features

        ## Getting Points ID

        points_id=[i['id'] for i in points_features]

        ## Getting Points Features

        ### Getting Points Features

        points_keys = []
        points_values = []

        for i in points_features:
                points_keys.append(i['properties'].keys())
                points_values.append(i['properties'].values())

        #######################################################################################################

        # LineString


        ## LineStrings Vertices

        linestrings_verts_1 = [items + (0,) for i in linestrings for items in i]

        ## Getting Lines Size

        ls_linestrings=[len(linestrings[i]) for i in range(0,len(linestrings))]

        ## Slice Linestrings

        it_lns = iter(linestrings_verts_1)

        linestrings_verts= [[next(it_lns) for _ in range(size)] for size in ls_linestrings]


        ## lineStrings Edges

        ### Creating List of Edges LineStrings
        linestrings_edges_p = []
        linestrings_edges_x = []

        for i in linestrings_verts:
            linestrings_edges_p.append([])
            for j in i:
                linestrings_edges_p[linestrings_verts.index(i)].append(i.index(j))

        ### Creating Second List of Edges (Shifted List)

        linestrings_edges_z = [linestrings_edges_p[linestrings_edges_p.index(items)][1:] + linestrings_edges_p[linestrings_edges_p.index(items)][:1] for items in linestrings_edges_p]

        ### Zip First and Second List of Edges

        linestrings_edges_h=[list(zip(linestrings_edges_p[items],linestrings_edges_z[items])) for items in range(0,len(linestrings_edges_p))]

        ### Remove Extra Edges

        linestrings_edges= [removeLastElement(i) for i in linestrings_edges_h]

        ## LineString Features


        ### Getting LineString ID

        linestrings_id=[i['id'] for i in linestrings_features]

        ### Getting Polygons Features

        linestrings_keys = []
        linestrings_values = []

        for i in linestrings_features:
                linestrings_keys.append(i['properties'].keys())
                linestrings_values.append(i['properties'].values())

        ########################################################################################################

        #### OUTPUTS

        nodes = points_verts
        nodes_id = points_id
        nodes_keys = points_keys
        nodes_values = points_values


        edges_verts = linestrings_verts
        edges = linestrings_edges
        edges_id = linestrings_id
        edges_keys = linestrings_keys
        edges_values = linestrings_values

        geoDataFrame = gdf
        nx = G
        
        ## Output

        self.outputs["Nodes"].sv_set(nodes)
        self.outputs["Nodes_ID"].sv_set(nodes_id)
        self.outputs["Nodes_Keys"].sv_set(nodes_keys)
        self.outputs["Nodes_Values"].sv_set(nodes_values)
        
        self.outputs["Edges_Verts"].sv_set(edges_verts)
        self.outputs["Edges"].sv_set(edges)
        self.outputs["Edges_ID"].sv_set(edges_id)
        self.outputs["Edges_Keys"].sv_set(edges_keys)
        self.outputs["Edges_Values"].sv_set(edges_values)
        
        self.outputs["DF"].sv_set(geoDataFrame)
        self.outputs["Network"].sv_set(nx)
        

def register():
    if ox is not None:
        bpy.utils.register_class(SvMegapolisLoadStreetNetwork)

def unregister():
    if ox is not None:
        bpy.utils.unregister_class(SvMegapolisLoadStreetNetwork)
