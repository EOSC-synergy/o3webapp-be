
from flask import request,jsonify
from abc import ABC, abstractmethod

from .plotData import PlotData
from .requestor import APIInfoRequestor,PlotypesRequestor,ModelsInfoRequestor,TypeModelsVarsRequestor,Tco3ZmRequestor,Tco3ReturnRequestor,Vmro3ZmRequestor,InfoUpdateRequestor,PlotDataRequestor
from .requestParser import TypeModelsVarsParser,Tco3ZmParser,Tco3ReturnParser,Vmro3ZmParser, PlotParser
from .plotter import Tco3ZmPlotter, Vmro3ZmPlotter, Tco3ReturnPlotter


# Controller, scheduling the process for handling the user-request. 
# Specific controller handles the request-object with the corresponding operation ID.
# 1. parsing the request-object offered by user-manager into plot-data.                             (plot-process)
# 2. analyzing the generated plot-data within the plot-data-comparer.                               (plot-process)
# 3. querying the info or data from O3as-API through the requestor.
# 4. parsing the response from O3as-API into plot-data or json file.
# 5. merging the plot-data containing the new model-data with old one within the plot-data-merger.  (plot-process)
# 6. passing the merged complete plot-data to the ploter responsible for drawing the figure.        (plot-process)
# 7. responding the resulting plot or file to the user-manager.
class Controller(ABC):
    def __init__(self, jsonRequest):
        self.jsonRequest = jsonRequest
    
    @abstractmethod
    def handle_process(self):
        pass
############################################################
#   Controller requiring info from O3as-API
############################################################
class RemoteController(Controller):
    pass

class InfoUpateController(RemoteController):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        self.infoRequestor = InfoUpdateRequestor()
    
    def handle_process(self):
        return jsonify(self.infoRequestor.request_info())

class APIInfoController(InfoUpateController):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        self.infoRequestor = APIInfoRequestor()
        
class ModelsInfoController(InfoUpateController):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        self.infoRequestor = ModelsInfoRequestor()

class PlotypesController(InfoUpateController):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        self.infoRequestor = PlotypesRequestor()
        
class TypeModelsVarsController(RemoteController):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        self.typeModelsVarsParser = TypeModelsVarsParser()
        self.typeModelsVarsRequestor = TypeModelsVarsRequestor()

    # I: <'pType': 'tco3_zm/vmro3_zm/tco3_return'>
    # O: <<'models': []>, <'vars': []>>
    def handle_process(self):
        typeName = self.typeModelsVarsParser.parse_user_request(self.jsonRequest)
        modelsJson = self.typeModelsVarsRequestor.request_models(typeName)
        completeJson = self.typeModelsVarsRequestor.request_vars()
        varsJson = self.typeModelsVarsParser.parse_varsjson_file(completeJson, typeName)
        #TODO structure of json response to frontend
        return jsonify({'models': modelsJson, 'vars': varsJson})

class PlotController(RemoteController):

    plotControllerDict = {'tco3_zm': (lambda jsonRequest: Tco3ZmController(jsonRequest)),
                          'vmro3_zm': (lambda jsonRequest: Vmro3ZmController(jsonRequest)),
                          'tco3_return': (lambda jsonRequest: Tco3ReturnController(jsonRequest))}

    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        self.plotParser = PlotParser()
        self.plotRequestor = PlotDataRequestor()
        self.plotter = Tco3ZmPlotter()

    def handle_process(self):
        self.plotData = self.plotParser.parse_request_2_plotdata(self.jsonRequest)
        # TODO check plotdata
        #self.plotData.print()
        modelDataJsonFile = self.plotRequestor.request_model_data(self.plotData)
        #print(modelDataJsonFile)
        self.plotParser.parse_json_2_plotdata(modelDataJsonFile, self.plotData)
        return self.plotter.plot_data(self.plotData)

class Tco3ZmController(PlotController):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        self.plotParser = Tco3ZmParser()
        self.plotRequestor = Tco3ZmRequestor()
        self.plotter = Tco3ZmPlotter()

class Tco3ReturnController(PlotController):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        self.plotParser = Tco3ReturnParser()
        self.plotRequestor = Tco3ReturnRequestor()
        self.plotter = Tco3ReturnPlotter()

class Vmro3ZmController(PlotController):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        self.plotParser = Vmro3ZmParser()
        self.plotRequestor = Vmro3ZmRequestor()
        self.plotter = Vmro3ZmPlotter()

############################################################
#   Controller requiring info from local storage
############################################################
class LocalController(Controller):
    pass

class DownloadController(LocalController):
    pass
        
#TODO for mean, median, trend
class StatisticController(LocalController):
    pass
