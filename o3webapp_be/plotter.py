from flask import url_for, redirect, Response, send_from_directory
import json
from math import pi
import numpy as np
from scipy import signal
from abc import ABC, abstractmethod

# bokeh plot
from bokeh.core.properties import String, Instance
import pandas as pd
from pandas import Series, DataFrame
from datetime import datetime as dt
from bokeh.models import ColumnDataSource, Legend, LegendItem, CustomJS, ColorPicker
from bokeh.models import DatetimeTickFormatter, FuncTickFormatter, PrintfTickFormatter, NumeralTickFormatter
from bokeh.models import Button, Panel, Tabs, RadioButtonGroup, Div, Slider, TextInput
from bokeh.layouts import column, row, WidgetBox, widgetbox
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.events import ButtonClick, Tap
from bokeh.palettes import Spectral11, Category20
from bokeh.models.tickers import AdaptiveTicker, CompositeTicker, YearsTicker, MonthsTicker, DaysTicker
from bokeh.models.tools import HoverTool
# bokeh io
from bokeh.io import show, output, export_png, export_svgs
from PIL import Image
from bokeh.embed import json_item, file_html
from bokeh.resources import CDN
from io import StringIO
from selenium import webdriver
import csv
from pathlib import Path
import os

from o3webapp_be.plotData import PlotData, PlotType, OutputFormat

####################################################
#version: V1.0
#author: Danni Bao ,Jingling He
#className: Plotter
#packageName: static
#description: 
####################################################
# Plotter,
# plotting the data stored within the plotData
# considering the parameter for variables and legends.

class Plotter(ABC):

    @abstractmethod
    def plot_data(self, plotdata):
        pass

    def init_plotter(self, plotdata):
        self.modelDict = plotdata.get_modeldata_dict()
        for name, model in self.modelDict.items():
            data = model.get_val_cds()
            df = pd.DataFrame(data=data)
            df['x'] = pd.to_datetime(df['x'])
            modelDict = {'x': df['x'], 'y': df['y']}
            cdsModel = ColumnDataSource(data=modelDict)
            model.reset_val_cds(cdsModel)
        self.nameModelDict = plotdata.get_name_model_dict()
        self.modelList = plotdata.get_modeldata_list()
        self.modelNum = plotdata.get_modeldata_num()
        self.plotType = plotdata.get_ptype()
        self.output = plotdata.get_output()

    @abstractmethod
    def build_models_dict(self):
        pass

    # TODO implemented in Responder, who takes care of the format of the output.
    def do_export(self, layout, plot):
        folder_path = Path(os.getenv('PLOT_FOLDER'))
        print(self.output)
        #options = webdriver.ChromeOptions()
        #options.add_experimental_option('excludeSwitches', ['enable-logging'])
        if self.output == OutputFormat["csv"]:
            #modelDict = self.build_models_dict()
            #with open(folder_path/'csv/plot.csv', 'w', newline='') as csvfile:
            #    writer = csv.writer(csvfile, delimiter = ' ')
            #    for name, model in modelDict.items():
            #        writer.writerow(model)

            df = pd.DataFrame(self.build_models_dict())
            df.to_csv(folder_path/'csv/plot.csv', encoding='utf-8', index=False)

            #df = pd.DataFrame(self.build_models_dict())
            #dfbuffer = StringIO()
            #df.to_csv(dfbuffer, encoding='utf-8', index=False)
            #dfbuffer.seek(0)
            #data = dfbuffer.getvalue()
            #return Response(data, mimetype="text/csv",
            #                headers={"Content-Disposition": "attachment;filename={}".format("plot.csv")})
            return send_from_directory(folder_path/'csv/', "plot.csv", as_attachment = True)
        elif self.output == OutputFormat["png"]:
            plot.background_fill_color = None
            plot.border_fill_color = None
            data = export_png(plot, filename=folder_path/"png/plot.png")
            #return Response(data, mimetype="image/png",
            #                headers={"Content-Disposition": "attachment;filename={}".format("plot.png")})
            return send_from_directory(folder_path/'png/', "plot.png", as_attachment = True)
        elif self.output == OutputFormat["svg"]:
            plot.background_fill_color = None
            plot.border_fill_color = None
            plot.output_backend = "svg"
            data = export_svgs(plot, filename=folder_path/"svg/plot.svg")
            #return Response(data, mimetype="image/svg+xml",
            #                headers={"Content-Disposition": "attachment;filename={}".format("plot.svg")})
            return send_from_directory(folder_path/'svg/', "plot.svg", as_attachment = True)
        elif self.output == OutputFormat["pdf"]:
            plot.background_fill_color = None
            plot.border_fill_color = None
            png = export_png(plot, filename=folder_path/"pdf/plot.png")
            image = Image.open(folder_path/"pdf/plot.png")
            pdf = image.convert('RGB')
            pdf.save(folder_path/'pdf/plot.pdf')
            #file = Response(pdf, mimetype="application/pdf",
            #                headers={"Content-Disposition": "attachment;filename={}".format("plot.pdf")})
            return send_from_directory(folder_path/"pdf/", "plot.pdf", as_attachment = True)
        else:
            data = json.dumps(json_item(layout))
            return Response(data, mimetype='application/json')

    def boxcar_easy(self, window, data):
        boxcar = np.ones(window)
        extLen = len(data) + 2 * window
        extData = np.ones(extLen)
        extData[:window] = data[0]
        extData[extLen - window:] = data[len(data) - 1]
        extData[window:extLen - window] = data
        boxcar_extData = signal.convolve(
            extData / np.sum(boxcar), boxcar, mode='same')
        return boxcar_extData[window:extLen - window]

    def boxcar_mirror(self, window, data):
        boxcar = np.ones(window)
        sgnl = np.r_[data[window - 1:0:-1], data, data[-2:-window - 1:-1]]
        boxcar_data = signal.convolve(
            sgnl / np.sum(boxcar), boxcar, mode='same')
        return boxcar_data[window - 1:-(window - 1)]

# Plotter,
# plotting the data in *-zm plot type, time -> messurement,
# whose x axis represents the time.


class ZmPlotter(Plotter):
    mmtLabels = ["mean", "median", "trend"]

    def plot_data(self, plotdata):
        self.init_plotter(plotdata)

        ################### init figure ##############################
        hoverTool = HoverTool(
            tooltips = [
            ("date", "@x{%F}"),
            ("time", "@x{%T}"),
            ("y", "$y"),
            ("name","$name")
            ],
            formatters={'@x': 'datetime'},
            mode = 'mouse'
            )
        
        p = figure(plot_width=1500, plot_height=500,
                   title=self.plotType.name, x_axis_type="datetime")
        p.add_tools(hoverTool)

        # TODO add color , hide and delete button
        ###################  mmt block #####################
        #+----------------+--------------+----------------+#
        #| mmtButtonGroup |  mmtBoxNum   | mmtBoxActivity |#
        #+----------------+--------------+----------------+#
        ####################################################
        #+----------------+----------------+               #
        #|+--boxHeader---+|+--boxHeader---+|               #
        #|| boxTitle     ||| boxTitle     ||               #
        #|| mmtLegendNum ||| mmtLegendNum ||               #
        #|| boxDelete    ||| boxDelete    ||               #
        #|+--------------+|+--------------+|               #
        #|  legend_1      |  legend_1      |               #
        #|  legend_2      |  legend_2      |               #
        #|  ...           |  ...           |               #
        #+----------------+----------------+               #
        ####################################################
        # ROW_2 :: mmt block                                ##################################
        maxBoxNum = 5
        maxLegendNum = 7
        # mmt block header
        mmtButtonGroup = RadioButtonGroup(labels=ZmPlotter.mmtLabels, css_classes = ["mmt_header", "extra-buttons"])
        boxNum = ["number" for i in range(maxBoxNum + 1)]
        boxActivity = ["activity" for i in range(maxBoxNum + 1)]
        mmtBoxNum = RadioButtonGroup(
            labels=boxNum, active=0, tags=[0], visible=False)
        mmtBoxActivity = RadioButtonGroup(
            labels=boxActivity, active=0, visible=False)
        yearRef = Button(
            label="1980 reference", tags=[], css_classes = ["year_reference"], visible=True)
        mmtLegendBlockHead = row(mmtButtonGroup, mmtBoxNum, mmtBoxActivity)
        # mmt box array
        boxHeaderW = 100
        mmtLegendH = 20
        mmtLegendW = 400
        ################# color pickers for all lines ##################
        colorPicker = {}

        ################# plotted_legends : model_legends + plotted_mmt_legends ##########################
        legendLayout = Legend(
            items=[], tags=[i for i in range(maxBoxNum)], location="center")
        ################# mmt_box : model_names #####################################
        mmtLegendBoxArr = self.setup_mmt_legendboxArr(maxBoxNum, maxLegendNum)
        ################# hidden_mmt_legends ##########################
        mmtModelPlotArr = self.plot_mmt(maxBoxNum, p, colorPicker)
        # mmt block
        mmtLegendBlock = column(mmtLegendBlockHead, mmtLegendBoxArr)
        ####################--------------CREATE MMT BOX---------------###############################

        #click mmt_button
        mmtButtonGroup.js_on_click(CustomJS(args=dict(mmtLegendBlock=mmtLegendBlock,
            legendLayout=legendLayout, mmtPlotArr=mmtModelPlotArr['mmtPlotArr'], 
            mmtLabels=ZmPlotter.mmtLabels, height=mmtLegendH, width=boxHeaderW, maxBoxNum=maxBoxNum), 
            code="""
                if(cb_obj.active == 'None') return;
                var blockHeader = (mmtLegendBlock.children)[0].children;
                var curBoxNum = blockHeader[1];
                var activeBox = blockHeader[2];
                var boxArr = (mmtLegendBlock.children)[1].children;
                if(activeBox.active > 0){
                    var oldBoxHeader = (boxArr[activeBox.active-1].children)[0]
                    var oldBoxTitle = (oldBoxHeader.children)[0];
                    oldBoxTitle.button_type = 'default';
                    var oldBoxDel = (oldBoxHeader.children)[2];
                    oldBoxDel.visible = false;
                }
                if(curBoxNum.active < maxBoxNum){
                    activeBox.active = ++curBoxNum.active;
                    var curBoxIndex = activeBox.active-1;
                    var boxHeader = (boxArr[curBoxIndex].children)[0];
                    var boxTitle = boxHeader.children[0];
                    boxTitle.label = mmtLabels[cb_obj.active]+'_'+curBoxNum.tags[0]++;
                    boxTitle.tags[0]=curBoxIndex;
                    boxTitle.tags[1]=cb_obj.active;
                    boxTitle.visible = true;
                    boxTitle.height = height;
                    boxTitle.width = width;
                    boxTitle.button_type = 'success';
                    var mmtLegend = mmtPlotArr[legendLayout.tags[0]];
                    legendLayout.tags.splice(0,1);
                    mmtLegend.label = boxTitle.label;
                    var mmtPlot = mmtLegend.renderers[0];
                    mmtPlot.name = boxTitle.label;
                    mmtPlot.change.emit();
                    var legendNum = legendLayout.items.length;
                    legendLayout.items.splice(legendNum,0,mmtLegend);
                    legendLayout.change.emit();
                    var boxDel = boxHeader.children[2];
                    boxDel.visible = true;
                    boxDel.height = height;
                    boxDel.width = height;
                    boxDel.button_type = 'danger';
                    boxDel.tags[0]=curBoxIndex;
                }else{
                    activeBox.active = 0;
                }
                mmtLegendBlock.change.emit();
                cb_obj.active = 'None';
                """))

        for boxIndex in range(maxBoxNum):
            legendBox = (mmtLegendBoxArr.children)[boxIndex]
            legendArr = legendBox.children
        ####################--------------SELECT/DESELECT MMT BOX---------------###############################
            # Click box_title
            legendBoxTitle = (legendArr[0].children)[0]
            legendBoxTitle.js_on_click(CustomJS(args=dict(mmtLegendBlock=mmtLegendBlock), 
                code="""
                    var blockHeader = (mmtLegendBlock.children)[0].children;
                    var activeBox = blockHeader[2];
                    var boxArr = (mmtLegendBlock.children)[1].children;
                    if(activeBox.active > 0){
                        var oldBoxHeader = (boxArr[activeBox.active-1].children)[0]
                        var oldBoxTitle = (oldBoxHeader.children)[0];
                        oldBoxTitle.button_type = 'default';
                        var oldBoxDel = (oldBoxHeader.children)[2];
                        oldBoxDel.visible = false;
                    }
                    var boxIndex = cb_obj.origin.tags[0];
                    if(activeBox.active != boxIndex + 1){
                        activeBox.active = boxIndex + 1;
                        var boxHeader = (boxArr[boxIndex].children)[0];
                        var boxTitle = (boxHeader.children)[0];
                        boxTitle.button_type = 'success';
                        var boxDel = (boxHeader.children)[2];
                        boxDel.visible = true;
                    }else{
                        activeBox.active = 0;
                    }
                    mmtLegendBlock.change.emit();
                    """))
            
        ####################--------------DELETE MMT BOX---------------###############################
            # Click box_delete
            legendBoxDelete = (legendArr[0].children)[2]
            legendBoxDelete.js_on_click(CustomJS(args=dict(mmtLegendBlock=mmtLegendBlock, 
                legendLayout=legendLayout, modelNum=self.modelNum), code="""
                    var boxIndex = cb_obj.origin.tags[0];
                    //update legend layout
                    var delPos = modelNum + boxIndex;
                    var delMmtPlot = legendLayout.items[delPos]
                    legendLayout.items.splice(delPos,1);
                    var mmtPlot = delMmtPlot.renderers[0];
                    mmtPlot.visible = false;
                    mmtPlot.change.emit();
                    legendLayout.tags.push(delMmtPlot.tags[0]);
                    legendLayout.change.emit();

                    var boxArr = (mmtLegendBlock.children)[1].children;
                    var delBox = boxArr[boxIndex];
                    //update box_index in shifted boxes
                    var j=boxIndex;
                    for (; j<boxArr.length-1; j++){
                        boxArr[j] = boxArr[j+1];
                        // update box j
                        var boxHeader = boxArr[j].children[0];
                        var boxTitle = boxHeader.children[0];
                        boxTitle.tags[0]=j;
                        var boxDel = boxHeader.children[2];
                        boxDel.tags[0]=j;
                        var curLegendNum = boxHeader.children[1].active;
                        for(var i = 1; i <= curLegendNum; i++){
                            boxArr[j].children[i].tags[0]=j;
                        }
                    }
                    boxArr[j] = delBox;
                    //clear last box
                    var delBoxHeader = delBox.children[0];
                    var delBoxTitle = delBoxHeader.children[0];
                    delBoxTitle.label = "";
                    delBoxTitle.tags[0]=j;
                    delBoxTitle.width = 0;
                    delBoxTitle.height = 0;
                    delBoxTitle.visible = false;
                    var delBoxDel = delBoxHeader.children[2];
                    delBoxDel.tags[0]=j;
                    delBoxDel.visible = false;
                    delBoxDel.width = 0;
                    delBoxDel.height = 0;
                    var curLegendNum = delBoxHeader.children[1].active;
                    delBoxHeader.children[1].active = 0;
                    for(var i = 1; i <= curLegendNum; i++){
                        var legend = delBox.children[i];
                        legend.label = "";
                        legend.tags[0]=j;
                        legend.width=0;
                        legend.height=0;
                        legend.visible=false;
                    }
                    //update mmt_block_header
                    var blockHeader = (mmtLegendBlock.children)[0].children;
                    blockHeader[1].active--;
                    blockHeader[2].active = 0;
                    blockHeader.change.emit();
                    mmtLegendBlock.change.emit();
                    """))

        ####################--------------REMOVE MMT MODEL---------------###############################
            # Click box_legend
            for legendIndex in range(1, maxLegendNum):
                legend = legendArr[legendIndex]
                legend.js_on_click(CustomJS(args=dict(mmtLegendBlock=mmtLegendBlock, plot = p), code="""
                        var boxIndex = cb_obj.origin.tags[0];
                        //search for the box
                        var boxArr = (mmtLegendBlock.children)[1].children;
                        var box = boxArr[boxIndex];
                        var boxHeader = box.children[0];
                        var mmtType = boxHeader.children[0].tags[1];
                        //update mmtplot
                        var modelName = cb_obj.origin.label;
                        var mmtBoxName = boxHeader.children[0].label;
                        var mmtPlot = plot.select(name=mmtBoxName)[0];
                        var mmtModel = mmtPlot.data_source;
                        //var mmtPos = modelNum + boxIndex;
                        //var mmtIndex = legendLayout.items[mmtPos].tags[0];
                        //var mmtPlot = legendLayout.items[mmtPos].renderers[0];
                        //var mmtModel = mmtModelArr[mmtIndex];

                        var yArr = (mmtModel.data)['y'];
                        var curLegendNum = boxHeader.children[1].active;

                        if(mmtType == 0){
                            var legendY = plot.select(name=modelName)[0].data_source.data['y'];
                            for (var j=0; j<yArr.length; j++){
                                if(curLegendNum == 1){
                                    //yArr[j] = 0;
                                }else{
                                    yArr[j] = (yArr[j]*(curLegendNum) - legendY[j])/(curLegendNum-1);
                                }
                            }
                        }else if(mmtType == 1){
                            var dataYArr=[];
                            for(var i=1; i<=curLegendNum; i++){
                                if(box.children[i].label != modelName){
                                    var curDataYArr = plot.select(name=box.children[i].label)[0].data_source.data['y'];
                                    dataYArr.push(curDataYArr);
                                }
                            }
                            for (var i=0; i<yArr.length; i++){
                                var dataXArr = [];
                                var legenNum =curLegendNum-1;
                                for(var j=0; j<legenNum; j++){
                                    dataXArr.push(dataYArr[j][i]);
                                }
                                if(legenNum == 0) {
                                    //yArr[i] = 0;
                                    continue;
                                }
                                dataXArr.sort();
                                yArr[i] = legenNum%2 ?dataXArr[(legenNum-1)/2]:
                                          (dataXArr[legenNum/2-1] + dataXArr[legenNum/2])/2;
                            }
                        }else if(mmtType == 2){
                            var dataYArr=[];
                            for(var i=1; i<=curLegendNum; i++){
                                if(box.children[i].label != modelName){
                                    var curDataYArr = plot.select(name=box.children[i].label)[0].data_source.data['y'];
                                    dataYArr.push(curDataYArr);
                                }
                            }
                            for (var i=0; i<yArr.length; i++){
                                var dataXArr = [];
                                var legenNum =curLegendNum-1;
                                for(var j=0; j<legenNum; j++){
                                    dataXArr.push(dataYArr[j][i]);
                                }

                                //calculate trend with least squared fit
                                if(legenNum == 0) {
                                    //yArr[i] = 0;
                                    continue;
                                }else if(legenNum == 1) {
                                    yArr[i] = dataXArr[0];
                                    continue;
                                }else if(legenNum == 2) {
                                    yArr[i] = (dataXArr[0]+dataXArr[1])/2;
                                    continue;
                                }
                                var scaleY = 10000;
                                var offsetY = dataYArr[0][0];
                                var factor = 60;
                                var count = 0;
                                var sumX = 0;
                                var sumX2 = 0;
                                var sumX3 = 0;
                                var sumX4 = 0;
                                var sumY = 0;
                                var sumXY = 0;
                                var sumX2Y = 0;
                                for (var x = 0; x < dataXArr.length; x++)
                                {
                                    count++;
                                    sumX += x;
                                    sumX2 += x*x;
                                    sumX3 += x*x*x;
                                    sumX4 += x*x*x*x;
                                    sumY += dataXArr[x];
                                    sumXY += x*dataXArr[x];
                                    sumX2Y += x*x*dataXArr[x];
                                }
                                //var det = count * sumX2 - sumX * sumX;
                                //var offset = (sumX2 * sumY - sumX * sumXY) / det;
                                //var scale = (count * sumXY - sumX * sumY) / det;
                                //yArr[i] = offset + factor * scale;
                                //continue;
                                var det = count*sumX2*sumX4 - count*sumX3*sumX3 - sumX*sumX*sumX4 + 2*sumX*sumX2*sumX3 - sumX2*sumX2*sumX2;
                                var offset = sumX*sumX2Y*sumX3 - sumX*sumX4*sumXY - sumX2*sumX2*sumX2Y + sumX2*sumX3*sumXY + sumX2*sumX4*sumY - sumX3*sumX3*sumY;
                                var scale = -count*sumX2Y*sumX3 + count*sumX4*sumXY + sumX*sumX2*sumX2Y - sumX*sumX4*sumY - sumX2*sumX2*sumXY + sumX2*sumX3*sumY;
                                var accel = sumY*sumX*sumX3 - sumY*sumX2*sumX2 - sumXY*count*sumX3 + sumXY*sumX2*sumX - sumX2Y*sumX*sumX + sumX2Y*count*sumX2;
                                yArr[i] = (offset + factor*scale + factor*factor*accel)/det/scaleY+offsetY;
                                    
                            }
                        }

                        mmtModel.change.emit();
                        mmtPlot.visible = (curLegendNum != 1);
                        mmtPlot.change.emit();

                        //switch the legends following the deleted legends upwards
                        var legendIndex = cb_obj.origin.tags[1];
                        var j=legendIndex;
                        for (; j<curLegendNum; j++){
                            var legend = box.children[j];
                            var nextLegend = box.children[j+1];
                            legend.label = nextLegend.label;
                        }
                        box.children[j].label = "";
                        box.children[j].visible = false;
                        box.children[j].height = 0;
                        (boxHeader.children)[1].active = curLegendNum - 1;
                        mmtLegendBlock.change.emit();
                        """))

        # ROW_1 :: p + legends #######################################################################

        linePalette = Category20[20]
        colorIndex = 0
        for name, model in self.modelDict.items():
            renderer = self.plot_model(p, model, linePalette[maxBoxNum + colorIndex])
            colorIndex += 1
            item = LegendItem(label=name, renderers=[renderer])
        ####################--------------ADD MMT MODEL---------------###############################
            renderer_cb = CustomJS(args=dict(mmtLegendBlock=mmtLegendBlock, plot = p, pickerDict=colorPicker, 
                height=mmtLegendH, width=mmtLegendW, maxLegendNum=maxLegendNum, modelName=name),code="""
                    var blockHeader = (mmtLegendBlock.children)[0].children;
                    var activeBox = blockHeader[2];
                    if(activeBox.active > 0){
                        var boxIndex = activeBox.active-1;
                        var boxArr = (mmtLegendBlock.children)[1].children;
                        var legendArr = boxArr[boxIndex].children;
                        var curLegendNum = (legendArr[0].children)[1].active;

                        if(curLegendNum < maxLegendNum){
                            var modelExists = false;
                            for(var i=1; i<=curLegendNum; i++){
                                if(legendArr[i].label == modelName) modelExists = true;
                            }
                            if(!modelExists){
                                (legendArr[0].children)[1].active++;
                                curLegendNum++;
                                legendArr[curLegendNum].tags[0] = boxIndex;
                                legendArr[curLegendNum].label = modelName;
                                legendArr[curLegendNum].visible = true;
                                legendArr[curLegendNum].height = height;
                                //legendArr[curLegendNum].width_policy = "fit";
                                legendArr[curLegendNum].width = width;
                                mmtLegendBlock.change.emit();

                                //update mmtplot
                                var mmtBoxName = (legendArr[0].children)[0].label;
                                var mmtType = (legendArr[0].children)[0].tags[1];
                                var mmtPlot = plot.select(name=mmtBoxName)[0];
                                var mmtModel = mmtPlot.data_source;
                                //var mmtPos = modelNum + boxIndex;
                                //var mmtIndex = legendLayout.items[mmtPos].tags[0];
                                //var mmtPlot = legendLayout.items[mmtPos].renderers[0];
                                //var mmtModel = mmtModelArr[mmtIndex];
                                var yArr = (mmtModel.data)['y'];
                                
                                var legendY = plot.select(name=modelName)[0].data_source.data['y'];
                                if(mmtType == 0){
                                    for (var i=0; i<yArr.length; i++){
                                        yArr[i] = (yArr[i]*(curLegendNum-1)+legendY[i])/curLegendNum;
                                    }
                                }else if(mmtType == 1){
                                    var dataYArr = [legendY];
                                    for(var i=1; i<curLegendNum; i++){
                                        var curDataYArr = plot.select(name=legendArr[i].label)[0].data_source.data['y'];
                                        dataYArr.push(curDataYArr);
                                    }
                                    for (var i=0; i<yArr.length; i++){
                                        var dataXArr = [];
                                        for(var j=0; j<curLegendNum; j++){
                                            dataXArr.push(dataYArr[j][i]);
                                        }
                                        dataXArr.sort();
                                        yArr[i] = curLegendNum%2 ? dataXArr[(curLegendNum-1)/2]:
                                                    (dataXArr[curLegendNum/2-1] + dataXArr[curLegendNum/2])/2;
                                    }
                                }else if(mmtType == 2){
                                    var dataYArr = [legendY];
                                    for(var i=1; i<curLegendNum; i++){
                                        var curDataYArr = plot.select(name=legendArr[i].label)[0].data_source.data['y'];
                                        dataYArr.push(curDataYArr);
                                    }
                                    for (var i=0; i<yArr.length; i++){
                                        var dataXArr = [];
                                        for(var j=0; j<curLegendNum; j++){
                                            dataXArr.push(dataYArr[j][i]);
                                        }
                                        //calculate trend with least squared fit
                                        if(curLegendNum == 1) {
                                            yArr[i] = dataXArr[0];
                                            continue;
                                        }else if(curLegendNum == 2) {
                                            yArr[i] = (dataXArr[0]+dataXArr[1])/2;
                                            continue;
                                        }
                                        var scaleY = 10000;
                                        var offsetY = dataYArr[0][0];
                                        var factor = 60;
                                        var count = 0;
                                        var sumX = 0;
                                        var sumX2 = 0;
                                        var sumX3 = 0;
                                        var sumX4 = 0;
                                        var sumY = 0;
                                        var sumXY = 0;
                                        var sumX2Y = 0;
                                        for (var x = 0; x < dataXArr.length; x++)
                                        {
                                            count++;
                                            sumX += x;
                                            sumX2 += x*x;
                                            sumX3 += x*x*x;
                                            sumX4 += x*x*x*x;
                                            sumY += dataXArr[x];
                                            sumXY += x*dataXArr[x];
                                            sumX2Y += x*x*dataXArr[x];
                                        }
                                        //var det = count * sumX2 - sumX * sumX;
                                        //var offset = (sumX2 * sumY - sumX * sumXY) / det;
                                        //var scale = (count * sumXY - sumX * sumY) / det;
                                        //yArr[i] = offset + factor * scale;
                                        //continue;
                                        var det = count*sumX2*sumX4 - count*sumX3*sumX3 - sumX*sumX*sumX4 + 2*sumX*sumX2*sumX3 - sumX2*sumX2*sumX2;
                                        var offset = sumX*sumX2Y*sumX3 - sumX*sumX4*sumXY - sumX2*sumX2*sumX2Y + sumX2*sumX3*sumXY + sumX2*sumX4*sumY - sumX3*sumX3*sumY;
                                        var scale = -count*sumX2Y*sumX3 + count*sumX4*sumXY + sumX*sumX2*sumX2Y - sumX*sumX4*sumY - sumX2*sumX2*sumXY + sumX2*sumX3*sumY;
                                        var accel = sumY*sumX*sumX3 - sumY*sumX2*sumX2 - sumXY*count*sumX3 + sumXY*sumX2*sumX - sumX2Y*sumX*sumX + sumX2Y*count*sumX2;
                                        yArr[i] = (offset + factor*scale + factor*factor*accel)/det/scaleY+offsetY;
                                    }
                                }
                                mmtModel.change.emit();
                                mmtPlot.visible = true;
                                mmtPlot.change.emit();
                                cb_obj.visible = false;
                            }
                        }
                    }
                    for(let pickerName in pickerDict){
                        var picker = pickerDict[pickerName];
                        picker.disabled=true;
                        picker.visible=false;
                        picker.change.emit();
                    }
                    var picker = pickerDict[modelName];
                    picker.disabled=false;
                    picker.visible=true;
                    picker.change.emit();
                """)
            renderer.js_on_change('visible', renderer_cb)  # 'muted'
            picker = ColorPicker(title=name, css_classes = ["color_picker_" + name], visible=False, disabled = True)
            picker.js_link('color', renderer.glyph, 'line_color')
            colorPicker[name] = picker
            legendLayout.items.append(item)

        self.setup_axis(p)
        p.toolbar.autohide = True
        self.setup_legends(p, legendLayout)
        sliderLayout = self.setup_slider_layout(p, legendLayout, mmtLegendBlock, colorPicker)
        # LAYOUT :: ROW_1, ROW_2 #########################
        layout = column(sliderLayout, mmtLegendBlock)
        # tab pages
        #tab1 = Panel(child=fig1, title="sine")
        #tab2 = Panel(child=fig2, title="cos")
        #tabs = Tabs(tabs=[ tab1, tab2 ])

        return self.do_export(layout, p)

    def setup_slider_layout(self, plot, legendLayout, mmtLegendBlock, colorPicker):
        sampleModel = list(self.modelDict.values())[0]
        timeLen = len(sampleModel.get_val_cds()['x'])
        maxLen = timeLen / 10 + 1
        callback = CustomJS(args=dict(mmtLegendBlock=mmtLegendBlock, plot = plot, legends=legendLayout.items, 
            modelDict = self.nameModelDict, modelNum=self.modelNum),code="""

                //modify model data, with boxcar based on origin data
                var copyDict = {};
                for(var k = 0; k <modelNum; k++){
                    var legend = legends[k];
                    var modelName = legend.label.value;
                    var originDataY = modelDict[modelName]['y'];
                    var lineData = legend.renderers[0].data_source;
                    var dataY = lineData.data['y'];
                    //calculate box car
                    var dataLen = originDataY.length;
                    var carLen = cb_obj.value;
                    var data_head = originDataY.slice(1, carLen);
                    var data_tail = originDataY.slice(dataLen-carLen, dataLen-1);
                    var data_ext = [];
                    for(let t of data_tail) data_ext.unshift(t);
                    data_ext = originDataY.concat(data_ext);
                    for(let h of data_head) data_ext.unshift(h);
                    var startIndex = (carLen-1)/2;
                    for(var i=startIndex; i<startIndex + dataLen; i++){
                        var localSum = 0;
                        for(var j=0; j<carLen; j++){
                            localSum += data_ext[i+j];
                        }
                        dataY[i] = localSum/carLen;
                    }
                    copyDict[modelName] = dataY;
                    lineData.change.emit();
                }

                //modify mmt data, with mean/median/trend based on modified model data
                var blockHeader = (mmtLegendBlock.children)[0].children;
                var curBoxNum = blockHeader[1].active;
                var boxArr = (mmtLegendBlock.children)[1].children;
                for(var k = 0; k <curBoxNum; k++){
                    var legendArr = boxArr[k].children;
                    var curLegendNum = legendArr[0].children[1].active;
                    var mmtBoxName = (legendArr[0].children)[0].label;
                    var mmtType = (legendArr[0].children)[0].tags[1];
                    var mmtPlot = plot.select(name=mmtBoxName)[0];
                    var mmtModel = mmtPlot.data_source;
                    var yArr = (mmtModel.data)['y'];
                    
                    if(mmtType == 0){
                        var dataYArr = [];
                        for(var i=1; i<=curLegendNum; i++){
                            var curDataYArr = copyDict[legendArr[i].label];
                            dataYArr.push(curDataYArr);
                        }
                        for (var i=0; i<yArr.length; i++){
                            var dataXSum = 0;
                            for(var j=0; j<curLegendNum; j++){
                                dataXSum += dataYArr[j][i];
                            }
                            if(curLegendNum == 0) {
                                //yArr[i] = 0;
                                continue;
                            }
                            yArr[i] = dataXSum/curLegendNum;
                        }
                    }else if(mmtType == 1){
                        var dataYArr = [];
                        for(var i=1; i<=curLegendNum; i++){
                            var curDataYArr = copyDict[legendArr[i].label];
                            dataYArr.push(curDataYArr);
                        }
                        for (var i=0; i<yArr.length; i++){
                            var dataXArr = [];
                            for(var j=0; j<curLegendNum; j++){
                                dataXArr.push(dataYArr[j][i]);
                            }
                            if(curLegendNum == 0) {
                                //yArr[i] = 0;
                                continue;
                            }
                            dataXArr.sort();
                            yArr[i] = curLegendNum%2 ? dataXArr[(curLegendNum-1)/2]:
                                        (dataXArr[curLegendNum/2-1] + dataXArr[curLegendNum/2])/2;
                        }
                    }else if(mmtType == 2){
                        var dataYArr = [];
                        for(var i=1; i<=curLegendNum; i++){
                            var curDataYArr = copyDict[legendArr[i].label];
                            dataYArr.push(curDataYArr);
                        }
                        for (var i=0; i<yArr.length; i++){
                            var dataXArr = [];
                            for(var j=0; j<curLegendNum; j++){
                                dataXArr.push(dataYArr[j][i]);
                            }
                            //calculate trend with least squared fit
                            if(curLegendNum == 0) {
                                //yArr[i] = 0;
                                continue;
                            }else if(curLegendNum == 1) {
                                yArr[i] = dataXArr[0];
                                continue;
                            }else if(curLegendNum == 2) {
                                yArr[i] = (dataXArr[0]+dataXArr[1])/2;
                                continue;
                            }
                            var scaleY = 10000;
                            var offsetY = dataYArr[0][0];
                            var factor = 60;
                            var count = 0;
                            var sumX = 0;
                            var sumX2 = 0;
                            var sumX3 = 0;
                            var sumX4 = 0;
                            var sumY = 0;
                            var sumXY = 0;
                            var sumX2Y = 0;
                            for (var x = 0; x < dataXArr.length; x++)
                            {
                                count++;
                                sumX += x;
                                sumX2 += x*x;
                                sumX3 += x*x*x;
                                sumX4 += x*x*x*x;
                                sumY += dataXArr[x];
                                sumXY += x*dataXArr[x];
                                sumX2Y += x*x*dataXArr[x];
                            }
                            //var det = count * sumX2 - sumX * sumX;
                            //var offset = (sumX2 * sumY - sumX * sumXY) / det;
                            //var scale = (count * sumXY - sumX * sumY) / det;
                            //yArr[i] = offset + factor * scale;
                            //continue;
                            var det = count*sumX2*sumX4 - count*sumX3*sumX3 - sumX*sumX*sumX4 + 2*sumX*sumX2*sumX3 - sumX2*sumX2*sumX2;
                            var offset = sumX*sumX2Y*sumX3 - sumX*sumX4*sumXY - sumX2*sumX2*sumX2Y + sumX2*sumX3*sumXY + sumX2*sumX4*sumY - sumX3*sumX3*sumY;
                            var scale = -count*sumX2Y*sumX3 + count*sumX4*sumXY + sumX*sumX2*sumX2Y - sumX*sumX4*sumY - sumX2*sumX2*sumXY + sumX2*sumX3*sumY;
                            var accel = sumY*sumX*sumX3 - sumY*sumX2*sumX2 - sumXY*count*sumX3 + sumXY*sumX2*sumX - sumX2Y*sumX*sumX + sumX2Y*count*sumX2;
                            yArr[i] = (offset + factor*scale + factor*factor*accel)/det/scaleY+offsetY;
                        }
                    }
                    mmtModel.change.emit();
                    mmtPlot.visible = true;
                    mmtPlot.change.emit();
                }
                """)
        slider = Slider(start=1, end=maxLen, value=1, step=1, title="smooth factor", css_classes = ["boxcar_factor"])
        slider.js_on_change('value', callback)
        return column(row(slider,row(list(colorPicker.values()))) ,plot)

    def build_models_dict(self):
        modelsDict = {}
        firstModelData = self.modelList[0].get_val_cds()
        modelsDict['Time'] = firstModelData['x']
        for model in self.modelList:
            modelName = model.get_name()
            modelData = model.get_val_cds()
            modelsDict[modelName] = modelData['y']
        return modelsDict

    def setup_mmt_legendboxArr(self, maxBoxNum, maxLegendNum):
        legendNum = ["number" for i in range(maxLegendNum)]
        mmtLegendBoxArr = []
        for boxIndex in range(maxBoxNum):
            boxTitle = Button(
                label="", tags=[-1, -1], css_classes = ["mmt_title"], width=0, height=0, visible=False)
            mmtLegendNum = RadioButtonGroup(
                labels=legendNum, active=0, visible=False, disabled=True)
            boxDel = Button(
                label="x", tags=[-1], css_classes = ["mmt_del"], width=0, height=0, visible=False)
            boxHeaderArr = [boxTitle, mmtLegendNum, boxDel]
            boxHeader = row(boxHeaderArr)
            legendArr = [boxHeader]
            for legendIndex in range(maxLegendNum):
                legendArr.append(
                    Button(label="", tags=[-1, legendIndex + 1], css_classes = ["mmt"], width=0, height=0, visible=False))
            mmtLegendBoxArr.append(column(legendArr))
        return row(mmtLegendBoxArr)

    def plot_mmt(self, maxBoxNum, plot, pickerDict):
        mmtPalette = Spectral11[0:maxBoxNum]
        sampleModel = list(self.modelDict.values())[0]
        data = sampleModel.get_val_cds()
        modelArr = []
        plotArr = []
        for mmtIndex in range(maxBoxNum):
            yArr = np.zeros(len(data['x']))
            yArr[:] = data['y'][0]
            modelDict = {'x': data['x'], 'y': yArr}
            mmtModel = ColumnDataSource(data=modelDict)
            mmtPlot = plot.line('x', 'y', source=mmtModel, line_dash="4 0", line_width=2, tags = [str(mmtIndex)],
                                line_color=mmtPalette[mmtIndex], line_alpha=0.6, visible=False)
            mmtPlot_cb = CustomJS(args=dict(pickerDict=pickerDict, modelName=str(mmtIndex)),code="""
                    for(let pickerName in pickerDict){
                        var picker = pickerDict[pickerName];
                        picker.disabled=true;
                        picker.visible=false;
                        picker.change.emit();
                    }
                    var picker = pickerDict[modelName];
                    picker.disabled=false;
                    picker.visible=true;
                    picker.title=cb_obj.name;
                    picker.change.emit();
                    
                """)
            mmtPlot.js_on_change('visible', mmtPlot_cb)  # 'muted'
            mmtLegend = LegendItem(
                label='', tags=[mmtIndex], renderers=[mmtPlot])
            modelArr.append(mmtModel)
            plotArr.append(mmtLegend)
            picker = ColorPicker(title=str(mmtIndex), css_classes = ["color_picker_" + str(mmtIndex)], visible=False, disabled = True)
            picker.js_link('color', mmtPlot.glyph, 'line_color')
            pickerDict[str(mmtIndex)] = picker
        return {'mmtModelArr': modelArr, 'mmtPlotArr': plotArr}

    def plot_model(self, plot, model, color):
        modelName = model.get_name()
        #color = model.get_para_color()
        highlighted = model.get_para_highlighted()
        muted_alpha = 0.8 * float(highlighted) + 0.2
        data = model.copy_val_cds()
        #data['y'] = self.boxcar_mirror(10, data['y'])
        return plot.line(data['x'], data['y'], line_dash="4 0", line_width=1, name = modelName,
                         line_color=color, line_alpha=0.5, muted_color=color, muted_alpha=muted_alpha)

    def setup_legends(self, plot, legendLayout):
        # title
        legendLayout.title = "climate models:"
        legendLayout.title_text_font_style = "bold"
        legendLayout.title_text_font_size = "15px"
        # label
        legendLayout.label_text_font = "times"
        legendLayout.label_text_font_style = "italic"
        legendLayout.label_text_color = "navy"
        # dimension
        legendLayout.label_standoff = 5
        legendLayout.glyph_width = 50
        # orientation
        # legendLayout.orientation = "horizontal"
        legendLayout.click_policy = "hide"  # "mute"  # or "hide"
        # legendLayout.location = "top_right"
        
        plot.add_layout(legendLayout, 'right')
        return legendLayout

    def setup_axis(self, plot):
        # axis
        plot.xaxis.axis_line_width = 2
        plot.xaxis.axis_line_color = "black"
        # axis label
        # plot.xaxis.axis_label = "Time"
        # plot.xaxis.axis_label_text_color = "#aa6666"
        # plot.xaxis.axis_label_standoff = 30
        plot.yaxis.axis_label = self.plotType.name
        plot.yaxis.axis_label_text_font_style = "italic"
        # tick line
        plot.xaxis.major_tick_line_color = "orange"
        plot.xaxis.major_tick_line_width = 3
        plot.xaxis.minor_tick_line_color = "black"
        plot.yaxis.minor_tick_line_width = 2
        plot.yaxis.minor_tick_line_color = "firebrick"
        plot.axis.major_tick_out = 10
        plot.axis.minor_tick_in = -3
        plot.axis.minor_tick_out = 8

        ONE_MILLI = 1.0
        ONE_SECOND = 1000.0
        ONE_MINUTE = 60.0 * ONE_SECOND
        ONE_HOUR = 60 * ONE_MINUTE
        ONE_DAY = 24 * ONE_HOUR
        ONE_MONTH = 30 * ONE_DAY  # An approximation, obviously.
        ONE_YEAR = 365 * ONE_DAY
        ymdTicker = CompositeTicker()
        ymdTicker.tickers = [
            AdaptiveTicker(
                mantissas=[1, 2, 5],
                base=10,
                min_interval=0,
                max_interval=500 * ONE_MILLI,
                num_minor_ticks=0
            ),
            AdaptiveTicker(
                mantissas=[1, 2, 5, 10, 15, 20, 30],
                base=60,
                min_interval=ONE_SECOND,
                max_interval=30 * ONE_MINUTE,
                num_minor_ticks=0
            ),
            AdaptiveTicker(
                mantissas=[1, 2, 4, 6, 8, 12],
                base=24,
                min_interval=ONE_HOUR,
                max_interval=12 * ONE_HOUR,
                num_minor_ticks=0
            ),
            AdaptiveTicker(
                mantissas=[1, 2, 5, 10, 15],
                base=30,
                min_interval=ONE_DAY,
                max_interval=15 * ONE_DAY,
                num_minor_ticks=0
            ),
            AdaptiveTicker(
                mantissas=[1, 2, 4, 6],
                base=12,
                min_interval=ONE_MONTH,
                max_interval=6 * ONE_MONTH,
                num_minor_ticks=0
            ),
            AdaptiveTicker(
                mantissas=[1, 2, 3, 4, 5],
                base=10,
                min_interval=ONE_YEAR,
                max_interval=5 * ONE_YEAR,
                num_minor_ticks=0
            ),
            DaysTicker(days=list(range(1, 32))),
            DaysTicker(days=list(range(1, 31, 3))),
            DaysTicker(days=[1, 8, 15, 22]),
            DaysTicker(days=[1, 15]),

            MonthsTicker(months=list(range(0, 12, 1))),
            MonthsTicker(months=list(range(0, 12, 2))),
            MonthsTicker(months=list(range(0, 12, 4))),
            MonthsTicker(months=list(range(0, 12, 6))),

            YearsTicker(),
        ]
        plot.xaxis.ticker = ymdTicker

        # format
        # plot.xaxis[0].formatter = NumeralTickFormatter(format="0.0%")
        # plot.yaxis[0].formatter = NumeralTickFormatter(format="$0.00")
        # plot.xaxis[0].formatter = PrintfTickFormatter(format="%4.1e")
        # plot.yaxis[0].formatter = PrintfTickFormatter(format="%5.3f mu")
        # plot.yaxis.formatter = FuncTickFormatter(code="""
        #    return Math.floor(tick) + " + " + (tick % 1).toFixed(2)
        #    """)
        plot.xaxis.formatter = DatetimeTickFormatter(
            hours=['%m/%d/%Y%Hh', '%m/%d/%Y%Hh'],
            days=['%m/%d/%Y', '%m/%d/%Y'],
            months=['%m. %Y', '%b %Y'],
            years=['%m. %Y']
            )
        plot.yaxis.major_label_text_color = "orange"
        # orientation
        plot.xaxis.major_label_orientation = pi / 4
        plot.yaxis.major_label_orientation = "vertical"


class Tco3ZmPlotter(ZmPlotter):
    pass


class Vmro3ZmPlotter(ZmPlotter):
    pass


class Tco3ReturnPlotter(Plotter):
    def plot_data(self, plotdata):
        pass

    def build_models_dict(self):
        pass
