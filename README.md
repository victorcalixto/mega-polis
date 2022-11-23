```bash
                       .|
                       | |
                       |'|            ._____
               ___    |  |            |.   |' .---"|
       _    .-'   '-. |  |     .--'|  ||   | _|    |
    .-'|  _.|  |    ||   '-__  |   |  |    ||      |
    |' | |.    |    ||       | |   |  |    ||      |
____|  '-'     '    ""       '-'   '-.'    '`      |_________________________
jgs~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

███    ███ ███████  ██████   █████        ██████   ██████  ██      ██ ███████ 
████  ████ ██      ██       ██   ██       ██   ██ ██    ██ ██      ██ ██      
██ ████ ██ █████   ██   ███ ███████ █████ ██████  ██    ██ ██      ██ ███████ 
██  ██  ██ ██      ██    ██ ██   ██       ██      ██    ██ ██      ██      ██ 
██      ██ ███████  ██████  ██   ██       ██       ██████  ███████ ██ ███████ 
                                                                               
```

A DATA-DRIVEN URBAN DESIGN TOOLKIT FOR SVERCHOK 
============================================

MEGA-POLIS is a Data-Driven Urban Design Toolkit. This is an addon for [Blender][1] that extends [Sverchok][2]
addon. 

This add-on is part of an ongoing research, and it still very experimental and under HEAVILY development.  

Meanwhile, the documentation is prepared, you can check this demonstration:

[![Watch the video](https://img.youtube.com/vi/lTRNIa2PwhQ/maxresdefault.jpg)](https://youtu.be/lTRNIa2PwhQ)

Features
--------

At the moment, this add-on includes the following nodes for Sverchok:

Gathering
---------

- Read GIS (shapefile, geopackage, geojson)
- Read CSV Files
- Read DEM (GeoTIFF)
- Read LAS (.las)
- OSM Downloader 
- Load Street Network
- Download Street Imagery
- Download Data URL
- Request Data API
- Get Pandas Feature
- Pandas Dataframe
- Pandas Series
- Get Sample Dataframe
- Split String

Analysis
--------

- DEM Terrain Attributes
- Network Analyses
- Shortest Path
- Whitebox GIS Tool (Whitebox Tools Connection)
- Isovists
- Dataframe Utils
- Object Detection (YoloV5)
- Detectron (Instance and Panoptic Segmentation based on Detectron2)
- Correlation
- Correlation With
- Get Feature At
- Get Feature Index
- Linear Model Selection
- Model Fit
- Model Predict

Generation
----------

- Faces from Vertices
- CSV to Dataframe
- Lat-Lon to Points 
- Pandas Filter
- Pandas Map Feature
- Sequential Colormap
- Transpose Dataframe
- Get File Path
- File to Geo Dataframe
- File to GeoJSON

Visualisation
-------------

- Seaborn Plot 
- WebVR Connector (A-Frame)
- Dashboard Creation
- Dashboard Bokeh Figure
- Dashboard Bokeh Plot Chart
- Dashboard Bokeh Plot Line
- Dashboard Dataframe
- Dashboard Load Map
- Dashboard Map
- Dashboard Markdown
- Dashboard Mesh
- Dashboard Plotly Figure
- Dashboard Plotly Scatter
- Dashboard Server
- Dataframe Visualisation
- Python Server

Documentation still under development. 

Installation
------------

* Download and Install [Sverchok][2]
* Download [MEGA-POLIS zip archive][4] from GitHub
* In Blender, go to User Preferences > Add-ons > install from file > choose
  zip-archive > activate flag beside MEGA-POLIS.
* Check the add-on options to install all dependencies.
* Save preferences, if you want to enable the add-on permanently.

LICENSE: GPL-3.

[1]: http://blender.org
[2]: https://github.com/nortikin/sverchok
[4]: https://github.com/victorcalixto/mega-polis
[6]: https://github.com/nortikin/sverchok/wiki/Dependencies


