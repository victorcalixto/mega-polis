import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

#Megapolis Dependencies
import json 

class SvMegapolisDashboardPlotlyScatter(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Dashboard Plotly Scatter
    Tooltip: Dashboard Plotly Scatter
    """
    bl_idname = 'SvMegapolisDashboardPlotlyScatter'
    bl_label = 'Dashboard Plotly Scatter'
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
        self.inputs.new('SvStringsSocket', "Dataframe")
        self.inputs.new('SvStringsSocket', "Scatter Parameters")

        #Outputs
        self.outputs.new('SvStringsSocket',"Dashboard Plotly Scatter")

    def process(self):
    
        if not self.inputs["Figure Name"].is_linked or not self.inputs["Dataframe"].is_linked or  not self.inputs["Scatter Parameters"].is_linked:
            return
        self.figname = self.inputs["Figure Name"].sv_get(deepcopy = False)
        self.dataframe = self.inputs["Dataframe"].sv_get(deepcopy = False)
        self.scatter= self.inputs["Scatter Parameters"].sv_get(deepcopy = False)

        figure_name=self.figname[0][0]
        
        scatter_parameters=self.scatter[0]
        df_in = self.dataframe

        scatter_values = list(scatter_parameters.values())
        scatter_keys = list(scatter_parameters.keys())

        result = df_in.to_json()
        parsed = json.loads(result)

        scatter_list =''

        for i in range(0,len(scatter_values)):
            if i == len(scatter_values)-1:
                scatter_list=scatter_list+f"{scatter_keys[i]}='{scatter_values[i]}'"
            else:
                scatter_list=scatter_list+f"{scatter_keys[i]}='{scatter_values[i]}',"

        scatter_str=f"""
{figure_name}_=pd.DataFrame.from_dict({parsed}) \n{figure_name} = px.scatter({figure_name}_,{scatter_list}) \n
                     """

        plotly_scatter = scatter_str

        ## Output

        self.outputs["Dashboard Plotly Scatter"].sv_set(plotly_scatter)

def register():
    bpy.utils.register_class(SvMegapolisDashboardPlotlyScatter)

def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardPlotlyScatter)
