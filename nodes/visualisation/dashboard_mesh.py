import bpy
from bpy.props import IntProperty
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

class SvMegapolisDashboardMesh(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Dashboard Mesh
    Tooltip: Dashboard Mesh
    """
    bl_idname = 'SvMegapolisDashboardMesh'
    bl_label = 'Dashboard Mesh'
    bl_icon = 'MESH_MONKEY'

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """Need to do UX transformation before updating node."""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        updateNode(self, context)

    plot_width: IntProperty(
        name="Plot Width",
        description="Plot Width",
        default=800,
        min=1,
        max=10000,
        update=update_sockets
    )

    plot_height: IntProperty(
        name="Plot Height",
        description="Plot Height",
        default=600,
        min=1,
        max=10000,
        update=update_sockets
    )

    # Blender Properties Buttons
    def sv_init(self, context):
        # Inputs
        self.inputs.new('SvVerticesSocket', "Vertices")
        self.inputs.new('SvStringsSocket', "Faces")

        # Outputs
        self.outputs.new('SvStringsSocket', "Dashboard Mesh")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'plot_width')
        layout.prop(self, 'plot_height')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        if not self.inputs["Vertices"].is_linked or not self.inputs["Faces"].is_linked:
            return
        
        self.vertices = self.inputs["Vertices"].sv_get(deepcopy=False)
        self.faces = self.inputs["Faces"].sv_get(deepcopy=False)
        
        vertices = self.vertices
        faces = self.faces
        plot_width = self.plot_width
        plot_height = self.plot_height

        geometry = f"""
plot_width = {plot_width}
plot_height = {plot_height}

vertices = {vertices}
faces = {faces}

vertices_array = np.array(vertices)

faces_l = [len(j) for i in faces for j in i]

for i in faces:
    for j in i:
        j.insert(0, faces_l[i.index(j)])

list_surf = []

for i in range(0, len(vertices)):
    faces_ = np.hstack(faces[i])
    vertices_ = np.array(vertices_array[i])
    list_surf.append(pv.PolyData(vertices_, faces_))

plotter = pv.Plotter()

for i in list_surf:
    plotter.add_mesh(i, color='grey')

pyvista_streamlit(plotter, plot_width, plot_height)
        """

        plot_pyvista = geometry
        
        # Output
        self.outputs["Dashboard Mesh"].sv_set(plot_pyvista)


def register():
    bpy.utils.register_class(SvMegapolisDashboardMesh)


def unregister():
    bpy.utils.unregister_class(SvMegapolisDashboardMesh)

