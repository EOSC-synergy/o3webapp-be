import requests
import json

from plotData import PlotData

# Requestor, querying the info or data from O3as-API.
class Requestor:
    def __init__(self):
        self.url = 'http://o3api.test.fedcloud.eu:30509/api/'
    
    def print_url_request(self):
        return self.url

class InfoUpdateRequestor(Requestor):
    def __init__(self):
        super().__init__()
        
    def request_info(self):
        r = requests.get(self.url)
        return r.json()

class APIInfoRequestor(InfoUpdateRequestor):
    def __init__(self):
        super().__init__()
        self.url += 'api-info'
    
class ModelsInfoRequestor(InfoUpdateRequestor):
    def __init__(self):
        super().__init__()
        self.url += 'models'

class PlotypesRequestor(InfoUpdateRequestor):
    def __init__(self):
        super().__init__()
        self.url += 'plots'

class TypeModelsVarsRequestor(Requestor):
    def __init__(self):
        super().__init__()
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def request_models(self, typeName):
        typeModelsUrl = self.url + 'models/list/' + typeName
        r = requests.post(typeModelsUrl, headers=self.headers)
        return r.json()

    def request_vars(self):
        typeVarsUrl = self.url + 'swagger.json'
        return requests.get(typeVarsUrl).json()

class PlotDataRequestor(Requestor):
        
    def request_model_data(self, plotData):
        self.plotData = plotData
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.params = self.prepare_params()
        self.url += 'plots/' + self.plotData.get_ptype_name() + "?" + self.params 
        r = requests.post(self.url, headers=self.headers)
        return r.json()

    def prepare_params(self):
        varDict = self.plotData.get_vardata_dict()
        varDict["model"]=self.merge_array(varDict["model"])
        varDict["month"]=self.merge_array(varDict["month"])
        varStr = self.merge_dict(varDict)
        return varStr
    
    def merge_dict(self, dict):
        separator = "&"
        equal = "="
        elementsStr = ""
        for k,v in dict.items():
            elementsStr += k + equal + v + separator
        elementsStr = elementsStr[:-len(separator)]
        return elementsStr

    def merge_array(self, array):
        separator = "%2C"
        elementsStr = ""
        for element in array:
            elementsStr += element + separator
        elementsStr = elementsStr[:-len(separator)]
        return elementsStr
    
class Tco3ZmRequestor(PlotDataRequestor):
    pass

class Tco3ReturnRequestor(PlotDataRequestor):
    pass

class Vmro3ZmRequestor(PlotDataRequestor):
    pass
