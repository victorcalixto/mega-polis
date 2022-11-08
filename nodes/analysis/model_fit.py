import bpy
from bpy.props import FloatProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

#Megapolis Dependencies

from megapolis.dependencies import sklearn as skl

class SvMegapolisModelFit(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Model Fit
    Tooltip: Model Fit
    """
    bl_idname = 'SvMegapolisModelFit'
    bl_label = 'Model Fit'
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
        description='Runs Model Fit', 
        update=update_sockets)
    
    train_size: FloatProperty(
        name="train_size",
        description="Train size for the model",
        default= .30,
        max= .99,
        min= .01,
        update=update_sockets)
    

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Model")
        self.inputs.new('SvStringsSocket', "X")
        self.inputs.new('SvStringsSocket', "y")

        # outputs
        
        self.outputs.new('SvStringsSocket', "Model Out")
                    
    def draw_buttons(self,context, layout):
        layout.prop(self, 'run')
        layout.prop(self, 'train_size')


    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
         
        if not self.inputs["Model"].is_linked or not self.inputs["X"].is_linked or not self.inputs["y"].is_linked:
            return
        self.model = self.inputs["Model"].sv_get(deepcopy = False)
        self.x = self.inputs["X"].sv_get(deepcopy = False)
        self.y = self.inputs["y"].sv_get(deepcopy = False)

        model = self.model[0]
        X = self.x 
        y = self.y 
        train_size = self.train_size 


        if self.run == True:

            X_train, X_test, y_train, y_test = skl.model_selection.train_test_split(X, y, shuffle=True, train_size=train_size)

            data = model.fit(X_train, y_train)

            predictions = data.predict(X_test)
            
            model_out = [data]

        ## Outputs
        
        self.outputs["Model Out"].sv_set(model_out)
        
def register():
    if skl is not None:
        bpy.utils.register_class(SvMegapolisModelFit)

def unregister():
    if skl is not None:
        bpy.utils.unregister_class(SvMegapolisModelFit)
