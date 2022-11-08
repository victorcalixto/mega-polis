import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import node_id, multi_socket, updateNode, levels_of_list_or_np


#Megapolis Dependencies
from megapolis.dependencies import wget

import os

class SvMegapolisDownloadDataUrl(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Download Data Url

    Tooltip: Download data from a weblink (Uniform Resource Locator - URL)
    """
    bl_idname = 'SvMegapolisDownloadDataUrl'
    bl_label = 'Download Data Url'
    bl_icon = 'MESH_DATA'


    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status
        
        updateNode(self,context)

    download: BoolProperty(
        name='download', 
        default=False,
        description='Download', 
        update=update_sockets)


    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "URL")
        self.inputs.new('SvStringsSocket', "Folder")
        
        #outputs
        self.outputs.new('SvStringsSocket', "Output Message")
   


    def draw_buttons(self,context, layout):
        layout.prop(self, 'download')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

 
    def process(self):
        if not self.inputs["URL"].is_linked or not self.inputs["Folder"].is_linked  :
            return
        self.url = self.inputs["URL"].sv_get(deepcopy = False)
        self.folder = self.inputs["Folder"].sv_get(deepcopy = False)
        
        folder_name = self.folder[0][0]
        message = ''
        
        if self.download == True: 
            if len(self.url[0])<= 1:
                url = self.url[0][0]
                name= os.path.basename(url)
                filename = wget.download(url, f"{folder_name}/{name}")
                message = [f"{filename} downloaded sucessful"]
            else:
                messages = []
                filenames = []
                for i in self.url[0]:
                    name= os.path.basename(i)
                    filename = wget.download(i, f"{folder_name}/{name}")
                    messages.append(i)
                message = [f"{messages} downloaded sucessful"]
        #outputs

        self.outputs["Output Message"].sv_set(message)



def register():
    if wget is not None:
        bpy.utils.register_class(SvMegapolisDownloadDataUrl)

def unregister():
    if wget is not None:
        bpy.utils.unregister_class(SvMegapolisDownloadDataUrl)
