import bpy
from bpy.props import FloatProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

#Megapolis Dependencies

from megapolis.dependencies import sklearn as skl

class SvMegapolisModelEvaluate(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Model Evaluate
    Tooltip: Model Evaluate
    """
    bl_idname = 'SvMegapolisModelEvaluate'
    bl_label = 'Model Evaluate'
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
        self.inputs.new('SvStringsSocket', "Model")
        self.inputs.new('SvStringsSocket', "Predictions")
        self.inputs.new('SvStringsSocket', "y")

        # outputs
        
        self.outputs.new('SvStringsSocket', "r2")
        self.outputs.new('SvStringsSocket', "rmse")

    def process(self):
         
        if not self.inputs["Model"].is_linked or not self.inputs["y"].is_linked or not self.inputs["Predictions"].is_linked :
            return
        self.model = self.inputs["Model"].sv_get(deepcopy = False)
        self.y = self.inputs["y"].sv_get(deepcopy = False)
        self.predictions = self.inputs["Predictions"].sv_get(deepcopy = False)


        model = self.model[0]
        predictions = self.predictions[0]
        y_test = self.y

        data_r2 = skl.metrics.r2_score(y_test, predictions)
        data_rmse = skl.metrics.mean_squared_error(y_test, predictions, squared=False)

        r2 = [data_r2]
        rmse = [data_rmse]
        
        ## Outputs
        
        self.outputs["r2"].sv_set(predictions)
        self.outputs["rmse"].sv_set(predictions)

def register():
    if skl is not None:
        bpy.utils.register_class(SvMegapolisModelEvaluate)

def unregister():
    if skl is not None:
        bpy.utils.unregister_class(SvMegapolisModelEvaluate)
