import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import rasterio as rio
import numpy as np

def makeFaces(x_shape,y_shape):
    xy = [[x*x_shape+y,x*x_shape+y+1,(x+1)*x_shape+y+1,(x+1)*x_shape+y] for x in range(y_shape-1) for y in range(x_shape-1)]
    return xy


class SvMegapolisReadDem(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Read DEM
    Tooltip: Read a Digital Elevation Model file (geotiff)
    """
    bl_idname = 'SvMegapolisReadDem'
    bl_label = 'Read DEM'
    bl_icon = 'MESH_DATA'
    sv_dependencies = {'rasterio'}

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvFilePathSocket', "Path")
       
        #outputs
        self.outputs.new('SvVerticesSocket', "Vertices")
        self.outputs.new('SvStringsSocket', "Faces")
        self.outputs.new('SvStringsSocket', "DEM data")

    def process(self):
        if not self.inputs["Path"].is_linked:
            return
        self.path = self.inputs["Path"].sv_get(deepcopy = False)
      
        path = self.path[0][0]

        dem = rio.open(path)
        dem_arr = dem.read(1).astype('float64')

        dim_x = dem.width
        dim_y = dem.height
        
        #origin = dem.transform * (0, 0)
        
        band1 = dem.read(1)
        height = band1.shape[0]
        width = band1.shape[1]
        cols, rows = np.meshgrid(np.arange(width), np.arange(height))

        xs, ys = rio.transform.xy(dem.transform, rows, cols)
        lons= np.array(xs)
        lats = np.array(ys)

        xyz = np.stack((lons, lats,band1),-1)
        dem.sample([lons,lats])

        grid = makeFaces(dim_x,dim_y)

        xyz= np.reshape(xyz , (dim_x * dim_y , 3))

        vertices = [xyz]

        faces = [grid]

        dem_data = dem_arr

        self.outputs["Vertices"].sv_set(vertices)
        self.outputs["Faces"].sv_set(faces)
        self.outputs["DEM data"].sv_set(dem_data)


def register():
    bpy.utils.register_class(SvMegapolisReadDem)


def unregister():
    bpy.utils.unregister_class(SvMegapolisReadDem)
