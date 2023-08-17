import math

from dash import Dash, dcc, html, Input, Output, State, callback, clientside_callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

import page

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


app.layout = html.Div(children=[
    html.Div([
        page.get_page(),
        html.Div(id="empty-div-1"),
        html.Div(id="empty-div-2")
    ], className="main-page-padding")
])


clientside_callback(
    """
    function(n_clicks, value) {
        return draw("canvas_m", value, 1);
    }
    """,
    Output("empty-div-1", "children"),
    Input("btn_draw_plot_men", "n_clicks"),
    State("input_attractivity_function_for_men", "value")
)


clientside_callback(
    """
    function(n_clicks, value) {
        return draw("canvas_f", value, 2);
    }
    """,
    Output("empty-div-2", "children"),
    Input("btn_draw_plot_women", "n_clicks"),
    State("input_attractivity_function_for_women", "value")
)


# @callback(
#     Output("btn_draw_plot_men", "disabled"),
#     Output("btn_draw_plot_women", "disabled"),
#     Input("btn_draw_plot_men", "n_clicks"),
#     Input("btn_draw_plot_women", "n_clicks")
# )
# def update_output_div(n_clicks_m, n_clicks_w):
#     return False, False


if __name__ == '__main__':
    # print(math.fabs(-9))
    app.run(debug=True)
