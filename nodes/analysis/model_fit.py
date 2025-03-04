import bpy
from bpy.props import FloatProperty, BoolProperty

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

# Megapolis Dependencies
from megapolis.dependencies import sklearn as skl


class SvMegapolisModelFit(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Model Fit
    Tooltip: Model Fit
    """
    bl_idname = 'SvMegapolisModelFit'
    bl_label = 'Model Fit'
    bl_icon = 'SNAP_FACE_CENTER'
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
        description='Runs Model Fit',
        update=update_sockets
    )

    train_size: FloatProperty(
        name="train_size",
        description="Train size for the model",
        default=0.30,
        max=0.99,
        min=0.01,
        update=update_sockets
    )

    def sv_init(self, context):
        # Inputs
        self.inputs.new('SvStringsSocket', "Model")
        self.inputs.new('SvStringsSocket', "X")
        self.inputs.new('SvStringsSocket', "y")

        # Outputs
        self.outputs.new('SvStringsSocket', "Model Out")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'run')
        layout.prop(self, 'train_size')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        if not self.inputs["Model"].is_linked or not self.inputs["X"].is_linked or not self.inputs["y"].is_linked:
            return

        self.model = self.inputs["Model"].sv_get(deepcopy=False)
        self.x = self.inputs["X"].sv_get(deepcopy=False)
        self.y = self.inputs["y"].sv_get(deepcopy=False)

        model = self.model[0]
        X = self.x
        y = self.y
        train_size = self.train_size

        if self.run:
            X_train, X_test, y_train, y_test = skl.model_selection.train_test_split(
                X, y, shuffle=True, train_size=train_size
            )

            data = model.fit(X_train, y_train)
            model_out = [data]
        else:
            model_out = ''

        # Outputs
        self.outputs["Model Out"].sv_set(model_out)


def register():
    bpy.utils.register_class(SvMegapolisModelFit)


def unregister():
    bpy.utils.unregister_class(SvMegapolisModelFit)

