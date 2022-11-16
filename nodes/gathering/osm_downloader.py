import bpy
from bpy.props import BoolProperty, EnumProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import osmnx as ox
import re


Download_method = namedtuple('DownloadMethod', ['Address', 'Place','Point','Bbox'])
DOWNLOADMETHOD = Download_method('Address', 'Place','Point','Bbox')
downloadmethod_items = [(i, i, '') for i in DOWNLOADMETHOD]


Features = namedtuple('Features', ['aerialway', 'aeroway','amenity','barrier','boundary','building', 'craft','emergency','geolofical','healthcare','highway','historic','landuse','leisure','man_made','military','natural','office','place','power','public_transport','railway','route','sport','telecom','tourism','water','waterway','additional_properties','annotations','name','properties','references','restrictions'])

FEATURES = Features('aerialway', 'aeroway','amenity','barrier','boundary','building', 'craft','emergency','geolofical','healthcare','highway','historic','landuse','leisure','man_made','military','natural','office','place','power','public_transport','railway','route','sport','telecom','tourism','water','waterway','additional_properties','annotations','name','properties','references','restrictions')
features_items = [(i, i, '') for i in FEATURES]



class SvMegapolisOSMDownloader(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: OSM Downloader
    Tooltip: Download an Open Streetmap file
    """
    bl_idname = 'SvMegapolisOSMDownloader'
    bl_label = 'OSM Downloader'
    bl_icon = 'MESH_DATA'
    

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status

        if self.download_method in DOWNLOADMETHOD.Address:
            set_hide(self.inputs['Address'], False)
            set_hide(self.inputs['Folder'], False)


            set_hide(self.inputs['Distance'], False)

            set_hide(self.inputs['Place'], True)
            
            set_hide(self.inputs['Coordinate_X'], True)
            set_hide(self.inputs['Coordinate_Y'], True)

            set_hide(self.inputs['North'], True)
            set_hide(self.inputs['South'], True)
            set_hide(self.inputs['East'], True)
            set_hide(self.inputs['West'], True)

        elif self.download_method in DOWNLOADMETHOD.Place:
            set_hide(self.inputs['Address'], True)
            set_hide(self.inputs['Folder'], False)


            set_hide(self.inputs['Distance'], True)

            set_hide(self.inputs['Place'], False)
            
            set_hide(self.inputs['Coordinate_X'], True)
            set_hide(self.inputs['Coordinate_Y'], True)

            set_hide(self.inputs['North'], True)
            set_hide(self.inputs['South'], True)
            set_hide(self.inputs['East'], True)
            set_hide(self.inputs['West'], True)

        elif self.download_method in DOWNLOADMETHOD.Point:
            set_hide(self.inputs['Address'], True)
            set_hide(self.inputs['Folder'], False)


            set_hide(self.inputs['Distance'], False)

            set_hide(self.inputs['Place'], True)
            
            set_hide(self.inputs['Coordinate_X'], False)
            set_hide(self.inputs['Coordinate_Y'], False)

            set_hide(self.inputs['North'], True)
            set_hide(self.inputs['South'], True)
            set_hide(self.inputs['East'], True)
            set_hide(self.inputs['West'], True)


        else:
            set_hide(self.inputs['Address'], True)
            set_hide(self.inputs['Folder'], False)


            set_hide(self.inputs['Distance'], True)

            set_hide(self.inputs['Place'], True)
            
            set_hide(self.inputs['Coordinate_X'], True)
            set_hide(self.inputs['Coordinate_Y'], True)

            set_hide(self.inputs['North'], False)
            set_hide(self.inputs['South'], False)
            set_hide(self.inputs['East'], False)
            set_hide(self.inputs['West'], False)

        updateNode(self,context)

    #Blender Properties Buttons

    download: BoolProperty(
        name="download",
        description="Run the Node to Download",
        default=False,
        update=update_sockets)

    download_method: EnumProperty(
        name='download_method', items=downloadmethod_items,
        default="Address",
        description='Choose an OSM Download Method', 
        update=update_sockets)
    
    features: EnumProperty(
        name='features', items=features_items,
        default="building",
        description='Choose a Feature to Download', 
        update=update_sockets)

    def sv_init(self, context):
        
        # inputs
        self.inputs.new('SvStringsSocket', "Address")
        self.inputs.new('SvStringsSocket', "Place")
       
        
        self.inputs.new('SvStringsSocket', "Coordinate_X")
        self.inputs.new('SvStringsSocket', "Coordinate_Y")
       
        self.inputs.new('SvStringsSocket', "North")
        self.inputs.new('SvStringsSocket', "South")
        self.inputs.new('SvStringsSocket', "East")
        self.inputs.new('SvStringsSocket', "West")
       

        self.inputs['Place'].hide_safe = True 
        
        self.inputs['Coordinate_X'].hide_safe = True 
        self.inputs['Coordinate_Y'].hide_safe = True 
        self.inputs['North'].hide_safe = True 
        self.inputs['South'].hide_safe = True 
        self.inputs['East'].hide_safe = True 
        self.inputs['West'].hide_safe = True 
        
        self.inputs.new('SvStringsSocket', "Distance")
        self.inputs.new('SvStringsSocket', "Folder")
       


        # outputs

        self.outputs.new('SvStringsSocket', "Output_Message")
        
        
    def draw_buttons(self,context, layout):
        layout.prop(self, 'download')
        layout.prop(self, 'download_method', expand=True)
        layout.prop(self, 'features')


    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
         
        if self.download_method in DOWNLOADMETHOD.Address:
            if not self.inputs["Address"].is_linked or not self.inputs["Distance"].is_linked or not self.inputs["Folder"].is_linked :
                return
            self.address = self.inputs["Address"].sv_get(deepcopy = False)
            self.distance = self.inputs["Distance"].sv_get(deepcopy = False)
            self.folder = self.inputs["Folder"].sv_get(deepcopy = False)
            
            address = self.address[0][0]
            distance = self.distance[0][0]
            folder = self.folder[0][0]


        elif self.download_method in DOWNLOADMETHOD.Place:
            if not self.inputs["Place"].is_linked or not self.inputs["Folder"].is_linked:
                return
            self.place = self.inputs["Place"].sv_get(deepcopy = False)
            self.folder = self.inputs["Folder"].sv_get(deepcopy = False)

            folder = self.folder[0][0]
            place = self.place[0][0]




        elif self.download_method in DOWNLOADMETHOD.Point:
            if not self.inputs["Coordinate_X"].is_linked or not self.inputs["Coordinate_Y"].is_linked or not self.inputs["Distance"].is_linked or not self.inputs["Folder"].is_linked :
                return
            self.coordinate_x = self.inputs["Coordinate_X"].sv_get(deepcopy = False)
            self.coordinate_y = self.inputs["Coordinate_Y"].sv_get(deepcopy = False)
            self.distance = self.inputs["Distance"].sv_get(deepcopy = False)
            self.folder = self.inputs["Folder"].sv_get(deepcopy = False)
            

            coordinate_x = self.coordinate_x[0][0]
            coordinate_y = self.coordinate_y[0][0]
            distance = self.distance[0][0]
            folder = self.folder[0][0]


        else:
            if not self.inputs["North"].is_linked or not self.inputs["South"].is_linked or not self.inputs["East"].is_linked or not self.inputs["West"].is_linked  or not self.inputs["Folder"].is_linked  :
                return
            self.north = self.inputs["North"].sv_get(deepcopy = False)
            self.south = self.inputs["South"].sv_get(deepcopy = False)
            self.east = self.inputs["East"].sv_get(deepcopy = False)
            self.west = self.inputs["West"].sv_get(deepcopy = False)

            self.folder = self.inputs["Folder"].sv_get(deepcopy = False)
            
            north = self.north[0][0]
            south= self.south[0][0]
            east = self.east[0][0]
            west = self.west[0][0]
            folder = self.folder[0][0]

        dictionary = {}
        dictionary[self.features] = True

        #if self.buildings == True:
        #dictionary["building"] = True
        #if self.amenity == True:
        #   dictionary["amenity"] = True
        # print(dictionary) 
        
        print(dictionary)

        if self.download == True: 
            if self.download_method in DOWNLOADMETHOD.Address:
                buildings = ox.geometries_from_address(str(address), dictionary, distance)
                #address_ = re.sub('[^A-Za-z0-9]+', ' ',address) 
                #buildings = buildings.loc[:,buildings.columns.str.contains(r'^((?!nodes).)*$')]
                buildings = buildings.loc[:,buildings.columns.str.contains('building|geometry|addr:|amenity|operator|name|historic|brand|cuisine|delivery|drive|internet|opening|outdoor|smoking|takeway|website|layer|source|shop|tourism|wheelchair|office|information|roof|emergency|man|access|parking|fixme|construction|toilets|denomination|religion|height|wikidata|leisure|area|healthcare|levels|diet|email|description|note|old_name|type')]
                buildings.to_file(f"{folder}{address}_{self.features}.geojson", driver="GeoJSON")
                
                #for geomtype in buildings.geom_type.unique():
                #    buildings[buildings.geom_type == geomtype].to_file(f"{folder}{address}_{self.features}_{geomtype}")

            elif self.download_method in DOWNLOADMETHOD.Place:
                buildings = ox.geometries_from_place(str(place), dictionary)
                #place_ = re.sub('[^A-Za-z0-9]+', ' ',place) 
                #buildings.to_file(f"{folder}{place_}_{self.features}.geojson", driver="GeoJSON", index =True)
                buildings = buildings.loc[:,buildings.columns.str.contains('building|geometry|addr:|amenity|operator|name|historic|brand|cuisine|delivery|drive|internet|opening|outdoor|smoking|takeway|website|layer|source|shop|tourism|wheelchair|office|information|roof|emergency|man|access|parking|fixme|construction|toilets|denomination|religion|height|wikidata|leisure|area|healthcare|levels|diet|email|description|note|old_name|type')]
                

                #buildings = buildings.loc[:,buildings.columns.str.contains('building:|addr:|geometry|amenity')]
                #buildings = buildings.loc[:,buildings.columns.str.contains(r'^((?!nodes).)*$')]
                
                buildings.to_file(f"{folder}{place}_{self.features}.geojson", driver="GeoJSON")
                

                #print(buildings)
                #buildings = buildings.loc[:,buildings.columns.str.contains('addr:|geometry')]
                #for geomtype in buildings.geom_type.unique():
                #    buildings[buildings.geom_type == geomtype].to_file(f"{folder}{place}_{self.features}_{geomtype}")


            elif self.download_method in DOWNLOADMETHOD.Point:
                point = (float(coordinate_x),float(coordinate_y))
                point_name = re.sub('[^A-Za-z0-9]+',' ', str(point_name))
                buildings = ox.geometries_from_point(point, dictionary, distance)
                buildings = buildings.loc[:,buildings.columns.str.contains('building|geometry|addr:|amenity|operator|name|historic|brand|cuisine|delivery|drive|internet|opening|outdoor|smoking|takeway|website|layer|source|shop|tourism|wheelchair|office|information|roof|emergency|man|access|parking|fixme|construction|toilets|denomination|religion|height|wikidata|leisure|area|healthcare|levels|diet|email|description|note|old_name|type')]
                
                buildings.to_file(f"{folder}{point_name}_{self.features}.geojson", driver="GeoJSON")
                


                #for geomtype in buildings.geom_type.unique():
                #    buildings[buildings.geom_type == geomtype].to_file(f"{folder}{point_name}_{self.features}_{geomtype}.gpkg", driver="GPKG", layer=geomtype)

            else:
                bbox = f'{north}_{south}_{east}_{west}'
                buildings = ox.geometries_from_bbox(north,south,east,west, dictionary)
                bbox_ = re.sub('[^A-Za-z0-9]+', ' ',bbox) 
                buildings = buildings.loc[:,buildings.columns.str.contains('building|geometry|addr:|amenity|operator|name|historic|brand|cuisine|delivery|drive|internet|opening|outdoor|smoking|takeway|website|layer|source|shop|tourism|wheelchair|office|information|roof|emergency|man|access|parking|fixme|construction|toilets|denomination|religion|height|wikidata|leisure|area|healthcare|levels|diet|email|description|note|old_name|type')]
                
                buildings.to_file(f"{folder}{bbox_}_{self.features}.geojson", driver="GeoJSON")
                

                #for geomtype in buildings.geom_type.unique():
                #    buildings[buildings.geom_type == geomtype].to_file(f"{folder}{bbox}_{self.features}_{geomtype}.gpkg", driver="GPKG", layer=geomtype)
        else:
            buildings = ''
        
        ## Output
        self.outputs["Output_Message"].sv_set(buildings)
        
def register():
    if ox is not None:
        bpy.utils.register_class(SvMegapolisOSMDownloader)

def unregister():
    if ox is not None:
        bpy.utils.unregister_class(SvMegapolisOSMDownloader)
