from flask import Flask, request, url_for, redirect, jsonify, json
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.exceptions import HTTPException
from userManager import UserManager, OpID
from backendException import LoginException


# Backend interface, which is responsible for :
# 1. listening to the user request from frontend,
# 2. passing all the information following the url
# 3. and the request-object to the user manager handling request with the corresponding process.
app = Flask(__name__)
cors = CORS(app)

########################################
# url list:                             
########################################

#/plot -> returns a Json with available plot types and settings for these
@app.route('/plot', methods=['GET', 'POST'])
def handle_request_for_ptype():
    try:
        userManager = UserManager(request)
        r = userManager.handle_process_on_plotpage(OpID.p_type)
    except Exception:
        print("plot type error")
        return ""
    else:
        return r

#/plot/<pType> -> returns Bokeh as json object with the specified plot drawn with the specified parameters (coming from the json on request)
@app.route('/plot/<pType>', methods=['GET', 'POST'])
def handle_request_for_plot(pType):
    try:
        userManager = UserManager(request)
        r = userManager.handle_process_on_plotpage(OpID.plot)
    except Exception:
        print("plot error")
        return "file"
    else:
        return r 

#/download/<format> -> download the plot in the given format (CSV, PNG, PDF...)
@app.route('/download/<format>', methods=['GET', 'POST'])
def handle_request_for_download(format):
    try:
        userManager = UserManager(request)
        r = userManager.handle_process_on_plotpage(OpID.plot)
    except Exception:
        print("download error")
        return "json file with exception info"
    else:
        return r

#/model_list/<pType> -> returns the available models for the given plottype
@app.route('/model_list/<pType>', methods=['GET', 'POST'])
def handle_request_for_typemv(pType):
    try:
        userManager = UserManager(request)
        r = userManager.handle_process_on_plotpage(OpID.t_M_V)
    except Exception:
        print("model list error")
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
    except Exception:
        print("login error")
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

parser = reqparse.RequestParser()
parser.add_argument('task')

class Plot(Resource):
    def get(self, format):
        pass

    def post(self, format):
        #args = parser.parse_args()
        #todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        #todo_id = 'todo%i' % todo_id
        #TODOS[todo_id] = {'task': args['task']}
        #return TODOS[todo_id], 201
        pass

api.add_resource(Plot, '/download/<format>')

