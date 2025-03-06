import bpy
from sverchok.node_tree import SverchCustomTreeNode


class SvMegapolisPandasFilter(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Pandas Filter
    Tooltip: Creates a Pandas Filter
    """
    bl_idname = 'SvMegapolisPandasFilter'
    bl_label = 'Pandas Filter'
    bl_icon = 'FILTER'
    sv_dependencies = {'pandas'}

    def sv_init(self, context):
        """ Initialize inputs and outputs for the node """
        # Inputs
        self.inputs.new('SvStringsSocket', "Dataframe")
        self.inputs.new('SvStringsSocket', "Filter")

        # Outputs
        self.outputs.new('SvStringsSocket', "Dataframe Output")

    def process(self):
        """ Apply filter to the dataframe """
        if not self.inputs["Dataframe"].is_linked or not self.inputs["Filter"].is_linked:
            return

        # Get the input values
        dataframe = self.inputs["Dataframe"].sv_get(deepcopy=False)
        filter_values = self.inputs["Filter"].sv_get(deepcopy=False)

        # Extract filter columns
        filters = filter_values[0][0].split(',')
        
        # Apply the filter to the dataframe
        df_out = dataframe.filter(items=filters)

        # Output the filtered dataframe
        self.outputs["Dataframe Output"].sv_set(df_out)


def register():
    bpy.utils.register_class(SvMegapolisPandasFilter)


def unregister():
    bpy.utils.unregister_class(SvMegapolisPandasFilter)

