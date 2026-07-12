import bpy
from bpy.props import EnumProperty
import numpy as np
import numexpr as ne

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

# ---- Attributes list (unchanged) ----
Attribute_type = namedtuple('AttributeType', [
    'aspect', 'profile_curvature','planform_curvature','curvature',
    'slope_riserun','slope_degrees','slope_percentage','slope_radians'
])
ATTRIBUTETYPE = Attribute_type(
    'aspect', 'profile_curvature','planform_curvature','curvature',
    'slope_riserun','slope_degrees','slope_percentage','slope_radians'
)
attributetype_items = [(i, i, '') for i in ATTRIBUTETYPE]

CELL_SIZE_DEFAULT = 1.0  # set to your DEM pixel size if needed

# ---- Core math using 3x3 finite differences + NumExpr ----
def _finite_diffs(a: np.ndarray, cell: float):
    """
    Compute first (p=dz/dx, q=dz/dy) and second (r,s,t) derivatives
    on a regular grid using 3x3 stencils. Edges are replicated.
    """
    A = np.pad(a, 1, mode='edge')

    z1 = A[:-2, :-2]; z2 = A[:-2, 1:-1]; z3 = A[:-2, 2:]
    z4 = A[1:-1, :-2]; z5 = A[1:-1, 1:-1]; z6 = A[1:-1, 2:]
    z7 = A[2:, :-2];  z8 = A[2:, 1:-1];  z9 = A[2:, 2:]

    inv8c = 1.0 / (8.0 * cell)
    invc2 = 1.0 / (cell * cell)
    # p, q
    p = ne.evaluate("((z3 + 2*z6 + z9) - (z1 + 2*z4 + z7)) * inv8c")
    q = ne.evaluate("((z7 + 2*z8 + z9) - (z1 + 2*z2 + z3)) * inv8c")
    # r, t, s (Zevenbergen & Thorne style weights)
    # r = d2z/dx2, t = d2z/dy2, s = d2z/dxdy
    r = ne.evaluate("( (z1 - 2*z2 + z3) + 2*(z4 - 2*z5 + z6) + (z7 - 2*z8 + z9) ) * (invc2/3.0)")
    t = ne.evaluate("( (z1 - 2*z4 + z7) + 2*(z2 - 2*z5 + z8) + (z3 - 2*z6 + z9) ) * (invc2/3.0)")
    s = ne.evaluate("(z1 - z3 - z7 + z9) * (0.25 * invc2)")
    return p, q, r, s, t

def _terrain_attribute(arr: np.ndarray, attrib: str, cell: float):
    p, q, r, s, t = _finite_diffs(arr, cell)
    # G = sqrt(p^2 + q^2)
    G = ne.evaluate("sqrt(p*p + q*q)")

    if attrib == "slope_riserun":
        out = G
    elif attrib == "slope_degrees":
        # atan(G) in radians -> degrees
        out = ne.evaluate("arctan(G)") * (180.0 / np.pi)
    elif attrib == "slope_percentage":
        out = ne.evaluate("G * 100.0")
    elif attrib == "slope_radians":
        out = ne.evaluate("arctan(G)")
    elif attrib == "aspect":
        # 0° = North, clockwise
        # asp = degrees(arctan2(-p, q)); rotate: (90 - asp) mod 360
        asp = np.degrees(np.arctan2(ne.evaluate("-p"), q))
        out = (90.0 - asp) % 360.0
    elif attrib == "profile_curvature":
        # kp = -(r*p^2 + 2*s*p*q + t*q^2) / (G^3)
        denom = ne.evaluate("G*G*G")
        num = ne.evaluate("-(r*p*p + 2.0*s*p*q + t*q*q)")
        with np.errstate(divide='ignore', invalid='ignore'):
            out = np.where(denom > 0, num / denom, 0.0)
    elif attrib == "planform_curvature":
        # kc = (r*q^2 - 2*s*p*q + t*p^2) / (G^3)
        denom = ne.evaluate("G*G*G")
        num = ne.evaluate("(r*q*q - 2.0*s*p*q + t*p*p)")
        with np.errstate(divide='ignore', invalid='ignore'):
            out = np.where(denom > 0, num / denom, 0.0)
    elif attrib == "curvature":
        out = ne.evaluate("r + t")  # Laplacian proxy
    else:
        raise ValueError(f"Unknown attribute: {attrib}")
    return out

# ---- Sverchok node (template preserved) ----
class SvMegapolisDemTerrainAttributesExt(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Dem Terrain Attributes Ext
    Tooltip: Provides methods for extract Terrain Attributes values: Aspect, Curvature, and Slope.
    """
    bl_idname = 'SvMegapolisDemTerrainAttributesExt'
    bl_label = 'Dem Terrain Attributes Ext'
    bl_icon = 'MESH_DATA'
    # Declare lightweight deps for Sverchok UI
    sv_dependencies = {'numpy', 'numexpr'}

    def update_sockets(self, context):
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status
        updateNode(self, context)

    attributetype: EnumProperty(
        name='Terrain Attribute', items=attributetype_items,
        default="slope_degrees",
        description='Choose a terrain attribute to extract values',
        update=update_sockets
    )

    def sv_init(self, context):
        self.inputs.new('SvStringsSocket', "Dem Array")
        self.outputs.new('SvVerticesSocket', "Attribute Values")
        self.outputs.new('SvVerticesSocket', "Array Out")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'attributetype', expand=False)

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        if not self.inputs["Dem Array"].is_linked:
            return

        arr_in = self.inputs["Dem Array"].sv_get(deepcopy=False)
        a = np.asarray(arr_in, dtype=float)
        if a.ndim != 2:
            try:
                a = np.array(a, dtype=float)
            except Exception:
                return
            if a.ndim != 2:
                return

        # Compute attribute with NumExpr-accelerated math
        out = _terrain_attribute(a, self.attributetype, CELL_SIZE_DEFAULT)

        # Flatten for Attribute Values; pass 2D array for Array Out
        self.outputs["Attribute Values"].sv_set(out.ravel().tolist())
        self.outputs["Array Out"].sv_set(out.tolist())

def register():
    bpy.utils.register_class(SvMegapolisDemTerrainAttributesExt)

def unregister():
    bpy.utils.unregister_class(SvMegapolisDemTerrainAttributesExt)

