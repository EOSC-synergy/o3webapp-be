import enum

# three plot types, default as tco3_zm = 1
class PlotType(enum.Enum):
   tco3_zm = 1
   vmro3_zm = 2
   tco3_return = 3

####################################################
# PlotData :
# --ptype
# --varData
# --modelData
####################################################
class PlotData:
    def __init__(self):
        self.ptype = PlotType[1]
        self.varData = VarData({})
        self.modelData = Data()

    def __init__(self, ptype, varData):
        self.ptype = PlotType[ptype]
        self.varData = VarData(varData)
        self.modelData = Data()

    def get_ptype_name(self):
        return self.ptype.name

    def get_vardata_dict(self):
        return self.varData.get_dict()
    
    def get_modeldata_dict(self):
        return self.modelData.get_dict()

    def print(self):
        print(self.ptype)
        self.varData.print()
        self.modelData.print()

class VarData:
    def __init__(self, varDataDict):
        self.varDataDict = varDataDict

    def get_dict(self):
        return self.varDataDict

    def print(self):
        print(self.varDataDict)

class Data:
    def __init__(self):
        self.modelDict = {}

    def get_dict(self):
        return self.modelDict

    def add_model(self, model):
        modelName = model.get_name()
        self.modelDict[modelName] = model

    # TODO set value of models
    def set_val_in_model(self, modelName, modelVal):
        model = self.modelDict[modelName]
        model.set_valDict(modelVal)

    # TODO set parameter of models
    def set_para(self):
        pass

    def print(self):
        print(self.modelDict)

#################################################
# climate model : 
# --vals : [coordX, coordY]
#          {val1X : val1Y,
#           val2X : val2Y, ...}
# --paras :
#################################################
class Model:
    def __init__(self, modelName):
        self.name = modelName
        self.val = ModelVal()
        self.para = ModelPara()

    def __init__(self, modelName, coordX, coordY):
        self.name = modelName
        self.val = ModelVal(coordX, coordY)
        self.para = ModelPara()

    def get_name(self):
        return self.name

    def get_val(self):
        return self.val

    def get_para(self):
        return self.para

    def set_valDict(self, valDict):
        self.val.set_dict(valDict)
        
class ModelVal:
    def __init__(self):
        self.valCoord = ["x", "y"]
        self.valDict = {}

    def __init__(self, coordX, coordY):
        self.valCoord = [coordX, coordY]
        self.valDict = {}

    def get_coord(self):
        return self.valCoord

    def get_dict(self):
        return self.valDict

    def get_valY(self, valX):
        return self.valDict[valX]

    def set_dict(self, valDict):
        self.valDict = valDict

    def set_val(self, valX, valY):
        self.valDict[valX] = valY
                
class ModelPara:
    def __init__(self):
        pass