
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
    sverchok_d.message =  "Sverchok addon is available"
except ImportError:
    message =  "Sverchok addon is not available. Megapolis will not work."
    print(message)
    sverchok = None

#geopandas
geopandas_d = ex_dependencies["geopandas"] = SvDependency("geopandas", "https://geopandas.org/en/stable/")
geopandas_d.pip_installable = True


try:
    import geopandas
    geopandas_d.message = "geopandas package is available"
    geopandas_d.module = geopandas
except ImportError:
    geopandas_d.message = "geopandas package is not available, the addon will not work"
    info(geopandas_d.message)
    geopandas = None

#leafmap
leafmap_d = ex_dependencies["leafmap"] = SvDependency("leafmap", "https://leafmap.org/")
leafmap_d.pip_installable = True

try:
    import leafmap
    leafmap_d.message = "leafmap package is available"
    leafmap_d.module = leafmap
except ImportError:
    leafmap_d.message = "leafmap package is not available, the addon will not work"
    info(leafmap_d.message)
    leafmap = None

#osmnx
osmnx_d = ex_dependencies["osmnx"] = SvDependency("osmnx", "https://github.com/gboeing/osmnx")
osmnx_d.pip_installable = True

try:
    import osmnx
    osmnx_d.message = "osmnx package is available"
    osmnx_d.module = osmnx
except ImportError:
    osmnx_d.message = "osmnx package is not available, the addon will not work"
    info(osmnx_d.message)
    osmnx = None

#pandas
pandas_d = ex_dependencies["pandas"] = SvDependency("pandas", "https://pandas.pydata.org/")
pandas_d.pip_installable = True

try:
    import pandas
    pandas_d.message = "pandas package is available"
    pandas_d.module = pandas
except ImportError:
    pandas_d.message = "pandas package is not available, the addon will not work"
    info(pandas_d.message)
    pandas = None

#laspy
laspy_d = ex_dependencies["laspy"] = SvDependency("laspy", "https://laspy.readthedocs.io/en/latest/installation.html")
laspy_d.pip_installable = True

try:
    import laspy
    laspy_d.message = "laspy package is available"
    laspy_d.module = laspy
except ImportError:
    laspy_d.message = "laspy package is not available, the addon will not work"
    info(laspy_d.message)
    laspy = None

#rasterio
rasterio_d = ex_dependencies["rasterio"] = SvDependency("rasterio", "https://rasterio.readthedocs.io/en/latest/installation.html")
rasterio_d.pip_installable = True

try:
    import rasterio
    rasterio_d.message = "rasterio package is available"
    rasterio_d.module = rasterio
except ImportError:
    rasterio_d.message = "rasterio package is not available, the addon will not work"
    info(rasterio_d.message)
    rasterio = None

#pillow
pillow_d = ex_dependencies["pillow"] = SvDependency("pillow", "https://pillow.readthedocs.io/en/stable/")
pillow_d.pip_installable = True

try:
    import PIL
    pillow_d.message = "pilllow package is available"
    pillow_d.module = PIL
except ImportError:
    pillow_d.message = "pillow package is not available, the addon will not work"
    info(pillow_d.message)
    pillow = None

#mapillary
mapillary_d = ex_dependencies["mapillary"] = SvDependency("mapillary", "https://pillow.readthedocs.io/en/stable/")
mapillary_d.pip_installable = True

try:
    import mapillary
    mapillary_d.message = "mapllary package is available"
    mapillary_d.module = mapillary
except ImportError:
    mapillary_d.message = "mapillary package is not available, the addon will not work"
    info(mapillary_d.message)
    mapillary = None

#wget
wget_d = ex_dependencies["wget"] = SvDependency("wget", "https://pillow.readthedocs.io/en/stable/")
wget_d.pip_installable = True

try:
    import wget
    wget_d.message = "wget package is available"
    wget_d.module = wget
except ImportError:
    wget_d.message = "wget package is not available, the addon will not work"
    info(wget_d.message)
    wget = None

#networkx
networkx_d = ex_dependencies["networkx"] = SvDependency("networkx", "https://pillow.readthedocs.io/en/stable/")
networkx_d.pip_installable = True

try:
    import networkx
    networkx_d.message = "networkx package is available"
    networkx_d.module = networkx
except ImportError:
    networkx_d.message = "networkx package is not available, the addon will not work"
    info(networkx_d.message)
    networkx = None

#scikit-learn
scikitlearn_d = ex_dependencies["scikitlearn"] = SvDependency("scikitlearn", "https://pillow.readthedocs.io/en/stable/")
scikitlearn_d.pip_installable = True

try:
    import sklearn
    scikitlearn_d.message = "scikit-learn package is available"
    scikitlearn_d.module = sklearn
except ImportError:
    scikitlearn_d.message = "scikit-learn package is not available, the addon will not work"
    info(scikitlearn_d.message)
    scikitlearn = None

#streamlit
streamlit_d = ex_dependencies["streamlit"] = SvDependency("streamlit", "https://pillow.readthedocs.io/en/stable/")
streamlit_d.pip_installable = True

try:
    import streamlit
    streamlit_d.message = "streamlit package is available"
    streamlit_d.module = streamlit
except ImportError:
    streamlit_d.message = "streamlit package is not available, the addon will not work"
    info(streamlit_d.message)
    streamlit = None

#pyvista
pyvista_d = ex_dependencies["pyvista"] = SvDependency("pyvista", "https://pillow.readthedocs.io/en/stable/")
pyvista_d.pip_installable = True

try:
    import pyvista
    pyvista_d.message = "pyvista package is available"
    pyvista_d.module = pyvista
except ImportError:
    pyvista_d.message = "pyvista package is not available, the addon will not work"
    info(pyvista_d.message)
    pyvista = None

#seaborn
seaborn_d = ex_dependencies["seaborn"] = SvDependency("seaborn", "https://pillow.readthedocs.io/en/stable/")
seaborn_d.pip_installable = True

try:
    import seaborn
    seaborn_d.message = "seaborn package is available"
    seaborn_d.module = seaborn
except ImportError:
    seaborn_d.message = "seaborn package is not available, the addon will not work"
    info(seaborn_d.message)
    seaborn = None

#visilibity
visilibity_d = ex_dependencies["visilibity"] = SvDependency("visilibity", "https://pillow.readthedocs.io/en/stable/")
visilibity_d.pip_installable = True

try:
    import visilibity
    visilibity_d.message = "visilibity package is available"
    visilibity_d.module = visilibity
except ImportError:
    visilibity_d.message = "visilibity package is not available, the addon will not work"
    info(visilibity_d.message)
    visilibity = None

#opencv
opencv_d = ex_dependencies["opencv"] = SvDependency("opencv", "https://pillow.readthedocs.io/en/stable/")
opencv_d.pip_installable = True

try:
    import cv2
    opencv_d.message = "opencv package is available"
    opencv_d.module = cv2
except ImportError:
    opencv_d.message = "opencv package is not available, the addon will not work"
    info(opencv_d.message)
    opencv = None

#keplergl
keplergl_d = ex_dependencies["keplergl"] = SvDependency("opencv", "https://pillow.readthedocs.io/en/stable/")
keplergl_d.pip_installable = True

try:
    import keplergl
    keplergl_d.message = "keplergl package is available"
    keplergl_d.module = keplergl
except ImportError:
    keplergl_d.message = "keplergl package is not available, the addon will not work"
    info(keplergl_d.message)
    keplergl = None

#plotly
plotly_d = ex_dependencies["plotly"] = SvDependency("plotly", "https://pillow.readthedocs.io/en/stable/")
plotly_d.pip_installable = True

try:
    import plotly
    plotly_d.message = "ploltly package is available"
    plotly_d.module = plotly
except ImportError:
    plotly_d.message = "keplergl package is not available, the addon will not work"
    info(plotly_d.message)
    plotly = None


















