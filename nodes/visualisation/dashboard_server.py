import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from multiprocessing import Process
import subprocess
import os
import sys

from megapolis.dependencies import psutil

class SvMegapolisDashboardServer(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Dashboard Server
    Tooltip: Dashboard Server
    """
    bl_idname = 'SvMegapolisDashboardServer'
    bl_label = 'Dashboard Server'
    bl_icon = 'MESH_DATA'
    sv_dependencies = {'psutil'}
    
    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self,context)
    
    #Blender Properties Buttons
    run:BoolProperty(
         name="run",
         description="Run Dashboard",
         default=False ,
         update=update_sockets)


    close: BoolProperty(
        name="close",
        description="Close the server",
        default=False,
        update=update_sockets)


    def sv_init(self, context):
        # inputs
        self.inputs.new('SvFilePathSocket', "Dashboard Name")

        #Outputs
        self.outputs.new('SvStringsSocket',"Output Message")
   
    def draw_buttons(self,context, layout):
        layout.prop(self, 'run')
        layout.prop(self, 'close')


    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)


    def process(self):
    
        if not self.inputs["Dashboard Name"].is_linked:
            return
        self.dashname = self.inputs["Dashboard Name"].sv_get(deepcopy = False)
        
        def killtree(pid, including_parent=False):
            parent = psutil.Process(pid)
            for child in parent.children(recursive=True):
                print (child), child
                child.kill()

            if including_parent:
                parent.kill()
        
        
        python = sys.executable

        dashboard_streamlit_name = self.dashname[0][0]
        message = ''
        def run_process(dashboard_streamlit_name):
            return_code = subprocess.run(['streamlit','run', dashboard_streamlit_name])
        
        if self.run == True:
            p = Process(target=run_process, args=(dashboard_streamlit_name,))
            p.start()

            message = ['Runnning']
        
        pid=os.getpid()
        
        if self.close == True:
            killtree(pid)
            message =''
        

        ## Output

        self.outputs["Output Message"].sv_set(message)

def register():
    bpy.utils.register_class(SvMegapolisDashboardServer)

def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardServer)
