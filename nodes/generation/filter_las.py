import bpy
import numpy as np
from bpy.props import EnumProperty
from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from megapolis.dependencies import laspy


Classification = namedtuple(
    "Classification",
    [
        "never", "uncla", "ground", "low_vegetation", "med_vegetation", "high_vegetation", "building",
        "noise", "reserved", "water", "rail", "road", "overlap", "wire_guard", "wire_conductor",
        "transmission", "wire_connector", "bridge", "high_noise"
    ]
)
CLASSIFICATION = Classification(*Classification._fields)
classification_items = [(i, i, "") for i in CLASSIFICATION]


def get_coordinates(points_filtered, las):
    """Calculate the real-world coordinates from LAS file data."""
    return np.stack(
        [
            (points_filtered.X * las.header.scales[0]) + las.header.offsets[0],
            (points_filtered.Y * las.header.scales[1]) + las.header.offsets[1],
            (points_filtered.Z * las.header.scales[2]) + las.header.offsets[2]
        ],
        axis=1
    )


class SvMegapolisFilterLas(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Filter Las
    Tooltip: Filter Las
    """
    bl_idname = "SvMegapolisFilterLas"
    bl_label = "Filter Las"
    bl_icon = "POINTCLOUD_POINT"

    classification: EnumProperty(
        name="Classification",
        items=classification_items,
        default="ground",
        description="Choose a Classification Feature",
        update=updateNode
    )

    def sv_init(self, context):
        """Initialize node inputs and outputs."""
        self.inputs.new("SvFilePathSocket", "Path")
        self.inputs.new("SvStringsSocket", "Points Data")
        self.outputs.new("SvStringsSocket", "Points Data Filtered")
        self.outputs.new("SvVerticesSocket", "Points")

    def draw_buttons(self, context, layout):
        """Draw classification selection UI."""
        layout.prop(self, "classification")

    def draw_buttons_ext(self, context, layout):
        """Extended UI panel."""
        self.draw_buttons(context, layout)

    def process(self):
        """Process LAS data and filter points based on classification."""
        if not self.inputs["Path"].is_linked or not self.inputs["Points Data"].is_linked:
            return

        path = self.inputs["Path"].sv_get(deepcopy=False)[0][0]
        points_data = self.inputs["Points Data"].sv_get(deepcopy=False)

        las = laspy.read(path)
        classification_dict = {cls: idx for idx, cls in enumerate(CLASSIFICATION)}

        points_filtered = points_data.points[points_data.classification == classification_dict[self.classification]]
        coordinates = get_coordinates(points_filtered, las)

        self.outputs["Points Data Filtered"].sv_set(points_filtered)
        self.outputs["Points"].sv_set([coordinates])


def register():
    bpy.utils.register_class(SvMegapolisFilterLas)


def unregister():
    bpy.utils.unregister_class(SvMegapolisFilterLas)

