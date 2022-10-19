import bpy
from bpy.props import IntProperty, EnumProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy


#Megapolis Dependencies
from megapolis.dependencies import sklearn as skl

Model_method = namedtuple('ModelMethod', ['linear', 'ransac','ridge','elasticnet','lasso'])
MODELMETHOD = Model_method('linear','ransac','ridge','elasticnet','lasso')
modelmethod_items = [(i, i, '') for i in MODELMETHOD]

if skl is None:
    add_dummy('SvMegapolisLinearModelSelection', 'Linear Model Selection', 'sklearn')
else:
    class SvMegapolisLinearModelSelection(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: Linear Model Selection
        Tooltip: Selection of a Linear Model: Linear, RANSAC, Ridge, ElasticNet, Lasso 
        """
        bl_idname = 'SvMegapolisLinearModelSelection'
        bl_label = 'Linear Model Selection'
        bl_icon = 'MESH_DATA'

        # Hide Interactive Sockets
        def update_sockets(self, context):
            """ need to do UX transformation before updating node"""
            def set_hide(sock, status):
                if sock.hide_safe != status:
                    sock.hide_safe = status
            updateNode(self,context)

        #Blender Properties Buttons
        
        modelmethod: EnumProperty(
            name='Method', items=modelmethod_items,
            default="linear",
            description='Choose a method for the Linear Regression', 
            update=update_sockets)


        def sv_init(self, context):
            # inputs
            
            # outputs
            self.outputs.new('SvVerticesSocket', "Model")

        def draw_buttons(self,context, layout):
            layout.prop(self, 'modelmethod', expand=False)

        def draw_buttons_ext(self, context, layout):
            self.draw_buttons(context, layout)

        def process(self):
             
            
            if self.modelmethod == "linear":
                model = skl.linear_model.LinearRegression()
            elif self.modelmethod == "ransac":
                model = skl.linear_model.RANSACRegressor()
            elif self.modelmethod == "ridge":
                model = skl.linear_model.Ridge()
            elif self.modelmethod == "elasticnet":
                model = skl.linear_model.ElasticNet()    
            elif self.modelmethod == "lasso":
                model = skl.linear_model.Lasso() 

            model_out = [model]

            ## Output

            self.outputs["Model"].sv_set(model_out)
            
def register():
    if skl is not None:
        bpy.utils.register_class(SvMegapolisLinearModelSelection)

def unregister():
    if skl is not None:
        bpy.utils.unregister_class(SvMegapolisLinearModelSelection)
