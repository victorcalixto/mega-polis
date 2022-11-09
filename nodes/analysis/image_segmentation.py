import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty

from collections import namedtuple
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode


#Megapolis Dependencies
from megapolis.dependencies import cv2
from megapolis.dependencies import torch
from megapolis.dependencies import pandas as pd
from megapolis.dependencies import detectron2


try:
    from detectron2.engine import DefaultPredictor
    from detectron2.config import get_cfg
    from detectron2.data import MetadataCatalog
    from detectron2.utils.visualizer import ColorMode, Visualizer
    from detectron2 import model_zoo
except:
    pass


import os
import numpy as np
from pathlib import Path

from collections import namedtuple



Detectron_method = namedtuple('DetectronMethod', ['OD', 'IS','KP','LVIS','PS'])
DETECTRONMETHOD = Detectron_method('OD', 'IS','KP','LVIS','PS')
detectronmethod_items = [(i, i, '') for i in DETECTRONMETHOD]

Method = namedtuple('DownloadMethod', ['Image','Folder','Video'])
METHOD = Method('Image','Folder','Video')
method_items = [(i, i, '') for i in METHOD]


Device = namedtuple('Device', ['cpu', 'gpu'])
DEVICE = Device('cpu', 'gpu')
device_items = [(i, i, '') for i in DEVICE]



class Detector:
    def __init__(self,device,thresh, model_type="OD"):
        self.cfg = get_cfg()
        self.model_type = model_type
            
        if model_type == "OD":#object detection
            #load models from zoo
            self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml"))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml")

        elif model_type == "IS":#instance segmentation
            self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_C4_1x.yaml"))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_C4_1x.yaml")

        elif model_type == "KP":#instance segmentation
            self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_X_101_32x8d_FPN_3x.yaml"))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Keypoints/keypoint_rcnn_X_101_32x8d_FPN_3x.yaml")

        elif model_type == "LVIS":#lvis segmentation
            self.cfg.merge_from_file(model_zoo.get_config_file("LVISv0.5-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_1x.yaml"))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("LVISv0.5-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_1x.yaml")

        elif model_type == "PS":#lvis segmentation
            self.cfg.merge_from_file(model_zoo.get_config_file("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml"))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml")

            self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = thresh
            
        if device == "cuda":
            self.cfg.MODEL.DEVICE = "cuda" # cpu or cuda
        else:
            self.cfg.MODEL.DEVICE = "cpu"
        self.predictor = DefaultPredictor(self.cfg)

    def onImage(self, imagePath,output_folder):
        image  = cv2.imread(imagePath)
        width = image.shape[1]
        height = image.shape[0]
        image_name = Path(imagePath).stem

        if self.model_type != "PS":
            predictions = self.predictor(image)
            viz = Visualizer(image[:,:,::-1],metadata=MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), instance_mode = ColorMode.IMAGE_BW)
            output = viz.draw_instance_predictions(predictions["instances"].to("cpu"))
            
            if self.model_type == "OD":
                cv2.imwrite(f"{output_folder}/{image_name}_OD.png", output.get_image()[:, :, ::-1])
            elif self.model_type == "IS":
                cv2.imwrite(f"{output_folder}/{image_name}_IS.png", output.get_image()[:, :, ::-1])
            elif self.model_type == "KP":
                cv2.imwrite(f"{output_folder}/{image_name}_KP.png", output.get_image()[:, :, ::-1])
            elif self.model_type == "LVIS":
                cv2.imwrite(f"{output_folder}/{image_name}_LVIS.png", output.get_image()[:, :, ::-1])


            if self.model_type == "IS" or self.model_type == "LVIS":
                scores = predictions["instances"].scores.to("cpu").numpy()
                boxes = predictions["instances"].pred_boxes.tensor.to("cpu").numpy()
                mask = predictions["instances"].pred_masks
                classes = predictions["instances"].pred_classes.to("cpu").numpy()
                class_names = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).thing_classes
                
                mask_px = torch.sum(torch.flatten(mask, start_dim=1),dim=1)
                pred_class_names = list(map(lambda x: class_names[x], classes))
                mask_px = mask_px.to("cpu").numpy()
                
                percentage_elements= ((mask_px *100)/(height * width)) 

                series_scores = pd.Series(np.round(scores,decimals=4), name = "Scores")
                series_classes = pd.Series(pred_class_names, name="Classes")
                series_pixel_ratio = pd.Series(np.round(percentage_elements,decimals=4), name = "Pixel_Ratio")
                df = pd.concat([series_classes, series_scores, series_pixel_ratio], axis=1)

                if self.model_type == "IS":

                    df.to_csv(f"{output_folder}/{image_name}_IS.csv", index=False)
                else:
                    df.to_csv(f"{output_folder}/{image_name}_LVIS.csv", index=False)


            elif self.model_type == "OD" or self.model_type == "KP":
                scores = predictions["instances"].scores.to("cpu").numpy()
                boxes = predictions["instances"].pred_boxes.tensor.to("cpu").numpy()
                classes = predictions["instances"].pred_classes.to("cpu").numpy()
                class_names = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).thing_classes
                
                pred_class_names = list(map(lambda x: class_names[x], classes))

                series_scores = pd.Series(np.round(scores,decimals=4), name = "Scores")
                series_classes = pd.Series(pred_class_names, name="Classes")
                
                df = pd.concat([series_classes, series_scores], axis=1)
                
                if self.model_type == "OD":

                    df.to_csv(f"{output_folder}/{image_name}_OD.csv", index=False)
                else:
                    df.to_csv(f"{output_folder}/{image_name}_KP.csv", index=False)



        else:
            
            predictions, segmentInfo = self.predictor(image)["panoptic_seg"]
            
            viz = Visualizer(image[:,:,::-1],MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]))
            output = viz.draw_panoptic_seg_predictions(predictions.to("cpu"),segmentInfo)
            
            things_names = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).thing_classes
            stuff_names = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).stuff_classes
            

            categories = [i["category_id"] for i in segmentInfo]
            
            pred_things_names = list(map(lambda x: things_names[x], categories))
            pred_stuff_names = list(map(lambda x: stuff_names[x], categories))
             
            #pred_class_names_stuff = list(map(lambda x: panoptic_stuff[x], categories))
           

            cv2.imwrite(f"{output_folder}/{image_name}_PS.png", output.get_image()[:, :, ::-1])

            id_pano = segmentInfo

            for i in segmentInfo:
                i["pixel_ratio"] = (i["area"]*100)/(height*width)
                if i["isthing"] == True:
                    i["category_name"] = pred_things_names[segmentInfo.index(i)]  
                else:
                    i["category_name"] = pred_stuff_names[segmentInfo.index(i)]  

            df = pd.DataFrame(segmentInfo)

            df.to_csv(f"{output_folder}/{image_name}_PS.csv", index=False)
        return df    

    def onFolder(self, input_folder,output_folder):
        for root, directories, file in os.walk(input_folder):
            for file in file:
                if(file.endswith(".jpg") or file.endswith(".png")):
                    
                    
                    imagePath = os.path.join(root,file) 
                    
                    image  = cv2.imread(imagePath)
                    
                    width = image.shape[1]
                    height = image.shape[0]

                    image_name = Path(imagePath).stem

                    if self.model_type != "PS":
                        predictions = self.predictor(image)
                        viz = Visualizer(image[:,:,::-1],metadata=MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), instance_mode = ColorMode.IMAGE_BW)
                        output =viz.draw_instance_predictions(predictions["instances"].to("cpu"))
                        
                        if self.model_type == "OD":
                            cv2.imwrite(f"{output_folder}/{image_name}_OD.png", output.get_image()[:, :, ::-1])
                        elif self.model_type == "IS":
                            cv2.imwrite(f"{output_folder}/{image_name}_IS.png", output.get_image()[:, :, ::-1])
                        elif self.model_type == "KP":
                            cv2.imwrite(f"{output_folder}/{image_name}_KP.png", output.get_image()[:, :, ::-1])
                        elif self.model_type == "LVIS":
                            cv2.imwrite(f"{output_folder}/{image_name}_LVIS.png", output.get_image()[:, :, ::-1])

 
                        if self.model_type == "IS" or self.model_type == "LVIS":
           
                            scores = predictions["instances"].scores.to("cpu").numpy()
                            boxes = predictions["instances"].pred_boxes.tensor.to("cpu").numpy()
                            mask = predictions["instances"].pred_masks
                            classes = predictions["instances"].pred_classes.to("cpu").numpy()
                            class_names = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).thing_classes
                            mask_px = torch.sum(torch.flatten(mask, start_dim=1),dim=1)
                            pred_class_names = list(map(lambda x: class_names[x], classes))
                            mask_px = mask_px.to("cpu").numpy()
                            
                            percentage_elements= ((mask_px *100)/(height * width)) 

                            series_scores = pd.Series(np.round(scores,decimals=4), name = "Scores")
                            series_classes = pd.Series(pred_class_names, name="Classes")
                            series_pixel_ratio = pd.Series(np.round(percentage_elements,decimals=4), name = "Pixel_Ratio")
                            df = pd.concat([series_classes, series_scores, series_pixel_ratio], axis=1)

                            if self.model_type == "IS":

                                df.to_csv(f"{output_folder}/{image_name}_IS.csv", index=False)
                            else:
                                df.to_csv(f"{output_folder}/{image_name}_LVIS.csv", index=False)

                        
                        elif self.model_type == "OD" or self.model_type == "KP":
                            scores = predictions["instances"].scores.to("cpu").numpy()
                            boxes = predictions["instances"].pred_boxes.tensor.to("cpu").numpy()
                            classes = predictions["instances"].pred_classes.to("cpu").numpy()
                            class_names = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).thing_classes
                            
                            pred_class_names = list(map(lambda x: class_names[x], classes))

                            series_scores = pd.Series(np.round(scores,decimals=4), name = "Scores")
                            series_classes = pd.Series(pred_class_names, name="Classes")
                            
                            df = pd.concat([series_classes, series_scores], axis=1)
                            
                            if self.model_type == "OD":

                                df.to_csv(f"{output_folder}/{image_name}_OD.csv", index=False)
                            else:
                                df.to_csv(f"{output_folder}/{image_name}_KP.csv", index=False)


                    else:
                        predictions, segmentInfo = self.predictor(image)["panoptic_seg"]
                        viz = Visualizer(image[:,:,::-1],MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]))
                        output = viz.draw_panoptic_seg_predictions(predictions.to("cpu"),segmentInfo)
                        
                        cv2.imwrite(f"{output_folder}/{image_name}_processed.png", output.get_image()[:, :, ::-1])
            
                        things_names = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).thing_classes
                        stuff_names = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).stuff_classes
                        

                        categories = [i["category_id"] for i in segmentInfo]
                        
                        pred_things_names = list(map(lambda x: things_names[x], categories))
                        pred_stuff_names = list(map(lambda x: stuff_names[x], categories))
                         
                        #pred_class_names_stuff = list(map(lambda x: panoptic_stuff[x], categories))
                       

                        cv2.imwrite(f"{output_folder}/{image_name}_PS.png", output.get_image()[:, :, ::-1])

                        id_pano = segmentInfo

                        for i in segmentInfo:
                            i["pixel_ratio"] = (i["area"]*100)/(height*width)
                            if i["isthing"] == True:
                                i["category_name"] = pred_things_names[segmentInfo.index(i)]  
                            else:
                                i["category_name"] = pred_stuff_names[segmentInfo.index(i)]  

                        df = pd.DataFrame(segmentInfo)

                        df.to_csv(f"{output_folder}/{image_name}_PS.csv", index=False)
                        


        cv2.imshow("Result", output.get_image()[:,:,::-1])
        cv2.waitKey(0)
        return df

    def onVideo(self,videoPath,output_folder):
        cap = cv2.VideoCapture(videoPath)
        video_name = Path(videoPath).stem

        if (cap.isOpened()==False):
            print("Error opening the file...")
            return
        (sucess,image) = cap.read()
        while sucess:
            if self.model_type != "PS":
                predictions = self.predictor(image)
                viz = Visualizer(image[:,:,::-1],metadata=MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), instance_mode = ColorMode.IMAGE_BW)
                output =viz.draw_instance_predictions(predictions["instances"].to("cpu"))
                
                if self.model_type == "IS" or self.model_type == "LVIS": 

                    scores = predictions["instances"].scores.to("cpu").numpy()
                    boxes = predictions["instances"].pred_boxes.tensor.to("cpu").numpy()
                    mask = predictions["instances"].pred_masks
                    classes = predictions["instances"].pred_classes.to("cpu").numpy()
                    class_names = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).thing_classes
                    mask_px = torch.sum(torch.flatten(mask, start_dim=1),dim=1)
                    pred_class_names = list(map(lambda x: class_names[x], classes))
                    mask_px = mask_px.to("cpu").numpy()
                    
                    percentage_elements= ((mask_px *100)/(height * width)) 

                    series_scores = pd.Series(np.round(scores,decimals=4), name = "Scores")
                    series_classes = pd.Series(pred_class_names, name="Classes")
                    series_pixel_ratio = pd.Series(np.round(percentage_elements,decimals=4), name = "Pixel_Ratio")
                    df = pd.concat([series_classes, series_scores, series_pixel_ratio], axis=1)
                    
                    if self.model_type == "IS":
                        df.to_csv(f"{output_folder}/{image_name}_IS.csv", index=False)
                    else:
                        df.to_csv(f"{output_folder}/{image_name}_LVIS.csv", index=False)


                    df.to_csv(f"{output_folder}/{video_name}.csv", index=False)
                
                elif self.model_type == "OD" or self.model_type == "KP":
                    scores = predictions["instances"].scores.to("cpu").numpy()
                    boxes = predictions["instances"].pred_boxes.tensor.to("cpu").numpy()
                    classes = predictions["instances"].pred_classes.to("cpu").numpy()
                    class_names = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).thing_classes
                    
                    pred_class_names = list(map(lambda x: class_names[x], classes))

                    series_scores = pd.Series(np.round(scores,decimals=4), name = "Scores")
                    series_classes = pd.Series(pred_class_names, name="Classes")
                    
                    df = pd.concat([series_classes, series_scores], axis=1)
                    if self.model_type == "OD":

                        df.to_csv(f"{output_folder}/{image_name}_OD.csv", index=False)
                    else:
                        df.to_csv(f"{output_folder}/{image_name}_KP.csv", index=False)


            else:
                predictions, segmentInfo = self.predictor(image)["panoptic_seg"]
                viz = Visualizer(image[:,:,::-1],MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]))
                output = viz.draw_panoptic_seg_predictions(predictions.to("cpu"),segmentInfo)
               
                things_names = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).thing_classes
                stuff_names = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).stuff_classes
                

                categories = [i["category_id"] for i in segmentInfo]
                
                pred_things_names = list(map(lambda x: things_names[x], categories))
                pred_stuff_names = list(map(lambda x: stuff_names[x], categories))
                 
                #pred_class_names_stuff = list(map(lambda x: panoptic_stuff[x], categories))

                cv2.imwrite(f"{output_folder}/{video_name}_PS.mp4", output.get_image()[:, :, ::-1])

                id_pano = segmentInfo

                for i in segmentInfo:
                    i["pixel_ratio"] = (i["area"]*100)/(height*width)
                    if i["isthing"] == True:
                        i["category_name"] = pred_things_names[segmentInfo.index(i)]  
                    else:
                        i["category_name"] = pred_stuff_names[segmentInfo.index(i)]  

                df = pd.DataFrame(segmentInfo)

                df.to_csv(f"{output_folder}/{video_name}_PS.csv", index=False)

                            
            cv2.imshow("Result", output.get_image()[:,:,::-1])
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            (sucess,image) = cap.read()
 

        return df



class SvMegapolisImageSegmentation(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Image Segmentation
    Tooltip: Image Segmentation
    """
    bl_idname = 'SvMegapolisImageSegmentation'
    bl_label = 'ImageSegmentation'
    bl_icon = 'MESH_DATA'
    

    # Hide Interactive Sockets
    def update_sockets(self, context):
        """ need to do UX transformation before updating node"""
        def set_hide(sock, status):
            if sock.hide_safe != status:
                sock.hide_safe = status
            
        if self.method in METHOD.Folder:
            set_hide(self.inputs['File'], True)
            set_hide(self.inputs['Folder Input'], False)
            set_hide(self.inputs['Folder Output'], False)

        else:
            set_hide(self.inputs['File'], False)
            set_hide(self.inputs['Folder Input'], True)
            set_hide(self.inputs['Folder Output'], False)

        updateNode(self,context)

    #Blender Properties Buttons

    run: BoolProperty(
        name="run",
        description="Run Detectron",
        default=False,
        update=update_sockets)
    
    detectron_method: EnumProperty(
        name='detectron_method', items=detectronmethod_items,
        default="IS",
        description='Choose a Detectron Method', 
        update=update_sockets)
    
    method: EnumProperty(
        name='method', items=method_items,
        default="Image",
        description='Choose a Method', 
        update=update_sockets)
    
    device: EnumProperty(
        name='device', items=device_items,
        default="cpu",
        description='CPU or GPU', 
        update=update_sockets)

    threshold: FloatProperty(
            name="threshold",
            description="Threshold detection value",
            default= .7,
            max= .99,
            min= .01,
            update=update_sockets)
        


    def sv_init(self, context):
       
        # inputs
        self.inputs.new('SvFilePathSocket', "File")
        self.inputs.new('SvStringsSocket', "Folder Input")
        self.inputs.new('SvStringsSocket', "Folder Output")
       

        self.inputs['Folder Input'].hide_safe = True 

        # outputs

        self.outputs.new('SvStringsSocket', "Dataframe")
        
        
    def draw_buttons(self,context, layout):
        layout.prop(self, 'run')
        layout.prop(self, 'detectron_method')
        layout.prop(self, 'method', expand=True)
        layout.prop(self, 'device', expand=True)
        layout.prop(self, 'threshold')



    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)

    def process(self):
         
        detector = Detector(self.device, self.threshold, self.detectron_method)


        if self.method in METHOD.Folder:
            if not self.inputs["Folder Input"].is_linked or not self.inputs["Folder Output"].is_linked :
                return
            self.folder_input = self.inputs["Folder Input"].sv_get(deepcopy = False)
            self.folder_output = self.inputs["Folder Output"].sv_get(deepcopy = False)
            
            results = ''
            if self.run == True:
                results = detector.onFolder(str(self.folder_input[0][0]),str(self.folder_output[0][0]))

        elif self.method in METHOD.Image:
            if not self.inputs["File"].is_linked or not self.inputs["Folder Output"].is_linked :
                return
            self.file = self.inputs["File"].sv_get(deepcopy = True)
            self.folder_output = self.inputs["Folder Output"].sv_get(deepcopy = True)
            
            results = ''
            if self.run == True:
                results = detector.onImage(str(self.file[0][0]),str(self.folder_output[0][0]))

        else:
            if not self.inputs["File"].is_linked:
                return
            self.file = self.inputs["File"].sv_get(deepcopy = False)
            self.folder_output = self.inputs["Folder Output"].sv_get(deepcopy = False)
            
            results = ''
            if self.run == True:
                results = detector.onVideo(str(self.file[0][0]),str(self.folder_output[0][0]))
        
        ## Output
        self.outputs["Dataframe"].sv_set(results)
        
def register():
    bpy.utils.register_class(SvMegapolisImageSegmentation)

def unregister():
    bpy.utils.unregister_class(SvMegapolisImageSegmentation)
