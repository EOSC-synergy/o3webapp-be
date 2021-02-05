
from flask import url_for,redirect,request
from controller import APIInfoController,PlotypesController,ModelsInfoController,TypeModelsVarsController,PlotController
# User Manager, which handle all kinds of user requests.
# 1.Arrange the user info and user status, for example authenticated status, user cookies and session
# 2.Handle the requset object received by backend interface

class UserManager:

    def __init__(self, request):
        self.request = request

    def handle_process_on_homepage(self):
        apiInfoController = APIInfoController()
        return apiInfoController.handle_process()
        

    def handle_process_on_plotpage(self, opID):
        if opID == 'api_info':
            apiInfoController = APIInfoController()
            return apiInfoController.handle_process()
        elif opID == 'p_type':
            plotTypeController = PlotypesController()
            return plotTypeController.handel_process()
        elif opID == 'model_info':
            modelsInfoController = ModelsInfoController()
            return modelsInfoController.handel_process()
        elif opID == 't_M_V':
            typeModelsVarsController = TypeModelsVarsController(self.request)
            return typeModelsVarsController.handel_process()
        elif opID == 'plot':
            plotController = PlotController(self.request)
            return plotController.handel_process()
        else:
            return "plot page"


