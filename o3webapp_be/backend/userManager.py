import enum
from flask import url_for,redirect,request, jsonify
import requests

from controller import APIInfoController,PlotypesController,ModelsInfoController,TypeModelsVarsController,PlotController


# Five kinds of operations, identified by OpID, default as api_info = 1
class OpID(enum.Enum):
   api_info = 1
   p_type = 2
   models_info = 3
   t_M_V = 4
   plot = 5

# User Manager, which handles all kinds of user requests :
# 1. Arranging the user info and user status, 
#    for example authenticated status, user cookies and sessions.
# 2. Handling the request-object received by backend interface,
#    choosing specific controller to handle the request corresponding to the operation ID,
#    extracting the json form from the request-object and feeding it to the controller.

class UserManager:

    opDict = {OpID.api_info: (lambda jsonRequest: APIInfoController(jsonRequest)),
              OpID.p_type: (lambda jsonRequest: PlotypesController(jsonRequest)),
              OpID.models_info: (lambda jsonRequest: ModelsInfoController(jsonRequest)),
              OpID.t_M_V: (lambda jsonRequest:TypeModelsVarsController(jsonRequest)),
              OpID.plot: (lambda jsonRequest:PlotController.plotControllerDict[jsonRequest['pType']](jsonRequest))}

    #TODO add opID for download and mean_median_trend etc.

    def __init__(self, userRequest):
        self.userRequest = userRequest
        self.jsonRequest = userRequest.get_json()
    
    #TODO handle login process on login page.
    # 1. Logging in as authenticated user
    def handle_process_on_loginpage(self, auth_code):

        if self.userRequest.method == 'POST':
            egi_token_url = 'https://aai-dev.egi.eu/oidc/token'
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            data = {'grant_type':'authorization_code', 'code': auth_code,
                    'redirect_uri': 'http://localhost:3000/redirect_url'}##o3web.test.fedcloud.eu
            auth = ('o3webapp', 'LTiU7yqg_GBCZlRjEVpctPOANIGjtzLGPFprIohg7pkOQ-Bl_iDEwjHdz9tBpL6qIiyN37SiJ83oLRrsv-qkpA')
            egi_auth = requests.post(egi_token_url, headers=headers, data=data, auth=auth).json()
            access_token = egi_auth['access_token']

            userinfo_url='https://aai-dev.egi.eu/oidc/userinfo'
            headers = {"Authorization": "Bearer " + access_token}
            egi_userinfo = requests.get(userinfo_url, headers=headers).json()
            username = egi_userinfo['name']
            sub = egi_userinfo['sub']
            return jsonify({'sub': sub, 'name': username})
        else:
            return redirect(url_for('static', filename='plotpage.html'))
        
    # 1. Checking the api_info
    # 2. Updating the list of plot types
    # 3. Updating the info of a specific model
    # 4. Updating the available model list and the required variables of the chosen plot type
    # 5. Plotting the figure according to the chosen plot type and variables for the chosen models
    def handle_process_on_plotpage(self, opID):
        if self.userRequest.method == 'POST':
            return UserManager.opDict[opID](self.jsonRequest).handle_process()
        else:
            return redirect(url_for('static', filename='plotpage.html'))
