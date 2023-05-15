import bpy
from bpy.props import BoolProperty, EnumProperty

from collections import namedtuple

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import laspy
import numpy as np

Classification = namedtuple('Classification',
     ['never', 'uncla', 'ground', 'low_vegetation', 'med_vegetation','high_vegetation', 'building', 'noise', 'reserved', 'water', 'rail',
      'road', 'overlap', 'wire_guard', 'wire_conductor', 'transmission', 'wire_connector',
      'bridge', 'high_noise'])
CLASSIFICATION = Classification('never', 'uncla', 'ground', 'low_vegetation', 'med_vegetation','high_vegetation', 'building', 'noise', 'reserved', 'water', 'rail',
      'road', 'overlap', 'wire_guard', 'wire_conductor', 'transmission', 'wire_connector',
      'bridge', 'high_noise')
classification_items = [(i, i, '') for i in CLASSIFICATION]

def getCoordinates(points_filtered,las):
    coordinates = np.stack(((points_filtered.X*las.header.scales[0])+las.header.offsets[0],(points_filtered.Y*las.header.scales[1])+las.header.offsets[1],(points_filtered.Z*las.header.scales[2])+las.header.offsets[2]), axis=1)
    return coordinates



class SvMegapolisFilterLas(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Filter Las
    Tooltip: Filter Las
    """
    bl_idname = 'SvMegapolisFilterLas'
    bl_label = 'Filter Las'
    bl_icon = 'MESH_DATA'
    

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self,context)

    #Blender Properties Buttons

    classification: EnumProperty(
        name='classification', items=classification_items,
        default="ground",
        description='Choose a Classification Feature', 
        update=update_sockets)


    def sv_init(self, context):
        
        # inputs
        self.inputs.new('SvFilePathSocket', "Path")
        self.inputs.new('SvStringsSocket', "Points Data")



        # outputs
        
        #Output
        self.outputs.new('SvStringsSocket', "Points Data Filtered")
        self.outputs.new('SvVerticesSocket', "Points")
        
        
    def draw_buttons(self,context, layout):
        layout.prop(self, 'classification')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        if not self.inputs["Path"].is_linked or not self.inputs["Points Data"].is_linked:
            return
        self.path = self.inputs["Path"].sv_get(deepcopy = False)
        self.points_data = self.inputs["Points Data"].sv_get(deepcopy = False)



        path=self.path[0][0]
        las = laspy.read(path)
        classification_dict={}

        for i in range(0,len(CLASSIFICATION)):
            classification_dict[CLASSIFICATION[i]]= i 
        
        points_filtered = self.points_data.points[self.points_data.classification == int(classification_dict[self.classification])]
    
        coordinates = getCoordinates(points_filtered,las)

        points = [coordinates]

        ## Output
        self.outputs["Points Data Filtered"].sv_set(points_filtered)
        self.outputs["Points"].sv_set(points)
            
def register():
    bpy.utils.register_class(SvMegapolisFilterLas)

def unregister():
    bpy.utils.unregister_class(SvMegapolisFilterLas)
