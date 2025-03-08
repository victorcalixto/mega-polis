import os
import bpy
from bpy.props import BoolProperty
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


class SvMegapolisDashboardCreation(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Dashboard Creation
    Tooltip: Dashboard Creation
    """
    bl_idname = 'SvMegapolisDashboardCreation'
    bl_label = 'Dashboard Creation'
    bl_icon = 'SEQ_SPLITVIEW'
    sv_dependencies = {'streamlit'}

    create: BoolProperty(
        name="Create",
        description="Create Dashboard",
        default=False,
        update=updateNode
    )

    def sv_init(self, context):
        # Inputs
        self.inputs.new('SvStringsSocket', "Dashboard Content")
        self.inputs.new('SvStringsSocket', "Dashboard Name")
        self.inputs.new('SvStringsSocket', "Folder")
        # Outputs
        self.outputs.new('SvStringsSocket', "Output Message")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'create')

    def process(self):
        if not (
            self.inputs["Dashboard Content"].is_linked and
            self.inputs["Dashboard Name"].is_linked and
            self.inputs["Folder"].is_linked
        ):
            return

        dashboard_content = self.inputs["Dashboard Content"].sv_get(deepcopy=False)[0]
        dashboard_name = str(self.inputs["Dashboard Name"].sv_get(deepcopy=False)[0][0])
        folder = self.inputs["Folder"].sv_get(deepcopy=False)[0][0]

        imports = """
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import io
import streamlit.components.v1 as components
from ipywidgets import embed
import pyvista as pv
from pyvista.jupyter.pv_pythreejs import convert_plotter
from pyvista import examples
import leafmap.kepler as kepler
from bokeh.plotting import figure
import seaborn as sns
import matplotlib.pyplot as plt
        """

        pyvista_def = """
pv.set_plot_theme('document')

def pyvista_streamlit(plotter, plot_width, plot_height):
    widget = convert_plotter(plotter)
    state = embed.dependency_state(widget)
    fp = io.StringIO()
    embed.embed_minimal_html(fp, None, title="", state=state)
    fp.seek(0)
    snippet = fp.read()
    components.html(snippet, width=plot_width, height=plot_height)
        """

        str_content = ''.join(dashboard_content)
        template_df = f"{imports}\n{pyvista_def}\n{str_content}"

        if self.create:
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, f"{dashboard_name}.py"), "w") as f:
                f.write(template_df)

        self.outputs["Output Message"].sv_set(template_df)


def register():
    bpy.utils.register_class(SvMegapolisDashboardCreation)


def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardCreation)

