import bpy
from bpy.props import EnumProperty
from collections import namedtuple

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


# Define a named tuple for colormaps
Sequential = namedtuple(
    "Sequential",
    (
        "viridis", "plasma", "inferno", "magma", "cividis", "Greys", "Purples",
        "Blues", "Greens", "Oranges", "Reds", "YlOrBr", "YlOrRd", "OrRd",
        "PuRd", "RdPu", "BuPu", "GnBu", "PuBu", "YlGnBu", "PuBuGn", "BuGn",
        "YlGn", "binary", "gist_yarg", "gist_gray", "gray", "bone", "pink",
        "spring", "summer", "autumn", "winter", "cool", "Wistia", "hot",
        "afmhot", "gist_heat", "copper"
    )
)

SEQUENTIAL = Sequential(*Sequential._fields)
sequential_items = [(i, i, "") for i in SEQUENTIAL]


class SvMegapolisColormap(SverchCustomTreeNode, bpy.types.Node):
    """
    A Sverchok node that provides a colormap selection.

    Allows the user to select a colormap from various predefined sequential colormaps.
    The selected colormap is output as a string.
    """
    bl_idname = "SvMegapolisColormap"
    bl_label = "ColorMap"
    bl_icon = "COLOR"

    def update_colormap_sockets(self, context):
        """Perform UX transformations before updating the node."""
        updateNode(self, context)

    # Blender Properties Buttons
    sequential: EnumProperty(
        name="Colormap",
        items=sequential_items,
        default=SEQUENTIAL.inferno,
        description="Choose a Colormap Theme",
        update=update_colormap_sockets,
    )

    def sv_init(self, context):
        """Initialize node outputs."""
        self.outputs.new("SvStringsSocket", "Colormap")

    def draw_buttons(self, context, layout):
        """Draw UI buttons."""
        layout.prop(self, "sequential")

    def draw_buttons_ext(self, context, layout):
        """Draw extended UI buttons."""
        self.draw_buttons(context, layout)

    def process(self):
        """Process node logic."""
        self.outputs["Colormap"].sv_set(self.sequential)


def register():
    bpy.utils.register_class(SvMegapolisColormap)


def unregister():
    bpy.utils.unregister_class(SvMegapolisColormap)

