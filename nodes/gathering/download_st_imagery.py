import bpy
from bpy.props import IntProperty, BoolProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

#Megapolis Dependencies

from megapolis.dependencies import geopandas as gpd
from megapolis.dependencies import pandas as pd
from megapolis.dependencies import osmnx as ox
from megapolis.dependencies import mapillary as mly

from shapely.geometry import shape, Polygon, Point, LineString, mapping
from pyproj import Proj, Transformer, CRS
import os
import threading
import json
import requests
import urllib.request


class SvMegapolisDownloadStImagery(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Download Street Imagery
    Tooltip: Download Geo-Referenced Mapillary Street Imagery
    """
    bl_idname = 'SvMegapolisDownloadStImagery'
    bl_label = 'Download Street Imagery'
    bl_icon = 'MESH_DATA'
    

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status
        
        updateNode(self,context)

    #Blender Properties Buttons

    projection: IntProperty(
        name="projection",
        description="CSR Projection Number",
        default=4236,
        update=update_sockets)
    
    download: BoolProperty(
        name='download', 
        default=False,
        description='Download the Street Imagery', 
        update=update_sockets)

    def sv_init(self, context):
        # inputs
        self.inputs.new('SvStringsSocket', "Folder")
        self.inputs.new('SvStringsSocket', "Radius")
        self.inputs.new('SvStringsSocket', "Longitude")
        self.inputs.new('SvStringsSocket', "Latitude")
        self.inputs.new('SvStringsSocket', "Max_Num_Photos")

        # outputs
        
        self.outputs.new('SvStringsSocket', "Images_Index")
        self.outputs.new('SvVerticesSocket', "Coordinates")
        self.outputs.new('SvStringsSocket', "Output_Message")
                    
    def draw_buttons(self,context, layout):
        layout.prop(self, 'download')
        layout.prop(self, 'projection')

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
         
        if self.download == False or not self.inputs["Folder"].is_linked:
            return
       
        self.folder = self.inputs["Folder"].sv_get(deepcopy = False)
        self.radius = self.inputs["Radius"].sv_get(deepcopy = False)
        self.longitude = self.inputs["Longitude"].sv_get(deepcopy = False)
        self.latitude = self.inputs["Latitude"].sv_get(deepcopy = False)
        self.max_photos = self.inputs["Max_Num_Photos"].sv_get(deepcopy = False)

        folder_name = str(self.folder[0][0])
        projection = self.projection 
        radius= self.radius[0][0]
        longitude =float(self.longitude[0][0])
        latitude = float(self.latitude[0][0])
        max_photos = self.max_photos[0][0]
        

        location = []
        #location_detect = []
        key = 'MLY|5526116027433453|857ad8b276f638faf29e70b5b46921fd'

        mly.interface.set_access_token(key)

        #images_dict = mly.interface.images_in_geojson(gdf_json, mode='r')

        images_dict = mly.interface.get_image_close_to(longitude=longitude, latitude=latitude, radius=radius)

        #df = gpd.read_file(images_dict)

        data = images_dict.to_dict()

        images_id = mly.utils.extract.extract_properties(data,properties=['id'])

        message = []

        #print(images_id)

        def downloadImages(images,folder_name,location,message):
            #images = images['id']
            try:
                os.mkdir(folder_name)
                #folder_detect = f"{folder_name}_detect"
                #os.mkdir(folder_detect)
            except:
                pass
            for i in images:
                header = {'Authorization' : 'OAuth {}'.format(key)}
                #url = 'https://graph.mapillary.com/{}?fields=thumb_2048_url'.format(i)
                #url = f"https://www.mapillary.com/embed?image_key={i}"
                url_json=f"https://graph.mapillary.com/{i}?access_token={key}&fields=thumb_original_url,computed_geometry,captured_at,computed_compass_angle"    
                #url_detections=f"https://graph.mapillary.com/{i}/detections?access_token={key}&fields=created_at,geometry,image,value"
                #print(data["thumb_original_url"])
                
                response = requests.get(url_json,headers=header)
                data = response.json()
                image_url = data['thumb_original_url']
                
                if response.status_code == 200:
                    with open(f"{folder_name}/{i}.jpg", 'wb') as f:
                        image_data = requests.get(image_url, stream=True).content
                        f.write(image_data)
                print(f"Downloaded {i}.jpg in {folder_name}")
                location.append(data["computed_geometry"]["coordinates"])
                message.append(f"Downloaded {i}.jpg in {folder_name}")
                
                
                
                """ Detections
                response = requests.get(url_detections,headers=header)
                data_detect = response.json()
                image_url_detect = data['thumb_original_url']
                if response.status_code == 200:
                    with open(f"./{folder_name}_detect/{i}_detect.jpg", 'wb') as f:
                        image_data_detect = requests.get(image_url_detect, stream=True).content
                        f.write(image_data_detect)
                print(f"Downloaded {i}_detect.jpg in {folder_name}_detect")
                location_detect.append(data["computed_geometry"]["coordinates"])
                print(data_detect)
                message.append(f"Downloaded {i}_detect.jpg in {folder_name}_detect")
                """



        images = images_id['id']


        #delete it later
        slice = images[0:int(max_photos)]

        #change name to  images

        if self.download == True:
            t1 = threading.Thread(target=downloadImages, args=(slice,folder_name,location,message))
            t1.start()
            t1.join()
          
        #downloadImages(slice,folder_name,location,location_detect) 


        coords = []



        #in_latlon = CRS.from_proj4("+proj=latlon")
        #out_proj = Proj(self.projection)
        
        transformer = Transformer.from_crs("+proj=latlon",f"epsg:{self.projection}")


        for i in location:
           x = i[0]
           y = i[1]
           x,y = transformer.transform(x,y)
           #x,y = transform(in_latlon,out_proj, x,y)
           z = 0
           coords.append([x,y,z])
          


        coords = [coords]

        coordinates = coords

        images_index = images

        ## Outputs
        
        self.outputs["Images_Index"].sv_set(images)
        self.outputs["Coordinates"].sv_set(coords)
        self.outputs["Output_Message"].sv_set(message)
        
def register():
    if mly is not None:
        bpy.utils.register_class(SvMegapolisDownloadStImagery)

def unregister():
    if mly is not None:
        bpy.utils.unregister_class(SvMegapolisDownloadStImagery)
