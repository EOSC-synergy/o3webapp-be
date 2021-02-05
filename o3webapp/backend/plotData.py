import enum

# three plot types, default as tco3_zm = 1
class PlotType(enum.Enum):
   tco3_zm = 1
   vmro3_zm = 2
   tco3_return = 3

# PlotData, containing the var-data and model-data.
class PlotData:
    def __init__(self):
        self.ptype = PlotType[1]
        self.varData = VarData({})
        self.modelList = Data()

    def __init__(self, ptype, varData):
        self.ptype = PlotType[ptype]
        self.varData = VarData(varData)
        self.modelList = Data()


    def get_ptype_name(self):
        return self.ptype.name

    def get_vardata_dict(self):
        return self.varData.get_vardata_dict()
    
    def print(self):
        print(self.ptype)
        self.varData.print()
        self.modelList.print()

class VarData:
    def __init__(self, varDataDict):
        self.varDataDict = varDataDict

    def get_vardata_dict(self):
        return self.varDataDict

    def print(self):
        print(self.varDataDict)

class Data:
    def __init__(self):
        self.modelList = {'model': []}

    def set_model(self, model):
        pass # self.modelList['model'] + model

    def print(self):
        print(self.modelList)

class Model:
    def __init__(self):
        pass

