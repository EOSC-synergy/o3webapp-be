from flask import request,jsonify
from plotData import PlotData
from requestor import APIInfoRequestor,PlotypesRequestor,ModelsInfoRequestor,TypeModelsVarsRequestor,Tco3ZmRequestor,Tco3ReturnRequestor,Vmro3ZmRequestor,PlotDataRequestor
from requestParser import TypeModelsVarsParser,InfoParser,PlotParser,Tco3ZmParser,Tco3ReturnParser,Vmro3ZmParser

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
    def __init__(self):
        super().__init__()
        self.infoRequestor = ModelsInfoRequestor()

class PlotypesController(InfoUpateController):
    def __init__(self):
        super().__init__()
        self.infoRequestor = PlotypesRequestor()
        
class TypeModelsVarsController(RemoteController):
    def __init__(self, jsonRequest):
        super().__init__()
        self.typeModelsVarsParser = TypeModelsVarsParser(jsonRequest)
        self.typeModelsVarsRequestor = TypeModelsVarsRequestor()

    def handle_process(self):
        typeName = self.typeModelsVarsParser.parse_user_request()
        modelsJson = self.typeModelsVarsRequestor.request_models(typeName)
        completeJson = self.typeModelsVarsRequestor.request_vars()
        varsJson = self.typeModelsVarsParser.parse_varsjson_file(completeJson, typeName)
        return jsonify({'models': modelsJson, 'vars': varsJson})

    
class PlotController(RemoteController):
    def __init__(self, jsonRequest):
        super().__init__()
        self.jsonRequest = jsonRequest

    def assign_plot_controller(self):
        typeName = self.plotData.ptype
        if typeName == 'tco3_zm':
            return Tco3ZmController(self.jsonRequest)
        elif typeName == 'vmro3_zm':
            return Vmro3ZmController(self.jsonRequest)
        elif typeName == 'tco3_return':
            return Tco3ReturnController(self.jsonRequest)
        else:
            return Tco3ZmController(self.jsonRequest)
    
    def handle_process(self):
        assignedController = self.assign_plot_controller()
        return jsonify(assignedController.handle_plot_process())

    def handle_plot_process(self):
        self.plotData = self.plotParser.parse_request_2_plotdata()
        plotJsonFile = self.plotDataRequestor.request_model_data(self.plotData)
        #TODO main process for plotdata structure and fill it
        return jsonify(plotJsonFile)

class Tco3ZmController(PlotController):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        self.plotRequestor = Tco3ZmRequestor()
        self.plotParser = Tco3ZmParser(self.jsonRequest)

class Tco3ReturnController(PlotController):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        self.plotRequestor = Tco3ReturnRequestor()
        self.plotParser = Tco3ReturnParser(self.jsonRequest)

class Vmro3ZmController(PlotController):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        self.plotRequestor = Vmro3ZmRequestor()
        self.plotParser = Vmro3ZmParser(self.jsonRequest)

############################################################
#   Controller requiring info from local storage
############################################################
class LocalController(Controller):
    def __init__(self, ):
        super().__init__()

class DownloadController(LocalController):
    def __init__(self, jsonRequest):
        super().__init__()
        
class StatisticController(LocalController):
    def __init__(self, jsonRequest):
        super().__init__()