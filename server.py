# IP pi - 192.168.43.250
# server IP - 192.168.43.142

from flask import Flask, request, jsonify
from time import sleep
import brain
#import CNNTest as CNN
import numpy as np
from PIL import Image

app = Flask(__name__)

@app.route("/")
def hello():
    return "Server is running . . ."

@app.route('/detectImage/<fileName>',methods=['GET'])
def detectImage(fileName):
    # Detecting objects
    objects = brain.predictRetina(fileName)
    return jsonify(objects)

@app.route('/detectImage/<algo>',methods=['POST'])
def recognizeImage(algo): 
    # Saving the image
    file = request.files['media']
    fileName = file.filename
    with open('saved_'+fileName,'wb') as f:
        f.write(file.read())
    
    # Detecting objects
    objects = []
    if algo == 'yolo':
        objects = brain.predictYOLO('saved_'+fileName)
    else:
        objects = brain.predictRetina('saved_'+fileName)

    # Returning response
    return jsonify(objects)

@app.route('/detectSign/<fileName>',methods=['GET'])
def detectSign(fileName):
    # TODO : Get method to identify sign 
    return 'Not completed'

@app.route('/detectSign',methods=['POST'])
def recognizeSign():
    # Saving the image
    file = request.files['media']
    fileName = file.filename
    with open('saved_'+fileName,'wb') as f:
        f.write(file.read())
    
    # TODO : Get method to identify sign 
    return 'Not completed'

@app.route('/detectSignData',methods=['POST'])
def recognizeSignData():
    imgX = request.json['imgX']
    imgX = np.array(imgX)
    resp = CNN.detectSignData(imgX)
    return resp

@app.route('/createDataset/<folderName>/<fileName>',methods=['POST'])
def createDataSet(folderName,fileName):
    # Saving the image
    file = request.files['media']
    with open('Dataset/'+folderName+'/'+fileName,'wb') as f:
        f.write(file.read())

    return fileName


if __name__ == "__main__":

    brain.trainRetina()
    brain.trainYOLO()

    print ("Done Training")

    # Starting the service 
    app.run(host= '0.0.0.0',debug=False,threaded=False)
