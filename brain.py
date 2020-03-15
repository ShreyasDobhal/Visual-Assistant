from imageai.Detection import ObjectDetection

retinaDetector = ObjectDetection()
yoloDetector = ObjectDetection()
detections = []

def trainRetina():
    retinaDetector.setModelTypeAsRetinaNet()
    retinaDetector.setModelPath("resnet50_coco_best_v2.0.1.h5")
    retinaDetector.loadModel()

def trainYOLO():
    yoloDetector.setModelTypeAsYOLOv3()
    yoloDetector.setModelPath("yolo.h5")
    yoloDetector.loadModel()

def predictRetina(fileName):
    detections = retinaDetector.detectObjectsFromImage(input_image=fileName, output_image_path='new_'+fileName)
    objects = []
    for eachObject in detections:
        obj = {'name':eachObject['name'],'percentage':eachObject['percentage_probability']}
        objects.append(obj)
    return objects

def predictYOLO(fileName):
    detections = yoloDetector.detectObjectsFromImage(input_image=fileName, output_image_path='new_'+fileName)
    objects = []
    for eachObject in detections:
        obj = {'name':eachObject['name'],'percentage':eachObject['percentage_probability']}
        objects.append(obj)
    return objects