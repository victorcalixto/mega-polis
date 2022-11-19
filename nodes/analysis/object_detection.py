import bpy
from bpy.props import FloatProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


import multiprocessing
from subprocess import call

import os

class SvMegapolisObjectDetection(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Object Detection
    Tooltip: Object Dectection (Instance Segmentation using YoloV5)
    """
    bl_idname = 'SvMegapolisObjectDetection'
    bl_label = 'Object Detection'
    bl_icon = 'MESH_DATA'
    

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status
        
        updateNode(self,context)

    #Blender Properties Buttons
    
    run: BoolProperty(
        name='run', 
        default=False,
        description='Runs Model Fit', 
        update=update_sockets)
    
    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Source")
        self.inputs.new('SvStringsSocket', "Folder")

        # outputs
        
        self.outputs.new('SvStringsSocket', "Output Message")
                    
    def draw_buttons(self,context, layout):
        layout.prop(self, 'run')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        
        if not self.inputs["Source"].is_linked or not self.inputs["Folder"].is_linked:
            return
        self.source = self.inputs["Source"].sv_get(deepcopy = False)
        self.folder = self.inputs["Folder"].sv_get(deepcopy = False)

        real_path = os.path.realpath(__file__)
        l = len(real_path)
        real_path= real_path[:l-35]
        source = self.source[0][0]

        folder=self.folder[0][0]

        def thread_second(source):
            call(["python", f"{real_path}/external/yolov5/detect_mega.py", "--source", source, "--name", folder, "--save-crop", "--save-txt","--save-conf"])
        
        if self.run ==True:
            processThread = multiprocessing.Process(target=thread_second, args=[source])  # <- note extra ','
            processThread.start()
            out = 'The file is running in the background'

        out = ''
        ## Outputs
        
        self.outputs["Output Message"].sv_set(out)
        
def register():
    bpy.utils.register_class(SvMegapolisObjectDetection)

def unregister():
    bpy.utils.unregister_class(SvMegapolisObjectDetection)
