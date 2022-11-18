import bpy
from bpy.props import IntProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

#Megapolis Dependencies

from megapolis.dependencies import requests
from datetime import datetime



class SvMegapolisRequestDataApi(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Request Data Api
    Tooltip: Request data from an Application Program Interface (API)
    """
    bl_idname = 'SvMegapolisRequestDataApi'
    bl_label = 'Request Data Api'
    bl_icon = 'MESH_DATA'
    sv_dependencies = {'requests'}

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status
        
        updateNode(self,context)

    #Blender Properties Buttons
    
    download: BoolProperty(
        name='download', 
        default=False,
        description='Download the requested data', 
        update=update_sockets)

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "API URL")
        self.inputs.new('SvStringsSocket', "Folder")

        # outputs
        
        self.outputs.new('SvStringsSocket', "JSON out")
        self.outputs.new('SvStringsSocket', "Status Message")
                    
    def draw_buttons(self,context, layout):
        layout.prop(self, 'download')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        if not self.inputs["API URL"].is_linked or not self.inputs["Folder"].is_linked: 
            return
        self.url_in = self.inputs["API URL"].sv_get(deepcopy = False)
        self.folder = self.inputs["Folder"].sv_get(deepcopy = False)

        url = self.url_in[0][0]
        folder_name = str(self.folder[0][0])
        
        response = requests.get(url)
        status_response = response.status_code

        if status_response == 200:
            status = "Data Collected"
            status = str(status_response)

            name = url.split("/")
            name = name[-1]
            json_out = response.json()
            
            if self.download == True:
                try:
                    with open(f"{folder_name}/{name}", 'w') as f:
                        f.write(response.text)
                        f.close()
                except UnicodeDecodeError:
                     pass
        else:
            status = f"Status code {status_response}. For requests API HTTP reponses look at the reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status"

        ## Outputs
        
        self.outputs["JSON out"].sv_set(json_out)
        self.outputs["Status Message"].sv_set(status)


def register():
    bpy.utils.register_class(SvMegapolisRequestDataApi)


def unregister():
    bpy.utils.unregister_class(SvMegapolisRequestDataApi)
