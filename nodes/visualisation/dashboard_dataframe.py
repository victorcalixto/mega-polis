import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import pandas as pd
from megapolis.dependencies import streamlit as st

#import json 

class SvMegapolisDashboardDataframe(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Dashboard Dataframe
    Tooltip: Dashboard Dataframe
    """
    bl_idname = 'SvMegapolisDashboardDataframe'
    bl_label = 'Dashboard Dataframe'
    bl_icon = 'MESH_DATA'
    sv_dependencies = {'pandas', 'streamlit'}
    
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
        self.inputs.new('SvStringsSocket', "Dataframe")
        
        #Outputs
        self.outputs.new('SvStringsSocket',"Dashboard Dataframe")

    def process(self):
    
        if not self.inputs["Dataframe"].is_linked:
            return
        
        self.dataframe = self.inputs["Dataframe"].sv_get(deepcopy = False)

        df=self.dataframe
        #df = pd.io.json.build_table_schema(df)
        df = pd.DataFrame.to_json(df)

        write = f"""
st.dataframe(pd.DataFrame.from_dict({df}))\n
             """

        st_df = write

        ## Output

        self.outputs["Dashboard Dataframe"].sv_set([st_df])


def register():
    bpy.utils.register_class(SvMegapolisDashboardDataframe)


def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardDataframe)
