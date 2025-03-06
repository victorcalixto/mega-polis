import bpy
from sverchok.node_tree import SverchCustomTreeNode


class SvMegapolisTransposeDataframe(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Transpose Dataframe
    Tooltip: Transpose a Dataframe
    """
    bl_idname = 'SvMegapolisTransposeDataframe'
    bl_label = 'Transpose Dataframe'
    bl_icon = 'CON_TRANSLIKE'
    sv_dependencies = {'pandas'}

    def sv_init(self, context):
        """ Initialize inputs and outputs """
        # Inputs
        self.inputs.new('SvStringsSocket', "Dataframe")

        # Outputs
        self.outputs.new('SvStringsSocket', "Dataframe Output")

    def process(self):
        """ Process the dataframe and transpose it """
        if not self.inputs["Dataframe"].is_linked:
            return

        # Get the input dataframe
        self.df = self.inputs["Dataframe"].sv_get(deepcopy=False)

        # Transpose the dataframe
        df_transposed = self.df.T

        # Output the transposed dataframe
        self.outputs["Dataframe Output"].sv_set(df_transposed)


def register():
    bpy.utils.register_class(SvMegapolisTransposeDataframe)


def unregister():
    bpy.utils.unregister_class(SvMegapolisTransposeDataframe)

