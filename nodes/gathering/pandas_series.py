import bpy
from sverchok.node_tree import SverchCustomTreeNode
import pandas as pd


class SvMegapolisPandasSeries(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Pandas Series
    Tooltip: Creates a Pandas Series from a list.
    """
    bl_idname = 'SvMegapolisPandasSeries'
    bl_label = 'Pandas Series'
    bl_icon = 'TEXT'
    sv_dependencies = {'osmnx'}

    def sv_init(self, context):
        """Initialize node inputs and outputs."""
        self.inputs.new('SvStringsSocket', "List")
        self.outputs.new('SvStringsSocket', "Pandas Series")

    def process(self):
        """Process node execution to create a Pandas Series."""
        if not self.inputs["List"].is_linked:
            return

        input_list = self.inputs["List"].sv_get(deepcopy=False)
        series = pd.Series(input_list[0])
        self.outputs["Pandas Series"].sv_set([series])


def register():
    """Register the node class in Blender."""
    bpy.utils.register_class(SvMegapolisPandasSeries)


def unregister():
    """Unregister the node class from Blender."""
    bpy.utils.unregister_class(SvMegapolisPandasSeries)

