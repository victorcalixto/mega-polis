
import bpy
import sys
from bpy.types import AddonPreferences

if bpy.app.version >= (2, 91, 0):
    PYPATH = sys.executable
else:
    PYPATH = bpy.app.binary_path_python

import megapolis
from sverchok.dependencies import draw_message
from megapolis.dependencies import ex_dependencies, pip, ensurepip
from sverchok.utils.context_managers import addon_preferences
from sverchok.ui.utils import message_on_layout

COMMITS_LINK = 'https://api.github.com/repos/victorcalixto/mega-polis/commits'
ADDON_NAME = megapolis.__name__
ADDON_PRETTY_NAME = 'MEGA-POLIS'
ARCHIVE_LINK = 'https://github.com/victorcalixto/mega-polis/archive/'
MASTER_BRANCH_NAME = 'main'

def draw_in_sv_prefs(layout):
    draw_message(layout, "geopandas", dependencies=ex_dependencies)
    draw_message(layout, "leafmap", dependencies=ex_dependencies)
    draw_message(layout, "osmnx", dependencies=ex_dependencies)
    draw_message(layout, "pandas", dependencies=ex_dependencies)
    draw_message(layout, "laspy", dependencies=ex_dependencies)
    draw_message(layout, "rasterio", dependencies=ex_dependencies)
    draw_message(layout, "pillow", dependencies=ex_dependencies)
    draw_message(layout, "mapillary", dependencies=ex_dependencies)
    draw_message(layout, "wget", dependencies=ex_dependencies)
    draw_message(layout, "networkx", dependencies=ex_dependencies)
    draw_message(layout, "scikitlearn", dependencies=ex_dependencies)
    draw_message(layout, "streamlit", dependencies=ex_dependencies)
    draw_message(layout, "pyvista", dependencies=ex_dependencies)
    draw_message(layout, "seaborn", dependencies=ex_dependencies)
    draw_message(layout, "visilibity", dependencies=ex_dependencies)
    draw_message(layout, "opencvpython", dependencies=ex_dependencies)
    draw_message(layout, "keplergl", dependencies=ex_dependencies)
    draw_message(layout, "plotly", dependencies=ex_dependencies)
    draw_message(layout, "requests", dependencies=ex_dependencies)
    draw_message(layout, "bokeh", dependencies=ex_dependencies)
    draw_message(layout, "pythreejs", dependencies=ex_dependencies)
    draw_message(layout, "shapely", dependencies=ex_dependencies)
    draw_message(layout, "pyproj", dependencies=ex_dependencies)
    draw_message(layout, "detectron2", dependencies=ex_dependencies)
    draw_message(layout, "torch", dependencies=ex_dependencies)
    draw_message(layout, "tabulate", dependencies=ex_dependencies)
    draw_message(layout, "psutil", dependencies=ex_dependencies)
    draw_message(layout, "matplotlib", dependencies=ex_dependencies)





def update_addon_ui(layout):
    layout.operator('node.sv_show_latest_commits', text='Show Last Commits').commits_link = COMMITS_LINK
    with addon_preferences(ADDON_NAME) as prefs:

        if not prefs.available_new_version:
            check = layout.operator('node.sverchok_check_for_upgrades_wsha', text='Check for Upgrades')
            check.commits_link = COMMITS_LINK
            check.addon_name = ADDON_NAME
        else:
            update_op = layout.operator('node.sverchok_update_addon', text=f'Upgrade {ADDON_PRETTY_NAME}')
            update_op.addon_name = ADDON_NAME
            update_op.master_branch_name = MASTER_BRANCH_NAME
            update_op.archive_link = ARCHIVE_LINK

def sv_draw_update_menu_in_panel(self, context):
    layout = self.layout
    box = layout.box()
    box.label(text=ADDON_PRETTY_NAME)
    update_addon_ui(box)

class SvMegapolisPreferences(AddonPreferences):
    bl_idname = __package__

    available_new_version: bpy.props.BoolProperty(default=False)
    dload_archive_name: bpy.props.StringProperty(name="archive name", default=MASTER_BRANCH_NAME) # default = "master"
    dload_archive_path: bpy.props.StringProperty(name="archive path", default=ARCHIVE_LINK)

    def draw(self, context):
        layout = self.layout

        def get_icon(package):
            if package is None:
                return 'CANCEL'
            else:
                return 'CHECKMARK'

        box = layout.box()

        box.label(text="Dependencies:")

        draw_message(box, "sverchok", dependencies=ex_dependencies)
        draw_message(box, "geopandas", dependencies=ex_dependencies)
        draw_message(box, "leafmap", dependencies=ex_dependencies)
        draw_message(box, "osmnx", dependencies=ex_dependencies)
        draw_message(box, "pandas", dependencies=ex_dependencies)
        draw_message(box, "laspy", dependencies=ex_dependencies)
        draw_message(box, "rasterio", dependencies=ex_dependencies)
        draw_message(box, "pillow", dependencies=ex_dependencies)
        draw_message(box, "mapillary", dependencies=ex_dependencies)
        draw_message(box, "wget", dependencies=ex_dependencies)
        draw_message(box, "networkx", dependencies=ex_dependencies)
        draw_message(box, "scikitlearn", dependencies=ex_dependencies)
        draw_message(box, "streamlit", dependencies=ex_dependencies)
        draw_message(box, "pyvista", dependencies=ex_dependencies)
        draw_message(box, "seaborn", dependencies=ex_dependencies)
        draw_message(box, "visilibity", dependencies=ex_dependencies)
        box.operator('wm.url_open', text="Read installation instructions for Swig (Visilibity dependency)").url="https://swig.org/download.html"
        draw_message(box, "opencv", dependencies=ex_dependencies)
        draw_message(box, "keplergl", dependencies=ex_dependencies)
        draw_message(box, "plotly", dependencies=ex_dependencies)
        draw_message(box, "requests", dependencies=ex_dependencies)
        draw_message(box, "pythreejs", dependencies=ex_dependencies)
        draw_message(box, "bokeh", dependencies=ex_dependencies)
        draw_message(box, "shapely", dependencies=ex_dependencies)
        draw_message(box, "pyproj", dependencies=ex_dependencies)
        draw_message(box, "detectron2", dependencies=ex_dependencies)
        draw_message(box, "torch", dependencies=ex_dependencies)
        draw_message(box, "tabulate", dependencies=ex_dependencies)
        draw_message(box, "psutil", dependencies=ex_dependencies)
        draw_message(box, "matplotlib", dependencies=ex_dependencies)




        box_extra = layout.box()
        
        box_extra.label(text="Extra Dependencies:")

        box_extra.operator('wm.url_open', text="Read installation instructions for Detectron 2").url="https://detectron2.readthedocs.io/en/latest/tutorials/install.html"
       
        box_extra.operator('wm.url_open', text="Read installation instructions in Pytorch website to install pytorch torchvision torchaudio cudatoolkit").url="https://pytorch.org/"
        
        box_extra.operator('wm.url_open', text="Read installation instructions for Rustup (Whitebox Tool dependency)").url="https://rustup.rs/"
 

        row = layout.row()
        row.operator('node.sv_show_latest_commits').commits_link = COMMITS_LINK
        if not self.available_new_version:
            check = row.operator('node.sverchok_check_for_upgrades_wsha', text='Check for Upgrades')
            check.commits_link = COMMITS_LINK
            check.addon_name = ADDON_NAME
        else:
            update_op = row.operator('node.sverchok_update_addon', text=f'Upgrade {ADDON_PRETTY_NAME}')
            update_op.addon_name = ADDON_NAME
            update_op.master_branch_name = MASTER_BRANCH_NAME
            update_op.archive_link = ARCHIVE_LINK

def register():
    bpy.utils.register_class(SvMegapolisPreferences)
    bpy.types.SV_PT_SverchokUtilsPanel.append(sv_draw_update_menu_in_panel)

def unregister():
    bpy.utils.unregister_class(SvMegapolisPreferences)
    bpy.types.SV_PT_SverchokUtilsPanel.remove(sv_draw_update_menu_in_panel)

if __name__ == '__main__':
    register()
