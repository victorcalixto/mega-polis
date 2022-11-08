import bpy
from bpy.props import IntProperty, EnumProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import pandas as pd

Correlation_method = namedtuple('CorrelationMethod', ['pearson', 'kendall','spearman'])
CORRELATIONMETHOD = Correlation_method('pearson','kendall','spearman')
correlationmethod_items = [(i, i, '') for i in CORRELATIONMETHOD]

class SvMegapolisCorrelationWith(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Correlation With
    Tooltip: Correlates a Dataframe with a Series using the methods; pearson, kendall, or spearman 
    """
    bl_idname = 'SvMegapolisCorrelationWith'
    bl_label = 'Correlation With'
    bl_icon = 'MESH_DATA'

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status
        updateNode(self,context)

    #Blender Properties Buttons
    
    correlation: EnumProperty(
        name='Method', items=correlationmethod_items,
        default="pearson",
        description='Choose a correlation method', 
        update=update_sockets)

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Dataframe")
        self.inputs.new('SvStringsSocket', "Series With")

        # outputs
        self.outputs.new('SvStringsSocket', "Correlation With")

    def draw_buttons(self,context, layout):
        layout.prop(self, 'correlation', expand=False)

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
         
        if not self.inputs["Dataframe"].is_linked or not self.inputs["Series With"].is_linked:
            return
        self.dataframe = self.inputs["Dataframe"].sv_get(deepcopy = False)
        self.series = self.inputs["Series With"].sv_get(deepcopy = False)

        series_with = self.series[0]
        df = self.dataframe
        data = df.corrwith(series_with, method=self.correlation)
        corr_with = [data]

        ## Output

        self.outputs["Correlation With"].sv_set(corr_with)


def register():
    if pd is not None:
        bpy.utils.register_class(SvMegapolisCorrelationWith)

def unregister():
    if pd is not None:
        bpy.utils.unregister_class(SvMegapolisCorrelationWith)
