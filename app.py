'''
from EmergencyDetection.pipeline.training_pipeline import TrainPipeline

obj = TrainPipeline()
obj.run_pipeline()
'''


import sys,os
from EmergencyDetection.pipeline.training_pipeline import TrainPipeline
from EmergencyDetection.utils.main_utils import decodeImage, encodeImageIntoBase64
from flask import Flask, request, jsonify, render_template,Response
from flask_cors import CORS, cross_origin
from EmergencyDetection.constant.application import APP_HOST, APP_PORT
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"



@app.route("/train")
def trainRoute():
    obj = TrainPipeline()
    obj.run_pipeline()
    return "Training Successful!!" 


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/predict", methods=['POST','GET'])
@cross_origin()
def predictRoute():
    try:
        image = request.json['image']
        decodeImage(image, clApp.filename)

        #os.system("cd yolov5/ && python detect.py --weights ../best.pt --img 416 --conf 0.5 --source ../data/inputImage.jpg")
        os.system("yolo task=detect mode=predict model=artifacts/model_trainer/best.pt conf=0.25 source=data/inputImage.jpg")
        #os.system("cd yolov5/ && python detect.py  --img 416 --conf 0.5 --source ../data/inputImage.jpg")

        opencodedbase64 = encodeImageIntoBase64("runs/detect/predict/inputImage.jpg")
        result = {"image": opencodedbase64.decode('utf-8')}
        os.system("rm -rf runs")

    except ValueError as val:
        print(val)
        return Response("Value not found inside  json data")
    except KeyError:
        return Response("Key value error incorrect key passed")
    except Exception as e:
        print(e)
        result = "Invalid input"

    return jsonify(result)



@app.route("/live", methods=['GET'])
@cross_origin()
def predictLive():
    try:
        os.system("yolo task=detect mode=predict model=artifacts/model_trainer/best.pt conf=0.25 source=0")
        os.system("rm -rf runs")
        return "Camera starting!!" 

    except ValueError as val:
        print(val)
        return Response("Value not found inside  json data")
    



if __name__ == "__main__":
    clApp = ClientApp()
    #app.run(host=APP_HOST, port=APP_PORT)
    #app.run(host='0.0.0.0', port=8080)
    app.run(host='0.0.0.0', port=80) # for Azure
    #



