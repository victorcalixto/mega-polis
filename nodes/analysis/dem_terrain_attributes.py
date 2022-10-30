import bpy
from bpy.props import IntProperty, EnumProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy


#Megapolis Dependencies
from megapolis.dependencies import richdem as rd

Attribute_type = namedtuple('AttributeType', ['aspect', 'profile_curvature','planform_curvature','curvature','slope_riserun','slope_degrees','slope_percentage','slope_radians'])
ATTRIBUTETYPE = Attribute_type('aspect', 'profile_curvature','planform_curvature','curvature','slope_riserun','slope_degrees','slope_percentage','slope_radians')
attributetype_items = [(i, i, '') for i in ATTRIBUTETYPE]

if rd is None:
    add_dummy('SvMegapolisDemTerrainAttributes', 'Dem Terrain Attributes', 'richdem')
else:
    class SvMegapolisDemTerrainAttributes(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: Dem Terrain Attributes
        Tooltip: Provides methods for extract Terrain Attributes values: Aspect, Curvature, and Slope. 
        """
        bl_idname = 'SvMegapolisDemTerrainAttributes'
        bl_label = 'Dem Terrain Attributes'
        bl_icon = 'MESH_DATA'

        # Hide Interactive Sockets
        def update_sockets(self, context):
            """ need to do UX transformation before updating node"""
            def set_hide(sock, status):
                if sock.hide_safe != status:
                    sock.hide_safe = status
            updateNode(self,context)

        #Blender Properties Buttons
        
        attributetype: EnumProperty(
            name='Terrain Attribute', items=attributetype_items,
            default="slope_degrees",
            description='Choose a terrain attribute to extract values', 
            update=update_sockets)


        def sv_init(self, context):
            # inputs
            self.inputs.new('SvStringsSocket', "Dem Array")
            
            # outputs
            
            self.outputs.new('SvVerticesSocket', "Attribute Values")

        def draw_buttons(self,context, layout):
            layout.prop(self, 'attributetype', expand=False)

        def draw_buttons_ext(self, context, layout):
            self.draw_buttons(context, layout)

        def process(self):
             
            if not self.inputs["Dem Array"].is_linked:
                return
            self.array = self.inputs["Dem Array"].sv_get(deepcopy = False)
                
            dem_richdem = rd.rdarray(self.array, no_data=-9999)

            #fig = rd.rdShow(dem_richdem, axes=False, cmap='bone', figsize=(16, 10));
            #fig


            dem_slope = rd.TerrainAttribute(dem_richdem, attrib=self.attributetype)
            #print(dem_slope[:10])

            #rd.rdShow(dem_slope, axes=False, cmap='YlOrBr', figsize=(16, 10));

            flatten_arr = dem_slope.flatten()

            #attribute_values = [flatten_arr.tolist()]
            attribute_values = flatten_arr



            ## Output

            self.outputs["Attribute Values"].sv_set(attribute_values)
            

def register():
    if rd is not None:
        bpy.utils.register_class(SvMegapolisDemTerrainAttributes)

def unregister():
    if rd is not None:
        bpy.utils.unregister_class(SvMegapolisDemTerrainAttributes)
