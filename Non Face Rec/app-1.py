import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
import base64

app = Flask(__name__)


#def function():
    # RUN ML MODEL HERE
    # return result


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        data = request.data
        d = json.loads(data)
        t = "test.jpg"
        k = os.getcwd()+"/Test"
        if not os.path.exists(k):
            os.makedirs(k)
        image_data = d['image']
        image_data += "=" * ((4 - len(image_data) % 4) % 4)
        with open(k+"/" + t, "wb") as fh:
            fh.write(base64.b64decode(image_data))
        # t = function and return t
        return 'Worked just fine!'

    else:
        return "Not how you use this!"


@app.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == 'POST':
        data = request.data
        d = json.loads(data)
        l = d['subject']
        trainee = d['fileno']
        cwd = os.getcwd()
        t = cwd + "/" + l
        if not os.path.exists(t):
            os.makedirs(t)
        folder = t
        image_data = d['image']
        image_data += "=" * ((4 - len(image_data) % 4) % 4)
        file = folder+"/" + l +"_"+trainee+".jpg"
        with open(file, "wb") as fh:
            fh.write(base64.b64decode(image_data))
        return 'wowzie first try'
    else:
        return 'Not how you use it!'


#@app.route('/fb', methods=['GET', 'POST'])
#def get_data():
#    if request.method == 'POST':
#        data = request.data
#        d = json.loads(data)


if __name__ == '__main__':
    app.run()
