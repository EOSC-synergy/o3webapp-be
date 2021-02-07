import requests
import json

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
    def __init__(self):
        super().__init__()
        
    def request_model_data(self, plotData):
        self.plotData = plotData
        self.url += 'plots/' + self.plotData.get_ptype_name()
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.varDict = self.plotData.get_vardata_dict()
        r = requests.post(self.url, headers=self.headers, params=self.varDict)
        return r.json()
    
class Tco3ZmRequestor(PlotDataRequestor):
    def __init__(self):
        super().__init__()

class Tco3ReturnRequestor(PlotDataRequestor):
    def __init__(self):
        super().__init__()

class Vmro3ZmRequestor(PlotDataRequestor):
    def __init__(self):
        super().__init__()