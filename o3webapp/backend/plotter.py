from plotData import PlotData
import json
from flask import url_for,redirect
from math import pi

# bokeh plot
import pandas as pd
from bokeh.models import ColumnDataSource
from datetime import datetime as dt
from bokeh.models import DatetimeTickFormatter
from bokeh.plotting import figure, output_file, show, curdoc
# bokeh io
from bokeh.io import show, output
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

    def __init__(self):
        pass

    def plot_data(self, plotdata):
        typeName = plotdata.get_ptype_name()
        assignedPlotter = Plotter.plotterDict[typeName](plotdata)
        #return assignedPlotter.plot_data_process_test()
        return assignedPlotter.plot_data_process()

    def plot_data_process(self):
        p = figure(plot_width=800, plot_height=250, x_axis_type="datetime")
        for modeldata in self.plotData.get_modeldata_list():
            self.plot_model(p, modeldata)
        
        #p.xaxis.formatter=DatetimeTickFormatter(
        #        hours=["%d %B %Y"],
        #        days=["%d %B %Y"],
        #        months=["%d %B %Y"],
        #        years=["%d %B %Y"],
        #    )
        #p.xaxis.major_label_orientation = pi/4
        output_file("static/o3as_plot.html")
        show(p)
        return json.dumps(json_item(p))
        #return redirect(url_for('static', filename='o3as_plot.html'))
        #return file_html(p, CDN, "my plot")

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

        # models_selection = CheckboxGroup(labels=modelsList, active=[])
        ## models_selection.js_on_click(update)
        ## models_selection.on_change('active', update)
        # group = widgetbox(activP, models_selection)
        # layout = row(group)

        # curdoc().add_root(layout)
        # curdoc().title = "O3as"
        # show(layout)
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

    def plot_model(self, plot, model):
        df = pd.DataFrame(data=model.get_val_cds())
        df['x'] = pd.to_datetime(df['x'])
        plot.line(df['x'], df['y'], color='navy', alpha=0.5)

class Tco3ZmPlotter(ZmPlotter):
    def __init__(self, plotdata):
        super().__init__()
        self.plotData = plotdata

class Vmro3ZmPlotter(ZmPlotter):
    def __init__(self, plotdata):
        super().__init__()
        self.plotData = plotdata

class Tco3ReturnPlotter(Plotter):
    def __init__(self, plotdata):
        super().__init__()
        self.plotData = plotdata
