import bpy
from bpy.props import BoolProperty, EnumProperty

from collections import namedtuple

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import matplotlib

try:
    from matplotlib.colors import ListedColormap, LinearSegmentedColormap
    from matplotlib import cm
except:
    pass

Sequential = namedtuple('Sequential',
     ['viridis', 'plasma', 'inferno', 'magma', 'cividis','Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
      'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
      'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn','binary', 'gist_yarg', 'gist_gray', 'gray', 'bone',
      'pink', 'spring', 'summer', 'autumn', 'winter', 'cool',
      'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper'])
SEQUENTIAL = Sequential('viridis', 'plasma', 'inferno', 'magma', 'cividis','Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
      'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
      'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn','binary', 'gist_yarg', 'gist_gray', 'gray', 'bone',
      'pink', 'spring', 'summer', 'autumn', 'winter', 'cool',
      'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper')
sequential_items = [(i, i, '') for i in SEQUENTIAL]



class SvMegapolisColormap(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Colormap
    Tooltip: Colormap
    """
    bl_idname = 'SvMegapolisColormap'
    bl_label = 'ColorMap'
    bl_icon = 'MESH_DATA'
    

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self,context)

    #Blender Properties Buttons

    sequential: EnumProperty(
        name='colormap', items=sequential_items,
        default="inferno",
        description='Choose a Colormap Theme', 
        update=update_sockets)


    def sv_init(self, context):
        
        # inputs
        # outputs
        
        #Output
        self.outputs.new('SvStringsSocket', "Colormap")
        
        
    def draw_buttons(self,context, layout):
        layout.prop(self, 'sequential')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
         
        ## Output
        self.outputs["Colormap"].sv_set(self.sequential)
            
def register():
    bpy.utils.register_class(SvMegapolisColormap)

def unregister():
    bpy.utils.unregister_class(SvMegapolisColormap)
