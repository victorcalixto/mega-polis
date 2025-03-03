import os
import bpy
from bpy.props import BoolProperty
from sverchok.data_structure import updateNode
from sverchok.node_tree import SverchCustomTreeNode
from megapolis.dependencies import wget


class SvMegapolisDownloadDataUrl(SverchCustomTreeNode, bpy.types.Node):
    """
    Node to download data from a provided URL.

    Tooltip: Downloads data from a web link (Uniform Resource Locator - URL).
    """
    bl_idname = "SvMegapolisDownloadDataUrl"
    bl_label = "Download Data Url"
    bl_icon = "URL"
    sv_dependencies = {"wget"}

    def update_sockets(self, context):
        """Perform UX transformation before updating the node."""
        updateNode(self, context)

    download: BoolProperty(
        name="Download",
        default=False,
        description="Download file from the URL",
        update=update_sockets
    )

    def sv_init(self, context):
        """Initialize input and output sockets."""
        self.inputs.new("SvStringsSocket", "URL")
        self.inputs.new("SvStringsSocket", "Folder")
        self.outputs.new("SvStringsSocket", "Output Message")

    def draw_buttons(self, context, layout):
        """Draw buttons in the node UI."""
        layout.prop(self, "download")

    def draw_buttons_ext(self, context, layout):
        """Extended UI layout."""
        self.draw_buttons(context, layout)

    def process(self):
        """Handle the download process."""
        if not self.inputs["URL"].is_linked or not self.inputs["Folder"].is_linked:
            return

        urls = self.inputs["URL"].sv_get(deepcopy=False)
        folders = self.inputs["Folder"].sv_get(deepcopy=False)

        if not urls or not folders or not urls[0] or not folders[0]:
            return

        folder_name = folders[0][0]
        message = []

        if self.download:
            for url in urls[0]:
                if not url:
                    continue
                file_name = os.path.basename(url)
                file_path = os.path.join(folder_name, file_name)
                wget.download(url, file_path)
                message.append(f"{file_name} downloaded successfully")

        # Output message
        self.outputs["Output Message"].sv_set(message)


def register():
    bpy.utils.register_class(SvMegapolisDownloadDataUrl)


def unregister():
    bpy.utils.unregister_class(SvMegapolisDownloadDataUrl)

