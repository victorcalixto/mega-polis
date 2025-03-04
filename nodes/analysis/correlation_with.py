import bpy
from bpy.props import EnumProperty
from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

# Define correlation methods
CorrelationMethod = namedtuple('CorrelationMethod', ['pearson', 'kendall', 'spearman'])
CORRELATION_METHODS = CorrelationMethod('pearson', 'kendall', 'spearman')
correlation_method_items = [(method, method, '') for method in CORRELATION_METHODS]


class SvMegapolisCorrelationWith(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Correlation With
    Tooltip: Correlates a DataFrame with a Series using the methods: pearson, kendall, or spearman.
    """
    bl_idname = 'SvMegapolisCorrelationWith'
    bl_label = 'Correlation With'
    bl_icon = 'PAUSE'
    sv_dependencies = {'pandas'}

    # Blender Property for correlation method selection
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
        self.inputs.new('SvStringsSocket', "Series With")
        self.outputs.new('SvStringsSocket', "Correlation With")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'correlation', expand=False)

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        """Compute correlation between DataFrame and Series."""
        if not self.inputs["Dataframe"].is_linked or not self.inputs["Series With"].is_linked:
            return

        dataframe = self.inputs["Dataframe"].sv_get(deepcopy=False)
        series_with = self.inputs["Series With"].sv_get(deepcopy=False)

        if not dataframe or not series_with:
            return

        # Compute correlation
        correlation_result = dataframe.corrwith(series_with[0], method=self.correlation)

        # Output result
        self.outputs["Correlation With"].sv_set([correlation_result])


def register():
    bpy.utils.register_class(SvMegapolisCorrelationWith)


def unregister():
    bpy.utils.unregister_class(SvMegapolisCorrelationWith)

