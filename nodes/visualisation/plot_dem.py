import bpy
from bpy.props import IntProperty, BoolProperty, EnumProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import richdem as rd

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

class SvMegapolisPlotDem(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Plot Dem
    Tooltip: Plot a Dem Array 
    """
    bl_idname = 'SvMegapolisPlotDem'
    bl_label = 'Plot Dem'
    bl_icon = 'MESH_DATA'

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status
        updateNode(self,context)

    #Blender Properties Buttons
    
    run: BoolProperty(
        name='run',
        default=False,
        description='Plot!', 
        update=update_sockets)
    
    axes: BoolProperty(
        name='axes',
        default=False,
        description='Boolean to show Plot Axes', 
        update=update_sockets)
    

    width:IntProperty(
        name='width',
        default=8,
        description='Plot Width', 
        update=update_sockets)
    
    height:IntProperty(
        name='height',
        default=5,
        description='Plot Width', 
        update=update_sockets)
    
    colour: EnumProperty(
        name='colour', items=sequential_items,
        default="inferno",
        description='Choose a Sequential Colormap Theme', 
        update=update_sockets)


    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Dem Array")
        
        # outputs
        

    def draw_buttons(self,context, layout):
        layout.prop(self, 'run', expand=False)
        layout.prop(self, 'axes', expand=False)
        layout.prop(self, 'width', expand=False)
        layout.prop(self, 'height', expand=False)
        layout.prop(self, 'colour')


    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
         
        if not self.inputs["Dem Array"].is_linked:
            return
        self.array = self.inputs["Dem Array"].sv_get(deepcopy = False)
        
        if self.run == True:
            rd.rdShow(self.array, ignore_colours=[0], axes=self.axes, cmap=self.colour, figsize=(self.width,self.height))

        ## Output
        

def register():
    if rd is not None:
        bpy.utils.register_class(SvMegapolisPlotDem)

def unregister():
    if rd is not None:
        bpy.utils.unregister_class(SvMegapolisPlotDem)
