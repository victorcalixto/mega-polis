import bpy
from bpy.props import BoolProperty, EnumProperty

from collections import namedtuple

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib import cm



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



class SvMegapolisSequentialColormap(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Sequential Colormap
    Tooltip: Sequential Colormap
    """
    bl_idname = 'SvMegapolisSequentialColormap'
    bl_label = 'SequentialColorMap'
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
        name='sequential_colormap', items=sequential_items,
        default="inferno",
        description='Choose a Sequential Colormap Theme', 
        update=update_sockets)


    def sv_init(self, context):
        
        # inputs
        self.inputs.new('SvStringsSocket', "Normalised Values")



        # outputs
        
        #Output
        self.outputs.new('SvStringsSocket', "Colormap")
        
        
    def draw_buttons(self,context, layout):
        layout.prop(self, 'sequential')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        if not self.inputs["Normalised Values"].is_linked:
            return
        self.values = self.inputs["Normalised Values"].sv_get(deepcopy = False)

        normalised_values=self.values[0][0]


        newcolours = []
        cmap = cm.get_cmap(self.sequential)

        for i in normalised_values:
            newcolours.append(cmap(i))

        colours = newcolours
 
        ## Output
        self.outputs["Colormap"].sv_set(colours)
            
def register():
    bpy.utils.register_class(SvMegapolisSequentialColormap)

def unregister():
    bpy.utils.unregister_class(SvMegapolisSequentialColormap)
