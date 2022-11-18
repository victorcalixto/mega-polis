from __future__ import print_function 
import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import visilibity as vis
import math


class SvMegapolisIsovists(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Isovists
    Tooltip: Creates a 2D Isovists based on a 2d Context
    """
    bl_idname = 'SvMegapolisIsovists'
    bl_label = 'Isovists'
    bl_icon = 'MESH_DATA'
    sv_dependencies = {'visilibity'}
    
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status
        updateNode(self,context)

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "NumVertices")
        self.inputs.new('SvStringsSocket', "Radius")
        self.inputs.new('SvVerticesSocket', "Origin")
        self.inputs.new('SvVerticesSocket', "Context")

        #outputs
        self.outputs.new('SvVerticesSocket', "Vertices Out")
        self.outputs.new('SvVerticesSocket', "Isovists Vertices")

    def process(self):
        if not self.inputs["NumVertices"].is_linked or not self.inputs["Radius"].is_linked or not self.inputs["Origin"].is_linked or not self.inputs["Context"].is_linked:
            return
        self.num_vertices = self.inputs["NumVertices"].sv_get(deepcopy = False)
        self.radius = self.inputs["Radius"].sv_get(deepcopy = False)
        self.origin = self.inputs["Origin"].sv_get(deepcopy = False)
        self.context = self.inputs["Context"].sv_get(deepcopy = False)
        
        radius = self.radius[0][0]
        vertices_num= self.num_vertices[0][0]
        origin = self.origin[0][0]
        shapes = self.context

        origin_x = origin[0]
        origin_y = origin[1]
        origin_z = origin[2]

        origin_2d = (origin[0], origin[1])

        theta = 360/vertices_num

        list_vertsX = [radius * math.cos(math.radians(theta*i))+ origin_x for i in range(vertices_num)]
        list_vertsY = [radius * math.sin(math.radians(theta*i)) + origin_y for i in range(vertices_num)]

        points = list((x,y,(0+origin_z)) for x,y in zip(list_vertsX,list_vertsY))

        epsilon = 0.001

        list_points = list(vis.Point(x,y) for x,y in zip(list_vertsX,list_vertsY))
        print(list_points)
        
        list_wall_x = list(x.x() for x in list_points)
        list_wall_y = list(y.y() for y in list_points)

        list_wall_x.append(list_points[-1].x())
        list_wall_y.append(list_points[-1].y())

        walls = vis.Polygon(list_points)

        observer = vis.Point(origin_2d[0],origin_2d[1])

        list_shapes = [[vis.Point(j[0],j[1]) for j in i] for i in shapes]
        
        list_holes = [vis.Polygon(i) for i in list_shapes]    

        enviroment = list_holes

        enviroment.insert(0,walls)

        env = vis.Environment(enviroment)

        isovist = vis.Visibility_Polygon(observer, env, epsilon)

        points_isovist = [(list([isovist[i].x(),isovist[i].y(),0])) for i in range(vertices_num)]

        vertices_out = [points]

        isovists_verts = [points_isovist]           
        
        #outputs           
        self.outputs["Vertices Out"].sv_set(vertices_out)
        self.outputs["Isovists Vertices"].sv_set(isovists_verts)


def register():
    bpy.utils.register_class(SvMegapolisIsovists)


def unregister():
    bpy.utils.unregister_class(SvMegapolisIsovists)
