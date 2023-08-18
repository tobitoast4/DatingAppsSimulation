import math
from threading import Thread

import dash
from dash import Dash, dcc, html, Input, Output, State, callback, clientside_callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import uuid

from app.webapp import page
from app.simulation import simulation

simulations = {}

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
app.layout = html.Div(children=[
    html.Div([
        page.get_page(),
        html.Div(id="empty-div-1"),
        html.Div(id="empty-div-2"),
        html.Div(id="current_simulation_id", children=None, style={"display": "none"}),
        html.Div(id="current_simulation_id_results", children=None, style={"display": "none"}),
        dcc.Interval(id="progress_interval", n_intervals=0, interval=500),
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


@callback(
    # Output("run_simulation", "disabled"),
    Output("current_simulation_id", "children"),
    Input("run_simulation", "n_clicks"),
    State("input_amount_of_men", "value"),
    State("input_amount_of_women", "value"),
    State("input_amount_of_women_a_man_will_see", "value"),
    State("input_amount_of_men_a_woman_will_see", "value"),
    # State("input_max_amount_of_likes_for_men", "value"),
    # State("input_max_amount_of_likes_for_women", "value"),
    # State("input_attractivity_function_for_men", "value"),
    # State("input_attractivity_function_for_women", "value"),
    prevent_initial_call=True
)
def button_click_run_simulation(n_clicks, amount_of_men, amount_of_women, amount_of_women_a_man_will_see, amount_of_men_a_woman_will_see):
    new_simulation = simulation.Simulation(amount_of_men, amount_of_women, amount_of_women_a_man_will_see, amount_of_men_a_woman_will_see)
    thread = Thread(target=new_simulation.run_sim, args=(1,))
    thread.start()
    simulation_id = str(uuid.uuid4())
    simulations.update({simulation_id: new_simulation})
    return simulation_id


@callback(
    Output("simulation_progress_bar", "value"),
    Output("simulation_progress_bar", "label"),
    Output("simulation_progress_status_text", "children"),
    Output("simulation_progress_bar", "className"),
    Output("run_simulation", "children"),
    Input("progress_interval", "n_intervals"),
    State("current_simulation_id", "children")
)
def update_progress(n, current_simulation_id):
    if current_simulation_id is not None:
        current_simulation = simulations[current_simulation_id]
        progress = current_simulation.progress.current_progress_in_percent()
        progress_text = current_simulation.progress.current_progress_status_text
        if progress >= 100:
            return progress, f"{progress} %" if progress >= 5 else "", progress_text, "hidden", "Rerun Simulation"
        # only add text after 5% progress to ensure text isn't squashed too much
        return progress, f"{progress} %" if progress >= 5 else "", progress_text, "", "Rerun Simulation"
    return 0, "", "", "", "Run Simulation"


@callback(
    Output("simulation_results", "children"),
    Output("current_simulation_id_results", "children"),
    Input("simulation_progress_status_text", "children"),
    State("current_simulation_id", "children"),
    State("current_simulation_id_results", "children"),
)
def show_results(simulation_progress_status_text, current_simulation_id, current_simulation_id_results):
    if simulation_progress_status_text == simulation.PROGRESS_STATE_TEXT_STATUS_5 and current_simulation_id != current_simulation_id_results:
        if current_simulation_id is not None:
            sim = simulations[current_simulation_id]
            return page.get_results_div(sim), current_simulation_id
    return dash.no_update


@callback(
    Output("granularity_text_for_fig1", "children"),
    Input("granularity_slider_for_fig1", "value")
)
def adjust_granularity(value):
    return value


@callback(
    Output("granularity_text_for_fig2", "children"),
    Input("granularity_slider_for_fig2", "value")
)
def adjust_granularity(value):
    return value


def run_server():
    app.run(debug=True)
