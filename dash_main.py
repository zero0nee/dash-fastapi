from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

### CONCLUSION: it is not possible to use Flask POST requests as inputs to plotly
### https://community.plotly.com/t/update-plot-in-dash-from-rest-api/10612/5
### https://community.plotly.com/t/how-to-connect-flask-wtf-form-responses-to-a-plotly-dash-dashboard/22162
### https://community.plotly.com/t/send-request-to-flask-api-with-dash-inside/21919/5
### https://community.plotly.com/t/update-dash-layout-using-rest-api/17555/5
### https://community.plotly.com/t/apis-on-dash-server/30966/5
### https://community.plotly.com/t/refresh-page-on-post-request/36812
# This dataframe has 244 lines, but 4 distinct values for `day`
df = px.data.tips()

fig = px.pie(df, values='tip', names='day')


# Create the Dash application, make sure to adjust requests_pathname_prefx
app_dash = dash.Dash(__name__, requests_pathname_prefix='/dash/')
app_dash.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    # content will be rendered in this element
    html.Div(id='page-content')
])

app_flask = app_dash.server

@app_dash.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    leaf_path = pathname.split("/")[-1]
    if leaf_path == "pie":
        return dcc.Graph(
            id='pie-graph',
            figure=px.pie(df, values='tip', names='day')
        )
    elif leaf_path == "sunburst":
        return dcc.Graph(
            id='sunburst-graph',
            figure=px.sunburst(df, path=['day', 'time', 'sex'], values='total_bill')
        )
    else:
        #return html.P("Error 404 - please select a proper graph endpoint")
        return dcc.Graph(
            id='sunburst-graph',
            figure=px.sunburst(df, path=['day', 'time', 'sex'], values='total_bill')
        )
        
@app_flask.route('/dash/test', methods=['POST'])
def req():
    df = px.data.medals_long()
    result = request.form
    return flask.redirect(flask.request.url)  # Should redirect to current page/ refresh page

# Now create your regular FASTAPI application
app = FastAPI()

@app.get("/hello_fastapi")
def read_main():
    return {"message": "Hello World"}


# Now mount you dash server into main fastapi application
app.mount("/dash", WSGIMiddleware(app_dash.server))