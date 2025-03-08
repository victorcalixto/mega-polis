import bpy
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


class SvMegapolisDashboardPlotlyFigure(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Dashboard Plotly Figure
    Tooltip: Dashboard Plotly Figure
    """
    bl_idname = 'SvMegapolisDashboardPlotlyFigure'
    bl_label = 'Dashboard Plotly Figure'
    bl_icon = 'IMAGE_RGB_ALPHA'

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """Need to do UX transformation before updating node."""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self, context)

    # Blender Properties Buttons
    def sv_init(self, context):
        # Inputs
        self.inputs.new('SvStringsSocket', "Figure Name")

        # Outputs
        self.outputs.new('SvStringsSocket', "Plotly Figure")

    def process(self):
        if not self.inputs["Figure Name"].is_linked:
            return
        
        self.figname = self.inputs["Figure Name"].sv_get(deepcopy=False)
        plotly_figure_name = self.figname[0][0]

        plot = f"""
st.plotly_chart({plotly_figure_name}, use_container_width=True) \n
        """

        plot_plotly_figure = plot
        
        # Output
        self.outputs["Plotly Figure"].sv_set(plot_plotly_figure)


def register():
    bpy.utils.register_class(SvMegapolisDashboardPlotlyFigure)


def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardPlotlyFigure)

