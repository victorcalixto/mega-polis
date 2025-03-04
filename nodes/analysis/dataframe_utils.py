import bpy
from bpy.props import IntProperty, EnumProperty
from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
import io

# Define DataFrame utility functions
InfoType = namedtuple('InfoType', ['info', 'head', 'tail', 'describe'])
INFO_TYPE = InfoType('info', 'head', 'tail', 'describe')
info_type_items = [(i, i, '') for i in INFO_TYPE]


class SvMegapolisDataframeUtils(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Dataframe Utils
    Tooltip: Provides utilities for exploratory data analysis: info, head, tail, and describe.
    """
    bl_idname = 'SvMegapolisDataframeUtils'
    bl_label = 'Dataframe Utils'
    bl_icon = 'TOOL_SETTINGS'
    sv_dependencies = {'pandas'}

    # Blender Properties
    infotype: EnumProperty(
        name='Function',
        items=info_type_items,
        default="info",
        description='Choose a function to explore the data',
        update=lambda self, context: self.update_sockets(context)
    )

    numberb: IntProperty(
        name="Number",
        default=5,
        min=1,
        update=updateNode
    )

    def update_sockets(self, context):
        """Update socket visibility based on the selected function."""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        if self.infotype in {INFO_TYPE.head, INFO_TYPE.tail}:
            set_hide(self.inputs['Number'], False)
        else:
            set_hide(self.inputs['Number'], True)

        updateNode(self, context)

    def sv_init(self, context):
        """Initialise inputs and outputs."""
        self.inputs.new('SvStringsSocket', "Dataframe")
        self.inputs.new('SvStringsSocket', "Number").prop_name = 'numberb'
        self.inputs['Number'].hide_safe = True  # Hide number input by default

        self.outputs.new('SvStringsSocket', "Value")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'infotype', expand=False)

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        """Perform the selected DataFrame utility function."""
        if not self.inputs["Dataframe"].is_linked:
            return

        dataframe = self.inputs["Dataframe"].sv_get(deepcopy=False)

        if self.infotype in {INFO_TYPE.head, INFO_TYPE.tail}:
            if not self.inputs["Number"].is_linked:
                return
            number = self.inputs["Number"].sv_get(deepcopy=False)[0][0]
        else:
            number = None

        # Apply the selected function
        if self.infotype == INFO_TYPE.head:
            value = dataframe.head(number)
        elif self.infotype == INFO_TYPE.tail:
            value = dataframe.tail(number)
        elif self.infotype == INFO_TYPE.info:
            buf = io.StringIO()
            dataframe.info(buf=buf)
            value = buf.getvalue()
        else:  # self.infotype == INFO_TYPE.describe
            value = dataframe.describe()

        # Output result
        self.outputs["Value"].sv_set(value)


def register():
    bpy.utils.register_class(SvMegapolisDataframeUtils)


def unregister():
    bpy.utils.unregister_class(SvMegapolisDataframeUtils)

