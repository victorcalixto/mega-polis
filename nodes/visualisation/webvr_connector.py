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
        self.inputs.new('SvStringsSocket', "Material")



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
    
        if not self.inputs["Folder"].is_linked or not self.inputs["Vertices"].is_linked or not self.inputs["Faces"].is_linked or not self.inputs["Material"].is_linked  :
            return
        self.folder = self.inputs["Folder"].sv_get(deepcopy = False)
        self.vertices = self.inputs["Vertices"].sv_get(deepcopy = False)
        self.faces = self.inputs["Faces"].sv_get(deepcopy = False)
        self.material = self.inputs["Material"].sv_get(deepcopy = False)



        aframe_folder=self.folder[0][0]
        vertices = self.vertices
        faces= self.faces
        height = self.height
        width = self.width
        material = self.material[0][0] 

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
        """
        faces_str=''

        faces_list = []
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
        """
        faces_list = []
        for i in faces:
            for j in i:
                    faces_list.append(f"geometry.faces.push(new THREE.Face3{j[0],j[1],j[2]});")

        faces_str = ''
        for i in faces_list:
            faces_str=faces_str+f"{i}\n"
            
        #vertices_str=vertices_str[:-1]

        #faces_str=faces_str[:-1]




        try:
            os.mkdir(aframe_folder)
        except:
            pass


        script_=f"""
        AFRAME.registerGeometry('example',@
              schema: @
                vertices: @
                  default: ['-10 10 0', '-10 -10 0', '10 -10 0', '10 -10 0'],
                !
              !,

              init: function (data) @
                var geometry = new THREE.Geometry();
                geometry.vertices = data.vertices.map(function (vertex) @
                    var points = vertex.split(' ').map(function(x)@return parseFloat(x);!);
                    return new THREE.Vector3(points[0], points[2], points[1]);
                !);
                geometry.computeBoundingBox();
                {faces_str}
                geometry.mergeVertices();
                geometry.computeFaceNormals();
                geometry.computeVertexNormals();
                this.geometry = geometry;
              !
            !);
            """

        script_=script_.replace("@","{")
        script_=script_.replace("!" , "}")



        html=f"""
          <html>
          <head>
            <script src='https://aframe.io/releases/1.1.0/aframe.min.js'></script>
            <script src='https://livejs.com/live.js'></script>
           
          <script >
               {script_}
             </script>
          
          </head> 
             
             
            <a-scene onchange="reloadThePage()">
              <a-entity  id=geo geometry="primitive: example; vertices: {vertices_str}" material="{material}"></a-entity>
              
              
              <a-sky color='#ECECEC'></a-sky>
            </a-scene>
            
           </html>
        """

        #component = f"components.html(\"\"\"{html}\"\"\",height={height},width={width},scrolling=False)"

        node_out = html

        vertices_out=vertices_str
        faces_out = faces_str

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
