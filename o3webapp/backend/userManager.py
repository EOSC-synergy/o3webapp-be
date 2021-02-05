
from flask import url_for,redirect,request
from controller import APIInfoController,PlotypesController,ModelsInfoController,TypeModelsVarsController,PlotController

# User Manager, which handles all kinds of user requests :
# 1. Arranging the user info and user status, for example authenticated status, user cookies and sessions.
# 2. Handling the requset-object received by backend interface

class UserManager:

    def __init__(self, request):
        self.request = request

    # 1. Checking the api_info
    # 2. Logging in as authenticated user
    def handle_process_on_homepage(self):
        if self.request.method == 'GET':
            apiInfoController = APIInfoController()
            return apiInfoController.handle_process()
        else:
            return redirect(url_for('static', filename='plotpage.html'))
        
    # 1. Checking the api_info
    # 2. Updating the list of plot types
    # 3. Updating the info of a specific model
    # 4. Updating the available model list and the required variables of the chosen plot type
    # 5. Plotting the figure according to the chosen plot type and variables for the chosen models
    def handle_process_on_plotpage(self, opID):
        if request.method == 'POST':
            if opID == 'api_info':
                apiInfoController = APIInfoController()
                return apiInfoController.handle_process()
            elif opID == 'p_type':
                plotTypeController = PlotypesController()
                return plotTypeController.handle_process()
            elif opID == 'model_info':
                modelsInfoController = ModelsInfoController(self.request)
                return modelsInfoController.handle_process()
            elif opID == 't_M_V':
                typeModelsVarsController = TypeModelsVarsController(self.request)
                return typeModelsVarsController.handle_process()
            elif opID == 'plot':
                plotController = PlotController(self.request)
                return plotController.handle_process()
            else:
                return "plot page"
        else:
            return redirect(url_for('static', filename='plotpage.html'))


