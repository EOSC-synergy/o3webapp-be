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
    def __init__(self, typeName):
        super().__init__()
        self.typeName = typeName
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def request_models(self):
        typeModelsUrl = self.url + 'models/list/' + self.typeName
        r = requests.post(typeModelsUrl, headers=self.headers)
        return r.json()

    def request_vars(self):
        typeVarsUrl = self.url + 'swagger.json'
        r = requests.get(typeVarsUrl)
        return self.extract_vars4ptype(r.json())

    def extract_vars4ptype(self, completeJson):
        ptype = '/plots/' + self.typeName
        parameterArray = completeJson['paths'][ptype]['post']['parameters']
        # TODO select items needed for the chosen plot type
        return list(map(lambda para: {'name': para['name'], 'type': para['type']}, parameterArray))


class ModelDataRequestor(Requestor):
    def __init__(self):
        super().__init__()
        
        
    def request_model_data(self, plotData):
        self.plotData = plotData
        self.url += 'plots/' + self.plotData.get_ptype_name()
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.varDict = self.plotData.get_vardata_dict()
        r = requests.post(self.url, headers=self.headers, params=self.varDict)
        return r.json()
    


class Tco3ZmRequestor(ModelDataRequestor):
    def __init__(self):
        super().__init__()

class Tco3ReturnRequestor(ModelDataRequestor):
    def __init__(self):
        super().__init__()

class Vmro3ZmRequestor(ModelDataRequestor):
    def __init__(self):
        super().__init__()