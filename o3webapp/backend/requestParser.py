import json
import enum
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
        self.jsonRequest = jsonRequest

    def parse_user_request(self):
        # TODO set ptypeIndex = 0 global here
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
        self.jsonRequest = jsonRequest
        # TODO set ptypeIndex = 0 global here
        self.typeName = self.jsonRequest['pType']

    def parse_ptype(self):
        return self.typeName

    def parse_request_2_plotdata(self):
        varData = self.jsonRequest
        del varData['pType']
        # TODO only one model can be parsed for now
        #for i in range(1,len(self.jsonRequest)):
        #    key = self.jsonRequest[i]['name']
        #    value = self.jsonRequest[i]['value']
        #    varData[key] = value
        plotdata = PlotData(self.typeName, varData)
        return plotdata

    def parse_json_2_plotdata(self, modelDataJsonFile, plotdata):
        plotdata.get_modeldata().set_val_in_modelDict(modelDataJsonFile)

class Tco3ZmParser(PlotParser):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)

class Tco3ReturnParser(PlotParser):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)

class Vmro3ZmParser(PlotParser):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)

class StatisticParser(PlotDataParser):
    def __init__(self):
        super().__init__()