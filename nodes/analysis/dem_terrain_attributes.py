import bpy
from bpy.props import EnumProperty
from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

# Megapolis Dependencies
from megapolis.dependencies import richdem as rd

# Define Terrain Attributes
AttributeType = namedtuple(
    'AttributeType',
    ['aspect', 'profile_curvature', 'planform_curvature', 'curvature',
     'slope_riserun', 'slope_degrees', 'slope_percentage', 'slope_radians']
)

ATTRIBUTE_TYPE = AttributeType(
    'aspect', 'profile_curvature', 'planform_curvature', 'curvature',
    'slope_riserun', 'slope_degrees', 'slope_percentage', 'slope_radians'
)

attribute_type_items = [(i, i, '') for i in ATTRIBUTE_TYPE]


class SvMegapolisDemTerrainAttributes(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: DEM Terrain Attributes
    Tooltip: Extracts terrain attributes such as Aspect, Curvature, and Slope.
    """
    bl_idname = 'SvMegapolisDemTerrainAttributes'
    bl_label = 'DEM Terrain Attributes'
    bl_icon = 'OUTLINER_DATA_LATTICE'
    sv_dependencies = {'richdem'}

    # Blender Properties
    attributetype: EnumProperty(
        name='Terrain Attribute',
        items=attribute_type_items,
        default="slope_degrees",
        description='Choose a terrain attribute to extract values',
        update=lambda self, context: updateNode(self, context)
    )

    def sv_init(self, context):
        """Initialize inputs and outputs."""
        self.inputs.new('SvStringsSocket', "DEM Array")
        self.outputs.new('SvVerticesSocket', "Attribute Values")
        self.outputs.new('SvVerticesSocket', "Array Out")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'attributetype', expand=False)

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
        """Compute the selected terrain attribute."""
        if not self.inputs["DEM Array"].is_linked:
            return

        dem_array = self.inputs["DEM Array"].sv_get(deepcopy=False)
        dem_richdem = rd.rdarray(dem_array, no_data=-9999)
        dem_slope = rd.TerrainAttribute(dem_richdem, attrib=self.attributetype)
        attribute_values = dem_slope.flatten()

        # Output results
        self.outputs["Attribute Values"].sv_set(attribute_values)
        self.outputs["Array Out"].sv_set(dem_slope)


def register():
    bpy.utils.register_class(SvMegapolisDemTerrainAttributes)


def unregister():
    bpy.utils.unregister_class(SvMegapolisDemTerrainAttributes)

