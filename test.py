import os
from flask import Flask, render_template, url_for, request
from bokeh.plotting import figure, gmap
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.embed import components
import pandas as pd
from bokeh.models import ColumnDataSource, HoverTool, GMapPlot, GMapOptions, DataRange1d, Slider, Select, CustomJS, DateRangeSlider
from bokeh.models import ColorBar, LinearColorMapper
from bokeh.palettes import Viridis256
import math
import numpy as np
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Dropdown
# from bokeh.io import curdoc
from bokeh.layouts import column,row
from numpy.random import random 
from bokeh.layouts import gridplot

species_csv=pd.read_csv("species.csv")
species_name=list(species_csv['scientific_name'].values)
base_url='https://raw.githubusercontent.com/IEScoders/EcoclimateTaiwan/master/output_csv/solenopsis_invicta/'


spec='solenopsis_invicta'
year='2010'
month='01'

# ei_csv=base_url+'{}-{}_{}.csv'.format(year,month,spec)

# months=['01','02','03','04','05','06','07','08','09','10','11','12']
# for year in np.arange(2010,2018,1):
#     for month in months:
#         ei_csv=base_url+'{}-{}_solenopsis_invicta.csv'.format(year,month)

def read_data(year='2015',month='01',spec='solenopsis_invicta'):
    ei_csv=base_url+'{}-{}_{}.csv'.format(year,month,spec)
    df=pd.read_csv(ei_csv)
    df.columns=["Index","EI","id","x","y"]
    x=df['x'].values
    y=df['y'].values
    EIvals=df['EI'].values
    psource=ColumnDataSource(
        data=dict(
            x=x,
            y=y,
            EIvals=EIvals,
        )
    )
    return psource
source=read_data()
# low=math.floor(np.min(df['EI'].values))
# high=math.ceil(np.max(df['EI'].values))
mapper=LinearColorMapper(palette=Viridis256,low=0, high=1)
color_bar=ColorBar(color_mapper=mapper,location=(0,0))




app = Flask(__name__)


posts_data = [
    {
        'bug': 'Red Mite',
        'predator': 'Birdy Bird',
        'crops_affected': "really can't say",
        'ei_val': '-999999'
    }#,
    # {
    #     'author': 'Jane Doe',
    #     'title': 'Blog Post 2',
    #     'content': 'Second post content',
    #     'date_posted': 'April 21, 2018'
    # }
]
app_title="BioZone"
## Home page Route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',posts=posts_data, app_title=app_title)

# # # Analysis Page Route
@app.route('/analysis')
def analysis():
    x = [x*0.005 for x in range(0, 200)]
    y = x

    source = ColumnDataSource(data=dict(x=x, y=y))

    plot = figure(plot_width=400, plot_height=400)
    plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

    def callback(source=source, window=None):
        data = source.data
        f = cb_obj.value                         # NOQA
        x, y = data['x'], data['y']
        for i in range(len(x)):
            y[i] = window.Math.pow(x[i], f)
        source.change.emit();

    slider = Slider(start=0.1, end=4, value=1, step=.1, title="power",
                    callback=CustomJS.from_py_func(callback))

    layout = column(slider, plot)
    script, div = components(layout)	
    return render_template("analysis.html", script=script, div=div, app_title=app_title)

if __name__=="__main__":
    app.run(debug=True)