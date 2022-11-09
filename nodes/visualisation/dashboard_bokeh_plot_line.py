import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies


class SvMegapolisDashboardBokehPlotLine(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Dashboard Bokeh Plot Line
    Tooltip: Dashboard Bokeh Plot Line
    """
    bl_idname = 'SvMegapolisDashboardBokehPlotLine'
    bl_label = 'Dashboard Bokeh Plot Line'
    bl_icon = 'MESH_DATA'

    
    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self,context)
       
    #Blender Properties Buttons
    line_width: IntProperty(
        name="line_width",
        description="Line Width",
        default=2 ,
        update=update_sockets)
    

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Figure Name")
        self.inputs.new('SvStringsSocket', "Legend Label")
        self.inputs.new('SvStringsSocket', "X Values")
        self.inputs.new('SvStringsSocket', "Y Values")
        #Outputs
        self.outputs.new('SvStringsSocket',"Dashboard Bokeh Line")
    
    def draw_buttons(self,context, layout):
        layout.prop(self, 'line_width')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)


    def process(self):
    
        if not self.inputs["Figure Name"].is_linked or not self.inputs["Legend Label"].is_linked or  not self.inputs["X Values"].is_linked or not self.inputs["Y Values"].is_linked:
            return
        self.figname = self.inputs["Figure Name"].sv_get(deepcopy = False)
        self.legend = self.inputs["Legend Label"].sv_get(deepcopy = False)
        self.x= self.inputs["X Values"].sv_get(deepcopy = False)
        self.y= self.inputs["Y Values"].sv_get(deepcopy = False)


        figure_name=self.figname[0][0]
        legend_label=self.legend[0][0]
        x_values=self.x[0]
        y_values=self.y[0]
        line_width = self.line_width

        line= f"""
{figure_name}.line({x_values}, {y_values}, legend_label='{legend_label}', line_width={line_width}) \n
           """

        st_bokeh_line = line

        ## Output

        self.outputs["Dashboard Bokeh Line"].sv_set(st_bokeh_line)

def register():
    bpy.utils.register_class(SvMegapolisDashboardBokehPlotLine)

def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardBokehPlotLine)
