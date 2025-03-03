import bpy
from sverchok.node_tree import SverchCustomTreeNode
from megapolis.dependencies import pandas as pd


class SvMegapolisPandasDataframe(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Pandas Series
    Tooltip: Creates a Pandas DataFrame from a Pandas Series
    """
    bl_idname = 'SvMegapolisPandasDataframe'
    bl_label = 'Pandas DataFrame'
    bl_icon = 'TEXT'
    sv_dependencies = {'pandas'}

    def sv_init(self, context):
        """Initialize input and output sockets."""
        self.inputs.new('SvStringsSocket', "Pandas Series")
        self.inputs.new('SvStringsSocket', "Feature Names")
        self.outputs.new('SvStringsSocket', "Pandas DataFrame")

    def process(self):
        """Process the input data and create a Pandas DataFrame."""
        if not self.inputs["Pandas Series"].is_linked or not self.inputs["Feature Names"].is_linked:
            return

        series = self.inputs["Pandas Series"].sv_get(deepcopy=False)
        features = self.inputs["Feature Names"].sv_get(deepcopy=False)

        dataframe = pd.concat(series, axis=1)
        dataframe.columns = features

        self.outputs["Pandas DataFrame"].sv_set(dataframe)


def register():
    bpy.utils.register_class(SvMegapolisPandasDataframe)


def unregister():
    bpy.utils.unregister_class(SvMegapolisPandasDataframe)

