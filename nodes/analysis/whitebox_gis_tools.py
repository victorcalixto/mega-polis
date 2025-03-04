import bpy
from bpy.props import BoolProperty

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

import multiprocessing
from subprocess import call


class SvMegapolisWhiteboxGisTools(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: WhiteboxGisTools
    Tooltip: Opens a Whitebox Tool Window
    """
    bl_idname = 'SvMegapolisWhiteboxGisTools'
    bl_label = 'Whitebox Gis Tools'
    bl_icon = 'SNAP_VOLUME'

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """Need to do UX transformation before updating node."""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status
        
        updateNode(self, context)

    # Blender Properties Buttons
    run: BoolProperty(
        name='Run', 
        default=False,
        description='Runs the Whitebox Node', 
        update=update_sockets
    )

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Whitebox Folder")

        # outputs
        self.outputs.new('SvStringsSocket', "Output Message")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'run')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        if not self.inputs["Whitebox Folder"].is_linked: 
            return

        self.folder = self.inputs["Whitebox Folder"].sv_get(deepcopy=False)
        whitebox_folder = self.folder[0][0]
        message = "Waiting to run..."

        def thread_second():
            call(["python", f"{whitebox_folder}/wb_runner.py"])
            
        if self.run:
            message = "Opening Whitebox Tools"
            process_thread = multiprocessing.Process(target=thread_second)  # <- note extra ','
            process_thread.start()

        # Outputs
        self.outputs["Output Message"].sv_set(message)


def register():
    bpy.utils.register_class(SvMegapolisWhiteboxGisTools)


def unregister():
    bpy.utils.unregister_class(SvMegapolisWhiteboxGisTools)

