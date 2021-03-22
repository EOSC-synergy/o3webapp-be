from flask import Flask,request,url_for,redirect, jsonify
from flask_cors import CORS
import requests
import os
from .userManager import UserManager


# Backend interface, which is responsible for :
# 1. listening to the user request from frontend,
# 2. passing all the information following the url
# 3. and the request-object to the user manager handling request with the corresponding process.
app = Flask(__name__)
cors = CORS(app)

########################################
# url list:                             
########################################

# url for homepage
#@app.route('/', methods=['GET', 'POST'])
# def handle_request_on_homepage():
#    userManager = UserManager(request)
#    return userManager.handle_process_on_homepage()

# url for plotpage with operation ID 
#@app.route('/plot/<opID>', methods=['GET', 'POST'])
# def handle_request_on_plotpage(opID):
#    userManager = UserManager(request)
#    return userManager.handle_process_on_plotpage(opID)

# url for plotpage without operation ID
#@app.route('/plot', methods=['GET', 'POST'])
# def enter_plotpage():
#    userManager = UserManager(request)
#    return userManager.handle_process_on_plotpage("api_info")




#TODO url of frontend pages
#/plot 
# -> returns a Json with available plot types and settings for these
@app.route('/plot', methods=['GET', 'POST'])
def handle_request_for_ptype():
    userManager = UserManager(request)
    r = userManager.handle_process_on_plotpage("p_type", "json") ## TODO
    # TODO debug
    print(r)
    return r

#/plot/<pType> -> returns Bokeh as json object with the specified plot drawn with the specified parameters (coming from the json on request)
@app.route('/plot/<pType>', methods=['GET', 'POST'])
def handle_request_for_plot(pType):
    userManager = UserManager(request)
    return userManager.handle_process_on_plotpage("plot", "json") ## TODO

#/download/<format> -> download the plot in the given format (CSV, PNG, PDF...)
@app.route('/download/<format>', methods=['GET', 'POST'])
def handle_request_for_download(format):
    # TODO debug
    #print(format)
    userManager = UserManager(request)
    r = userManager.handle_process_on_plotpage("plot", format) ## TODO "pdf"
    # TODO debug
    #print(r)
    return r

#/model_list/<pType> -> returns the available models for the given plottype
@app.route('/model_list/<pType>', methods=['GET', 'POST'])
def handle_request_for_typemv(pType):
    # TODO debug
    print(request.method)
    userManager = UserManager(request)
    r = userManager.handle_process_on_plotpage("t_M_V", "json") ## TODO
    # TODO debug
    print(r)
    return r

#/model_info/<model> returns the info for the specified model

# TODO get token by code from EGI
@app.route('/login/<auth_code>', methods=['GET','POST'])
def login(auth_code):
    print(auth_code)
    egi_token_url = 'https://aai-dev.egi.eu/oidc/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    #fetch server url from environment variable
    server_url = os.getenv('FRONTEND_SERVER_URL', 'http://localhost:3000')
    redirect_url = server_url + '/redirect_url'
    data = {'grant_type':'authorization_code', 'code': auth_code,
            'redirect_uri': redirect_url}

    try:
        f = open("/run/secrets/egi_auth.txt", "r")
    except:
        f = open("../../egi_auth.txt", "r")
    
    client_secret = f.read()
    print(client_secret)
    auth = ('o3webapp', client_secret)
    egi_auth = requests.post(egi_token_url, headers=headers, data=data, auth=auth).json()

    try:
        access_token = egi_auth['access_token']

        userinfo_url='https://aai-dev.egi.eu/oidc/userinfo'
        headers = {"Authorization": "Bearer " + access_token}
        egi_userinfo = requests.get(userinfo_url, headers=headers).json()
        username = egi_userinfo['name']
        sub = egi_userinfo['sub']

        return jsonify({'sub': sub, 'name': username})
    except:
        print("Error:")
        print(egi_auth)

#with app.test_request_context():
    #print(url_for('/plot/', opID ='api_info'))
    #print(url_for('static', filename='plotpage.html'))

#with app.test_request_context('/plot/', method='POST'):
    #assert request.path == '/plot/'
    #assert request.method == 'POST'
