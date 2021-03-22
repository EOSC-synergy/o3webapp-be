from flask import url_for,redirect,request
from .controller import APIInfoController,PlotypesController,ModelsInfoController,TypeModelsVarsController,PlotController

# User Manager, which handles all kinds of user requests :
# 1. Arranging the user info and user status, 
#    for example authenticated status, user cookies and sessions.
# 2. Handling the request-object received by backend interface,
#    choosing specific controller to handle the request corresponding to the operation ID,
#    extracting the json form from the request-object and feeding it to the controller.

class UserManager:

    opDict = {'api_info': (lambda jsonRequest: APIInfoController(jsonRequest)),
              'p_type': (lambda jsonRequest: PlotypesController(jsonRequest)),
              'models_info': (lambda jsonRequest: ModelsInfoController(jsonRequest)),
              't_M_V': (lambda jsonRequest:TypeModelsVarsController(jsonRequest)),
              'plot': (lambda jsonRequest:PlotController.plotControllerDict[jsonRequest['pType']](jsonRequest))}

              
    #TODO add opID for download and mean_median_trend etc.

    def __init__(self, userRequest):
        self.userRequest = userRequest
        self.jsonRequest = userRequest.get_json()
    
    #TODO handle process on corresponding pages.

    # 1. Checking the api_info
    # 2. Logging in as authenticated user
    def handle_process_on_homepage(self):
        if self.userRequest.method == 'GET':
            return UserManager.opDict['api_info'](self.jsonRequest).handle_process()
        else:
            return redirect(url_for('static', filename='plotpage.html'))
        
    # 1. Checking the api_info
    # 2. Updating the list of plot types
    # 3. Updating the info of a specific model
    # 4. Updating the available model list and the required variables of the chosen plot type
    # 5. Plotting the figure according to the chosen plot type and variables for the chosen models
    ## TODO temporarily add parameter: format
    def handle_process_on_plotpage(self, opID, format):
        if self.userRequest.method == 'POST':
            self.jsonRequest["output"] = format ## TODO
            return UserManager.opDict[opID](self.jsonRequest).handle_process()
        else:
            return redirect(url_for('static', filename='plotpage.html'))
