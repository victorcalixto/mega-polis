import bpy
from bpy.props import IntProperty, EnumProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import osmnx as ox
from megapolis.dependencies import networkx as nx



Analysis_method = namedtuple('AnalysisMethod', ['closeness_centrality','betweenness_centrality','degree_centrality','basic'])
ANALYSISMETHOD = Analysis_method('closeness_centrality','betweenness_centrality','degree_centrality','basic')
analysismethod_items = [(i, i, '') for i in ANALYSISMETHOD]

class SvMegapolisNetworkAnalyses(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Network Analyses
    Tooltip: Network Analises: Closeness Centrality and Degree Centrality  
    """
    bl_idname = 'SvMegapolisNetworkAnalyses'
    bl_label = 'Network Analyses'
    bl_icon = 'MESH_DATA'

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status
        updateNode(self,context)

    #Blender Properties Buttons
    
    analysismethod: EnumProperty(
        name='Analysis Methods', items=analysismethod_items,
        default="closeness_centrality",
        description='Choose a Network Analysis Method', 
        update=update_sockets)

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Nx Graph")
        self.inputs.new('SvStringsSocket', "Colour Map")

        # outputs
       
        self.outputs.new('SvStringsSocket', "Nx Values")
        self.outputs.new('SvStringsSocket', "Nx Edges Colours")


    def draw_buttons(self,context, layout):
        layout.prop(self, 'analysismethod', expand=False)

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
         
        if not self.inputs["Nx Graph"].is_linked or not self.inputs["Colour Map"].is_linked: 
            return
        self.graph = self.inputs["Nx Graph"].sv_get(deepcopy = False)
        self.colour = self.inputs["Colour Map"].sv_get(deepcopy = False)
                    
        G = self.graph
        colormap_type = self.colour[0][0]

        def nx_analysis(nodes, method):
            if method == "closeness_centrality":
                closeness_centrality = nx.closeness_centrality(nx.line_graph(G))
                nx.set_edge_attributes(G, closeness_centrality, method)
                values_centrality = closeness_centrality.values()
                ec = ox.plot.get_edge_colors_by_attr(G, method, cmap=colormap_type)
                return [list(values_centrality)],[list(ec)]
            
            elif method == "betweenness_centrality":
                betweenness_centrality= nx.betweenness_centrality(nx.line_graph(G))
                nx.set_edge_attributes(G, betweenness_centrality, method)
                values_centrality = betweenness_centrality.values()
                ec = ox.plot.get_edge_colors_by_attr(G, method, cmap=colormap_type)
                return [list(values_centrality)],[list(ec)]

            elif method == "degree_centrality": 
                degree_centrality = nx.degree_centrality(nx.line_graph(G))
                nx.set_edge_attributes(G, degree_centrality, method)
                ec = ox.plot.get_edge_colors_by_attr(G, method, cmap=colormap_type)
                values_centrality = degree_centrality.values()
                return [list(values_centrality)], [list(ec)]

            
            elif method == "basic":
                nodes_proj = ox.graph_to_gdfs(G, edges=False)
                graph_area_m = nodes_proj.unary_union.convex_hull.area
                basic_stats = ox.basic_stats(G)
                basic_result = ox.basic_stats(G, area=graph_area_m, clean_int_tol=15)
                return basic_result



        results = nx_analysis(G,self.analysismethod)

        nx_results = results[0]
        nx_edges_colours = results[1] 

        ## Output

        self.outputs["Nx Values"].sv_set(nx_results)
        self.outputs["Nx Edges Colours"].sv_set(nx_edges_colours)
        

def register():
    if nx is not None:
        bpy.utils.register_class(SvMegapolisNetworkAnalyses)

def unregister():
    if nx is not None:
        bpy.utils.unregister_class(SvMegapolisNetworkAnalyses)
