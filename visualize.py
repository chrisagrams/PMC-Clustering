import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df = pd.read_parquet('clustered_data_20000.parquet')

fig = px.scatter(
    df,
    x='x',
    y='y',
    color='cluster',
    custom_data=['pmcid'],
    title="PMC Clustering"
)

app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(
        id='scatter-plot',
        figure=fig,
        style={'width': '100vw', 'height': '100vh'}
    ),
    html.Div(id='dummy')
], style={'margin': '0', 'padding': '0'})

app.clientside_callback(
    """
    function(clickData) {
        if (clickData) {
            var pmcid = clickData.points[0].customdata[0];
            var url = "https://pmc.ncbi.nlm.nih.gov/articles/" + pmcid + "/";
            window.open(url, "_blank");
        }
        return "";
    }
    """,
    Output('dummy', 'children'),
    Input('scatter-plot', 'clickData')
)

if __name__ == '__main__':
    app.run(debug=True)
