import bpy
from bpy.props import EnumProperty
from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

# Megapolis Dependencies
try:
    from matplotlib import cm
except ImportError:
    pass

# Define sequential colormap themes
Sequential = namedtuple('Sequential', [
    'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
    'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn', 'binary',
    'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'hot',
    'afmhot', 'gist_heat', 'copper'
])
SEQUENTIAL = Sequential(
    'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
    'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn', 'binary',
    'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'hot',
    'afmhot', 'gist_heat', 'copper'
)
sequential_items = [(i, i, '') for i in SEQUENTIAL]


class SvMegapolisSequentialColormap(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Sequential Colormap
    Tooltip: Applies a sequential colormap to a set of normalized values.
    """
    bl_idname = 'SvMegapolisSequentialColormap'
    bl_label = 'Sequential Colormap'
    bl_icon = 'COLORSET_12_VEC'

    # Hide interactive sockets
    def update_sockets(self, context):
        """ Perform UX transformation before updating node """
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self, context)

    # Blender Properties Buttons
    sequential_colormap: EnumProperty(
        name='Sequential Colormap',
        items=sequential_items,
        default="inferno",
        description='Choose a Sequential Colormap Theme',
        update=update_sockets
    )

    def sv_init(self, context):
        """ Initialize inputs and outputs """
        # Inputs
        self.inputs.new('SvStringsSocket', "Normalised Values")

        # Outputs
        self.outputs.new('SvStringsSocket', "Colormap")

    def draw_buttons(self, context, layout):
        """ Draw buttons for colormap selection """
        layout.prop(self, 'sequential_colormap')

    def draw_buttons_ext(self, context, layout):
        """ Extend button layout """
        self.draw_buttons(context, layout)

    def process(self):
        """ Process the normalized values and apply colormap """
        if not self.inputs["Normalised Values"].is_linked:
            return

        values = self.inputs["Normalised Values"].sv_get(deepcopy=False)
        normalised_values = values[0][0]

        # Apply selected colormap
        cmap = cm.get_cmap(self.sequential_colormap)
        new_colours = [cmap(i) for i in normalised_values]

        # Output colormap
        self.outputs["Colormap"].sv_set(new_colours)


def register():
    bpy.utils.register_class(SvMegapolisSequentialColormap)


def unregister():
    bpy.utils.unregister_class(SvMegapolisSequentialColormap)

