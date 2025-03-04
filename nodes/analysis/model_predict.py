import bpy
from bpy.props import BoolProperty

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


class SvMegapolisModelPredict(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Model Predict
    Tooltip: Model Predict
    """
    bl_idname = 'SvMegapolisModelPredict'
    bl_label = 'Model Predict'
    bl_icon = 'AUTOMERGE_OFF'
    sv_dependencies = {'sklearn'}

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """Need to do UX transformation before updating node."""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self, context)

    # Blender Properties Buttons
    run: BoolProperty(
        name='run',
        default=False,
        description='Runs Model Predict',
        update=update_sockets
    )

    def sv_init(self, context):
        # Inputs
        self.inputs.new('SvStringsSocket', "Model")
        self.inputs.new('SvStringsSocket', "X")

        # Outputs
        self.outputs.new('SvStringsSocket', "Predictions Array")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'run')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        if not self.inputs["Model"].is_linked or not self.inputs["X"].is_linked:
            return

        self.model = self.inputs["Model"].sv_get(deepcopy=False)
        self.x = self.inputs["X"].sv_get(deepcopy=False)

        model = self.model[0]
        X_test = self.x

        if self.run:
            data = model.predict(X_test)
            predictions = [data]
        else:
            predictions = ''

        # Outputs
        self.outputs["Predictions Array"].sv_set(predictions)


def register():
    bpy.utils.register_class(SvMegapolisModelPredict)


def unregister():
    bpy.utils.unregister_class(SvMegapolisModelPredict)

