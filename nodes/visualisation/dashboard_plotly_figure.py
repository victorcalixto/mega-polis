import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy


#Megapolis Dependencies


class SvMegapolisDashboardPlotlyFigure(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Dashboard Plotly Figure
    Tooltip: Dashboard Plotly Figure
    """
    bl_idname = 'SvMegapolisDashboardPlotlyFigure'
    bl_label = 'Dashboard Plotly Figure'
    bl_icon = 'MESH_DATA'

    
    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self,context)
   
    #Blender Properties Buttons
    
    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Figure Name")

        #Outputs
        self.outputs.new('SvStringsSocket',"Plotly Figure")

    def process(self):
    
        if not self.inputs["Figure Name"].is_linked:
            return
        self.name = self.inputs["Figure Name"].sv_get(deepcopy = False)

        plotly_figure_name = self.name[0][0]
        
        plot  = f"st.plotly_chart({plotly_figure_name}, use_container_width=True) \n"

        plot_plotly_figure = plot
        ## Output

        self.outputs["Plotly Figure"].sv_set(plot+plotly_figure)

def register():
    bpy.utils.register_class(SvMegapolisDashboardPlotlyFigure)

def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardPlotlyFigure)