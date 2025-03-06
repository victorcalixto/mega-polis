import bpy
from sverchok.node_tree import SverchCustomTreeNode


def make_faces(lst, x_shape, y_shape):
    """Generate face indices from a grid of vertices."""
    lst.extend(
        [
            (x * x_shape + y, x * x_shape + y + 1, (x + 1) * x_shape + y + 1, (x + 1) * x_shape + y)
            for x in range(y_shape - 1)
            for y in range(x_shape - 1)
        ]
    )


class SvMegapolisFacesFromVertices(SverchCustomTreeNode, bpy.types.Node):
    
    """
    Triggers: FacesFromVertices
    Tooltip: Faces from Vertices
    """

    bl_idname = "SvMegapolisFacesFromVertices"
    bl_label = "Faces From Vertices"
    bl_icon = "VIEW_ORTHO"

    def sv_init(self, context):
        """Initialize node inputs and outputs."""
        self.inputs.new("SvVerticesSocket", "Vertices")
        self.inputs.new("SvStringsSocket", "X Shape")
        self.inputs.new("SvStringsSocket", "Y Shape")
        self.outputs.new("SvStringsSocket", "Faces")

    def process(self):
        """Generate faces from vertices."""
        if not (self.inputs["Vertices"].is_linked and
                self.inputs["X Shape"].is_linked and
                self.inputs["Y Shape"].is_linked):
            return

        x_shape = self.inputs["X Shape"].sv_get(deepcopy=False)[0][0]
        y_shape = self.inputs["Y Shape"].sv_get(deepcopy=False)[0][0]

        faces_s = []
        make_faces(faces_s, x_shape, y_shape)
        
        self.outputs["Faces"].sv_set([faces_s])


def register():
    bpy.utils.register_class(SvMegapolisFacesFromVertices)


def unregister():
    bpy.utils.unregister_class(SvMegapolisFacesFromVertices)

