import json
import enum

from o3webapp_be.plotData import PlotData, PlotType
from o3webapp_be.backendException import TypeModelsVarsParserException
####################################################
#version: V1.0
#author: Boyan zhong
#className: requestParser
#packageName: static
#description: 
####################################################
#Parser, parsing the request-object into info or plotData.
class Parser:
    pass
    
############################################################
#   Parser : request-object -> info                        #
############################################################

class InfoParser(Parser):
    pass

class InfoUpateParser(InfoParser):
    pass

class TypeModelsVarsParser(InfoParser):

    def parse_user_request(self, jsonRequest):
        ptype = jsonRequest['pType']
        if ptype in PlotType.__members__:
            return ptype
        else:
            raise TypeModelsVarsParserException(ptype)
    
    # parse response file from o3api 
    # extract the needed vars from a complete json file in to a json file for a selected plot type 
    def parse_varsjson_file(self, completeJson, typeName):
        ptype = '/plots/' + typeName
        # TODO select items needed for the chosen plot type
        varPattern = lambda para: {'name': para['name'], 'type': para['type']}
        paraArray = lambda completeJson, ptype: completeJson['paths'][ptype]['post']['parameters']
        parameterArray = paraArray(completeJson, ptype)
        return list(map(varPattern, parameterArray))
    
############################################################
#   Parser : request-object -> PlotData
############################################################

class PlotDataParser(Parser):
    pass

class PlotParser(PlotDataParser):

    def parse_ptype(self, jsonRequest):
        return jsonRequest['pType']

    def parse_request_2_plotdata(self, jsonRequest):
        varData = jsonRequest
        typeName = varData['pType']
        del varData['pType']
        output = varData['output']
        del varData['output']
        plotdata = PlotData(typeName, varData, output)
        return plotdata

    def parse_json_2_plotdata(self, modelDataJsonFile, plotdata):
        plotdata.get_modeldata().set_val_in_modelDict(modelDataJsonFile)

class Tco3ZmParser(PlotParser):
    pass

class Tco3ReturnParser(PlotParser):
    pass

class Vmro3ZmParser(PlotParser):
    pass

