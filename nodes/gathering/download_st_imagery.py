import os
import threading
import bpy
from bpy.props import IntProperty, BoolProperty

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

# Megapolis Dependencies
from megapolis.dependencies import mapillary as mly
from megapolis.dependencies import requests

try:
    from pyproj import Transformer
except ImportError:
    Transformer = None


class SvMegapolisDownloadStImagery(SverchCustomTreeNode, bpy.types.Node):
    """
    Node to download geo-referenced Mapillary street imagery.

    Tooltip: Downloads street-level imagery using Mapillary API.
    """
    bl_idname = "SvMegapolisDownloadStImagery"
    bl_label = "Download Street Imagery"
    bl_icon = "IMAGE_RGB"
    sv_dependencies = {"mapillary", "requests"}

    def update_sockets(self, context):
        """Perform UX transformation before updating the node."""
        updateNode(self, context)

    # Blender Properties Buttons
    projection: IntProperty(
        name="Projection",
        description="CSR Projection Number",
        default=4236,
        update=update_sockets
    )

    download: BoolProperty(
        name="Download",
        default=False,
        description="Download the street imagery",
        update=update_sockets
    )

    def sv_init(self, context):
        """Initialize input and output sockets."""
        self.inputs.new("SvStringsSocket", "Mapillary_Key")
        self.inputs.new("SvStringsSocket", "Folder")
        self.inputs.new("SvStringsSocket", "Longitude")
        self.inputs.new("SvStringsSocket", "Latitude")
        self.inputs.new("SvStringsSocket", "Max_Num_Photos")

        self.outputs.new("SvStringsSocket", "Images_Index")
        self.outputs.new("SvVerticesSocket", "Coordinates")
        self.outputs.new("SvStringsSocket", "Output_Message")

    def draw_buttons(self, context, layout):
        """Draw UI buttons for the node."""
        layout.prop(self, "download")
        layout.prop(self, "projection")

    def draw_buttons_ext(self, context, layout):
        """Extended UI layout."""
        self.draw_buttons(context, layout)

    def process(self):
        """Handles downloading of street imagery."""
        if not self.download or not self.inputs["Folder"].is_linked:
            return

        mapillary_key = self.inputs["Mapillary_Key"].sv_get(deepcopy=False)
        folder = self.inputs["Folder"].sv_get(deepcopy=False)
        longitude = self.inputs["Longitude"].sv_get(deepcopy=False)
        latitude = self.inputs["Latitude"].sv_get(deepcopy=False)
        max_photos = self.inputs["Max_Num_Photos"].sv_get(deepcopy=False)

        if not (mapillary_key and folder and longitude and latitude and max_photos):
            return

        mapillary_key = str(mapillary_key[0][0])
        folder_name = str(folder[0][0])
        longitude = float(longitude[0][0])
        latitude = float(latitude[0][0])
        max_photos = int(max_photos[0][0])

        location = []
        mly.interface.set_access_token(mapillary_key)

        print(f"Longitude: {longitude}")
        print(f"Latitude: {latitude}")

        images_dict = mly.interface.get_image_close_to(longitude, latitude)
        data = images_dict.to_dict()
        images_id = mly.utils.extract.extract_properties(data, properties=["id"])
        message = []

        def download_images(images, folder_name, location, message):
            """Downloads images from Mapillary."""
            os.makedirs(folder_name, exist_ok=True)

            for image_id in images:
                header = {"Authorization": f"OAuth {mapillary_key}"}
                url_json = (
                    f"https://graph.mapillary.com/{image_id}"
                    f"?access_token={mapillary_key}"
                    "&fields=thumb_original_url,computed_geometry,"
                    "captured_at,computed_compass_angle"
                )

                response = requests.get(url_json, headers=header)
                if response.status_code == 200:
                    data = response.json()
                    image_url = data.get("thumb_original_url")

                    if image_url:
                        image_path = os.path.join(folder_name, f"{image_id}.jpg")
                        with open(image_path, "wb") as f:
                            f.write(requests.get(image_url, stream=True).content)

                        print(f"Downloaded {image_id}.jpg in {folder_name}")
                        location.append(data["computed_geometry"]["coordinates"])
                        message.append(f"Downloaded {image_id}.jpg in {folder_name}")

        images = images_id["id"]
        image_subset = images[:max_photos]

        if self.download:
            download_thread = threading.Thread(
                target=download_images,
                args=(image_subset, folder_name, location, message),
            )
            download_thread.start()
            download_thread.join()

        coords = []

        if Transformer:
            transformer = Transformer.from_crs("+proj=latlon", f"epsg:{self.projection}")

            for loc in location:
                x, y = transformer.transform(loc[0], loc[1])
                coords.append([x, y, 0])

        coords = [coords]

        # Outputs
        self.outputs["Images_Index"].sv_set(images)
        self.outputs["Coordinates"].sv_set(coords)
        self.outputs["Output_Message"].sv_set(message)


def register():
    bpy.utils.register_class(SvMegapolisDownloadStImagery)


def unregister():
    bpy.utils.unregister_class(SvMegapolisDownloadStImagery)

