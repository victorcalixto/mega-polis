import bpy
from bpy.props import EnumProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy


#Megapolis Dependencies
from megapolis.dependencies import pandas as pd

Correlation_method = namedtuple('CorrelationMethod', ['pearson', 'kendall','spearman'])
CORRELATIONMETHOD = Correlation_method('pearson','kendall','spearman')
correlationmethod_items = [(i, i, '') for i in CORRELATIONMETHOD]

if pd is None:
    add_dummy('SvMegapolisCorrelation', 'Correlation', 'pandas')
else:
    class SvMegapolisCorrelation(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: Correlation
        Tooltip: Correlates a Dataframe using the methods; pearson, kendall, or spearman 
        """
        bl_idname = 'SvMegapolisCorrelation'
        bl_label = 'Correlation'
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
            # outputs
            self.outputs.new('SvStringsSocket', "Correlation")

        def draw_buttons(self,context, layout):
            layout.prop(self, 'correlation', expand=False)

        def draw_buttons_ext(self, context, layout):
            self.draw_buttons(context, layout)

        def process(self):
             
            if not self.inputs["Dataframe"].is_linked:
                return
            self.dataframe = self.inputs["Dataframe"].sv_get(deepcopy = False)

            df = self.dataframe
            data = df.corr(method=self.correlation)
            corr = [data]


            ## Output

            self.outputs["Correlation"].sv_set(corr)


def register():
    if pd is not None:
        bpy.utils.register_class(SvMegapolisCorrelation)

def unregister():
    if pd is not None:
        bpy.utils.unregister_class(SvMegapolisCorrelation)
