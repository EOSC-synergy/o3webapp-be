from plotData import PlotData, PlotType, OutputFormat
from flask import url_for,redirect, Response
import json
from math import pi

# bokeh plot
from bokeh.core.properties import String, Instance
import pandas as pd
from datetime import datetime as dt
from bokeh.models import ColumnDataSource, Legend, LegendItem, CustomJS
from bokeh.models import DatetimeTickFormatter, FuncTickFormatter, PrintfTickFormatter, NumeralTickFormatter
from bokeh.models import Button, Panel, Tabs, RadioButtonGroup, Div, Slider, TextInput
from bokeh.layouts import column, row
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.events import ButtonClick, Tap
# bokeh io
from bokeh.io import show, output, export_png
from bokeh.embed import json_item,file_html
from bokeh.resources import CDN

#TODO######################################################
import numpy as np
from bokeh.palettes import Spectral11
from pandas import Series,DataFrame
from bokeh.layouts import WidgetBox, widgetbox
#TODO#######################################################

# Plotter, 
# plotting the data stored within the plotData
# considering the parameter for variables and legends.
class Plotter:

    plotterDict = {'tco3_zm': (lambda plotdata: Tco3ZmPlotter(plotdata)),
                   'vmro3_zm': (lambda plotdata: Vmro3ZmPlotter(plotdata)),
                   'tco3_return': (lambda plotdata: Tco3ReturnPlotter(plotdata))}

    def init_plotter(self, plotdata):
        self.modelDict = plotdata.get_modeldata_dict()
        self.modelList = plotdata.get_modeldata_list()
        self.plotType = plotdata.get_ptype()
        self.output = plotdata.get_output()

    def plot_data(self, plotdata):
        typeName = plotdata.get_ptype_name()
        assignedPlotter = Plotter.plotterDict[typeName](plotdata)
        #return assignedPlotter.plot_data_process_test()
        plot = assignedPlotter.plot_data_process()

        # TODO convert plot into required format
        output = plotdata.get_output()
        if output == OutputFormat["json"]:
            data = json.dumps(json_item(plot))
            return Response(data, mimetype='application/json')
        elif output == OutputFormat["png"]:
            Plot.background_fill_color = None
            Plot.border_fill_color = None
            data = export_png(plot, filename="plot.png")
            return Response(data, mimetype="image/png",
                headers={"Content-Disposition": "attachment;filename={}".format("plot.png")})

    def do_export(self, data, format):
        # svg = dataHub.trackCompositor.render()
        # converter = export.getExportConverter(dataHub.args, format)
        if format == "svg":
            mimetype = "image/svg+xml"
            # data = svg
        elif format == "png":
            mimetype = "image/png"
            # data = export.convertSVG(svg, "png", converter)
        elif format == "pdf":
            mimetype = "application/pdf"
            # data = export.convertSVG(svg, "pdf", converter)
        else:
            raise Exception("unknown format")
        response = Response(data, mimetype=mimetype,
            headers={"Content-Disposition": "attachment;filename={}".format("plot.png")})
        return response

# Plotter, 
# plotting the data in *-zm plot type, time -> messurement,
# whose x axis represents the time.
class ZmPlotter(Plotter):

    def plot_data_process(self):
        output_file("static/o3as_plot.html")
        
        p = figure(plot_width=800, plot_height=250, title=self.plotType.name, x_axis_type="datetime")

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
        mmtLabels = ["tco3_zm", "vmro3_zm", "tco3_return"]
        mmtButtonGroup = RadioButtonGroup(labels=mmtLabels)
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
        mmtLegendBoxArr = self.setup_mmt_legendboxArr(maxBoxNum, maxLegendNum)
        mmtModelPlotArr = self.plot_mmt(maxBoxNum, p)
        ## mmt block
        mmtLegendBlock = column(mmtLegendBlockHead, mmtLegendBoxArr)
        mmtButtonGroup.js_on_click(CustomJS(args=dict(mmtLegendBlock=mmtLegendBlock,
            mmtLabels=mmtLabels, height=mmtLegendH, width=boxHeaderW, maxBoxNum=maxBoxNum, 
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
                # TODO legend.js_on_click to delete #######################################
                legend.js_on_click(CustomJS(args=dict(mmtBlockHead=mmtLegendBlockHead,
                    mmtBoxArr=mmtLegendBoxArr, bgColor=bgColor, boxIndex=legendIndex), code="""
                        """))


        # ROW_1 :: p + legends #######################################################################
                        
        items = []
        for name, model in self.modelDict.items():
            renderer = self.plot_model(p, model)
            item = LegendItem(label=name, renderers=[renderer])
            renderer_cb = CustomJS(args=dict(mmtLegendBlock=mmtLegendBlock, mmtModelArr=mmtModelPlotArr['mmtModelArr'],
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
                            var mmtModel = mmtModelArr[activeBox.active-1].data;
                            var yArr = mmtModel['y'];
                            for (var i=0; i<yArr.length; i++){
                                yArr[i] = (yArr[i]*(curLegendNum.active-1)+legendY[i]*curLegendNum.active)/curLegendNum.active;
                            }
                            mmtModel.change.emit();
                            cb_obj.visible = false;
                        }
                    """)
            renderer.js_on_change('muted', renderer_cb)
            items.append(item)

        self.setup_axis(p)
        p.toolbar.autohide = True
        legend = self.setup_legends(p, items)

        # ROW_test ################################################
        x = [x*0.005 for x in range(0, 200)]
        y = x
        source2 = ColumnDataSource(data=dict(x=x, y=y))
        plot2 = figure(plot_width=400, plot_height=400)
        plot2.line('x', 'y', source=source2, line_width=3, line_alpha=0.6)
        callback2 = CustomJS(args=dict(source=source2), code="""
            var data = source.data;
            var f = cb_obj.value
            var x = data['x']
            var y = data['y']
            for (var i = 0; i < x.length; i++) {
                y[i] = Math.pow(x[i], f)
            }
            source.change.emit();
        """)
        slider2 = Slider(start=0.1, end=4, value=1, step=.1, title="power")
        slider2.js_on_change('value', callback2)
        layout2 = column(slider2, plot2)

        # LAYOUT :: ROW_1, ROW_2, ROW_test #########################
        layout = column(p, mmtLegendBlock, layout2)
        # tab pages
        #tab1 = Panel(child=fig1, title="sine")
        #tab2 = Panel(child=fig2, title="cos")
        #tabs = Tabs(tabs=[ tab1, tab2 ])
        return layout
    

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
            mmtDF = pd.DataFrame(data=modelDict)
            mmtPlot = plot.line(mmtDF['x'], mmtDF['y'], line_dash="4 0", line_width=1, line_color=mmtPalette[mmtIndex], line_alpha=0.5, visible=True)
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

        legend.click_policy="mute"
        # legend.click_policy="hide"
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
    def __init__(self, plotdata):
        self.init_plotter(plotdata)

class Vmro3ZmPlotter(ZmPlotter):
    def __init__(self, plotdata):
        self.init_plotter(plotdata)

class Tco3ReturnPlotter(Plotter):
    def __init__(self, plotdata):
        self.init_plotter(plotdata)
