from plotData import PlotData, PlotType, OutputFormat
from flask import url_for,redirect, Response
import json
from math import pi
import numpy as np
import pdfkit

# bokeh plot
from bokeh.core.properties import String, Instance
import pandas as pd
from pandas import Series,DataFrame
from datetime import datetime as dt
from bokeh.models import ColumnDataSource, Legend, LegendItem, CustomJS
from bokeh.models import DatetimeTickFormatter, FuncTickFormatter, PrintfTickFormatter, NumeralTickFormatter
from bokeh.models import Button, Panel, Tabs, RadioButtonGroup, Div, Slider, TextInput
from bokeh.layouts import column, row, WidgetBox, widgetbox
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.events import ButtonClick, Tap
from bokeh.palettes import Spectral11
# bokeh io
from bokeh.io import show, output, export_png, export_svgs
from bokeh.embed import json_item,file_html
from bokeh.resources import CDN
from io import StringIO

from abc import ABC, abstractmethod

# Plotter, 
# plotting the data stored within the plotData
# considering the parameter for variables and legends.
class Plotter(ABC):

    @abstractmethod
    def plot_data(self, plotdata):
        pass

    def init_plotter(self, plotdata):
        self.modelDict = plotdata.get_modeldata_dict()
        self.modelList = plotdata.get_modeldata_list()
        self.plotType = plotdata.get_ptype()
        self.output = plotdata.get_output()

    @abstractmethod
    def build_models_dict(self):
        pass

    def do_export(self, layout, plot):
        if self.output == OutputFormat["csv"]:
            df = pd.DataFrame(self.build_models_dict())
            dfbuffer = StringIO()
            df.to_csv(dfbuffer, encoding='utf-8', index=False)
            dfbuffer.seek(0)
            data = dfbuffer.getvalue()
            return Response(data, mimetype="text/csv",
                headers={"Content-Disposition": "attachment;filename={}".format("plot.csv")})
        elif self.output == OutputFormat["png"]:
            plot.background_fill_color = None
            plot.border_fill_color = None
            data = export_png(plot, filename="plot.png")
            return Response(data, mimetype="image/png",
                headers={"Content-Disposition": "attachment;filename={}".format("plot.png")})
        elif self.output == OutputFormat["svg"]:
            plot.background_fill_color = None
            plot.border_fill_color = None
            plot.output_backend = "svg"
            data = export_svgs(plot, filename="plot.svg")
            return Response(data, mimetype="image/svg+xml",
                headers={"Content-Disposition": "attachment;filename={}".format("plot.svg")})
#        elif self.output == OutputFormat["pdf"]:
#            output_file("static/o3as_plot.html")
#            show(plot)
#            data = pdfkit.from_file('static/o3as_plot.html', 'plot.pdf')
#            return Response(data, mimetype="application/pdf",
#                headers={"Content-Disposition": "attachment;filename={}".format("plot.pdf")})
        else:
            data = json.dumps(json_item(layout))
            return Response(data, mimetype='application/json')

# Plotter, 
# plotting the data in *-zm plot type, time -> messurement,
# whose x axis represents the time.
class ZmPlotter(Plotter):
    mmtLabels = ["mean", "median", "trend"]

    def build_models_dict(self):
        modelsDict = {}
        firstModelData = self.modelList[0].get_val_cds()
        modelsDict['Time'] = firstModelData['x']
        for model in self.modelList:
            modelName = model.get_name()
            modelData = model.get_val_cds()
            modelsDict[modelName] = modelData['y']
        return modelsDict

    def plot_data(self, plotdata):
        self.init_plotter(plotdata)

        p = figure(plot_width=700, plot_height=300, title=self.plotType.name, x_axis_type="datetime")

        ###################  mmt block #####################
        #+----------------+--------------+----------------+#
        #| mmtButtonGroup |  mmtBoxNum   | mmtBoxActivity |#
        #+----------------+--------------+----------------+#
        ####################################################
        #+----------------+----------------+               #
        #|+--boxHeader---+|+--boxHeader---+|               #
        #|| boxTitle     ||| boxTitle     ||               #
        #|| mmtLegendNum ||| mmtLegendNum ||               #
        #|+--------------+|+--------------+|               #
        #|  legend_1      |  legend_1      |               #
        #|  legend_2      |  legend_2      |               #
        #|  ...           |  ...           |               #
        #+----------------+----------------+               #
        ####################################################
        # ROW_2 :: mmt block                                ##################################
        maxBoxNum = 5
        maxLegendNum = 5
        ## mmt block header
        mmtButtonGroup = RadioButtonGroup(labels=ZmPlotter.mmtLabels)
        boxNum = ["number" for i in range(maxBoxNum)]
        boxActivity = ["activity" for i in range(maxBoxNum)]
        mmtBoxNum = RadioButtonGroup(labels=boxNum, active=0, visible=False)
        mmtBoxActivity = RadioButtonGroup(labels=boxActivity, active=0, visible=False)
        mmtLegendBlockHead = row(mmtButtonGroup, mmtBoxNum, mmtBoxActivity)
        ## mmt box array
        bgColor = "black"
        defaultBoxColor = "white"
        selectedBoxColor = "red"
        boxHeaderW = 100
        mmtLegendH = 20
        mmtLegendW = 400
        #TODO add button beside the box title for color-div and remove-option of the box
        mmtLegendBoxArr = self.setup_mmt_legendboxArr(maxBoxNum, maxLegendNum)
        mmtModelPlotArr = self.plot_mmt(maxBoxNum, p)
        ## mmt block
        mmtLegendBlock = column(mmtLegendBlockHead, mmtLegendBoxArr)
        mmtButtonGroup.js_on_click(CustomJS(args=dict(mmtLegendBlock=mmtLegendBlock,
            mmtLabels=ZmPlotter.mmtLabels, height=mmtLegendH, width=boxHeaderW, maxBoxNum=maxBoxNum, 
            selColor=selectedBoxColor, defaultColor=defaultBoxColor), code="""
                if(cb_obj.active == 'None') return;
                var blockHeader = (mmtLegendBlock.children)[0].children;
                var curBoxNum = blockHeader[1];
                var activeBox = blockHeader[2];
                var boxArr = (mmtLegendBlock.children)[1].children;
                if(activeBox.active > 0){
                    var oldBoxTitle = (((boxArr[activeBox.active-1].children)[0]).children)[0];
                    oldBoxTitle.button_type = 'default';
                    oldBoxTitle.background=defaultColor;
                }
                if(curBoxNum.active < maxBoxNum){
                    activeBox.active = ++curBoxNum.active;
                    var boxTitle = (((boxArr[activeBox.active-1].children)[0]).children)[0];
                    boxTitle.label = mmtLabels[cb_obj.active]+'_'+curBoxNum.active;
                    boxTitle.visible = true;
                    boxTitle.height = height;
                    boxTitle.width = width;
                    boxTitle.button_type = 'success';
                    boxTitle.background=selColor;
                }else{
                    activeBox.active = 0;
                }
                mmtLegendBlock.change.emit();
                cb_obj.active = 'None';
                """))
 
        for boxIndex in range(maxBoxNum):
            legendBox = (mmtLegendBoxArr.children)[boxIndex]
            legendArr = legendBox.children
            legendBoxTitle = (legendArr[0].children)[0]
            legendBoxTitle.js_on_click(CustomJS(args=dict(mmtLegendBlock=mmtLegendBlock,
                boxIndex=boxIndex, selColor=selectedBoxColor, defaultColor=defaultBoxColor), code="""
                    var blockHeader = (mmtLegendBlock.children)[0].children;
                    var curBoxNum = blockHeader[1];
                    var activeBox = blockHeader[2];
                    var boxArr = (mmtLegendBlock.children)[1].children;
                    if(activeBox.active > 0){
                        var oldBoxTitle = (((boxArr[activeBox.active-1].children)[0]).children)[0];
                        oldBoxTitle.button_type = 'default';
                        oldBoxTitle.background=defaultColor;
                    }
                    activeBox.active = boxIndex + 1;
                    var boxTitle = (((boxArr[boxIndex].children)[0]).children)[0];
                    boxTitle.button_type = 'success';
                    boxTitle.background = selColor;
                    mmtLegendBlock.change.emit();
                    """))
            for legendIndex in range(1, maxLegendNum):
                legend = legendArr[legendIndex]
                # TODO legend.js_on_click to delete model #######################################
                legend.js_on_click(CustomJS(args=dict(mmtBlockHead=mmtLegendBlockHead,
                    mmtBoxArr=mmtLegendBoxArr, bgColor=bgColor, boxIndex=legendIndex), code="""
                        """))

        # ROW_1 :: p + legends #######################################################################
        items = []
        for name, model in self.modelDict.items():
            renderer = self.plot_model(p, model)
            item = LegendItem(label=name, renderers=[renderer])
            renderer_cb = CustomJS(args=dict(mmtLegendBlock=mmtLegendBlock, 
                mmtModelArr=mmtModelPlotArr['mmtModelArr'], mmtPlotArr=mmtModelPlotArr['mmtPlotArr'],
                height=mmtLegendH, width=mmtLegendW, maxLegendNum=maxLegendNum, 
                legendName=name, model=model.get_val_cds(), legendColor=renderer.glyph.line_color),
                code="""
                        var blockHeader = (mmtLegendBlock.children)[0].children;
                        var activeBox = blockHeader[2];
                        var boxArr = (mmtLegendBlock.children)[1].children;
                        var legendArr = boxArr[activeBox.active-1].children;
                        var curLegendNum = (legendArr[0].children)[1];

                        if(activeBox.active > 0 && curLegendNum.active < maxLegendNum){
                            for(var i=1; i<=curLegendNum.active; i++){
                                if(legendArr[i].label == legendName) return;
                            }
                            curLegendNum.active++;
                            legendArr[curLegendNum.active].label = legendName;
                            legendArr[curLegendNum.active].visible = true;
                            legendArr[curLegendNum.active].height = height;
                            //legendArr[curLegendNum.active].width_policy = "fit";
                            legendArr[curLegendNum.active].width = width;
                            legendArr[curLegendNum.active].background = legendColor;
                            mmtLegendBlock.change.emit();
                            //update mmtplot
                            var legendY = model['y'];
                            var mmtModel = mmtModelArr[activeBox.active-1];
                            var mmtPlot = mmtPlotArr[activeBox.active-1];
                            var yArr = (mmtModel.data)['y'];
                            for (var i=0; i<yArr.length; i++){
                                yArr[i] = (yArr[i]*(curLegendNum.active-1)+legendY[i])/curLegendNum.active;
                            }
                            mmtModel.change.emit();
                            mmtPlot.visible = true;
                            mmtPlot.change.emit();
                            cb_obj.visible = false;
                        }
                    """)
            renderer.js_on_change('muted', renderer_cb)
            items.append(item)

        self.setup_axis(p)
        p.toolbar.autohide = True
        legend = self.setup_legends(p, items)

        # LAYOUT :: ROW_1, ROW_2 #########################
        layout = column(p, mmtLegendBlock)
        # tab pages
        #tab1 = Panel(child=fig1, title="sine")
        #tab2 = Panel(child=fig2, title="cos")
        #tabs = Tabs(tabs=[ tab1, tab2 ])

        # output
        return self.do_export(layout, p)
    
    def setup_mmt_legendboxArr(self, maxBoxNum, maxLegendNum):
        legendNum = ["number" for i in range(maxLegendNum)]
        mmtLegendBoxArr = []
        for boxIndex in range(maxBoxNum):
            boxTitle = Button(label="", width=0, height=0, visible=False)
            mmtLegendNum = RadioButtonGroup(labels=legendNum, active=0, visible=False)
            boxHeader = column(boxTitle, mmtLegendNum)
            legendArr = [boxHeader]
            for legendIndex in range(maxLegendNum):
                legendArr.append(Button(label="", width=0, height=0, visible=False))
            mmtLegendBoxArr.append(column(legendArr))
        return row(mmtLegendBoxArr)

    def plot_mmt(self, maxBoxNum, plot):
        mmtPalette = Spectral11[0:maxBoxNum]
        sampleModel = list(self.modelDict.values())[0]
        df = pd.DataFrame(data=sampleModel.get_val_cds())
        df['x'] = pd.to_datetime(df['x'])
        modelArr = []
        plotArr = []
        for mmtIndex in range(maxBoxNum):
            yArr = np.zeros(len(df['x']))
            yArr[:] = mmtIndex*100
            modelDict = {'x':df['x'], 'y':yArr}
            mmtModel = ColumnDataSource(data=modelDict)
            mmtPlot = plot.line('x', 'y', source=mmtModel, line_dash="4 0", line_width=2, line_color=mmtPalette[mmtIndex], line_alpha=0.6, visible=False)
            modelArr.append(mmtModel)
            plotArr.append(mmtPlot)
        return {'mmtModelArr':modelArr, 'mmtPlotArr':plotArr}

    def plot_model(self, plot, model):
        #mypalette = Spectral11[0:100]
        name = model.get_name()
        color = model.get_para_color()
        highlighted = model.get_para_highlighted()
        muted_alpha = 0.8 * float(highlighted) + 0.2
        df = pd.DataFrame(data=model.get_val_cds())
        df['x'] = pd.to_datetime(df['x'])
        return plot.line(df['x'], df['y'], line_dash="4 0", line_width=1,
                        line_color=color, line_alpha=0.5, muted_color=color, muted_alpha=muted_alpha)
                        #legend_label=name)

    def setup_legends(self, plot, items):
        legend = Legend(items=items, location="center")
        # title
        legend.title = "climate models:"
        legend.title_text_font_style = "bold"
        legend.title_text_font_size = "15px"
        # label
        legend.label_text_font = "times"
        legend.label_text_font_style = "italic"
        legend.label_text_color = "navy"
        # dimension
        legend.label_standoff = 5
        legend.glyph_width = 50
        # orientation
        # legend.orientation = "horizontal"

        legend.click_policy="mute"  # or "hide"
        # legend.location = "top_right"
        plot.add_layout(legend, 'right')
        return legend
        
    def setup_axis(self, plot):
        # axis
        plot.xaxis.axis_line_width = 3
        plot.xaxis.axis_line_color = "red"
        # axis label
        # plot.xaxis.axis_label = "Time"
        # plot.xaxis.axis_label_text_color = "#aa6666"
        # plot.xaxis.axis_label_standoff = 30
        plot.yaxis.axis_label = self.plotType.name
        plot.yaxis.axis_label_text_font_style = "italic"
        # tick line
        plot.xaxis.major_tick_line_color = "orange"
        plot.xaxis.major_tick_line_width = 3
        plot.xaxis.minor_tick_line_color = None
        plot.yaxis.minor_tick_line_color = "firebrick"
        plot.axis.major_tick_out = 10
        plot.axis.minor_tick_in = -3
        plot.axis.minor_tick_out = 8
        # format
        # plot.xaxis[0].formatter = NumeralTickFormatter(format="0.0%")
        # plot.yaxis[0].formatter = NumeralTickFormatter(format="$0.00")
        # plot.xaxis[0].formatter = PrintfTickFormatter(format="%4.1e")
        # plot.yaxis[0].formatter = PrintfTickFormatter(format="%5.3f mu")
        # plot.yaxis.formatter = FuncTickFormatter(code="""
        #    return Math.floor(tick) + " + " + (tick % 1).toFixed(2)
        #    """)
        plot.xaxis.formatter=DatetimeTickFormatter(
                hours = ['%Hh', '%H:%M'],
                days = ['%m/%d/%Y', '%a%d'],
                months = ['%m/%Y', '%b %Y'],
                years = ['%Y']
            )
        plot.yaxis.major_label_text_color = "orange"
        # orientation
        plot.xaxis.major_label_orientation = pi/4
        plot.yaxis.major_label_orientation = "vertical"


class Tco3ZmPlotter(ZmPlotter):
    pass

class Vmro3ZmPlotter(ZmPlotter):
    pass

class Tco3ReturnPlotter(Plotter):
    pass
