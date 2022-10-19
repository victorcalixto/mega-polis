import bpy
from sverchok.ui.nodeview_space_menu import make_extra_category_menus, layout_draw_categories
from megapolis.nodes_index import nodes_index
from megapolis.dependencies import geopandas as gpd
from megapolis.dependencies import leafmap, osmnx, pandas, laspy, rasterio, PIL, mapillary, wget,networkx, sklearn, streamlit,pyvista,seaborn,visilibity,cv2,plotly,keplergl,requests,richdem

def plain_node_list():
    node_categories = {}
    index = nodes_index()
    for category, items in index:
        nodes = []
        for _, node_name in items:
            nodes.append([node_name])
        node_categories[category] = nodes
    return node_categories

node_cats = plain_node_list()

class NODEVIEW_MT_MEGAPOLIS(bpy.types.Menu):
    bl_label = "Mega-Polis"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        if gpd is None:
            layout.operator('node.sv_ex_pip_install', text="Install geopandas Library with PIP").package = "geopandas"
        if leafmap is None:
            layout.operator('node.sv_ex_pip_install', text="Install leafmap Library with PIP").package = "leafmap"
        if osmnx is None:
            layout.operator('node.sv_ex_pip_install', text="Install osmnx Library with PIP").package = "leafmap"
        if pandas is None:
            layout.operator('node.sv_ex_pip_install', text="Install pandas Library with PIP").package = "leafmap"
        if laspy is None:
            layout.operator('node.sv_ex_pip_install', text="Install laspy Library with PIP").package = "leafmap"

        if rasterio is None:
            layout.operator('node.sv_ex_pip_install', text="Install rasterio Library with PIP").package = "rasterio"

        if PIL is None:
            layout.operator('node.sv_ex_pip_install', text="Install pillow Library with PIP").package = "pillow"

        if mapillary is None:
            layout.operator('node.sv_ex_pip_install', text="Install mapillary Library with PIP").package = "mapillary"

        if wget is None:
            layout.operator('node.sv_ex_pip_install', text="Install wget Library with PIP").package = "mapillary"

        if networkx is None:
            layout.operator('node.sv_ex_pip_install', text="Install networkx Library with PIP").package = "networkx"

        if sklearn is None:
            layout.operator('node.sv_ex_pip_install', text="Install scikit-learn Library with PIP").package = "scikit-learn"

        if streamlit is None:
            layout.operator('node.sv_ex_pip_install', text="Install streamlit Library with PIP").package = "streamlit"

        if pyvista is None:
            layout.operator('node.sv_ex_pip_install', text="Install pyvista Library with PIP").package = "pyvista"

        if seaborn is None:
            layout.operator('node.sv_ex_pip_install', text="Install seaborn Library with PIP").package = "seaborn"

        if visilibity is None:
            layout.operator('node.sv_ex_pip_install', text="Install visilibity Library with PIP").package = "visilibity"
        if cv2 is None:
            layout.operator('node.sv_ex_pip_install', text="Install opencv-python Library with PIP").package = "opencv-python"
        if keplergl is None:
            layout.operator('node.sv_ex_pip_install', text="Install keplergl Library with PIP").package = "keplergl"
        if plotly is None:
            layout.operator('node.sv_ex_pip_install', text="Install plotly Library with PIP").package = "plotly"
        if requests is None:
            layout.operator('node.sv_ex_pip_install', text="Install requests Library with PIP").package = "requests"
        if richdem is None:
            layout.operator('node.sv_ex_pip_install', text="Install richdem Library with PIP").package = "richdem"
        


        else:
            #layout_draw_categories(self.layout, self.bl_label, node_cats['Utils'])
            layout.menu("NODEVIEW_MT_MEGAPOLISGatheringMenu")
            layout.menu("NODEVIEW_MT_MEGAPOLISAnalysisMenu")
            layout.menu("NODEVIEW_MT_MEGAPOLISGenerationMenu")
            layout.menu("NODEVIEW_MT_MEGAPOLISVisualisationMenu")

# does not get registered
class NodeViewMenuTemplate(bpy.types.Menu):
    bl_label = ""
    def draw(self, context):
        layout_draw_categories(self.layout, self.bl_label, node_cats[self.bl_label])

def make_class(name, bl_label):
    name = 'NODEVIEW_MT_MEGAPOLIS' + name + 'Menu'
    clazz = type(name, (NodeViewMenuTemplate,), {'bl_label': bl_label})
    return clazz

menu_classes = [
    make_class('Gathering', 'Gathering'),
    make_class('Analysis', 'Analysis'),
    make_class('Generation', 'Generation'),
    make_class('Visualisation', 'Visualisation'),
    ]

def register():
    for class_name in menu_classes:
        bpy.utils.register_class(class_name)
    bpy.utils.register_class(NODEVIEW_MT_MEGAPOLIS)

def unregister():
    for class_name in menu_classes:
        bpy.utils.unregister_class(class_name)
    bpy.utils.unregister_class(NODEVIEW_MT_MEGAPOLIS)
