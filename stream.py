#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
from flask import Flask, render_template, Response,request,jsonify,redirect,url_for
import datetime
#import os
#import glob
#import time

#import numpy as np

cam=None
capdir="cap"

class MyCamera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def __del__(self):
        self.cap.release()

    def getframe(self):
        ret,frame = self.cap.read()

        if ret == False : return None

        frame = cv2.rotate(frame, cv2.ROTATE_180)

        return frame


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

#def gen(cam):
def gen():

    while True:
        frame=cam.getframe()

        if frame is None : break

        _,jpeg = cv2.imencode('.jpg', frame)

        b = jpeg.tobytes()

        #yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + b + b'\r\n\r\n')

        yield (b'--frame\r\n'
               b'Content-Type:image/jpeg\r\n'
               b'Content-Length: ' + f"{len(b)}".encode() + b'\r\n'
               b'\r\n' + b + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/feed")
def feed():

#    return Response(gen(MyCamera()),mimetype="multipart/x-mixed-replace; boundary=frame")
    return Response(gen(),mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/cap",methods=["POST"])
def cap():

    now = datetime.datetime.now()
    fn = now.strftime('%Y%m%d%H%M%S')

    path="{0}/{1}.jpg".format(capdir,fn)
    frame=cam.getframe()
    cv2.imwrite(path,frame)

    return redirect(url_for("index"))

if __name__ == '__main__':

    cam=MyCamera()
    app.run(host='0.0.0.0', debug=False,threaded=True)

#    app.run(host='0.0.0.0', debug=True)
#    python3 stream.py  2>/dev/null &   :start



# In[ ]:





# In[ ]:
