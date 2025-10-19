<p align="center" width="100%">
    <img width="33%" src="https://i.imgur.com/DmcjzUc.png">
</p>
<h1 align="center"><b>MEGA-POLIS</b></h1>
<h3 align="center"> A Free and Open Source Data-Driven Urban Design Toolkit for Sverchok </h1>


MEGA-POLIS is a Data-Driven Urban Design Toolkit. This is an addon for [Blender][1] that extends [Sverchok][2]
addon. While the documentation is not ready, you can check the thesis chapter that describes the  tool development [here](https://www.victorcalixto.xyz/phd_thesis/ct-development.html). Also, you can check this demonstration:

[![Watch the video](https://img.youtube.com/vi/lTRNIa2PwhQ/maxresdefault.jpg)](https://youtu.be/lTRNIa2PwhQ)

![](https://community.osarch.org/uploads/editor/z9/z4mow9t071rz.gif)

![](https://community.osarch.org/uploads/editor/ix/l882bk7h2h94.gif)


Features
--------

At the moment, this add-on includes the following nodes for Sverchok:

Gathering
---------

- Read GIS (shapefile, geopackage, geojson)
  
![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/02_read_gis.png)
 
- Read CSV Files
  
 ![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/07_read_csv.png)

- Read DEM (GeoTIFF)
  
 ![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/04_read_dem.png)
  
- Read LAS (.las)

 ![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/05_read_las.png)

  
- OSM Downloader

- Load Street Network

 ![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/03_load_street_network.png)
  
- Download Street Imagery
  
 ![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/01_tool_mapillary.gif)

- Download Data URL
  
![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/12_download_data_url.gif)

- Request Data API
  
 ![]( https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/13_request_data_api.gif)

- Get Pandas Feature
- Pandas Dataframe

![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/10_pandas_dataframe.png)
  
- Pandas Series

![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/09_pandas_series.png)

- Get Sample Dataframe
- Split String
  
![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/11_split_string.png)

Analysis
--------

- DEM Terrain Attributes
  
![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/14_dem_terrain_attributes.png)

- Network Analyses

![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/17_network_analyses.gif)

- Shortest Path

![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/18_shortest_path.gif)

- Whitebox GIS Tool (Whitebox Tools Connection)

![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/15_whitebox_gis.gif)

- Isovists

![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/16_isovists.png)

- Dataframe Utils

![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/19_dataframe_utils.gif)

- Object Detection (YoloV5)

![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/21-object-detection.gif)

- Detectron (Instance and Panoptic Segmentation based on Detectron2)

![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/22_image_segmentation.gif)

- Correlation
  
![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/20_correlation.png)

- Correlation With
- Get Feature At
- Get Feature Index
- Linear Model Selection
- Model Fit
- Model Predict

Generation
----------

- Faces from Vertices
  
![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/23-faces-from-vertices.gif)
  
- CSV to Dataframe
- Lat-Lon to Points 
- Pandas Filter
  
![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/25-pandas-filter.png)

- Pandas Map Feature
- Sequential Colormap
- Transpose Dataframe
- Get File Path
- File to Geo Dataframe
- File to GeoJSON

Visualisation
-------------

- Seaborn Plot
  
![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/32-seaborn-plot.gif)
  
- WebVR Connector (A-Frame)

![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/31-webvr-connector.gif)
  
- Dashboard Creation
- Dashboard Bokeh Figure
- Dashboard Bokeh Plot Chart
- Dashboard Bokeh Plot Line
- Dashboard Dataframe
  
![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/33-dashboard-dataframe.gif)

- Dashboard Load Map
- Dashboard Map

![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/30-dashboard-map.gif)

- Dashboard Markdown

![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/34-dashboard-markdown.gif)

- Dashboard Mesh
  
![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/29-mesh-dashboard.gif)

- Dashboard Plotly Figure
- Dashboard Plotly Scatter
- Dashboard Server
- Dataframe Visualisation
- Python Server
  
![](https://www.victorcalixto.xyz/phd_thesis/images/tool-dev/35-visualisation-supporting-tools.png)

Documentation still under development. 

Installation
------------

* Download and Install [Sverchok][2]
* Download [MEGA-POLIS zip archive][4] from GitHub
* In Blender, go to User Preferences > Add-ons > install from file > choose
  zip-archive > activate flag beside MEGA-POLIS.
* Check the add-on options to install all dependencies*.
* Save preferences, if you want to enable the add-on permanently.

##### About Dependencies

The **Mapillary** depency requires that you install an older version of numpy compared to Sverchok. You can install the older version, then update numpy after install Mapillary

```bash
pip install numpy --upgrade
```
The dependency **Visilibity** requires [Swig](https://swig.org/download.html) 

**Debian**
```bash
sudo apt install swig
```
**Arch Linux**
```bash
sudo pacman -S swig
```
**Windows**

You can get the binary from the [website](https://swig.org/download.html) or [here](http://prdownloads.sourceforge.net/swig/swigwin-4.1.1.zip)

The **RichDEM** dependecy requires GDAL, MPI, and Boost.

**Debian**

```bash
sudo apt install openmpi-bin libgdal-dev libopenmpi-dev libboost-iostreams-dev
```

**Arch Linux**

```bash
sudo pacman -S boost gdal openmpi
```

For Windows, check the binaries and compilation process at [Boost](https://www.boost.org/users/download/), [GDAL](https://gdal.org/download.html), [Open-MPI](https://www.open-mpi.org/software/ompi/v1.6/ms-windows.php) 


The **Detectron2** dependecy has no official support for Windows. However, there are some attemps to compile it using Visual C++. You can check the discussion [here](https://github.com/facebookresearch/detectron2/issues/4015). 

To make sure that all dependencies will be recognised by Blender-Sverchok you can run Blender with the flag 

```bash
blender --python-use-system-env
```

LICENSE: GPL-3.

[1]: http://blender.org
[2]: https://github.com/nortikin/sverchok
[4]: https://github.com/victorcalixto/mega-polis
[6]: https://github.com/nortikin/sverchok/wiki/Dependencies


