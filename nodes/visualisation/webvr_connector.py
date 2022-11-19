import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
import os

class SvMegapolisWebVRConnector(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Web VR Connector
    Tooltip: Web VR Connector
    """
    bl_idname = 'SvMegapolisWebVRConnector'
    bl_label = 'Web VR Connector'
    bl_icon = 'MESH_DATA'

    
    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self,context)
    
    height: IntProperty(
        name="height",
        description="height",
        default=600 ,
        update=update_sockets)
    
    width: IntProperty(
        name="width",
        description="width",
        default=800 ,
        update=update_sockets)
    
    create: BoolProperty(
        name="create",
        description="Create Html",
        default=False ,
        update=update_sockets)


    #Blender Properties Buttons
    
    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Folder")
        self.inputs.new('SvVerticesSocket', "Vertices")
        self.inputs.new('SvStringsSocket', "Faces")


        #Outputs
        self.outputs.new('SvStringsSocket',"Html")
        self.outputs.new('SvVerticesSocket',"Vertices Out")
        self.outputs.new('SvStringsSocket',"Faces Out")

    def draw_buttons(self,context, layout):
        layout.prop(self, 'create')
        layout.prop(self, 'height')
        layout.prop(self, 'width')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
    
        if not self.inputs["Folder"].is_linked or not self.inputs["Vertices"].is_linked or not self.inputs["Faces"].is_linked :
            return
        self.folder = self.inputs["Folder"].sv_get(deepcopy = False)
        self.vertices = self.inputs["Vertices"].sv_get(deepcopy = False)
        self.faces = self.inputs["Faces"].sv_get(deepcopy = False)


        aframe_folder=self.folder[0][0]
        vertices = self.vertices
        faces= self.faces
        height = self.height
        width = self.width

        size ="a-scene[height:{0}px;width:{1}px;]".format(height,width)

        size = size.replace("[","{")
        size = size.replace("]","}")

        vertices_str=''
        for i in vertices:
            for j in i:
                count = 0
                for k in j:
                    if count == len(j)-1:
                        vertices_str=vertices_str+f"{k},"
                        count = count+1
                    else:
                        vertices_str=vertices_str+f"{k} "
                        count = count+1


        faces_str=''
        for i in faces:
            for j in i:
                count= 0
                for k in j:
                    if count == len(j)-1:
                        faces_str=faces_str+f"{k} -1,"
                        count = count+1
                    else:
                        faces_str=faces_str+f"{k} "
                        count = count+1


        vertices_str=vertices_str[:-1]
        faces_str=faces_str[:-1]
        try:
            os.mkdir(aframe_folder)
        except:
            pass

        html=f"""
          <head>
            <script src='https://aframe.io/releases/0.5.0/aframe.js'></script>
             <script src="https://raw.githubusercontent.com/andreasplesch/aframe-indexedfaceset-geometry/master/dist/aframe-indexedfaceset-geometry.min.js"></script>
          </head>
          <body>
            <a-scene>
              <a-indexedfaceset vertices="{vertices_str}" faces="{faces_str}"></a-indexedfaceset>
              <a-sky color='#ECECEC'></a-sky>
            </a-scene>
          
          </body>

        """

        #component = f"components.html(\"\"\"{html}\"\"\",height={height},width={width},scrolling=False)"

        node_out = html

        vertices_out=vertices_str
        faces_out = faces_str
        if self.create ==True:
            with open(f"{aframe_folder}/index.html", "w") as f:
                f.write(html)

        ## Output

        self.outputs["Html"].sv_set(node_out)
        self.outputs["Vertices Out"].sv_set(vertices_out)
        self.outputs["Faces Out"].sv_set(faces_out)


def register():
    bpy.utils.register_class(SvMegapolisWebVRConnector)

def unregister():
    bpy.utils.unregister_class(SvMegapolisWebVRConnector)
