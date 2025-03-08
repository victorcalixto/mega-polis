import bpy
from bpy.props import BoolProperty, StringProperty

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import levels_of_list_or_np
from sverchok.utils.sv_text_io_common import (
    READY_COLOR, TEXT_IO_CALLBACK
)
from megapolis.dependencies import pandas as pd
from megapolis.dependencies import tabulate

try:
    from tabulate import tabulate
except ImportError:
    pass


def get_sv_data(node):
    out = []
    if node.inputs['Data'].links:
        data = node.inputs['Data'].sv_get(deepcopy=False)
        pd.set_option('display.max_rows', None)
        df_vis = tabulate(data, headers='keys', tablefmt='psql', showindex=True, numalign="right")
        out = str(df_vis)
    return out


def format_to_text(data):
    deptl = levels_of_list_or_np(data)
    out = ''
    if deptl > 1:
        for i, sub_data in enumerate(data):
            if i > 0:
                out += '\n'
            sub_data_len = len(sub_data) - 1
            for j, d in enumerate(sub_data):
                out += str(d)
                if j < sub_data_len:
                    out += '\n'
    else:
        for d in data:
            out += str(d) + '\n'
    return out


class SvMegapolisDataframeVis(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Dataframe to Sverchok Text
    Tooltip: Quickly write A Dataframe from NodeView to text datablock
    """
    bl_idname = 'SvMegapolisDataframeVis'
    bl_label = 'Dataframe Vis'
    bl_icon = 'WORDWRAP_ON'

    sv_modes = [
        ('compact', 'Compact', 'Using str()', 1),
        ('pretty', 'Pretty', 'Using pretty print', 2)
    ]

    def change_mode(self, context):
        self.inputs.clear()
        self.inputs.new('SvStringsSocket', 'Data')

    def pointer_update(self, context):
        if self.file_pointer:
            self.text = self.file_pointer.name
        else:
            self.text = ""

    text: StringProperty(name='text')
    file_pointer: bpy.props.PointerProperty(type=bpy.types.Text, poll=lambda s, o: True, update=pointer_update)

    append: BoolProperty(default=False, description="Append to output file")
    base_name: StringProperty(name='base_name', default='Col ')
    multi_socket_type: StringProperty(name='multi_socket_type', default='SvStringsSocket')

    autodump: BoolProperty(default=False, description="autodump", name="auto dump")
    unwrap: BoolProperty(default=True, description="unwrap", name="unwrap")

    def sv_init(self, context):
        self.inputs.new('SvStringsSocket', 'Data')

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        col.prop(self, 'autodump', toggle=True)

        row = col.row(align=True)
        row.prop_search(self, 'file_pointer', bpy.data, 'texts', text="Write")
        row.operator("text.new", icon="ZOOM_IN", text='')

        if not self.autodump:
            col2 = col.column(align=True)
            row = col2.row(align=True)
            row.scale_y = 4.0 if self.prefs_over_sized_buttons else 1
            row.operator(TEXT_IO_CALLBACK, text='D U M P').fn_name = 'dump'
            col2.prop(self, 'append', text="Append")

    def process(self):
        # upgrades older versions of ProfileMK3 to the version that has self.file_pointer
        if self.text and not self.file_pointer:
            text = self.get_bpy_data_from_name(self.text, bpy.data.texts)
            if text:
                self.file_pointer = text

        if self.autodump:
            self.append = False
            self.dump()

    # Build a string with data from sockets
    def dump(self):
        out = self.get_data()
        if len(out) == 0:
            return False

        if self.file_pointer:
            self.text = self.file_pointer.name

        if not self.append:
            bpy.data.texts[self.text].clear()
        bpy.data.texts[self.text].write(out)
        self.color = READY_COLOR

        return True

    def get_data(self):
        out = get_sv_data(node=self)
        return out


def register():
    bpy.utils.register_class(SvMegapolisDataframeVis)


def unregister():
    bpy.utils.unregister_class(SvMegapolisDataframeVis)

