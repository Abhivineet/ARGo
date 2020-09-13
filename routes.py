from app import app
from flask import request
import json
from app.models import User
from app import db
import os
import subprocess
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import time
from imutils.video import VideoStream
import base64
@app.route('/')
@app.route('/index')

def index():
    return "Hello, World!"


@app.route('/create_user', methods =['POST'])

def create_user():
    print(request.data)
    data = json.loads(request.data.decode('utf8'))
    #user = User(user_id = data["userid"], username=data["username"], password_hash=data["password"], email=data["email"])
    #db.session.add(user)
    #db.session.commit()

    print(data)
    return "OK" #+ data["username"]


@app.route('/face_embed',methods = ['POST'])

def face_embed():
    #The images need to be sent as a JSON array, all 10 or how many ever of them.
    #This part processes those 10 and then stores the embedding. 
    d = json.loads(request.data)
    image_path = '/Users/gokul/PycharmProjects/server_f/temp_images/'
    encodings_path = '/Users/gokul/PycharmProjects/server_f/encodings/'
    uid = d['user_id']
    image_data = d['images']
    encod_user = []
    encod_id = []
    #print(image_data)
    for img in image_data:
        #print(img)
        #img+="="*((4-len(img)%4)%4)
        #print(img)
        imagePath = image_path + str(time.time()) +'.jpg'
        with open(imagePath, "wb") as fh:
                fh.write(base64.b64decode(img))

        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb,model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            encod_user.append(encoding)
            encod_id.append(uid)

    data = {"encodings": encod_user, "names": encod_id}
    path_to_save = encodings_path + "Encodings" + str(uid)
    f = open(path_to_save, "wb")
    f.write(pickle.dumps(data))
    f.close()
    print(len(encod_user))
    # print(type(request.data))
    return "OK"
    # inp = json.loads(request.data.decode('utf8'))["arg"]
    # return subprocess.check_output(['python3','test.py', '-i', inp]).decode('utf8')
    #return os.getcwd()

@app.route('/face_rec',methods = ['GET'])
def face_rec():
    #Send image as normal base64 string, no need of an array. 
    encodings_path = '/Users/gokul/PycharmProjects/server_f/encodings/'
    d = json.loads(request.data)

    image_data = d['images']
    image_data+="="*((4-len(image_data)%4)%4)
    image_path = '/Users/gokul/PycharmProjects/server_f/temp_images/'
    imagePath = image_path + str(time.time())
    with open(imagePath, "wb") as fh:
            fh.write(base64.b64decode(image_data))

    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb,model="hog")
    enc_rec = face_recognition.face_encodings(rgb, boxes)
    names = []
    list_of_files = os.listdir(encodings_path)
    #print(list_of_files)
    files_to_ignore = ['.DS_Store']
    #num_files = len(list_of_files)
    for file in list_of_files:
        if file not in files_to_ignore:
            encodings_data = pickle.loads(open(encodings_path + file,"rb").read())
            #print(type(encodings_data))
            for encoding in enc_rec:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(encodings_data["encodings"],encoding)
                name = "Unknown"
                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                            name = encodings_data["names"][i]
                            counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    name = max(counts, key=counts.get)

                    # update the list of names
                names.append(name)
    print(names)
    return 'OK' + names[1]
