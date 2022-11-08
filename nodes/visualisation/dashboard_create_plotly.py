import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode



Plot_Type = namedtuple('PlotType', ['line', 'scatter','bar','pie','area','timeline'])
PLOTTYPE = Plot_Type('line', 'scatter','bar','pie','area','timeline')
plottype_items = [(i, i, '') for i in PLOTTYPE]



#Megapolis Dependencies
import json 

class SvMegapolisDashboardCreatePlotly(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Dashboard Create Plotly
    Tooltip: Dashboard Create Plotly
    """
    bl_idname = 'SvMegapolisDashboardCreatePlotly'
    bl_label = 'Dashboard Create Plotly'
    bl_icon = 'MESH_DATA'

    
    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self,context)
    
    plottype: EnumProperty(
        name="Plot Type", items=plottype_items,
        description="CSR Projection Number",
        default='line',
        update=update_sockets)
    
      
    #Blender Properties Buttons
    
    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Figure Name")
        self.inputs.new('SvStringsSocket', "Dataframe")
        self.inputs.new('SvStringsSocket', "Parameters Plot")

        #Outputs
        self.outputs.new('SvStringsSocket',"Dashboard Plotly Figure")
    
    def draw_buttons(self,context, layout):
        layout.prop(self, 'plottype')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)


    def process(self):
    
        if not self.inputs["Figure Name"].is_linked or not self.inputs["Dataframe"].is_linked or not self.inputs["Parameters Plot"].is_linked:
            return
        self.figname = self.inputs["Figure Name"].sv_get(deepcopy = False)
        self.dataframe = self.inputs["Dataframe"].sv_get(deepcopy = False)
        self.parameters_plot= self.inputs["Parameters Plot"].sv_get(deepcopy = False)

        parameters= self.parameters_plot[0]
        figure_name=self.figname[0][0]
        df_in = self.dataframe
        plot_type = self.plottype
        ## Output

        def plot_figure(parameters,plot_type):
            figure_values = list(parameters.values())
            figure_keys = list(parameters.keys())

            result = df_in.to_json()
            parsed = json.loads(result)

            figure_list =''

            for i in range(0,len(figure_values)):
                if i == len(figure_values)-1:
                    figure_list=figure_list+f"{figure_keys[i]}='{figure_values[i]}'"
                else:
                    figure_list=figure_list+f"{figure_keys[i]}='{figure_values[i]}',"

            figure_str=f"""
{figure_name}_=pd.DataFrame.from_dict({parsed}) \n{figure_name} = px.{plot_type}({figure_name}_,{figure_list}) \n
                        """
            
            return figure_str

        figure = plot_figure(parameters,plot_type)

        plotly_figure = figure

        self.outputs["Dashboard Plotly Figure"].sv_set(plotly_figure)

def register():
    bpy.utils.register_class(SvMegapolisDashboardCreatePlotly)

def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardCreatePlotly)
