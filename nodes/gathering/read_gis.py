import bpy
from bpy.props import IntProperty, EnumProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
#from sverchok.utils.dummy_nodes import add_dummy


#Megapolis Dependencies
from megapolis.dependencies import geopandas as gpd
from megapolis.dependencies import osmnx as ox
from megapolis.dependencies import shapely

try:
    from shapely.geometry import mapping
except:
    pass
#Polygon = shapely.geometry.Polygon
#Point = shapely.geometry.Point
#LineString = shapely.geometry.LineString
#mapping = shapely.geometry.mapping 

from itertools import islice 
import itertools


Filetype_GIS = namedtuple('FileType', ['Path', 'URL'])
FILETYPEGIS = Filetype_GIS('Path', 'URL')
filetypegis_items = [(i, i, '') for i in FILETYPEGIS]



class SvMegapolisReadGis(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Read GIS
    Tooltip: Read GIS file (shapefile,geopackage, and geoJSON)
    """
    bl_idname = 'SvMegapolisReadGis'
    bl_label = 'Read Gis'
    bl_icon = 'MESH_DATA'
    sv_dependencies = {'geopandas', 'osmnx'}

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        if self.filetype_gis in FILETYPEGIS.Path:
            set_hide(self.inputs['Path'], False)
            set_hide(self.inputs['URL'], True)
        else:
            set_hide(self.inputs['URL'],False)
            set_hide(self.inputs['Path'],True)
        updateNode(self,context)

    #Blender Properties Buttons

    projection: IntProperty(
        name="projection",
        description="CSR Projection Number",
        default=4236,
        update=update_sockets)
    
    filetype_gis: EnumProperty(
        name='filetype_gis', items=filetypegis_items,
        default="Path",
        description='Choose the input GIS file type', 
        update=update_sockets)


    def sv_init(self, context):
        # inputs
        self.inputs.new('SvFilePathSocket', "Path")
        self.inputs.new('SvStringsSocket', "URL")
        self.inputs['URL'].hide_safe = True 
        # outputs
        
        ## Polygons
        self.outputs.new('SvVerticesSocket', "Polygons_Vertices")
        self.outputs.new('SvStringsSocket', "Polygons_Edges")
        self.outputs.new('SvStringsSocket', "Polygons_Keys")
        self.outputs.new('SvStringsSocket', "Polygons_Values")
        self.outputs.new('SvStringsSocket', "Polygons_ID")
        
        ## MultiPolygons
        self.outputs.new('SvVerticesSocket', "MP_Polygons_Vertices")
        self.outputs.new('SvStringsSocket', "MP_Polygons_Edges")
        self.outputs.new('SvStringsSocket', "MP_Polygons_Keys")
        self.outputs.new('SvStringsSocket', "MP_Polygons_Values")
        self.outputs.new('SvStringsSocket', "MP_Polygons_ID")

        ## Points
        self.outputs.new('SvVerticesSocket', "Points_Vertices")
        self.outputs.new('SvStringsSocket', "Points_Keys")
        self.outputs.new('SvStringsSocket', "Points_Values")
        self.outputs.new('SvStringsSocket', "Points_ID")

        ## Lines
        self.outputs.new('SvVerticesSocket', "Lines_Vertices")
        self.outputs.new('SvStringsSocket', "Lines_Edges")
        self.outputs.new('SvStringsSocket', "Lines_Keys")
        self.outputs.new('SvStringsSocket', "Lines_Values")
        self.outputs.new('SvStringsSocket', "Lines_ID")
        
        ##Geopandas dataframe
        self.outputs.new('SvStringsSocket', "Gdf_Out")
        
    def draw_buttons(self,context, layout):
        layout.prop(self, 'projection')
        layout.prop(self, 'filetype_gis', expand=True)

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
         
        if self.filetype_gis in FILETYPEGIS.Path:
            if not self.inputs["Path"].is_linked:
                return
            self.path = self.inputs["Path"].sv_get(deepcopy = False)
            file_name = str(self.path[0][0])
        else:
            if not self.inputs["URL"].is_linked:
                return
            self.path = self.inputs["URL"].sv_get(deepcopy = False)
            file_name = str(self.path[0][0])
        
        geometry_shp = gpd.read_file(file_name)
        gdf = geometry_shp
        #gdf.set_crs(f'self.projection', allow_override=True)
        #gdf = ox.projection.project_gdf(gdf, to_crs=self.projection)
        gdf = gdf.to_crs(self.projection)

        #gdf.to_crs(f'epsg:{gis_crs}')

        poly=gdf["geometry"]


        all_features= mapping(gdf)

        test= mapping(poly)

        multipolygons = []
        polygons =[]
        linestrings = []
        multilinestrings=[]
        points= []
        multipoints=[]
        polygons_features = []
        multipolygons_features = []
        points_features = []
        linestrings_features = []



        #############################################################################################
        # Functions


        def chunk(it, size):
            it = iter(it)
            return iter(lambda: tuple(islice(it, size)), ())

        def unequal_divide(iterable, chunks):
            it = iter(iterable)
            return [list(islice(it, c)) for c in chunks]

        def removeLastElement(givenlist):
            # using pop() function
            givenlist.pop()
            # return the result list
            return givenlist

        def shift(seq, n=0):
            a = n % len(seq)
            return seq[-a:] + seq[:-a]

        ############################################################################################

        for i in range(0,len(poly)):
            if test["features"][i]["geometry"]["type"] == "MultiPolygon":
                multipolygons.append(test["features"][i]["geometry"]["coordinates"])
                multipolygons_features.append(all_features["features"][i])
            elif test["features"][i]["geometry"]["type"] == "Polygon":
                polygons.append(test["features"][i]["geometry"]["coordinates"][0])
                polygons_features.append(all_features["features"][i])
            elif test["features"][i]["geometry"]["type"] == "LineString":
                linestrings.append(test["features"][i]["geometry"]["coordinates"])
                linestrings_features.append(all_features["features"][i])
            elif test["features"][i]["geometry"]["type"] == "MultiLineString":
                multilinestrings.append(test["features"][i]["geometry"]["coordinates"][0])
            elif test["features"][i]["geometry"]["type"] == "Point":
                points.append(test["features"][i]["geometry"]["coordinates"])
                points_features.append(all_features["features"][i])
            elif test["features"][i]["geometry"]["type"] == "MultiPoint":
                multipoints.append(test["features"][i]["geometry"]["coordinates"][0])


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

        print(linestrings_verts)

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

        # Multipolygons

        multipolygons_size = []

        for i in multipolygons:
            multipolygons_size.append(len(i))

        #Creating Vertices MultiPolygons

        multipolygons_verts_1 = [item + (0,) for i in multipolygons for j in i for k in j for item in k]

        ls_multipolygons =[]

        for i in multipolygons:
            for j in i:
                for k in j:
                    ls_multipolygons.append(len(k))    


        it_mult = iter(multipolygons_verts_1)

        multipolygons_verts= [[next(it_mult) for _ in range(size)] for size in ls_multipolygons]

        m_pl_size = []

        for i in multipolygons_verts:
            m_pl_size.append(len(i))


        ## Mulipolygons divide verts in number of polygons

        mp_verts_to_clean = unequal_divide(multipolygons_verts,multipolygons_size)


        ## Mulipolygons delete list level

        mp_verts = [list(itertools.chain(*sub)) for sub in mp_verts_to_clean]

        # MultiPolygon Edges

        ## Manipulations in list to create edges

        new_list = unequal_divide(m_pl_size,multipolygons_size)
        new_list_2= []


        soma_list = []
        for i in new_list:
           soma_list.append(sum(i))

        for i in soma_list:
            new_list_2.append([])
            #print(i)
            
            #for j in range(0,i):
              #  print(soma_list.index(i))
             #   new_list_2[soma_list.index(i)].append(j)
        for i in range(0,len(soma_list)):
            print(i)
            for j in range(0,soma_list[i]):
                 new_list_2[i].append(j) 
            

        #for i in new_list_2:
           

        new_list_3 =[]

        for i in range(0, len(new_list_2)):
            lista = new_list_2[i]
            chunks = new_list[i]
            new_list_3.append(unequal_divide(lista, chunks))



        m_edges_shift = []

        for i in new_list_3:
            m_edges_shift.append([])
            for j in i:
                m_edges_shift[new_list_3.index(i)].append(shift(j,1))



        m_edges_chunk =[]

        m_edges_h =[]

        for i in range(0,len(new_list_3)-1):
            m_edges_h.append([])
            for j in range(0,len(new_list_3[i])):
                m_edges_h[i].append(list(zip(new_list_3[i][j],m_edges_shift[i][j])))

        mp_edges = [list(itertools.chain(*sub)) for sub in m_edges_h]

        ###########################################################################################
        #Polygons

        ## Creating Vertices Polygons

        polygons_verts_1 = [item + (0,) for i in polygons for item in i]

        ##Getting list size Polygons

        ls_polygons=[len(polygons[i]) for i in range(0,len(polygons))]

        ##Slice List of Vertices 

        it = iter(polygons_verts_1)

        polygons_verts= [[next(it) for _ in range(size)] for size in ls_polygons]

        # Polygon Edges

        ## Creating List of Edges Polygon

        polygons_edges_p = []
        polygons_edges_x = []

        for i in polygons_verts:
            polygons_edges_p.append([])
            for j in i:
                polygons_edges_p[polygons_verts.index(i)].append(i.index(j))

        ## Creating Second List of Edges (Shifted List)

        polygons_edges_z = [polygons_edges_p[polygons_edges_p.index(items)][1:] + polygons_edges_p[polygons_edges_p.index(items)][:1] for items in polygons_edges_p]

        ## Zip First and Second List of Edges

        polygons_edges_h=[list(zip(polygons_edges_p[items],polygons_edges_z[items])) for items in range(0,len(polygons_edges_p))]

        ## Remove Extra Edges

        polygons_edges= [removeLastElement(i) for i in polygons_edges_h]



        #################################################################################################################################
        ## Polygons Features

        #print(polygons_features[0])

        ### Getting Polygons ID

        polygons_id=[i['id'] for i in polygons_features]

        ### Getting Polygons Features

        polygons_keys = []
        polygons_values = []

        for i in polygons_features:
                polygons_keys.append(i['properties'].keys())
                polygons_values.append(i['properties'].values())



        ##################################################################################################################################

        ## Multipolygons Features 

        ### Getting multipolygons ID

        mp_id=[i['id'] for i in multipolygons_features]

        ### Getting Multipolygons Features

        mp_keys = []
        mp_values = []

        for i in multipolygons_features:
                mp_keys.append(i['properties'].keys())
                mp_values.append(i['properties'].values())

        


        ## Polygons

        self.outputs["Polygons_Vertices"].sv_set(polygons_verts)
        self.outputs["Polygons_Edges"].sv_set(polygons_edges)
        self.outputs["Polygons_Keys"].sv_set(polygons_keys)
        self.outputs["Polygons_Values"].sv_set(polygons_values)
        self.outputs["Polygons_ID"].sv_set(polygons_id)
        
        ## MultiPolygons
        
        self.outputs["MP_Polygons_Vertices"].sv_set(mp_verts)
        self.outputs["MP_Polygons_Edges"].sv_set(mp_edges)
        self.outputs["MP_Polygons_Keys"].sv_set(mp_keys)
        self.outputs["MP_Polygons_Values"].sv_set(mp_values)
        self.outputs["MP_Polygons_ID"].sv_set(mp_id)

        ## Points

        self.outputs["Points_Vertices"].sv_set(points_verts)
        self.outputs["Points_Keys"].sv_set(points_keys)
        self.outputs["Points_Values"].sv_set(points_values)
        self.outputs["Points_ID"].sv_set(points_id)
        
        ## Lines

        self.outputs["Lines_Vertices"].sv_set(linestrings_verts)
        self.outputs["Lines_Edges"].sv_set(linestrings_edges)
        self.outputs["Lines_Keys"].sv_set(linestrings_keys)
        self.outputs["Lines_Values"].sv_set(linestrings_values)
        self.outputs["Lines_ID"].sv_set(linestrings_id)
        
        ##Geopandas dataframe
        self.outputs["Gdf_Out"].sv_set(gdf)


def register():
    bpy.utils.register_class(SvMegapolisReadGis)


def unregister():
    bpy.utils.unregister_class(SvMegapolisReadGis)
