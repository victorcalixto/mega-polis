import bpy
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from megapolis.dependencies import pandas as pd


class SvMegapolisDashboardDataframe(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Dashboard Dataframe
    Tooltip: Dashboard Dataframe
    """
    bl_idname = 'SvMegapolisDashboardDataframe'
    bl_label = 'Dashboard Dataframe'
    bl_icon = 'WORDWRAP_ON'
    sv_dependencies = {'pandas', 'streamlit'}

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """Need to do UX transformation before updating node."""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self, context)

    # Blender Properties Buttons
    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Dataframe")

        # Outputs
        self.outputs.new('SvStringsSocket', "Dashboard Dataframe")

    def process(self):
        if not self.inputs["Dataframe"].is_linked:
            return

        self.dataframe = self.inputs["Dataframe"].sv_get(deepcopy=False)
        df = pd.DataFrame.to_json(self.dataframe)

        write = f"""
st.dataframe(pd.DataFrame.from_dict({df}))\n
        """

        st_df = write

        # Output
        self.outputs["Dashboard Dataframe"].sv_set([st_df])


def register():
    bpy.utils.register_class(SvMegapolisDashboardDataframe)


def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardDataframe)

