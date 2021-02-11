from plotData import PlotData
import json
from flask import url_for,redirect
from math import pi

import pandas as pd
from datetime import datetime as dt
from bokeh.models import DatetimeTickFormatter
from bokeh.plotting import figure, output_file, show

from bokeh.embed import json_item,file_html
from bokeh.resources import CDN

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
        return assignedPlotter.plot_data_process()

    def plot_data_process(self):
        p = figure(plot_width=800, plot_height=250, x_axis_type="datetime")
        for modeldata in self.plot_data.get_modeldata_list():
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

class ZmPlotter(Plotter):

    def plot_model(self, plot, model):
        df = pd.DataFrame(data=model.get_val_cds())
        df['x'] = pd.to_datetime(df['x'])
        plot.line(df['x'], df['y'], color='navy', alpha=0.5)

class Tco3ZmPlotter(ZmPlotter):
    def __init__(self, plotdata):
        super().__init__()
        self.plot_data = plotdata

class Vmro3ZmPlotter(ZmPlotter):
    def __init__(self, plotdata):
        super().__init__()
        self.plot_data = plotdata

class Tco3ReturnPlotter(Plotter):
    def __init__(self, plotdata):
        super().__init__()
        self.plot_data = plotdata
