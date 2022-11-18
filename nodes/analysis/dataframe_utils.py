import bpy
from bpy.props import IntProperty, EnumProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

#Megapolis Dependencies
from megapolis.dependencies import pandas as pd
import io

Info_type = namedtuple('InfoType', ['info','head','tail','decribe'])
INFOTYPE = Info_type('info','head','tail','describe')
infotype_items = [(i, i, '') for i in INFOTYPE]

class SvMegapolisDataframeUtils(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Dataframe Utils
    Tooltip: Dataframe Utilits for Exploratory Data Analysis: info, head, tail, and decribe  
    """
    bl_idname = 'SvMegapolisDataframeUtils'
    bl_label = 'Dataframe Utils'
    bl_icon = 'MESH_DATA'

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status
        

        if self.infotype in INFOTYPE.head or self.infotype in INFOTYPE.tail: 
            set_hide(self.inputs['Dataframe'], False)
            set_hide(self.inputs['Number'], False)
        else:
            set_hide(self.inputs['Dataframe'], False)
            set_hide(self.inputs['Number'], True)

        updateNode(self,context)

    #Blender Properties Buttons
    
    infotype: EnumProperty(
        name='Function', items=infotype_items,
        default="info",
        description='Choose a Function to Explore the Data', 
        update=update_sockets)
    
    numberb : IntProperty(
        name = "number",
        default = 5,
        min = 1,
        update = updateNode)


    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Dataframe")
        self.inputs.new('SvStringsSocket', "Number").prop_name='numberb'
        
        self.inputs['Number'].hide_safe = True 
        
        # outputs
       
        self.outputs.new('SvStringsSocket',"Value")

    def draw_buttons(self,context, layout):
        layout.prop(self, 'infotype', expand=False)
        #if self.infotype == 'head' or self.infotype == 'tail':
        #    layout.prop(self, 'numberb')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        
        if self.infotype in INFOTYPE.head or self.infotype in INFOTYPE.tail:
            if not self.inputs["Dataframe"].is_linked:
                return
            self.df = self.inputs["Dataframe"].sv_get(deepcopy = False)
            self.number= self.inputs["Number"].sv_get(deepcopy = False)
            df = self.df
            number= self.number
        else:
            if not self.inputs["Dataframe"].is_linked: 
                return       
            self.df = self.inputs["Dataframe"].sv_get(deepcopy = False)
            df = self.df

        if self.infotype in INFOTYPE.head:
            value= df.head(number[0][0])
        
        elif self.infotype in INFOTYPE.tail:
        
            value = df.tail(number[0][0])
        
        elif self.infotype in INFOTYPE.info:
            buf = io.StringIO()
            value= df.info(buf=buf)
            value = buf.getvalue()
        else:
            value = df.describe()
        
        ## Output

        self.outputs["Value"].sv_set(value)
        
def register():
    if pd is not None:
        bpy.utils.register_class(SvMegapolisDataframeUtils)

def unregister():
    if pd is not None:
        bpy.utils.unregister_class(SvMegapolisDataframeUtils)
