from __future__ import print_function
import bpy
import math
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

# from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


# Megapolis Dependencies
# We will no longer use visilibity

class SvMegapolisIsovists(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Isovists
    Tooltip: Creates a 2D Isovists based on a 2D Context
    """
    bl_idname = 'SvMegapolisIsovists'
    bl_label = 'Isovists'
    bl_icon = 'MESH_DATA'

    def update_sockets(self, context):
        """ Need to do UX transformation before updating node. """
        
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status
        
        updateNode(self, context)

    def sv_init(self, context):
        # Inputs
        self.inputs.new('SvStringsSocket', "NumVertices")
        self.inputs.new('SvStringsSocket', "Radius")
        self.inputs.new('SvVerticesSocket', "Origin")
        self.inputs.new('SvVerticesSocket', "Context")

        # Outputs
        self.outputs.new('SvVerticesSocket', "Vertices Out")
        self.outputs.new('SvVerticesSocket', "Isovists Vertices")

    def process(self):
        if not (self.inputs["NumVertices"].is_linked and 
                self.inputs["Radius"].is_linked and 
                self.inputs["Origin"].is_linked and 
                self.inputs["Context"].is_linked):
            return

        self.num_vertices = self.inputs["NumVertices"].sv_get(deepcopy=False)
        self.radius = self.inputs["Radius"].sv_get(deepcopy=False)
        self.origin = self.inputs["Origin"].sv_get(deepcopy=False)
        self.context = self.inputs["Context"].sv_get(deepcopy=False)

        radius = self.radius[0][0]
        vertices_num = self.num_vertices[0][0]
        origin = self.origin[0][0]
        shapes = self.context

        origin_x = origin[0]
        origin_y = origin[1]
        origin_z = origin[2]

        origin_2d = (origin[0], origin[1])

        theta = 360 / vertices_num

        list_verts_x = [radius * math.cos(math.radians(theta * i)) + origin_x for i in range(vertices_num)]
        list_verts_y = [radius * math.sin(math.radians(theta * i)) + origin_y for i in range(vertices_num)]

        points = list((x, y, (0 + origin_z)) for x, y in zip(list_verts_x, list_verts_y))

        epsilon = 0.001

        # Create polygon from the vertices of the context (shapes)
        list_shapes = [Polygon([(point[0], point[1]) for point in shape]) for shape in shapes]

        # Create the observer point
        observer = Point(origin_2d[0], origin_2d[1])

        # Create the outer walls of the polygon
        polygon_points = list(zip(list_verts_x, list_verts_y))
        walls = Polygon(polygon_points)

        # Determine if the observer is inside any walls and compute the visible area
        isovist_polygon = self.calculate_isovist(observer, walls, list_shapes, epsilon)

        # Generate points from the isovist polygon
        points_isovist = [(list([point[0], point[1], 0])) for point in isovist_polygon.exterior.coords]

        vertices_out = [points]

        isovists_verts = [points_isovist]

        # Outputs
        self.outputs["Vertices Out"].sv_set(vertices_out)
        self.outputs["Isovists Vertices"].sv_set(isovists_verts)

    def calculate_isovist(self, observer, walls, list_holes, epsilon):
        """
        Function to calculate the isovist of an observer using walls and obstacles (holes).
        Returns a Polygon representing the visible area.
        """
        # Union of all the holes
        all_obstacles = unary_union(list_holes)

        # Combine walls and obstacles
        environment = walls.difference(all_obstacles)

        # Compute the visibility polygon from the observer point
        isovist = environment.intersection(observer.buffer(1, resolution=16))

        # Ensure there are no issues with small geometry errors
        if isovist.is_empty:
            return Polygon()

        return isovist


def register():
    bpy.utils.register_class(SvMegapolisIsovists)


def unregister():
    bpy.utils.unregister_class(SvMegapolisIsovists)

