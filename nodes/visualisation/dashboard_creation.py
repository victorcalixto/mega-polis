import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy


#Megapolis Dependencies
from megapolis.dependencies import pandas as pd
from megapolis.dependencies import streamlit as st

#import json 

if st is None:
    add_dummy('SvMegapolisDashboardCreation', 'Dashboard Creation', 'streamlit')
else:
    class SvMegapolisDashboardCreation(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: Dashboard Creation
        Tooltip: Dashboard Creation
        """
        bl_idname = 'SvMegapolisDashboardCreation'
        bl_label = 'Dashboard Creation'
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
            self.inputs.new('SvStringsSocket', "Dashboard Content")
            self.inputs.new('SvStringsSocket', "Dashboard Name")
            self.inputs.new('SvStringsSocket', "Folder")

            #Outputs
            self.outputs.new('SvStringsSocket',"Output Message")

        def process(self):
        
            if not self.inputs["Dashboard Content"].is_linked or not self.inputs["Dashboard Name"].is_linked :
                return
            
            self.content = self.inputs["Dashboard Content"].sv_get(deepcopy = False)
            self.name = self.inputs["Dashboard Name"].sv_get(deepcopy = False)
            self.folder = self.inputs["Folder"].sv_get(deepcopy = False)

            dashboard_content = self.content
            folder = str(self.folder[0][0])

            imports = """
            import streamlit as st
            import plotly.express as px
            import plotly.figure_factory as ff
            import pandas as pd
            from numpy import array
            import numpy as np
            import io
            import streamlit.components.v1 as components
            from ipywidgets import embed
            import pyvista as pv
            from pyvista.jupyter.pv_pythreejs import convert_plotter
            from pyvista import examples
            import leafmap.kepler as kepler
            from bokeh.plotting import figure
            import streamlit.components.v1 as components
            import seaborn as sns
            import matplotlib.pyplot as plt

            """


            plotly_test="""
            # Add histogram data
            x1 = np.random.randn(200) - 2
            x2 = np.random.randn(200)
            x3 = np.random.randn(200) + 2

            # Group data together
            hist_data = [x1, x2, x3]

            group_labels = ['Group 1', 'Group 2', 'Group 3']

            # Create distplot with custom bin_size
            fig = ff.create_distplot(
                     hist_data, group_labels, bin_size=[.1, .25, .5])

            # Plot!
            st.plotly_chart(fig, use_container_width=True)

            """


            pyvista_def=f"""
            pv.set_plot_theme('document')

            def pyvista_streamlit(plotter,plot_width,plot_height):
                widget = convert_plotter(plotter)
                state = embed.dependency_state(widget)
                fp = io.StringIO()
                embed.embed_minimal_html(fp, None, title="", state=state)
                fp.seek(0)
                snippet = fp.read()
                components.html(snippet, width=plot_width, height=plot_height)

            """

            #dashboard_content=dashboard_content[0]
            dashboard_name=self.name[0][0]
              
            str_content=''

            for i in dashboard_content: 
               str_content=str_content+f"{i}"
               
            #print(str_content)
                    
            template_df=f"{imports}"+f"{pyvista_def}"+f"{str_content}"+f"{plotly_test}"
            try:
                os.mkdir(folder)
                #folder_detect = f"{folder_name}_detect"
                #os.mkdir(folder_detect)
            except:
                pass
            with open(dashboard_name, "w") as f:
                f.write(f"{folder}/{template_df}")

            ## Output

            self.outputs["Output Message"].sv_set(st_df)


def register():
    if st is not None:
        bpy.utils.register_class(SvMegapolisDashboardCreation)

def unregister():
    if st is not None:
        bpy.utils.unregister_class(SvMegapolisDashboardCreation)

