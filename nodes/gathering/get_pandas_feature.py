import bpy
from sverchok.node_tree import SverchCustomTreeNode


class SvMegapolisGetPandasFeature(SverchCustomTreeNode, bpy.types.Node):
    """
    Node to extract a specific feature (column) from a Pandas DataFrame.

    Tooltip: Retrieves a feature from a Pandas series.
    """
    bl_idname = "SvMegapolisGetPandasFeature"
    bl_label = "Get Pandas Feature"
    bl_icon = "TEXT"
    sv_dependencies = {"pandas"}

    def sv_init(self, context):
        """Initialize input and output sockets."""
        self.inputs.new("SvStringsSocket", "Dataframe")
        self.inputs.new("SvStringsSocket", "Feature")

        self.outputs.new("SvStringsSocket", "Dataframe Out")
        self.outputs.new("SvStringsSocket", "List Out")

    def process(self):
        """Extracts the specified feature (column) from the DataFrame."""
        if not (self.inputs["Dataframe"].is_linked and self.inputs["Feature"].is_linked):
            return

        df_input = self.inputs["Dataframe"].sv_get(deepcopy=False)
        feature_input = self.inputs["Feature"].sv_get(deepcopy=False)

        if not df_input or not feature_input:
            return

        feature_name = feature_input[0][0]

        # Ensure df_input is a valid DataFrame and feature_name exists
        if feature_name not in df_input:
            print(f"Feature '{feature_name}' not found in DataFrame.")
            return

        feature_data = df_input[feature_name]
        list_out = feature_data.tolist()

        # Outputs
        self.outputs["Dataframe Out"].sv_set(feature_data)
        self.outputs["List Out"].sv_set(list_out)


def register():
    bpy.utils.register_class(SvMegapolisGetPandasFeature)


def unregister():
    bpy.utils.unregister_class(SvMegapolisGetPandasFeature)

