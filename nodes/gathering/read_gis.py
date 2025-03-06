import bpy
import numpy as np
import geopandas as gpd
from shapely.geometry import mapping
from numba import njit
from sverchok.node_tree import SverchCustomTreeNode

class SvMegapolisReadGis(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Read GIS
    Tooltip: Read GIS file (shapefile, geopackage, and geoJSON)
    """
    bl_idname = 'SvMegapolisReadGis'
    bl_label = 'Read Gis'
    bl_icon = 'MESH_DATA'
    sv_dependencies = {'geopandas', 'osmnx',"numba"}

    def process(self):
        file_name = self.inputs["File"].sv_get()[0]  # Assuming an input slot for file
        projection = self.inputs["Projection"].sv_get()[0]  # Assuming an input slot for projection

        if not file_name:
            return

        # Read GIS file and reproject
        geometry_shp = gpd.read_file(file_name)
        gdf = geometry_shp.to_crs(projection)

        # Convert geometries to dictionary format
        test = mapping(gdf["geometry"])

        # Process geometries with Numba-optimized functions
        multipolygons, polygons, linestrings, points = parse_geometry(test["features"])

        # Convert to NumPy arrays
        polygons_verts, polygons_edges, polygons_keys, polygons_values, polygons_id = process_polygons(polygons)
        mp_verts, mp_edges, mp_keys, mp_values, mp_id = process_multipolygons(multipolygons)
        points_verts, points_keys, points_values, points_id = process_points(points)
        linestrings_verts, linestrings_edges, linestrings_keys, linestrings_values, linestrings_id = process_lines(linestrings)

        ## Output to Sverchok
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

        ## Geopandas DataFrame
        self.outputs["Gdf_Out"].sv_set(gdf)

@njit
def parse_geometry(features):
    """Extract geometry data efficiently using Numba."""
    num_features = len(features)
    multipolygons = []
    polygons = []
    linestrings = []
    points = []

    for i in range(num_features):
        geom = features[i]["geometry"]
        if geom is None:
            continue
        geom_type = geom["type"]
        coords = geom["coordinates"]

        if geom_type == "MultiPolygon":
            multipolygons.append(coords)
        elif geom_type == "Polygon":
            polygons.append(coords[0])  # Outer ring only
        elif geom_type == "LineString":
            linestrings.append(coords)
        elif geom_type == "Point":
            points.append(coords)

    return multipolygons, polygons, linestrings, points

@njit
def process_polygons(polygons):
    """Process polygon geometries and compute edges."""
    num_polygons = len(polygons)
    verts = []
    edges = []
    keys = []
    values = []
    ids = np.arange(num_polygons)  # Assign IDs

    for i in range(num_polygons):
        polygon = np.array(polygons[i], dtype=np.float64)
        verts.append(polygon.tolist())

        num_vertices = len(polygon)
        edges.append(np.array([[j, (j + 1) % num_vertices] for j in range(num_vertices)], dtype=np.int32).tolist())

        keys.append(i)  # Dummy keys (modify as needed)
        values.append(i)  # Dummy values (modify as needed)

    return verts, edges, keys, values, ids.tolist()

@njit
def process_multipolygons(multipolygons):
    """Process MultiPolygon geometries."""
    verts, edges, keys, values, ids = process_polygons(multipolygons)  # Reuse polygon function
    return verts, edges, keys, values, ids

@njit
def process_points(points):
    """Process point geometries."""
    num_points = len(points)
    verts = np.array(points, dtype=np.float64).tolist()
    keys = list(range(num_points))
    values = list(range(num_points))
    ids = np.arange(num_points).tolist()

    return verts, keys, values, ids

@njit
def process_lines(linestrings):
    """Process linestring geometries."""
    num_lines = len(linestrings)
    verts = []
    edges = []
    keys = []
    values = []
    ids = np.arange(num_lines).tolist()

    for i in range(num_lines):
        line = np.array(linestrings[i], dtype=np.float64)
        verts.append(line.tolist())

        num_vertices = len(line)
        edges.append(np.array([[j, j + 1] for j in range(num_vertices - 1)], dtype=np.int32).tolist())

        keys.append(i)  # Dummy keys (modify as needed)
        values.append(i)  # Dummy values (modify as needed)

    return verts, edges, keys, values, ids

def register():
    bpy.utils.register_class(SvMegapolisReadGis)

def unregister():
    bpy.utils.unregister_class(SvMegapolisReadGis)
