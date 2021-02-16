from plotData import PlotData, PlotType, OutputFormat
import json
from flask import url_for,redirect, Response
from math import pi

# bokeh plot
import pandas as pd
from bokeh.models import ColumnDataSource, Legend, DatetimeTickFormatter, FuncTickFormatter, PrintfTickFormatter, NumeralTickFormatter
from datetime import datetime as dt
from bokeh.plotting import figure, output_file, show, curdoc
# bokeh io
from bokeh.io import show, output, export_png
from bokeh.embed import json_item,file_html
from bokeh.resources import CDN


#TODO######################################################
import requests
from bokeh.palettes import Spectral11
from pandas import Series,DataFrame
import numpy as np
from bokeh.models import Panel, CheckboxGroup, CustomJS
from bokeh.layouts import column, row, WidgetBox, widgetbox
from bokeh.server.server import Server
from bokeh.models.widgets import Tabs
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


#TODO##########################################################################
    def plot_data_process_test(self):
        modelsList = self.plotData.get_modeldata_list()
        output_file("static/o3as_plot.html")
        # color list
        size = len(modelsList)
        mypalette = Spectral11[0:size]
        # plot
        p = figure(plot_width=1000, plot_height=600, title='tco3_zm', 
                x_axis_label='Time', y_axis_label='Ozone concentration')
        activP = self.getPlot(p, modelsList, mypalette)
        show(activP)

        # check box for models
        models_selection = CheckboxGroup(labels=modelsList, active=[])
        # models_selection.js_on_click(update)
        # models_selection.on_change('active', update)
        group = widgetbox(activP, models_selection)
        layout = row(group)
        # curdoc
        curdoc().add_root(layout)
        curdoc().title = "O3as"
        show(layout)

        
        return json.dumps(json_item(activP))

    def getPlot(self, p, modelsList, palette):
        colorIndex = 0
        for model in modelsList:
            p.line(x = model + 'x', y = model + 'y', legend = model,color = palette[colorIndex])
            #p.line(x = model + 'x', y = model + 'y',source = sourceDic, legend = model,color = palette[colorIndex])
            colorIndex += 1
        return p

    def modelDataSet(self, activModelsList, dicFromURL):
        activDic = {}
        for activModel in activModelsList:
            for key in dicFromURL:
                if key == activModel + 'x' or key == activModel + 'y':
                    activDic[key] = dicFromURL[key]
        activeSourceDic = ColumnDataSource(activDic)
        return activeSourceDic

    def update(self, attr, old, new, models_selection, sourceDic):
        print('updated')
        models_to_plot = [models_selection.labels[i] for i in models_selection.active]
        # new_sourceDic = modelDataSet(models_to_plot)
        # sourceDic.data.update(new_sourceDic.data)
        print('updated')

#TODO##########################################################################

class ZmPlotter(Plotter):

    def plot_data_process(self):
        output_file("static/o3as_plot.html")
        p = figure(plot_width=800, plot_height=250, title=self.plotType.name, x_axis_type="datetime")
        items = []
        for name, model in self.modelDict.items():
            items.append((name, [self.plot_model(p, model)]))
        
        self.setup_legends(p, items)
        self.setup_axis(p)

        p.toolbar.autohide = True
        show(p)
        return p
        #return redirect(url_for('static', filename='o3as_plot.html'))
        #return file_html(p, CDN, "my plot")

    def plot_model(self, plot, model):
        name = model.get_name()
        color = model.get_para_color()
        highlighted = model.get_para_highlighted()
        muted_alpha = 0.8 * float(highlighted) + 0.2
        df = pd.DataFrame(data=model.get_val_cds())
        df['x'] = pd.to_datetime(df['x'])
        return plot.line(df['x'], df['y'], line_dash="4 0", line_width=1,
                        color=color, alpha=0.5, muted_color=color, muted_alpha=muted_alpha)
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
        plot.add_layout(legend, 'right')
        # plot.legend.click_policy="hide"
        # plot.legend.location = "top_right"
        
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
