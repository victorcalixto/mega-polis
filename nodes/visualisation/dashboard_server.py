import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy


#Megapolis Dependencies
from multiprocessing import Process
import subprocess


class SvMegapolisDashboardServer(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Dashboard Server
    Tooltip: Dashboard Server
    """
    bl_idname = 'SvMegapolisDashboardServer'
    bl_label = 'Dashboard Server'
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
        self.inputs.new('SvStringsSocket', "Dashboard Name")

        #Outputs
        self.outputs.new('SvStringsSocket',"Output Message")
    
    def process(self):
    
        if not self.inputs["Dashboard Name"].is_linked:
            return
        self.name = self.inputs["Dashboard Name"].sv_get(deepcopy = False)

        dashboard_streamlit_name = self.name[0][0]

        def run_process(dashboard_streamlit_name):
            return_code = subprocess.run(['streamlit','run', dashboard_streamlit_name])

        p = Process(target=run_process, args=(dashboard_streamlit_name,))
        p.start()

        message = ['Runnning']

        ## Output

        self.outputs["Output Message"].sv_set(message)

def register():
    bpy.utils.register_class(SvMegapolisDashboardServer)

def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardServer)
