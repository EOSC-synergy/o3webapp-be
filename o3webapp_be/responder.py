from flask import Response, send_from_directory, send_file, jsonify
import json
import pandas as pd
from abc import ABC, abstractmethod
# bokeh io
from bokeh.plotting import output_file, show # TODO test in local page
from bokeh.io import export_png, export_svgs
from bokeh.embed import json_item, file_html
from selenium import webdriver
#from PIL import Image
import cairosvg
from io import BytesIO
import os
import tempfile

from o3webapp_be.plotData import PlotData, PlotType, OutputFormat


####################################################
#version: V1.0
#author: Boyan zhong
#className: Responder
#packageName: static
#description: 
####################################################
#Responder, who takes care of the format for the response back to the frontend.

class Responder(ABC):
    
    @abstractmethod
    def respond_data(self, data, plotdata):
        pass
    
############################################################
#   Responder : info from remote o3api forwarded           #
############################################################

class InfoResponder(Responder):
    
    def respond_data(self, data, plotdata):
        return self.respond_info(data)

    def respond_info(self, info):
        return jsonify(info)

class InfoUpateResponder(InfoResponder):
    pass

class ModelInfoResponder(InfoResponder):
    pass

class TypeModelsVarsResponder(InfoResponder):

    def respond_info(self, modelsAndVars):
        response = {'models': modelsAndVars[0], 'vars': modelsAndVars[1]}
        return jsonify(response)
    
############################################################
#   Responder : plot from local plotter formatted          #
############################################################

class PlotDataResponder(Responder):
    
    outputFormatDict = {OutputFormat.csv: (lambda pType: CSVDownloadResponder.pTypeDict[pType]()),
                        OutputFormat.pdf: (lambda pType: PDFDownloadResponder()),
                        OutputFormat.svg: (lambda pType: SVGDownloadResponder()),
                        OutputFormat.png: (lambda pType: PNGDownloadResponder()),
                        OutputFormat.json: (lambda pType:PlotResponder())}

    def respond_data(self, data, plotdata):
        self.plotdata=plotdata
        return self.respond_plot(data, plotdata)

    def respond_plot(self, data, plotdata):
        self.output = self.plotdata.get_output()
        self.pType = self.plotdata.get_ptype()
        dataPlot = data["plot"]
        if self.output == OutputFormat.json:
            dataPlot = data["layout"]# TODO data
        return PlotDataResponder.outputFormatDict[self.output](self.pType).respond_plot(dataPlot, plotdata)

class PlotResponder(PlotDataResponder):

    def respond_plot(self, layout, plotdata):
        #output_file(os.getenv('PLOT_FOLDER')+'o3as_plot.html')
        #show(layout)
        data = json.dumps(json_item(layout))
        return Response(data, mimetype='application/json')

class DownloadResponder(PlotDataResponder):

    folder_path = os.getenv('PLOT_FOLDER')

    #def __init__(self):
        #options = webdriver.ChromeOptions()
        #options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #    pass

    def respond_plot(self, plot, plotdata):
        pass

class CSVDownloadResponder(DownloadResponder):
    
    pTypeDict = {PlotType.tco3_zm: (lambda : ZmCSVDownloadResponder()),
                PlotType.vmro3_zm: (lambda : ZmCSVDownloadResponder()),
                PlotType.tco3_return: (lambda : ReturnCSVDownloadResponder())}

    def build_models_dict(self, plotdata):
        pass

    def respond_plot(self, plot, plotdata):
        #modelDict = self.build_models_dict(plotdata)
        #with open(folder_path/'csv/plot.csv', 'w', newline='') as csvfile:
        #    writer = csv.writer(csvfile, delimiter = ' ')
        #    for name, model in modelDict.items():
        #        writer.writerow(model)

        df = pd.DataFrame(self.build_models_dict(plotdata))
        df.to_csv(self.folder_path+'csv/plot.csv', encoding='utf-8', index=False)

        #df = pd.DataFrame(self.build_models_dict(plotdata))
        #dfbuffer = StringIO()
        #df.to_csv(dfbuffer, encoding='utf-8', index=False)
        #dfbuffer.seek(0)
        #data = dfbuffer.getvalue()
        #return Response(data, mimetype="text/csv",
        #                headers={"Content-Disposition": "attachment;filename={}".format("plot.csv")})
        #return send_from_directory(folder_path+'csv/', "plot.csv", as_attachment = True)
        file_to_be_sent = open(self.folder_path+'csv/plot.csv','rb')
        return send_file(file_to_be_sent, attachment_filename="plot.csv", as_attachment = True)
        
class ZmCSVDownloadResponder(CSVDownloadResponder):
    
    def build_models_dict(self, plotdata):
        modelsDict = {}

        varData = plotdata.get_vardata_dict()
        year_begin = varData['begin']
        year_end = varData['end']
        month = varData['month']
        lat_min = varData['lat_min']
        lat_max = varData['lat_max']
        varPara = '    year_begin: '+year_begin+', year_end: '+year_end+', lat_min: '+lat_min+', lat_max: '+lat_max+', month: '+month.__str__()

        #modelsDict['year_end'] = varData['end']
        #modelsDict['month'] = varData['month']
        #modelsDict['lat_min'] = varData['lat_min']
        #modelsDict['lat_max'] = varData['lat_max']

        modelList = plotdata.get_modeldata_list()
        firstModelData = modelList[0].get_val_cds()
        modelsDict['           Time          '] = firstModelData['x']
        for model in modelList:
            modelName = model.get_name()
            modelData = model.get_val_cds()
            modelsDict[modelName] = modelData['y']

        modelsDict[varPara] = ''
        return modelsDict
        
class ReturnCSVDownloadResponder(CSVDownloadResponder):
    
    def build_models_dict(self, plotdata):
        pass

class PDFDownloadResponder(DownloadResponder):
    
    def respond_plot(self, plot, plotdata):
        plot.background_fill_color = None
        plot.border_fill_color = None
        plot.output_backend = "svg"

        buffer_plot = BytesIO()  # store in IO buffer, not a file        
        with tempfile.NamedTemporaryFile(suffix='.svg') as temp:
            print("TMP FILE:", temp.name, temp)
            svg = export_svgs(plot, filename=temp.name)
            cairosvg.svg2pdf(url=temp.name, write_to=buffer_plot)
            #image = Image.open(temp.name)
            #pdf = image.convert('RGB')
            #pdf.save(buffer_plot, 'pdf')
            #pdf.close()
            buffer_plot.seek(0)
            return send_file(buffer_plot,
                             as_attachment=True,
                             attachment_filename="plot.pdf",
                             mimetype='application/pdf')

class SVGDownloadResponder(DownloadResponder):
    
    def respond_plot(self, plot, plotdata):
        plot.background_fill_color = None
        plot.border_fill_color = None
        plot.output_backend = "svg"
        data = export_svgs(plot, filename=self.folder_path/"svg/plot.svg")
        #return Response(data, mimetype="image/svg+xml",
        #                headers={"Content-Disposition": "attachment;filename={}".format("plot.svg")})
        return send_from_directory(self.folder_path/'svg/', "plot.svg", as_attachment = True)

class PNGDownloadResponder(DownloadResponder):
    
    def respond_plot(self, plot, plotdata):
        plot.background_fill_color = None
        plot.border_fill_color = None
        data = export_png(plot, filename=self.folder_path/"png/plot.png")
        #return Response(data, mimetype="image/png",
        #                headers={"Content-Disposition": "attachment;filename={}".format("plot.png")})
        return send_from_directory(self.folder_path/'png/', "plot.png", as_attachment = True)

class JSONDownloadResponder(DownloadResponder):
    
    def respond_plot(self, plot, plotdata):
        data = json.dumps(json_item(plot))
        return Response(data, mimetype='application/json')
