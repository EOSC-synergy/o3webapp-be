from flask import Flask, request, url_for, redirect, jsonify, json,send_from_directory
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.exceptions import HTTPException
from .userManager import UserManager, OpID
from .backendException import LoginException
from pathlib import Path
import os
import io
import base64
from PIL import Image


# Backend interface, which is responsible for :
# 1. listening to the user request from frontend,
# 2. passing all the information following the url
# 3. and the request-object to the user manager handling request with the corresponding process.
app = Flask(__name__)
cors = CORS(app)
app.use_x_sendfile=True

########################################
# url list:                             
########################################

#/plot -> returns a Json with available plot types and settings for these
@app.route('/plot', methods=['GET', 'POST'])
def handle_request_for_ptype():
    try:
        userManager = UserManager(request)
        r = userManager.handle_process_on_plotpage(OpID.p_type)
    except Exception as e:
        print(e)
        return ""
    else:
        return r

#/plot/<pType> -> returns Bokeh as json object with the specified plot drawn with the specified parameters (coming from the json on request)
@app.route('/plot/<pType>', methods=['GET', 'POST'])
def handle_request_for_plot(pType):
    try:
        userManager = UserManager(request)
        r = userManager.handle_process_on_plotpage(OpID.plot)
    except Exception as e:
        print(e)
        return "file"
    else:
        return r

#/download/<format> -> download the plot in the given format (CSV, PNG, PDF...)
@app.route('/download11/<format>', methods=['GET', 'POST'])
def handle_request_for_download(format):
    try:
        userManager = UserManager(request)
        r = userManager.handle_process_on_plotpage(OpID.plot)
    except Exception as e:
        print(e)
        return "json file with exception info"
    else:
        return r

#/model_list/<pType> -> returns the available models for the given plottype
@app.route('/model_list/<pType>', methods=['GET', 'POST'])
def handle_request_for_typemv(pType):
    try:
        userManager = UserManager(request)
        r = userManager.handle_process_on_plotpage(OpID.t_M_V)
    except Exception as e:
        print(e)
        return "json file with exception info"
    else:
        return r

#/model_info/<model> -> returns the info for the specified model

#/login/<auth_code> -> returns the token required by auth_code from EGI
@app.route('/login/<auth_code>', methods=['GET','POST'])
def login(auth_code):
    try:
        userManager = UserManager(request)
        r = userManager.handle_process_on_loginpage(auth_code)
    except LoginException as e:
        return e.args
    except Exception as e:
        print(e)
        return ""
    else:
        return r


########################################
# HTTP Exception list:                             
########################################
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


########################################
# API list:                             
########################################
api = Api(app)

class Plot(Resource):
    def get(self, format):
        return 'cant find download information',404

    def post(self, format):
        try:
            userManager = UserManager(request)
            r = userManager.handle_process_on_plotpage(OpID.plot)
            #print(r)
            img = self.get_encoded_img()
            response_data = {"image": img}
        except FileNotFoundError as e:
            print(e)
            return "json file with exception info",204
        except Exception as e:
            print(e)
            return "json file with exception info",205
        else:
            return response_data, 200
            #return jsonify(response_data),200
            #return r,200

    def get_encoded_img(self):
        folder_path = Path(os.getenv('PLOT_FOLDER'))
        img_byte_arr = io.BytesIO()
        img = Image.open(folder_path/"pdf/plot.png", mode='r')
        #img.save(img_byte_arr, format='PNG')
        pdf = img.convert('RGB')
        pdf.save(img_byte_arr, format='PDF')
        my_encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
        return my_encoded_img

api.add_resource(Plot, '/download/<format>')
