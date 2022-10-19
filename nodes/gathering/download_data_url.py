import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy

#Megapolis Dependencies
from megapolis.dependencies import wget


import wget 

if wget is None:
    add_dummy('SvMegapolisDownloadDataUrl', 'Download Data Url', 'wget')
else:
    class SvMegapolisDownloadDataUrl(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: Download Data Url

        Tooltip: Download data from a weblink (Uniform Resource Locator - URL)
        """
        bl_idname = 'SvMegapolisDownloadDataUrl'
        bl_label = 'Download Data Url'
        bl_icon = 'MESH_DATA'

        def sv_init(self, context):
            # inputs
            self.inputs.new('SvStringsSocket', "URL")
            
            #outputs
            self.outputs.new('SvStringsSocket', "Output Message")

        def process(self):
            if not self.inputs["URL"].is_linked:
                return
            self.url = self.inputs["URL"].sv_get(deepcopy = False)
            
            if len(self.url[0])<= 1:
                url = self.url[0][0]
                filename = wget.download(url)
                message = [f"{filename} downloaded sucessful"]
            else:
                messages = []
                filenames = []
                for i in self.url[0]:
                    filename = wget.download(i)
                    messages.append(i)
                message = [f"{messages} downloaded sucessful"]
           
            self.outputs["Output Message"].sv_set(message)

def register():
    if wget is not None:
        bpy.utils.register_class(SvMegapolisDownloadDataUrl)

def unregister():
    if wget is not None:
        bpy.utils.unregister_class(SvMegapolisDownloadDataUrl)
