
bl_info = {
    "name": "Megapolis",
    "author": "Victor Calixto",
    "version": (0, 0, 0, 0),
    "blender": (3, 3, 0),
    "location": "Node Editor",
    "category": "Node",
    "description": "A Computational Data-Driven Urban Design Tool",
    "warning": "",
    "wiki_url": "https://github.com/victorcalixto/mega-polis",
    "tracker_url": "https://github.com/victorcalixto/mega-polis/issues"
}

import sys
import importlib
from pathlib import Path
import nodeitems_utils

from sverchok.utils import yaml_parser
from sverchok.ui.nodeview_space_menu import add_node_menu
from sverchok.utils.logging import info, debug

# make sverchok the root module name, (if sverchok dir not named exactly "sverchok")
if __name__ != "megapolis":
    sys.modules["megapolis"] = sys.modules[__name__]


import megapolis
from megapolis import icons, settings #menu, settings, sockets, examples
from megapolis.utils import show_welcome

def nodes_index():
    return [
            ("Gathering", [
                ("gathering.read_gis","SvMegapolisReadGis"),
                ("gathering.read_csv","SvMegapolisReadCsv"),
                ("gathering.read_json","SvMegapolisReadJson"),
                ("gathering.read_dem","SvMegapolisReadDem"),
                ("gathering.read_las","SvMegapolisReadLas"),
                ("gathering.download_st_imagery","SvMegapolisDownloadStImagery"),
                ("gathering.load_street_network","SvMegapolisLoadStreetNetwork"),
                ("gathering.osm_downloader","SvMegapolisOSMDownloader"),
                ("gathering.pandas_series","SvMegapolisPandasSeries"),
                ("gathering.pandas_dataframe","SvMegapolisPandasDataframe"),
                ("gathering.split_string","SvMegapolisSplitString"),
                ("gathering.download_data_url","SvMegapolisDownloadDataUrl"),
                ("gathering.request_data_api","SvMegapolisRequestDataApi"),
                ("gathering.get_pandas_feature","SvMegapolisGetPandasFeature"),
                ("gathering.get_sample_dataframe","SvMegapolisGetSampleDataframe")



                ]),
            ("Analysis", [

                ("analysis.whitebox_gis_tools","SvMegapolisWhiteboxGisTools"),
                ("analysis.dem_terrain_attributes","SvMegapolisDemTerrainAttributes"),
                ("analysis.network_analyses","SvMegapolisNetworkAnalyses"),
                ("analysis.isovists","SvMegapolisIsovists"),
                ("analysis.shortest_path","SvMegapolisShortestPath"),
                ("analysis.get_feature_index","SvMegapolisGetFeatureIndex"),
                ("analysis.get_feature_at","SvMegapolisGetFeatureAt"),
                ("analysis.correlation","SvMegapolisCorrelation"),
                ("analysis.correlation_with","SvMegapolisCorrelationWith"),
                ("analysis.linear_model_selection","SvMegapolisLinearModelSelection"),
                ("analysis.model_fit","SvMegapolisModelFit"),
                ("analysis.model_predict","SvMegapolisModelPredict"),
                ("analysis.model_evaluate","SvMegapolisModelEvaluate"),
                ("analysis.dataframe_utils","SvMegapolisDataframeUtils"),
                ("analysis.object_detection","SvMegapolisObjectDetection"),
                ("analysis.image_segmentation","SvMegapolisImageSegmentation")



                ]),


            ("Generation", [

                ("generation.lat_lon_to_points","SvMegapolisLatLonToPoints"),
                ("generation.faces_from_vertices","SvMegapolisFacesFromVertices"),
                ("generation.pandas_filter","SvMegapolisPandasFilter"),
                ("generation.transpose_dataframe","SvMegapolisTransposeDataframe"),
                ("generation.pandas_map_feature","SvMegapolisPandasMapFeature"),
                ("generation.file_to_gdf","SvMegapolisFileToGdf"),
                ("generation.file_to_geojson","SvMegapolisFileToGeoJson"),
                ("generation.csv_to_dataframe","SvMegapolisCsvToDataframe"),
                ("generation.sequential_colormap","SvMegapolisSequentialColormap"),
                ("generation.colormap","SvMegapolisColormap"),
                ("generation.get_file_path","SvMegapolisGetFilePath"),
                ("generation.create_dictionary","SvMegapolisCreateDictionary")


                ]),
            ("Visualisation", [
                
                ("visualisation.dataframe_vis","SvMegapolisDataframeVis"),
                ("visualisation.seaborn_plot","SvMegapolisSeabornPlot"),
                ("visualisation.plot_dem","SvMegapolisPlotDem"),
                ("visualisation.dashboard_mesh","SvMegapolisDashboardMesh"),
                ("visualisation.dashboard_map","SvMegapolisDashboardMap"),
                ("visualisation.dashboard_load_map","SvMegapolisDashboardLoadMap"),
                ("visualisation.dashboard_bokeh_figure","SvMegapolisDashboardBokehFigure"),
                ("visualisation.dashboard_bokeh_plot_line","SvMegapolisDashboardBokehPlotLine"),
                ("visualisation.dashboard_bokeh_plot_chart","SvMegapolisDashboardBokehPlotChart"),
                ("visualisation.dashboard_plotly_figure","SvMegapolisDashboardPlotlyFigure"),
                ("visualisation.dashboard_markdown","SvMegapolisDashboardMarkdown"),
                ("visualisation.dashboard_plotly_scatter","SvMegapolisDashboardPlotlyScatter"),
                ("visualisation.dashboard_dataframe","SvMegapolisDashboardDataframe"),
                ("visualisation.dashboard_creation","SvMegapolisDashboardCreation"),
                ("visualisation.python_server","SvMegapolisPythonServer"),
                ("visualisation.webvr_connector","SvMegapolisWebVRConnector"),
                ("visualisation.dashboard_server","SvMegapolisDashboardServer"),
                ("visualisation.dashboard_geojson_to_map","SvMegapolisDashboardGeojsonToMap"),
                ("visualisation.dashboard_create_plotly","SvMegapolisDashboardCreatePlotly"),


                ]),
                      ]

config_file = Path(__file__).parents[0]/'index.yaml'

add_node_menu.append_from_config(yaml_parser.load(Path(__file__).parents[0]/'index.yaml'))

def make_node_list():
    modules = []
    base_name = "megapolis.nodes"
    index = nodes_index()
    for category, items in index:
        for item in items:
            if not item:
                continue
            module_name, node_name = item
            module = importlib.import_module(f".{module_name}", base_name)
            modules.append(module)
    return modules

imported_modules = [icons] + make_node_list()

reload_event = False

if "bpy" in locals():
    reload_event = True
    info("Reloading MEGAPOLIS...")


import bpy

def register_nodes():
    node_modules = make_node_list()
    for module in node_modules:
        module.register()
    info("Registered %s nodes", len(node_modules))

def unregister_nodes():
    global imported_modules
    for module in reversed(imported_modules):
        module.unregister()


our_menu_classes = []

def reload_modules():
    global imported_modules
    for im in imported_modules:
        debug("Reloading: %s", im)
        importlib.reload(im)

def register():
    global our_menu_classes

    debug("Registering megapolis")

    add_node_menu.register()
    settings.register()
    icons.register()

    register_nodes()
    show_welcome()

    
def unregister():
    global our_menu_classes
    if 'MEGAPOLIS' in nodeitems_utils._node_categories:
        nodeitems_utils.unregister_node_categories("MEGAPOLIS")
    for clazz in our_menu_classes:
        try:
            bpy.utils.unregister_class(clazz)
        except Exception as e:
            print("Can't unregister menu class %s" % clazz)
            print(e)
    unregister_nodes()

    icons.unregister()
    settings.unregister()
