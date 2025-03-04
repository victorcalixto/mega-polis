import bpy
from sverchok.node_tree import SverchCustomTreeNode


class SvMegapolisGetFeatureAt(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Get Feature At
    Tooltip: Retrieves a feature from a DataFrame at specified X and Y feature indices.
    """
    bl_idname = 'SvMegapolisGetFeatureAt'
    bl_label = 'Get Feature At'
    bl_icon = 'PRESET_NEW'
    sv_dependencies = {'pandas'}

    def sv_init(self, context):
        """Initialize input and output sockets."""
        self.inputs.new('SvStringsSocket', "Dataframe")
        self.inputs.new('SvStringsSocket', "Feature X")
        self.inputs.new('SvStringsSocket', "Feature Y")
        self.outputs.new('SvStringsSocket', "Feature Out")

    def process(self):
        """Extracts a feature at the given X and Y indices."""
        if not (self.inputs["Dataframe"].is_linked and
                self.inputs["Feature X"].is_linked and
                self.inputs["Feature Y"].is_linked):
            return

        df = self.inputs["Dataframe"].sv_get(deepcopy=False)
        feature_x = self.inputs["Feature X"].sv_get(deepcopy=False)
        feature_y = self.inputs["Feature Y"].sv_get(deepcopy=False)

        index_feature_x = feature_x[0][0]
        index_feature_y = feature_y[0][0]

        feature_value = df.at[index_feature_x, index_feature_y]

        # Output the retrieved feature
        self.outputs["Feature Out"].sv_set([feature_value])


def register():
    bpy.utils.register_class(SvMegapolisGetFeatureAt)


def unregister():
    bpy.utils.unregister_class(SvMegapolisGetFeatureAt)

