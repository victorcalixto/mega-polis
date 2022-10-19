import bpy
from bpy.props import IntProperty, EnumProperty

#from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy


#Megapolis Dependencies
from megapolis.dependencies import laspy 
import numpy as np


if laspy is None:
    add_dummy('SvMegapolisReadLas', 'Read LAS', 'laspy')
else:
    class SvMegapolisReadLas(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: Read LAS
        Tooltip: Read a LAS Point Cloud File 
        """
        bl_idname = 'SvMegapolisReadLas'
        bl_label = 'Read LAS'
        bl_icon = 'MESH_DATA'
        

        def sv_init(self, context):
            # inputs
            self.inputs.new('SvFilePathSocket', "Path")
            
            #outputs
            self.outputs.new('SvVerticesSocket', "Points")
            self.outputs.new('SvStringsSocket', "Points Data")
            self.outputs.new('SvStringsSocket', "Intensity")
            self.outputs.new('SvStringsSocket', "Classification")
            self.outputs.new('SvStringsSocket', "Classification Colours")

        def process(self):
            if not self.inputs["Path"].is_linked:
                return
            self.path = self.inputs["Path"].sv_get(deepcopy = False)
          
            las = laspy.read(self.path[0][0])
            intensity = las.intensity.astype("uint32")
            classification = las.classification

            colors_classification = {
                                0:["never",(0,0,0,1)],
                                1:["uncla",(.1,.8462,.02,1)],
                                2:["ground",(.6,.2,0,1)],
                                3:["low_vegetation", (.2,1,.47,1)],
                                4:["med_vegetation",(0,.53,.18,1)],
                                5:["high_vegetation",(0,.36,.12,1)],
                                6:["building", (.97,1,.06,1)],
                                7:["noise", (.0275,.18,1,1)],
                                8:["reserved",(.4,.1,1,1)],
                                9:["water",(0,.6,.9,1)],
                                10:["rail",(1,.53,.3,1)],
                                11:["road",(.8,.27,0,1),],
                                12:["overlap",(.9,0,.15,1)],
                                13:["wire_guard",(.67,.5,1,1)],
                                14:["wire_conductor",(.43,.32,.64,1)],
                                15:["transmission",(.64,.16,.18,1)],
                                16:["wire_connector",(.93,.24,.25,1)],
                                17:["bridge",(.83,1,0,1)],
                                18:["high_noise",(1,0,0,1)],
                                }
            names = list(las.point_format.dimension_names)

            coordinates = np.array(list(zip((las.X*las.header.scales[0])+las.header.offsets[0],(las.Y*las.header.scales[1])+las.header.offsets[1],(las.Z*las.header.scales[2])+las.header.offsets[2])))

            colors = []

            colors_keys = list(colors_classification.keys())


            for i in classification:
                colors.append(colors_classification[i][1])

            intensity = [intensity.tolist()]

            points_data =  las
            points = [coordinates]
            points_intensity = intensity
            points_classification = [classification]
            points_classification_color = [colors]
            
            #Outputs
            self.outputs["Points"].sv_set([coordinates])
            self.outputs["Points Data"].sv_set(las)
            self.outputs["Intensity"].sv_set(intensity)
            self.outputs["Classification"].sv_set([classification])
            self.outputs["Classification Colours"].sv_set([colors])

def register():
    if laspy is not None:
        bpy.utils.register_class(SvMegapolisReadLas)

def unregister():
    if laspy is not None:
        bpy.utils.unregister_class(SvMegapolisReadLas)
