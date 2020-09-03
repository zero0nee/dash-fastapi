from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import plotly
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import json

def create_plot(df, feature_type):
    if feature_type == "pie":
        figure=px.pie(df, values='tip', names='day')
    else:
        figure=px.sunburst(df, path=['day', 'time', 'sex'], values='total_bill')
    return plotly.offline.plot(figure, output_type='div')


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/graphs/{figure}", response_class=HTMLResponse)
async def read_item(request: Request, figure: str):
    #TODO - Figure out layout
    df = px.data.tips()
    if not figure:
        figure = 'bar'

    html_string = '''
    <html>
        <head>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
        </head>
        <body>
        <h1>Pie chart</h1>
        ''' + create_plot(df, "pie") + '''
        <h1>Sunburst chart</h1>
        ''' + create_plot(df, "sunburst") + '''
        </body>
    </html>'''

    #return templates.TemplateResponse("index.html", {"request": request,"bar": html_div})
    return html_string
