import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from collections import namedtuple

#Megapolis Dependencies
from megapolis.dependencies import pandas as pd
from megapolis.dependencies import sklearn

try:
    import sklearn.datasets as datasets
except:
    pass



Dataframe = namedtuple('Dataframe', ['iris', 'california_housing','diabetes','digits','wine'])
DATAFRAME = Dataframe('iris', 'california_housing','diabetes','digits','wine')
dataframe_items = [(i, i, '') for i in DATAFRAME]


class SvMegapolisGetSampleDataframe(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Get Sample Dataframe
    Tooltip: Get a Dataframe Sample
    """
    bl_idname = 'SvMegapolisGetSampleDataframe'
    bl_label = 'Get Sample Dataframe'
    bl_icon = 'MESH_DATA'
    sv_dependencies = {'pandas'}
    # Hide Interactive Sockets
    
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self,context)

    #Blender Properties Buttons
    
    dataframe: EnumProperty(
        name='dataframe', items=dataframe_items,
        default="iris",
        description='Choose a Dataframe', 
        update=update_sockets)

    def sv_init(self, context):
        # inputs
       
        #outputs
        self.outputs.new('SvStringsSocket', "Dataframe")
    
    def draw_buttons(self,context, layout):
        layout.prop(self, 'dataframe')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)


    def process(self):
        if self.dataframe in DATAFRAME.iris:
            iris = datasets.load_iris(return_X_y=True, as_frame=True)
            df = list(iris)
            df = df[0]
            data = df

        elif self.dataframe in DATAFRAME.california_housing:
            housing = datasets.fetch_california_housing(return_X_y=True, as_frame=True)
            df = list(housing)
            df = df[0]
            data = df
        elif self.dataframe in DATAFRAME.diabetes:
            diabetes = datasets.load_diabetes(return_X_y=True, as_frame=True)
            df = list(diabetes)
            df = df[0]
            data = df
        elif self.dataframe in DATAFRAME.digits:
            digits = datasets.load_digits(return_X_y=True, as_frame=True)
            df = list(digits)
            df = df[0]
            data = df

        elif self.dataframe in DATAFRAME.wine:
            wine = datasets.load_wine(return_X_y=True, as_frame=True)
            df = list(wine)
            df = df[0]
            data = df

        self.outputs["Dataframe"].sv_set(data)


def register():
    bpy.utils.register_class(SvMegapolisGetSampleDataframe)


def unregister():
    bpy.utils.unregister_class(SvMegapolisGetSampleDataframe)
