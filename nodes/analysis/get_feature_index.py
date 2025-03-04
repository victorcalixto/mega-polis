import bpy
from sverchok.node_tree import SverchCustomTreeNode


class SvMegapolisGetFeatureIndex(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Get Feature Index
    Tooltip: Retrieves a feature from a DataFrame using integer-based index lookup (iat).
    """
    bl_idname = 'SvMegapolisGetFeatureIndex'
    bl_label = 'Get Feature Index'
    bl_icon = 'EVENT_I'
    sv_dependencies = {'pandas'}

    def sv_init(self, context):
        """Initialize input and output sockets."""
        self.inputs.new('SvStringsSocket', "Dataframe")
        self.inputs.new('SvStringsSocket', "Index Feature X")
        self.inputs.new('SvStringsSocket', "Index Feature Y")
        self.outputs.new('SvStringsSocket', "Feature Out")

    def process(self):
        """Extracts a feature using integer-based index lookup."""
        if not (self.inputs["Dataframe"].is_linked and
                self.inputs["Index Feature X"].is_linked and
                self.inputs["Index Feature Y"].is_linked):
            return

        df = self.inputs["Dataframe"].sv_get(deepcopy=False)
        index_x = self.inputs["Index Feature X"].sv_get(deepcopy=False)[0][0]
        index_y = self.inputs["Index Feature Y"].sv_get(deepcopy=False)[0][0]

        feature_value = df.iat[index_x, index_y]

        # Output the retrieved feature
        self.outputs["Feature Out"].sv_set([feature_value])


def register():
    bpy.utils.register_class(SvMegapolisGetFeatureIndex)


def unregister():
    bpy.utils.unregister_class(SvMegapolisGetFeatureIndex)

