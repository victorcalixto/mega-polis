
from sverchok.dependencies import SvDependency

ex_dependencies = dict()

try:
    import sverchok
    from sverchok.utils.logging import info, error, debug

    from sverchok.dependencies import (
            SvDependency,
            ensurepip,
            pip, scipy, geomdl, skimage,
            mcubes, circlify,
            FreeCAD
        )

    sverchok_d = ex_dependencies["sverchok"] = SvDependency(None, "https://github.com/nortikin/sverchok")
    sverchok_d.module = sverchok
except ImportError:
    message =  "Sverchok addon is not available. Megapolis will not work."
    print(message)
    sverchok = None

#geopandas
geopandas_d = ex_dependencies["geopandas"] = SvDependency("geopandas", "https://geopandas.org/en/stable/")
geopandas_d.pip_installable = True


try:
    import geopandas
    geopandas_d.module = geopandas
except ImportError:
    geopandas = None

#leafmap
leafmap_d = ex_dependencies["leafmap"] = SvDependency("leafmap", "https://leafmap.org/")
leafmap_d.pip_installable = True

try:
    import leafmap
    leafmap_d.module = leafmap
except ImportError:
    leafmap = None

#osmnx
osmnx_d = ex_dependencies["osmnx"] = SvDependency("osmnx", "https://github.com/gboeing/osmnx")
osmnx_d.pip_installable = True

try:
    import osmnx
    osmnx_d.module = osmnx
except ImportError:
    osmnx = None

#pandas
pandas_d = ex_dependencies["pandas"] = SvDependency("pandas", "https://pandas.pydata.org/")
pandas_d.pip_installable = True

try:
    import pandas
    pandas_d.module = pandas
except ImportError:
    pandas = None

#laspy
laspy_d = ex_dependencies["laspy"] = SvDependency("laspy", "https://laspy.readthedocs.io/en/latest/installation.html")
laspy_d.pip_installable = True

try:
    import laspy
    laspy_d.module = laspy
except ImportError:
    laspy = None

#rasterio
rasterio_d = ex_dependencies["rasterio"] = SvDependency("rasterio", "https://rasterio.readthedocs.io/en/latest/installation.html")
rasterio_d.pip_installable = True

try:
    import rasterio
    rasterio_d.module = rasterio
except ImportError:
    rasterio = None

#pillow
pillow_d = ex_dependencies["pillow"] = SvDependency("pillow", "https://pillow.readthedocs.io/en/stable/")
pillow_d.pip_installable = True

try:
    import PIL
    pillow_d.module = PIL
except ImportError:
    pillow = None

#mapillary
mapillary_d = ex_dependencies["mapillary"] = SvDependency("mapillary", "https://github.com/mapillary/mapillary-python-sdk")
mapillary_d.pip_installable = True

try:
    import mapillary
    mapillary_d.module = mapillary
except ImportError:
    mapillary = None

#wget
wget_d = ex_dependencies["wget"] = SvDependency("wget", "https://pypi.org/project/wget/")
wget_d.pip_installable = True

try:
    import wget
    wget_d.module = wget
except ImportError:
    wget = None

#networkx
networkx_d = ex_dependencies["networkx"] = SvDependency("networkx", "https://networkx.org/")
networkx_d.pip_installable = True

try:
    import networkx
    networkx_d.module = networkx
except ImportError:
    networkx = None

#scikit-learn
scikitlearn_d = ex_dependencies["scikit-learn"] = SvDependency("scikit-learn", "https://scikit-learn.org/")
scikitlearn_d.pip_installable = True

try:
    import sklearn
    scikitlearn_d.module = sklearn
except ImportError:
    sklearn = None

#streamlit
streamlit_d = ex_dependencies["streamlit"] = SvDependency("streamlit", "https://streamlit.io/")
streamlit_d.pip_installable = True

try:
    import streamlit
    streamlit_d.module = streamlit
except ImportError:
    streamlit = None

#pyvista
pyvista_d = ex_dependencies["pyvista"] = SvDependency("pyvista", "https://docs.pyvista.org/")
pyvista_d.pip_installable = True

try:
    import pyvista
    pyvista_d.module = pyvista
except ImportError:
    pyvista = None

#seaborn
seaborn_d = ex_dependencies["seaborn"] = SvDependency("seaborn", "https://seaborn.pydata.org/")
seaborn_d.pip_installable = True

try:
    import seaborn
    seaborn_d.module = seaborn
except ImportError:
    seaborn = None

#visilibity
visilibity_d = ex_dependencies["visilibity"] = SvDependency("visilibity", "https://karlobermeyer.github.io/VisiLibity1/")
visilibity_d.pip_installable = True

try:
    import visilibity
    visilibity_d.module = visilibity
except ImportError:
    visilibity = None

#opencv
opencvpython_d = ex_dependencies["opencv-python"] = SvDependency("opencv-python", "https://github.com/opencv/opencv-python")
opencvpython_d.pip_installable = True

try:
    import cv2
    opencvpython_d.module = cv2
except ImportError:
    cv2 = None

#keplergl
keplergl_d = ex_dependencies["keplergl"] = SvDependency("keplergl", "https://github.com/keplergl/kepler.gl/tree/master/bindings/kepler.gl-jupyter")
keplergl_d.pip_installable = True

try:
    import keplergl
    keplergl_d.module = keplergl
except ImportError:
    keplergl = None

#plotly
plotly_d = ex_dependencies["plotly"] = SvDependency("plotly", "https://plotly.com/python/")
plotly_d.pip_installable = True

try:
    import plotly
    plotly_d.module = plotly
except ImportError:
    plotly = None

#requests
requests_d = ex_dependencies["requests"] = SvDependency("requests", "https://pypi.org/project/requests")
requests_d.pip_installable = True

try:
    import requests
    requests_d.module = requests
except ImportError:
    requests = None

#richdem
richdem_d = ex_dependencies["richdem"] = SvDependency("richdem", "https://richdem.com/")
richdem_d.pip_installable = True

try:
    import richdem
    richdem_d.module = richdem
except ImportError:
    richdem = None

#pythreejs
pythreejs_d = ex_dependencies["pythreejs"] = SvDependency("pythreejs", "https://github.com/jupyter-widgets/pythreejs")
pythreejs_d.pip_installable = True

try:
    import pythreejs
    pythreejs_d.module = pythreejs
except ImportError:
    pythreejs = None

#bokeh
bokeh_d = ex_dependencies["bokeh"] = SvDependency("bokeh", "https://bokeh.org/")
bokeh_d.pip_installable = True

try:
    import bokeh
    bokeh_d.module = bokeh
except ImportError:
    bokeh = None

#shapely
shapely_d = ex_dependencies["shapely"] = SvDependency("shapely", "https://pypi.org/project/shapely/")
shapely_d.pip_installable = True

try:
    import shapely
    shapely_d.module = shapely
except ImportError:
    shapely = None

#requests
requests_d = ex_dependencies["requests"] = SvDependency("requests", "https://requests.readthedocs.io/en/latest/")
requests_d.pip_installable = True

try:
    import requests
    requests_d.module = requests
except ImportError:
    requests = None

#pyproj
pyproj_d = ex_dependencies["pyproj"] = SvDependency("pyproj", "https://pypi.org/project/pyproj/")
pyproj_d.pip_installable = True

try:
    import pyproj
    pyproj_d.module = pyproj
except ImportError:
    pyproj = None

#detectron2
detectron2_d = ex_dependencies["detectron2"] = SvDependency("detectron2", "https://detectron2.readthedocs.io/en/latest/tutorials/install.html")
detectron2_d.pip_installable = False

try:
    import detectron2
    detectron2_d.module = detectron2
except ImportError:
    detectron2 = None

#torch
torch_d = ex_dependencies["torch"] = SvDependency("torch", "https://pytorch.org/")
torch_d.pip_installable = False

try:
    import torch
    torch_d.module = torch
except ImportError:
    torch = None

#tabulate
tabulate_d = ex_dependencies["tabulate"] = SvDependency("tabulate", "https://github.com/astanin/python-tabulate")
tabulate_d.pip_installable = True

try:
    import tabulate
    tabulate_d.module = tabulate
except ImportError:
    tabulate = None

#psutil
psutil_d = ex_dependencies["psutil"] = SvDependency("psutil", "https://github.com/giampaolo/psutil")
psutil_d.pip_installable = True

try:
    import psutil
    psutil_d.module = psutil
except ImportError:
    psutil = None

#matplotlib
matplotlib_d = ex_dependencies["matplotlib"] = SvDependency("matplotlib", "https://matplotlib.org/")
matplotlib_d.pip_installable = True

try:
    import matplotlib
    matplotlib_d.module = matplotlib
except ImportError:
    matplotlib = None

#richdem
richdem_d = ex_dependencies["richdem"] = SvDependency("richdem", "https://richdem.readthedocs.io/en/latest/")
richdem_d.pip_installable = True

try:
    import richdem
    richdem_d.module = richdem
except ImportError:
    richdem = None











