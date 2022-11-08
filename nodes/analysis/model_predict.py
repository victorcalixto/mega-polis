import bpy
from bpy.props import FloatProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

#Megapolis Dependencies

from megapolis.dependencies import sklearn as skl

class SvMegapolisModelPredict(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Model Predict
    Tooltip: Model Predict
    """
    bl_idname = 'SvMegapolisModelPredict'
    bl_label = 'Model Predict'
    bl_icon = 'MESH_DATA'
    

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status
        
        updateNode(self,context)

    #Blender Properties Buttons
    
    run: BoolProperty(
        name='run', 
        default=False,
        description='Runs Model Predict', 
        update=update_sockets)
    
    
    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Model")
        self.inputs.new('SvStringsSocket', "X")

        # outputs
        
        self.outputs.new('SvStringsSocket', "Predictions Array")


    def draw_buttons(self,context, layout):
        layout.prop(self, 'run')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
         
        if not self.inputs["Model"].is_linked or not self.inputs["X"].is_linked:
            return
        self.model = self.inputs["Model"].sv_get(deepcopy = False)
        self.x = self.inputs["X"].sv_get(deepcopy = False)

        model = self.model[0]

        X_test = self.x

        if self.run == True:
            data = model.predict(X_test)
            predictions = [data]

        ## Outputs
        
        self.outputs["Predictions Array"].sv_set(predictions)
        
def register():
    if skl is not None:
        bpy.utils.register_class(SvMegapolisModelPredict)

def unregister():
    if skl is not None:
        bpy.utils.unregister_class(SvMegapolisModelPredict)
