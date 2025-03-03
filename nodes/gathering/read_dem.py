import bpy
import rasterio as rio
import numpy as np
from sverchok.node_tree import SverchCustomTreeNode


# Megapolis Dependencies

def make_faces(x_shape, y_shape):
    """Generate faces for a grid based on the shape."""
    return [
        [x * x_shape + y, x * x_shape + y + 1, (x + 1) * x_shape + y + 1, (x + 1) * x_shape + y]
        for x in range(y_shape - 1) for y in range(x_shape - 1)
    ]


class SvMegapolisReadDem(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Read DEM
    Tooltip: Read a Digital Elevation Model file (GeoTIFF)
    """
    bl_idname = 'SvMegapolisReadDem'
    bl_label = 'Read DEM'
    bl_icon = 'VIEW_PERSPECTIVE'
    sv_dependencies = {'rasterio'}

    def sv_init(self, context):
        """Initialize the inputs and outputs for the node."""
        # Inputs
        self.inputs.new('SvFilePathSocket', "Path")
        
        # Outputs
        self.outputs.new('SvVerticesSocket', "Vertices")
        self.outputs.new('SvStringsSocket', "Faces")
        self.outputs.new('SvStringsSocket', "DEM data")

    def process(self):
        """Process the DEM file and set the outputs."""
        if not self.inputs["Path"].is_linked:
            return

        self.path = self.inputs["Path"].sv_get(deepcopy=False)
        file_path = self.path[0][0]

        with rio.open(file_path) as dem:
            dem_arr = dem.read(1).astype('float64')

            dim_x = dem.width
            dim_y = dem.height

            band1 = dem.read(1)
            height, width = band1.shape
            cols, rows = np.meshgrid(np.arange(width), np.arange(height))

            xs, ys = rio.transform.xy(dem.transform, rows, cols)
            lons = np.array(xs)
            lats = np.array(ys)

            xyz = np.stack((lons, lats, band1), -1)

            grid = make_faces(dim_x, dim_y)

            xyz = np.reshape(xyz, (dim_x * dim_y, 3))

            vertices = [xyz]
            faces = [grid]
            dem_data = dem_arr

            # Set the outputs
            self.outputs["Vertices"].sv_set(vertices)
            self.outputs["Faces"].sv_set(faces)
            self.outputs["DEM data"].sv_set(dem_data)


def register():
    """Register the custom node class."""
    bpy.utils.register_class(SvMegapolisReadDem)


def unregister():
    """Unregister the custom node class."""
    bpy.utils.unregister_class(SvMegapolisReadDem)

