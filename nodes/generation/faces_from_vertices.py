import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

#Megapolis Dependencies

def makeFaces(list,x_shape,y_shape):
    for x in range(y_shape-1):
        for y in range(x_shape-1):
            list.append([x*x_shape+y,x*x_shape+y+1,(x+1)*x_shape+y+1,(x+1)*x_shape+y])


class SvMegapolisFacesFromVertices(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: FacesFromVertices
    Tooltip: Faces from Vertices
    """
    bl_idname = 'SvMegapolisFacesFromVertices'
    bl_label = 'Faces From Vertices'
    bl_icon = 'MESH_DATA'
    

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvVerticesSocket', "Vertices")
        self.inputs.new('SvStringsSocket', "X Shape")
        self.inputs.new('SvStringsSocket', "Y Shape")

        #outputs
        self.outputs.new('SvStringsSocket', "Faces")

    def process(self):
        if not self.inputs["Vertices"].is_linked or not self.inputs["X Shape"].is_linked or not self.inputs["Y Shape"].is_linked:
            return
        self.vertices = self.inputs["Vertices"].sv_get(deepcopy = False)
        self.x = self.inputs["X Shape"].sv_get(deepcopy = False)
        self.y = self.inputs["Y Shape"].sv_get(deepcopy = False)
      
        x_shape= self.x[0][0]

        y_shape = self.y[0][0]

        faces_s = []

        makeFaces(faces_s,x_shape,y_shape)

        faces = [faces_s]

        #Outputs       
        self.outputs["CSV List"].sv_set(faces)

def register():
    bpy.utils.register_class(SvMegapolisFacesFromVertices)

def unregister():
    bpy.utils.unregister_class(SvMegapolisFacesFromVertices)
