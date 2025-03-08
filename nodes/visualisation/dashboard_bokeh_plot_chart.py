import bpy

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


class SvMegapolisDashboardBokehPlotChart(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Dashboard Bokeh Plot Chart
    Tooltip: Dashboard Bokeh Plot Chart
    """
    bl_idname = 'SvMegapolisDashboardBokehPlotChart'
    bl_label = 'Dashboard Bokeh Plot Chart'
    bl_icon = 'XRAY'

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
        self.outputs.new('SvStringsSocket', "Bokeh Chart")

    def process(self):
        if not self.inputs["Figure Name"].is_linked:
            return

        self.figname = self.inputs["Figure Name"].sv_get(deepcopy=False)
        figure_name = self.figname[0][0]

        plot = (
            f"st.bokeh_chart({figure_name}, use_container_width=False)\n"
        )

        st_bokeh_plot_chart = plot

        # Output
        self.outputs["Bokeh Chart"].sv_set(st_bokeh_plot_chart)


def register():
    bpy.utils.register_class(SvMegapolisDashboardBokehPlotChart)


def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardBokehPlotChart)

