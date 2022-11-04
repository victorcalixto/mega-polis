import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy

#Megapolis Dependencies

class SvMegapolisDashboardMarkdown(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Dashboard Markdown
    Tooltip: Dashboard Markdown
    """
    bl_idname = 'SvMegapolisDashboardMarkdown'
    bl_label = 'Dashboard Markdown'
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
        self.inputs.new('SvStringsSocket', "Markdown Text")

        #Outputs
        self.outputs.new('SvStringsSocket',"Markdown Out")

    def process(self):
    
        if not self.inputs["Markdown Text"].is_linked:
            return
        self.text = self.inputs["Markdown Text"].sv_get(deepcopy = False)

        st_markdown_tx=self.text[0]


        text ="""
st.markdown(\"\"\"{0}\"\"\")\n\n
              """.format(st_markdown_tx)

        st_markdown_out = [text]


        ## Output

        self.outputs["Markdown Out"].sv_set(st_markdown_out)


def register():
    bpy.utils.register_class(SvMegapolisDashboardMarkdown)

def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardMarkdown)
