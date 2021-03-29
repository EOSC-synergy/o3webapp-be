
# Exceptions in backend: 
# Specific exceptions for the corresponding operation processes.

##################################
# Exception for login
##################################
class LoginException(Exception):
    def __init__(self, eType):
        self.eType = eType
    
    def __str__(self):
        if self.eType == 1:
            return "Empty auth_code!"
        else:
            return "Fail to login!"

##################################
# Exception for OpID.api_info
##################################
class APIInfoException(Exception):
    def __init__(self, jsonRequest):
        pass
    
    def __str__(self):
        pass

class APIInfoRequestorException(APIInfoException):
    def __init__(self, jsonRequest):
        pass
    
    def __str__(self):
        pass

##################################
# Exception for OpID.p_type
##################################
class PlotypesException(Exception):
    def __init__(self, jsonRequest):
        pass
    
    def __str__(self):
        pass

class PlotypesRequestorException(PlotypesException):
    def __init__(self, jsonRequest):
        pass
    
    def __str__(self):
        pass

##################################
# Exception for OpID.models_info
##################################
class ModelsInfoException(Exception):
    def __init__(self, jsonRequest):
        pass
    
    def __str__(self):
        pass

class ModelsInfoRequestorException(ModelsInfoException):
    def __init__(self, jsonRequest):
        pass
    
    def __str__(self):
        pass

##################################
# Exception for OpID.t_M_V
##################################
class TypeModelsVarsException(Exception):
    def __init__(self, jsonRequest):
        pass
    
    def __str__(self):
        pass

class TypeModelsVarsParserException(TypeModelsVarsException):
    def __init__(self, wrongPType):
        self.wrongPType = wrongPType

    def __str__(self):
        return "Wrong pType: " + self.wrongPType

class TypeModelsVarsRequestorException(TypeModelsVarsException):
    def __init__(self, jsonRequest):
        pass
    
    def __str__(self):
        pass

##################################
# Exception for OpID.plot
##################################
class PlotException(Exception):
    def __init__(self, jsonRequest):
        pass
    
    def __str__(self):
        pass

class PlotParserException(PlotException):
    def __init__(self, jsonRequest):
        pass
    
    def __str__(self):
        pass

class PlotDataRequestorException(PlotException):
    def __init__(self, jsonRequest):
        pass
    
    def __str__(self):
        pass

class PlotterException(PlotException):
    def __init__(self, jsonRequest):
        pass
    
    def __str__(self):
        pass
