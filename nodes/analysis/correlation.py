import bpy
from bpy.props import EnumProperty
from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

# Define correlation methods
CorrelationMethod = namedtuple('CorrelationMethod', ['pearson', 'kendall', 'spearman'])
CORRELATION_METHODS = CorrelationMethod('pearson', 'kendall', 'spearman')
correlation_method_items = [(method, method, '') for method in CORRELATION_METHODS]


class SvMegapolisCorrelation(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Correlation
    Tooltip: Correlates a Dataframe using the methods; pearson, kendall, or spearman.
    """
    bl_idname = 'SvMegapolisCorrelation'
    bl_label = 'Correlation'
    bl_icon = 'SNAP_EDGE'
    sv_dependencies = {'pandas'}

    # Blender Properties Buttons
    correlation: EnumProperty(
        name='Method',
        items=correlation_method_items,
        default="pearson",
        description='Choose a correlation method',
        update=lambda self, context: updateNode(self, context)
    )

    def sv_init(self, context):
        """Initialize inputs and outputs."""
        self.inputs.new('SvStringsSocket', "Dataframe")
        self.outputs.new('SvStringsSocket', "Correlation")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'correlation', expand=False)

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        """Process the correlation calculation."""
        if not self.inputs["Dataframe"].is_linked:
            return

        dataframe = self.inputs["Dataframe"].sv_get(deepcopy=False)

        if not dataframe:
            return

        # Compute correlation
        correlation_matrix = dataframe.corr(method=self.correlation)

        # Output the correlation matrix
        self.outputs["Correlation"].sv_set([correlation_matrix])


def register():
    bpy.utils.register_class(SvMegapolisCorrelation)


def unregister():
    bpy.utils.unregister_class(SvMegapolisCorrelation)

