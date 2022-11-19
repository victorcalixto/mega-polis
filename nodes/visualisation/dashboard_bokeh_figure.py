import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies


class SvMegapolisDashboardBokehFigure(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Dashboard Bokeh Figure
    Tooltip: Dashboard Bokeh Figure
    """
    bl_idname = 'SvMegapolisDashboardBokehFigure'
    bl_label = 'Dashboard Bokeh Figure'
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
        self.inputs.new('SvStringsSocket', "Figure Name")
        self.inputs.new('SvStringsSocket', "Title")
        self.inputs.new('SvStringsSocket', "X Label")
        self.inputs.new('SvStringsSocket', "Y Label")

        #Outputs
        self.outputs.new('SvStringsSocket',"Dashboard Bokeh Plot")

    def process(self):
    
        if not self.inputs["Figure Name"].is_linked or not self.inputs["Title"].is_linked or  not self.inputs["X Label"].is_linked or not self.inputs["Y Label"].is_linked:
            return
        self.bokehname = self.inputs["Figure Name"].sv_get(deepcopy = False)
        self.title = self.inputs["Title"].sv_get(deepcopy = False)
        self.x= self.inputs["X Label"].sv_get(deepcopy = False)
        self.y= self.inputs["Y Label"].sv_get(deepcopy = False)

        figure_name=self.bokehname[0][0]
        title=self.title[0][0]
        x_label=self.x[0][0]
        y_label=self.y[0][0]

        figure_plot=f"""
{figure_name} = figure(title='{title}',x_axis_label='{x_label}',y_axis_label='{y_label}') \n \n
                 """

        st_bokeh_plot = [figure_plot]

                ## Output

        self.outputs["Dashboard Bokeh Plot"].sv_set(st_bokeh_plot)

def register():
    bpy.utils.register_class(SvMegapolisDashboardBokehFigure)

def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardBokehFigure)
