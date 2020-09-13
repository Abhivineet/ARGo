import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
import base64

app = Flask(__name__)

def function():
    return

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        data = request.data
        d = json.loads(data)
        t = "test.bmp"
        image_data = d['image']
        image_data+="="*((4-len(image_data)%4)%4)
        with open(t, "wb") as fh:
            fh.write(base64.b64decode(image_data))
        return 'Worked just fine!'
        
    else:
        return "Not how you use this!"

if __name__ == '__main__':
    app.run()

