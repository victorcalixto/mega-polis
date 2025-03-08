import bpy
import json
from collections import namedtuple

from bpy.props import EnumProperty
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


PlotType = namedtuple('PlotType', ['line', 'scatter', 'bar', 'pie', 'area', 'timeline'])
PLOT_TYPES = PlotType('line', 'scatter', 'bar', 'pie', 'area', 'timeline')
PLOT_TYPE_ITEMS = [(i, i, '') for i in PLOT_TYPES]


class SvMegapolisDashboardCreatePlotly(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Dashboard Create Plotly
    Tooltip: Dashboard Create Plotly
    """
    bl_idname = 'SvMegapolisDashboardCreatePlotly'
    bl_label = 'Dashboard Create Plotly'
    bl_icon = 'IMAGE_RGB'

    def update_sockets(self, context):
        """Need to do UX transformation before updating node."""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self, context)

    plottype: EnumProperty(
        name="Plot Type",
        items=PLOT_TYPE_ITEMS,
        description="CSR Projection Number",
        default='line',
        update=update_sockets
    )

    def sv_init(self, context):
        # Inputs
        self.inputs.new('SvStringsSocket', "Figure Name")
        self.inputs.new('SvStringsSocket', "Dataframe")
        self.inputs.new('SvStringsSocket', "Parameters Plot")

        # Outputs
        self.outputs.new('SvStringsSocket', "Dashboard Plotly Figure")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'plottype')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        if not (
            self.inputs["Figure Name"].is_linked and
            self.inputs["Dataframe"].is_linked and
            self.inputs["Parameters Plot"].is_linked
        ):
            return

        figname = self.inputs["Figure Name"].sv_get(deepcopy=False)
        dataframe = self.inputs["Dataframe"].sv_get(deepcopy=False)
        parameters_plot = self.inputs["Parameters Plot"].sv_get(deepcopy=False)

        parameters = parameters_plot[0]
        figure_name = figname[0][0]
        df_in = dataframe
        plot_type = self.plottype

        def plot_figure(params, p_type):
            figure_values = list(params.values())
            figure_keys = list(params.keys())

            result = df_in.to_json()
            parsed = json.loads(result)

            figure_list = ', '.join(
                f"{key}='{value}'" for key, value in zip(figure_keys, figure_values)
            )

            figure_str = (
                f"{figure_name}_ = pd.DataFrame.from_dict({parsed})\n"
                f"{figure_name} = px.{p_type}({figure_name}_, {figure_list})\n"
            )
            return figure_str

        plotly_figure = plot_figure(parameters, plot_type)
        self.outputs["Dashboard Plotly Figure"].sv_set(plotly_figure)


def register():
    bpy.utils.register_class(SvMegapolisDashboardCreatePlotly)


def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardCreatePlotly)

