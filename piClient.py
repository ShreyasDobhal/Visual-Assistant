import requests
import json
from PIL import Image
import cv2
from glob import glob 
from playsound import playsound
from gtts import gTTS
import threading
import speech_recognition as sr
from time import sleep

URL = 'http://192.168.43.142:5000/'
QUERY = 'detectImage/'
YOLO = 'yolo'
RETINA = 'retina'

filename = 'image.png'

r=sr.Recognizer()

opMode = 1

detectMode = ["objects","object","detect","object detection"]
ocrMode = ["ocr","read","document"]
stopMode = ["stop","pause","end"]

def speechRecog():
    global opMode
    while True:
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                print(text)
                for word in detectMode:
                    if word in text:
                        opMode = 1
                
                for word in ocrMode:
                    if word in text:
                        opMode = 2
                
                for word in stopMode:
                    if word in text:
                        opMode = 0
            except:
                ...
        sleep(0.1)

def detectImage():
    while True:
        if opMode == 1:
            print ("Detecting")
            # detectObjects()
        elif opMode == 2:
            print ("OCR")
            # OCR()
        sleep(0.1)

def detectObjects():
    camera = cv2.VideoCapture(3)
    ret, frame = camera.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    
    # cv2.imshow('Camera', rgb) # Comment for PI

    out = cv2.imwrite(filename, frame)

    print ("File saved ")
    files = {'media': open(filename, 'rb')}
    print ("Sending")
    response = requests.post(URL+QUERY+YOLO, files=files)
    print ("Received")
    print (response.text)

    hashMap = {}

    for obj in json.loads(response.text):
        hashMap[obj['name']] = 1
    
    for obj in hashMap:
        if len(glob(obj+".mp3"))==0:
            print ("Creating new file")
            tts = gTTS(text=obj, lang='en')
            tts.save(obj+".mp3")
            print ("File created")
        print ("Playing sound")
        playsound(obj+'.mp3', True)

    del(camera)

def OCR():
    # TODO add OCR code here
    print ("Output from OCR")


if __name__ == "__main__": 

    speechRecog()
    # t1 = threading.Thread(target=speechRecog, args=()) 
    # t2 = threading.Thread(target=detectImage, args=()) 
  
    # t1.start() 
    # t2.start() 