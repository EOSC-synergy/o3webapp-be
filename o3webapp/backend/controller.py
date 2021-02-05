from flask import request,jsonify
from plotData import PlotData
from requestor import APIInfoRequestor,PlotypesRequestor,ModelsInfoRequestor,TypeModelsVarsRequestor,Tco3ZmRequestor,Tco3ReturnRequestor,Vmro3ZmRequestor

# Controller, scheduling the process for handling the user-request. 
# Specific controller handles the request-object with the corresponding operation ID.
# 1. parsing the request-object offered by user-manager into plot-data.                             (plot-process)
# 2. analyzing the generated plot-data within the plot-data-comparer.                               (plot-process)
# 3. querying the info or data from O3as-API through the requestor.
# 4. parsing the response from O3as-API into plot-data or json file.
# 5. merging the plot-data containing the new model-data with old one within the plot-data-merger.  (plot-process)
# 6. passing the merged complete plot-data to the ploter responsible for drawing the figure.        (plot-process)
# 7. responding the resulting plot or file to the user-manager.
class Controller:
    def __init__(self):
        pass
    
    def handle_process(self):
        pass
############################################################
#   Controller requiring info from O3as-API
############################################################
class RemoteController(Controller):
    def __init__(self):
        super().__init__()

class InfoUpateController(RemoteController):

    def handle_process(self):
        return jsonify(self.infoRequestor.request_info())

class APIInfoController(InfoUpateController):
    def __init__(self):
        super().__init__()
        self.infoRequestor = APIInfoRequestor()
        
class ModelsInfoController(InfoUpateController):
    def __init__(self, userRequest):
        super().__init__()
        self.jsonRequest = userRequest.get_json()
        self.modelName = self.jsonRequest[1]['value']
        self.infoRequestor = ModelsInfoRequestor(self.modelName)

class PlotypesController(InfoUpateController):
    def __init__(self):
        super().__init__()
        self.infoRequestor = PlotypesRequestor()
        
class TypeModelsVarsController(RemoteController):
    def __init__(self, userRequest):
        super().__init__()
        self.jsonRequest = userRequest.get_json()
        self.typeName = self.jsonRequest[0]['value']
        self.typeModelsVarsRequestor = TypeModelsVarsRequestor(self.typeName)

    def handle_process(self):
        return jsonify(self.request_models_vars())

    # I: <'pType': 'tco3_zm/vmro3_zm/tco3_return'>
    # O: <<'models': []>, <'vars': []>>
    def request_models_vars(self):
        return {'models': self.request_models() , 'vars': self.request_vars()}

    def request_models(self):
        return self.typeModelsVarsRequestor.request_models()
        
    def request_vars(self):
        return self.typeModelsVarsRequestor.request_vars()

class PlotController(RemoteController):
    def __init__(self, request):
        super().__init__()
        self.userRequest = request
        self.jsonRequest = self.userRequest.get_json()
        self.typeName = self.jsonRequest[0]['value']

    def assign_plot_controller(self):
        if self.typeName == 'tco3_zm':
            return Tco3ZmController(self.userRequest)
        elif self.typeName == 'vmro3_zm':
            return Vmro3ZmController(self.userRequest)
        elif self.typeName == 'tco3_return':
            return Tco3ReturnController(self.userRequest)
        else:
            return 'plot type does not exist!'
    
    def handle_process(self):
        assignedController = self.assign_plot_controller()
        return jsonify(assignedController.handle_plot_process())

    def handle_plot_process(self):
        self.parse_request_2_plotdata()
        return self.plotRequestor.request_model_data(self.plotData)

    def parse_request_2_plotdata(self):
        varData = {}
        for i in range(1,len(self.jsonRequest)):
            key = self.jsonRequest[i]['name']
            value = self.jsonRequest[i]['value']
            varData[key] = value

        self.plotData = PlotData(self.typeName, varData)

class Tco3ZmController(PlotController):
    def __init__(self, request):
        super().__init__(request)
        self.plotRequestor = Tco3ZmRequestor()

class Tco3ReturnController(PlotController):
    def __init__(self, request):
        super().__init__(request)
        self.plotRequestor = Tco3ReturnRequestor()

class Vmro3ZmController(PlotController):
    def __init__(self, request):
        super().__init__(request)
        self.plotRequestor = Vmro3ZmRequestor()

############################################################
#   Controller requiring info from local storage
############################################################
class LocalController(Controller):
    def __init__(self):
        super().__init__()