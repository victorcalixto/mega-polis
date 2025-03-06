import bpy
from sverchok.node_tree import SverchCustomTreeNode

class SvMegapolisPandasMapFeature(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: PandasMapFeature
    Tooltip: Applies a dictionary mapping to a feature column in a pandas dataframe
    """
    bl_idname = 'SvMegapolisPandasMapFeature'
    bl_label = 'Pandas Map Feature'
    bl_icon = 'CON_TRANSFORM_CACHE'
    sv_dependencies = {'pandas'}

    def sv_init(self, context):
        """ Initialize inputs and outputs for the node """
        # Inputs
        self.inputs.new('SvStringsSocket', "Dataframe")
        self.inputs.new('SvStringsSocket', "Feature")
        self.inputs.new('SvStringsSocket', "Dict Map Values")

        # Outputs
        self.outputs.new('SvStringsSocket', "Dataframe Output")

    def process(self):
        """ Process the dataframe and apply the dictionary mapping to the feature column """
        if not self.inputs["Dataframe"].is_linked or not self.inputs["Feature"].is_linked or not self.inputs["Dict Map Values"].is_linked:
            return

        # Get the input values
        dataframe = self.inputs["Dataframe"].sv_get(deepcopy=False)
        feature = self.inputs["Feature"].sv_get(deepcopy=False)[0][0]
        dict_map = self.inputs["Dict Map Values"].sv_get(deepcopy=False)[0]

        # Apply the dictionary map to the feature column
        mapped_data = dataframe[feature].map(dict_map)

        # Output the mapped dataframe
        self.outputs["Dataframe Output"].sv_set(mapped_data)

def register():
    bpy.utils.register_class(SvMegapolisPandasMapFeature)

def unregister():
    bpy.utils.unregister_class(SvMegapolisPandasMapFeature)

