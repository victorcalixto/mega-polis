import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies


class SvMegapolisDashboardLoadMap(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Dashboard Load Map
    Tooltip: Dashboard Load Map
    """
    bl_idname = 'SvMegapolisDashboardLoadMap'
    bl_label = 'Dashboard Load Map'
    bl_icon = 'MESH_DATA'

    
    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self,context)
    
    map_height: IntProperty(
        name="map_height",
        description="Zoom",
        default=600 ,
        update=update_sockets)
    
    map_width: IntProperty(
        name="map_width",
        description="Zoom",
        default=800 ,
        update=update_sockets)
    
    #Blender Properties Buttons
    
    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Map Name")

        #Outputs
        self.outputs.new('SvStringsSocket',"Dashboard Map")

    def draw_buttons(self,context, layout):
        layout.prop(self, 'map_height')
        layout.prop(self, 'map_width')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
    
        if not self.inputs["Map Name"].is_linked:
            return
        self.mapname = self.inputs["Map Name"].sv_get(deepcopy = False)

        map_height = self.map_height
        map_width= self.map_width

        map_name = self.mapname[0][0]
        
        load =f"""
{map_name}.to_streamlit(height={map_height},width={map_width})\n
           """

        load_map=load

        ## Output

        self.outputs["Dashboard Map"].sv_set(load_map)

def register():
    bpy.utils.register_class(SvMegapolisDashboardLoadMap)

def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardLoadMap)
