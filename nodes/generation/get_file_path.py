import bpy
import os
from sverchok.node_tree import SverchCustomTreeNode


class SvMegapolisGetFilePath(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: GetFilePath
    Tooltip: Get File Path
    """
    bl_idname = "SvMegapolisGetFilePath"
    bl_label = "Get File Path"
    bl_icon = "FILE_FOLDER"

    def sv_init(self, context):
        """Initialize node inputs and outputs."""
        self.inputs.new("SvFilePathSocket", "File")
        self.outputs.new("SvStringsSocket", "File Path")

    def process(self):
        """Extract the directory path from the input file."""
        if not self.inputs["File"].is_linked:
            return

        file_path = self.inputs["File"].sv_get(deepcopy=False)[0][0]
        directory = os.path.dirname(os.path.abspath(file_path))

        self.outputs["File Path"].sv_set([directory])


def register():
    bpy.utils.register_class(SvMegapolisGetFilePath)


def unregister():
    bpy.utils.unregister_class(SvMegapolisGetFilePath)

