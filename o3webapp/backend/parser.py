import json
import enum

# , default as ptype = 1
class RequestIndex(enum.Enum):
   apiRequest = 1
   vmro3_zm = 2
   tco3_return = 3

# Parser, parsing the request-object into info or plotData.
class Parser:
    # TODO enum for index
    def __init__(self, jsonRequest):
        
    
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

    
class TypeModelsVarsParser(InfoParser):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        # TODO set ptypeIndex = 0 global here
        
        self.typeName = jsonRequest[0]['value']

    def parse_user_request_vars(self):
        return self.typeName

    

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

class PlotParser(PlotDataParser):
    def __init__(self, jsonRequest):
        super().__init__(jsonRequest)
        # TODO set ptypeIndex = 0 global here
        self.typeName = self.jsonRequest[0]['value']

    def parse_request_2_plotdata(self):
        varData = {}
        for i in range(1,len(self.jsonRequest)):
            key = self.jsonRequest[i]['name']
            value = self.jsonRequest[i]['value']
            varData[key] = value

        return PlotData(self.typeName, varData)

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