import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy


#Megapolis Dependencies
from megapolis.dependencies import rasterio as rio
from megapolis.dependencies import pandas as pd
from rasterio.plot import show
from matplotlib import pyplot as plt
import numpy as np



def makeFaces(list,x_shape,y_shape):
    for x in range(y_shape-1):
        for y in range(x_shape-1):
            list.append([x*x_shape+y,x*x_shape+y+1,(x+1)*x_shape+y+1,(x+1)*x_shape+y])


if rio is None:
    add_dummy('SvMegapolisReadDem', 'Read DEM', 'rasterio')
else:
    class SvMegapolisReadDem(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: Read DEM
        Tooltip: Read a Digital Elevation Model file (geotiff)
        """
        bl_idname = 'SvMegapolisReadDem'
        bl_label = 'Read DEM'
        bl_icon = 'MESH_DATA'
        

        def sv_init(self, context):
            # inputs
            self.inputs.new('SvFilePathSocket', "Path")
           
            #outputs
            self.outputs.new('SvStringsSocket', "Vertices")
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
            
            origin = dem.transform * (0, 0)

            coords = []

            band1 = dem.read(1)
            height = band1.shape[0]
            width = band1.shape[1]
            cols, rows = np.meshgrid(np.arange(width), np.arange(height))

            xs, ys = rio.transform.xy(dem.transform, rows, cols)
            lons= np.array(xs)
            lats = np.array(ys)


            #print(lons[0],lats[0])

            #for x in np.nditer(lons):
            #   for y in np.nditer(lats):


            xyz = np.stack((lons, lats,band1),-1)
            #print(xyz)
            dem.sample([lons,lats])

            #print(xyz)


            #print(xy[0])
            #dataset1 = dem
            #val = dataset1.read(1)
            #no_data=dataset1.nodata
            #data = [(dataset1.xy(x,y)[0],dataset1.xy(x,y)[1],val[x,y]) for x,y in np.ndindex(val.shape) if val[x,y] != no_data]
            #lon = [i[0] for i in data]
            #lat = [i[1] for i in data]
            #d = [i[2] for i in data]
            #res = pd.DataFrame({"long":lon,'lat':lat,"data":val})


            #xy = list(zip(lons,lats))
            #
            #for x in range(0,dim_x):
            #   for y in range(0,dim_y):
            #       coords.append(dem.xy(x,y))  #input px, py  
                 
            #print(res)


            """
            fig, ax = plt.subplots(1, figsize=(12, 12))
            show(dem, cmap='Greys_r', ax=ax)
            plt.axis("off")
            plt.show()
            """
            #print(dem.indexes)


            faces_m = []

            makeFaces(faces_m,dim_x,dim_y)

            #print(faces_m)

            faces_arr = np.array(faces_m)

            #print(faces_arr)

            print(xyz.shape)

            xyz= np.reshape(xyz , (dim_x * dim_y , 3))

            print(xyz.shape)


            xyz = xyz.tolist()


            #print(faces_arr)

            vertices = [xyz]



            #print(faces_a)
            #faces_m = np.array_split(faces_arr, dem.height)
            #print(faces_m)

            faces = [faces_m]
            dem_data = dem_arr

            '''

            fig, ax = plt.subplots(1, figsize=(12, 12))
            show(dem_array, cmap='Greys_r', ax=ax)
            show(dem_array, contour=True, ax=ax, linewidths=0.7)
            plt.axis("off")
            plt.show()


            import richdem as rd
            dem_richdem = rd.rdarray(dem_array, no_data=-9999)

            fig = rd.rdShow(dem_richdem, axes=False, cmap=’bone’, figsize=(16, 10));
            fig

            dem_slope = rd.TerrainAttribute(dem_richdem, attrib=’slope_degrees’)
            rd.rdShow(dem_slope, axes=False, cmap=’YlOrBr’, figsize=(16, 10));


            dem_filled = rd.FillDepressions(dem_richdem, in_place=False)
            dem_filled_fig = rd.rdShow(dem_filled, ignore_colours=[0], axes=False, cmap=’jet’, vmin=fig[‘vmin’], vmax=fig[‘vmax’], figsize=(16,10))



            '''
           
            self.outputs["Vertices"].sv_set(vertices)
            self.outputs["Faces"].sv_set(faces_m)
            self.outputs["DEM data"].sv_set(dem_data)

def register():
    if rio is not None:
        bpy.utils.register_class(SvMegapolisReadDem)

def unregister():
    if rio is not None:
        bpy.utils.unregister_class(SvMegapolisReadDem)
