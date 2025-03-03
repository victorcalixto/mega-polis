import bpy
from bpy.props import IntProperty, EnumProperty
from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

# Megapolis Dependencies
import geopandas as gpd

try:
    from shapely.geometry import mapping
except ImportError:
    pass

from itertools import islice


# Named tuple for GIS Filetype
Filetype_GIS = namedtuple('FileType', ['Path', 'URL'])
FILETYPEGIS = Filetype_GIS('Path', 'URL')
filetypegis_items = [(i, i, '') for i in FILETYPEGIS]


class SvMegapolisReadGis(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Read GIS
    Tooltip: Read GIS file (shapefile, geopackage, and geoJSON)
    """
    bl_idname = 'SvMegapolisReadGis'
    bl_label = 'Read GIS'
    bl_icon = 'WORLD'
    sv_dependencies = {'geopandas', 'osmnx'}

    def update_sockets(self, context):
        """Need to do UX transformation before updating the node."""
        
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        if self.filetype_gis in FILETYPEGIS.Path:
            set_hide(self.inputs['Path'], False)
            set_hide(self.inputs['URL'], True)
        else:
            set_hide(self.inputs['URL'], False)
            set_hide(self.inputs['Path'], True)

        updateNode(self, context)

    # Blender Properties Buttons
    projection: IntProperty(
        name="Projection",
        description="CSR Projection Number",
        default=4236,
        update=update_sockets
    )
    
    filetype_gis: EnumProperty(
        name='Filetype GIS',
        items=filetypegis_items,
        default="Path",
        description='Choose the input GIS file type',
        update=update_sockets
    )

    def sv_init(self, context):
        # Inputs
        self.inputs.new('SvFilePathSocket', "Path")
        self.inputs.new('SvStringsSocket', "URL")
        self.inputs['URL'].hide_safe = True

        # Outputs
        # Polygons
        self.outputs.new('SvVerticesSocket', "Polygons_Vertices")
        self.outputs.new('SvStringsSocket', "Polygons_Edges")
        self.outputs.new('SvStringsSocket', "Polygons_Keys")
        self.outputs.new('SvStringsSocket', "Polygons_Values")
        self.outputs.new('SvStringsSocket', "Polygons_ID")
        
        # MultiPolygons
        self.outputs.new('SvVerticesSocket', "MP_Polygons_Vertices")
        self.outputs.new('SvStringsSocket', "MP_Polygons_Edges")
        self.outputs.new('SvStringsSocket', "MP_Polygons_Keys")
        self.outputs.new('SvStringsSocket', "MP_Polygons_Values")
        self.outputs.new('SvStringsSocket', "MP_Polygons_ID")

        # Points
        self.outputs.new('SvVerticesSocket', "Points_Vertices")
        self.outputs.new('SvStringsSocket', "Points_Keys")
        self.outputs.new('SvStringsSocket', "Points_Values")
        self.outputs.new('SvStringsSocket', "Points_ID")

        # Lines
        self.outputs.new('SvVerticesSocket', "Lines_Vertices")
        self.outputs.new('SvStringsSocket', "Lines_Edges")
        self.outputs.new('SvStringsSocket', "Lines_Keys")
        self.outputs.new('SvStringsSocket', "Lines_Values")
        self.outputs.new('SvStringsSocket', "Lines_ID")
        
        # Geopandas dataframe
        self.outputs.new('SvStringsSocket', "Gdf_Out")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'projection')
        layout.prop(self, 'filetype_gis', expand=True)

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        """Process the GIS file based on the selected file type (Path or URL)."""
        if self.filetype_gis in FILETYPEGIS.Path:
            if not self.inputs["Path"].is_linked:
                return
            self.path = self.inputs["Path"].sv_get(deepcopy=False)
            file_name = str(self.path[0][0])
        else:
            if not self.inputs["URL"].is_linked:
                return
            self.path = self.inputs["URL"].sv_get(deepcopy=False)
            file_name = str(self.path[0][0])
        
        geometry_shp = gpd.read_file(file_name)
        gdf = geometry_shp.to_crs(self.projection)

        poly = gdf["geometry"]
        all_features = mapping(gdf)
        test = mapping(poly)

        # Initialize lists
        multipolygons = []
        polygons = []
        linestrings = []
        multilinestrings = []
        points = []
        multipoints = []
        polygons_features = []
        multipolygons_features = []
        points_features = []
        linestrings_features = []

        def chunk(it, size):
            it = iter(it)
            return iter(lambda: tuple(islice(it, size)), ())

        def unequal_divide(iterable, chunks):
            it = iter(iterable)
            return [list(islice(it, c)) for c in chunks]

        def remove_last_element(givenlist):
            """Remove the last element from the list."""
            givenlist.pop()
            return givenlist

        def shift(seq, n=0):
            """Shift elements in the list by n positions."""
            a = n % len(seq)
            return seq[-a:] + seq[:-a]

        # Process geometries
        for i in range(len(poly)):
            if test["features"][i]["geometry"] is None:
                continue
            else:
                geometry_type = test["features"][i]["geometry"]["type"]
                if geometry_type == "MultiPolygon":
                    multipolygons.append(test["features"][i]["geometry"]["coordinates"])
                    multipolygons_features.append(all_features["features"][i])
                elif geometry_type == "Polygon":
                    polygons.append(test["features"][i]["geometry"]["coordinates"][0])
                    polygons_features.append(all_features["features"][i])
                elif geometry_type == "LineString":
                    linestrings.append(test["features"][i]["geometry"]["coordinates"])
                    linestrings_features.append(all_features["features"][i])
                elif geometry_type == "MultiLineString":
                    multilinestrings.append(test["features"][i]["geometry"]["coordinates"][0])
                elif geometry_type == "Point":
                    points.append(test["features"][i]["geometry"]["coordinates"])
                    points_features.append(all_features["features"][i])
                elif geometry_type == "MultiPoint":
                    multipoints.append(test["features"][i]["geometry"]["coordinates"][0])

        # Process Points
        points_verts = [[i + (0,)] for i in points]
        points_keys, points_values = [], []
        for i in points_features:
            points_keys.append(i['properties'].keys())
            points_values.append(i['properties'].values())

        # Process LineString
        linestrings_verts_1 = [items + (0,) for i in linestrings for items in i]
        ls_linestrings = [len(linestrings[i]) for i in range(len(linestrings))]
        it_lns = iter(linestrings_verts_1)
        linestrings_verts = [[next(it_lns) for _ in range(size)] for size in ls_linestrings]

        # Create LineString Edges
        linestrings_edges_p = []
        for i in linestrings_verts:
            linestrings_edges_p.append([i.index(j) for j in i])

        linestrings_edges_z = [linestrings_edges_p[i][1:] + linestrings_edges_p[i][:1] for i in range(len(linestrings_edges_p))]
        linestrings_edges_h = [list(zip(linestrings_edges_p[i], linestrings_edges_z[i])) for i in range(len(linestrings_edges_p))]
        linestrings_edges = [remove_last_element(i) for i in linestrings_edges_h]

        # Process Multipolygons
        multipolygons_verts_1 = [item + (0,) for i in multipolygons for j in i for k in j for item in k]
        ls_multipolygons = [len(k) for i in multipolygons for j in i for k in j]
        it_mult = iter(multipolygons_verts_1)
        multipolygons_verts = [[next(it_mult) for _ in range(size)] for size in ls_multipolygons]

        # Process Polygons
        polygons_verts_1 = [item + (0,) for i in polygons for item in i]
        ls_polygons = [len(polygons[i]) for i in range(len(polygons))]
        it = iter(polygons_verts_1)
        polygons_verts = [[next(it) for _ in range(size)] for size in ls_polygons]

        # Create Polygon Edges
        polygons_edges_p = []
        for i in polygons_verts:
            polygons_edges_p.append([i.index(j) for j in i])

        polygons_edges_z = [polygons_edges_p[i][1:] + polygons_edges_p[i][:1] for i in range(len(polygons_edges_p))]
        polygons_edges_h = [list(zip(polygons_edges_p[i], polygons_edges_z[i])) for i in range(len(polygons_edges_p))]
        polygons_edges = polygons_edges_h

        # Set outputs
        self.outputs["Polygons_Vertices"].sv_set(polygons_verts)
        self.outputs["Polygons_Edges"].sv_set(polygons_edges)
        self.outputs["Polygons_Keys"].sv_set([f['properties'].keys() for f in polygons_features])
        self.outputs["Polygons_Values"].sv_set([f['properties'].values() for f in polygons_features])
        self.outputs["Polygons_ID"].sv_set([f['id'] for f in polygons_features])

        self.outputs["MP_Polygons_Vertices"].sv_set(multipolygons_verts)
        self.outputs["MP_Polygons_Edges"].sv_set([[]] * len(multipolygons_verts))
        self.outputs["MP_Polygons_Keys"].sv_set([f['properties'].keys() for f in multipolygons_features])
        self.outputs["MP_Polygons_Values"].sv_set([f['properties'].values() for f in multipolygons_features])
        self.outputs["MP_Polygons_ID"].sv_set([f['id'] for f in multipolygons_features])

        self.outputs["Points_Vertices"].sv_set(points_verts)
        self.outputs["Points_Keys"].sv_set([f['properties'].keys() for f in points_features])
        self.outputs["Points_Values"].sv_set([f['properties'].values() for f in points_features])
        self.outputs["Points_ID"].sv_set([f['id'] for f in points_features])

        self.outputs["Lines_Vertices"].sv_set(linestrings_verts)
        self.outputs["Lines_Edges"].sv_set(linestrings_edges)
        self.outputs["Lines_Keys"].sv_set([f['properties'].keys() for f in linestrings_features])
        self.outputs["Lines_Values"].sv_set([f['properties'].values() for f in linestrings_features])
        self.outputs["Lines_ID"].sv_set([f['id'] for f in linestrings_features])

        self.outputs["Gdf_Out"].sv_set([all_features])

def register():
    bpy.utils.register_class(SvMegapolisReadGis)


def unregister():
    bpy.utils.unregister_class(SvMegapolisReadGis)
