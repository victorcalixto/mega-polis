import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.dummy_nodes import add_dummy


#Megapolis Dependencies
from megapolis.dependencies import seaborn as sns
import  threading
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")

import secrets

Plot = namedtuple('Plot', ['regplot', 'pairplot'])
PLOT = Plot('regplot', 'pairplot')
plot_items = [(i, i, '') for i in PLOT]

if sns is None:
    add_dummy('SvMegapolisSeabornPlot', 'Seaborn Plot', 'seaborn')
else:
    class SvMegapolisSeabornPlot(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: Seaborn Plot
        Tooltip: Plot
        """
        bl_idname = 'SvMegapolisSeabornPlot'
        bl_label = 'Seaborn Plot'
        bl_icon = 'MESH_DATA'
        

        # Hide Interactive Sockets
        def update_sockets(self, context):
            """ need to do UX transformation before updating node"""
            def set_hide(sock, status):
                if sock.hide_safe != status:
                    sock.hide_safe = status

            if self.plot in PLOT.regplot:
                set_hide(self.inputs['Dataframe'], False)
                set_hide(self.inputs['Feature X'], False)
                set_hide(self.inputs['Feature y'], False)
            else:
                set_hide(self.inputs['Dataframe'],False)
                set_hide(self.inputs['Feature X'],True)
                set_hide(self.inputs['Feature y'],True)

            updateNode(self,context)

        #Blender Properties Buttons
        
        plot: EnumProperty(
            name='plot', items=plot_items,
            default="regplot",
            description='Choose a plot type', 
            update=update_sockets)
        
        run: BoolProperty(
                default=False, 
                description="run", 
                name="run",
                update=update_sockets)

        def sv_init(self, context):
            # inputs
            self.inputs.new('SvStringsSocket', "Dataframe")
            self.inputs.new('SvStringsSocket', "Feature X")
            self.inputs.new('SvStringsSocket', "Feature y")
        
        def draw_buttons(self,context, layout):
            layout.prop(self, 'run')
            layout.prop(self, 'plot', expand=True)

        def draw_buttons_ext(self, context, layout):
            self.draw_buttons(context, layout)

        def process(self):
            hex_name=secrets.token_hex(nbytes=16)


            def showRegPlot(df,feature_x,feature_y):
                sns.set_theme(color_codes=True)
                sns.regplot(x=feature_x, y=feature_y , data=df)
                plt.show()

            def showPairPlot(df):
                sns.set_theme(color_codes=True)
                sns.pairplot(df)
                plt.show()

            if self.plot in PLOT.pairplot:
                if not self.inputs["Dataframe"].is_linked:
                    return
                self.df = self.inputs["Dataframe"].sv_get(deepcopy = False)
                df = self.df 
                
                #showPairPlot(df)
                if self.run == True:
                    
                    exec(f"t1_{hex_name} = threading.Thread(target=showPairPlot, args=(df,))")
                    exec(f"t1_{hex_name}.start()")
                else:
                    hex_name=secrets.token_hex(nbytes=16)


                    
            else:
                if not self.inputs["Dataframe"].is_linked or not self.inputs["Feature X"].is_linked or not self.inputs["Feature y"].is_linked :
                    return
                self.df = self.inputs["Dataframe"].sv_get(deepcopy = False)
                self.x = self.inputs["Feature X"].sv_get(deepcopy = False)
                self.y = self.inputs["Feature y"].sv_get(deepcopy = False)
                
                df = self.df
                feature_x = self.x[0][0]
                feature_y = self.y[0][0]

                #showRegPlot(df,feature_x,feature_y)
                if self.run ==True: 
                    exec(f"t2_{hex_name} = threading.Thread(target=showPairPlot, args=(df,))")
                    exec(f"t2_{hex_name}.start()")
                else:
                    hex_name=secrets.token_hex(nbytes=16)



def register():
    if sns is not None:
        bpy.utils.register_class(SvMegapolisSeabornPlot)

def unregister():
    if sns is not None:
        bpy.utils.unregister_class(SvMegapolisSeabornPlot)
