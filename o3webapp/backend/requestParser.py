import json
import enum
import requests
from plotData import PlotData

# , default as ptype = 1
class RequestIndex(enum.Enum):
   apiRequest = 1
   vmro3_zm = 2
   tco3_return = 3

# Parser, parsing the request-object into info or plotData.
class Parser:
    # TODO enum for index
    def __init__(self, jsonRequest):
        pass
    
############################################################
#   Parser : request-object -> info                        #
############################################################

class InfoParser(Parser):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)

    def parse_info(self):
        # TODO use modelIndex = 1 instead
        return self.jsonRequest[1]['value']

class InfoUpateParser(InfoParser):
    pass

    
class TypeModelsVarsParser(InfoParser):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        # TODO set ptypeIndex = 0 global here
        self.jsonRequest = jsonRequest
        
        

    def parse_user_request(self):
        return self.jsonRequest[0]['value']

    
    # parse response file from o3api 
    # I: <'pType': 'tco3_zm/vmro3_zm/tco3_return'>
    # O: <<'models': []>, <'vars': []>>

    # extract the needed vars from a complete json file in to a json file for a selected plot type 
    def parse_varsjson_file(self, completeJson, typeName):
        ptype = '/plots/' + typeName
        # TODO select items needed for the chosen plot type
        varPattern = lambda para: {'name': para['name'], 'type': para['type']}
        paraArray = lambda completeJson, ptype: completeJson['paths'][ptype]['post']['parameters']
        parameterArray = paraArray(completeJson, ptype)
        return list(map(varPattern, parameterArray))
    

    

    

class DownloadParser(InfoParser):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        # TODO setup index of download format
        self.format = self.jsonRequest[10]['value']
############################################################
#   Parser : request-object -> PlotData
############################################################

class PlotDataParser(Parser):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)

    def parse_plotData(self):
        pass

################# TODO #########################
class PlotParser(PlotDataParser):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        # TODO set ptypeIndex = 0 global here
        self.jsonRequest = jsonRequest
        self.typeName = self.jsonRequest[0]['value']

    def parse_request_2_plotdata(self):
        varData = {}
        for i in range(1,len(self.jsonRequest)):
            key = self.jsonRequest[i]['name']
            value = self.jsonRequest[i]['value']
            varData[key] = value
        return PlotData(self.typeName, varData)

    def fill_json_into_plotdata(plotJsonFlie, plotData):
        
    

class Tco3ZmParser(PlotParser):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        self.plotRequestor = Tco3ZmRequestor()

class Tco3ReturnParser(PlotParser):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        self.plotRequestor = Tco3ReturnRequestor()

class Vmro3ZmParser(PlotParser):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        self.plotRequestor = Vmro3ZmRequestor()

class StatisticParser(PlotDataParser):
    def __init__(self):
        super().__init__()