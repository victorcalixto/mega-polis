import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from multiprocessing import Process
import subprocess
import sys
import os
import webbrowser


from megapolis.dependencies import psutil

class SvMegapolisPythonServer(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Python Server
    Tooltip: Python Server
    """
    bl_idname = 'SvMegapolisPythonServer'
    bl_label = 'Python Server'
    bl_icon = 'MESH_DATA'

    
    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self,context)
    
    port: IntProperty(
        name="port",
        description="Port to run the server",
        default=8800,
        update=update_sockets)
    
    close: BoolProperty(
        name="close",
        description="Close the server",
        default=False,
        update=update_sockets)
    
    run: BoolProperty(
        name="run",
        description="Run the server",
        default=False,
        update=update_sockets)
    

    #Blender Properties Buttons
    
    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Folder")

        #Outputs
        self.outputs.new('SvStringsSocket',"Output Message")

    def draw_buttons(self,context, layout):
        layout.prop(self, 'port')
        layout.prop(self, 'run')
        layout.prop(self, 'close')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
    
        if not self.inputs["Folder"].is_linked:
            return
        self.folder = self.inputs["Folder"].sv_get(deepcopy = False)
        port = self.port

        run_folder = self.folder[0][0]

        def killtree(pid, including_parent=False):
            parent = psutil.Process(pid)
            for child in parent.children(recursive=True):
                print (child), child
                child.kill()

            if including_parent:
                parent.kill()
        

        python = sys.executable
        message = ''      

        def run_process_python(python, port, run_folder):
            return_code = subprocess.run([python,'-m', 'http.server', str(port), '--directory', run_folder])


        try:
            if self.run == True:
                p = Process(target=run_process_python, args=(python,port,run_folder,))
                p.start()
                message = ['Runnning']
                webbrowser.open(f"localhost:{port}")
        except:
            pass

        pid=os.getpid()

        ## when you want to kill everything, including this program

        if self.close == True:
            killtree(pid)
            message =''
        
        ## Output

        self.outputs["Output Message"].sv_set(message)

def register():
    bpy.utils.register_class(SvMegapolisPythonServer)

def unregister():
    bpy.utils.unregister_class(SvMegapolisPythonServer)
