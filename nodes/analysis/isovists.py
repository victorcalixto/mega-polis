import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy


#Megapolis Dependencies
from megapolis.dependencies import visilibity as vis
import math

if vis is None:
    add_dummy('SvMegapolisIsovists', 'Isovists', 'visilibity')
else:
    class SvMegapolisIsovists(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: Isovists
        Tooltip: Creates a 2D Isovists based on a 2d Context
        """
        bl_idname = 'SvMegapolisIsovists'
        bl_label = 'Isovists'
        bl_icon = 'MESH_DATA'
        

        def sv_init(self, context):
            # inputs
            self.inputs.new('SvStringsSocket', "Num of Vertices")
            self.inputs.new('SvStringsSocket', "Radius")
            self.inputs.new('SvVerticesSocket', "Origin")
            self.inputs.new('SvVerticesSocket', "2D Contextual Polygons")

            #outputs
            self.outputs.new('SvVerticesSocket', "Vertices Out")
            self.outputs.new('SvVerticesSocket', "Isovists Vertices")

        def process(self):
            if not self.inputs["Num of Vertices"].is_linked or not self.inputs["Radius"].is_linked or not self.inputs["Origin"].is_linked or self.inputs["2D Contextual Polygons"].is_linked:
                return
            self.num_vertices = self.inputs["Num of Vertices"].sv_get(deepcopy = False)
            self.radius = self.inputs["Radius"].sv_get(deepcopy = False)
            self.origin = self.inputs["Origin"].sv_get(deepcopy = False)
            self.context = self.inputs["2d Contextual Polygons"].sv_get(deepcopy = False)

            radius = self.radius[0][0]
            vertices_num= self.num_vertices[0][0]
            origin = self.origin[0][0]
            shapes = self.context


            origin_x = origin[0]
            origin_y = origin[1]
            origin_z = origin[2]


            origin_2d = (origin[0], origin[1])

            theta = 360/vertices_num

            list_vertsX = []
            list_vertsY = []

            for i in range(vertices_num):
                list_vertsX.append(radius * math.cos(math.radians(theta*i))+ origin_x)
                list_vertsY.append(radius * math.sin(math.radians(theta*i)) + origin_y)

            points = list((x,y,(0+origin_z)) for x,y in zip(list_vertsX,list_vertsY))

            vertices_2d = list([x,y] for x,y in zip(list_vertsX,list_vertsY))

            epsilon = 0.001

            list_shapes = []
            list_holes_x = []
            list_holes_y = []
            holes = []
            list_holes = []


            list_points = list(vis.Point(x,y) for x,y in zip(list_vertsX,list_vertsY))

            list_wall_x = list(x.x() for x in list_points)
            list_wall_y = list(y.y() for y in list_points)

            list_wall_x.append(list_points[-1].x())
            list_wall_y.append(list_points[-1].y())

            walls = vis.Polygon(list_points)

            observer = vis.Point(origin_2d[0],origin_2d[1])

            shapes_inv = [i.reverse() for i in shapes]

            for i in shapes:
                list_shapes.append([])       
                for j in i:
                    list_shapes[shapes.index(i)].append((vis.Point(j[0],j[1])))
                

            for i in list_shapes:
                list_holes_x.append([])
                list_holes_y.append([])
                for j in i:
                    list_holes_x[list_shapes.index(i)].append(j.x())
                    list_holes_y[list_shapes.index(i)].append(j.y())  
                    
            for i in list_shapes:    
                list_holes.append(vis.Polygon(i))
                

            enviroment = list_holes

            enviroment.insert(0,walls)

            env = vis.Environment(enviroment)

            isovist = vis.Visibility_Polygon(observer, env, epsilon)

            points_isovist =[]



            for i in range(vertices_num):
               points_isovist.append(list([isovist[i].x(),isovist[i].y(),0]))


            vertices_out = [points]

            isovists_verts = [points_isovist]           

            #outputs           
            self.outputs["Vertices Out"].sv_set(points)
            self.outputs["Isovists Vertices"].sv_set(points_isovists)

def register():
    if vis is not None:
        bpy.utils.register_class(SvMegapolisIsovists)

def unregister():
    if vis is not None:
        bpy.utils.unregister_class(SvMegapolisIsovists)
