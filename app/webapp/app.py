import math
from threading import Thread
from werkzeug.exceptions import HTTPException, InternalServerError

import dash
from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL, callback, clientside_callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import uuid

from app.webapp import page
from app.webapp import utils
from app.simulation import simulation
from app.simulation import utils as sim_utils
from app.webapp import utils as web_utils

simulations = {}

# Use dbc.icons.BOOTSTRAP or dbc.icons.FONT_AWESOME for icons (see https://stackoverflow.com/a/76015777/14522363)
app = Dash(__name__, external_stylesheets=[dbc.icons.FONT_AWESOME, dbc.themes.SLATE])
app.title = "Dating Apps Simulation"
app._favicon = "favicon.svg"
app.layout = html.Div(children=[
    html.Div([
        page.get_page(),
        html.Div(id="empty-div-1"),
        html.Div(id="empty-div-2"),
        html.Div(id="current_simulation_id", children=None, style={"display": "block"}),
        html.Div(id="current_simulation_id_results", children=None, style={"display": "none"}),
        dcc.Interval(id="progress_interval", n_intervals=0, interval=500),
    ], className="main-page-padding", id="page"),
    html.Div(id="notify-holder", className="notify-container"),
    html.Div(id={"type": "error_div", "index": "run_simulation_errors"}, children=None, style={"display": "none"}),
])


clientside_callback(
    """
    function(children) {
        arr = children[0];
        if (arr.length > 1) {
            console.log(arr[0]);
            console.log(arr[1]);
            showNotify("error", arr[0], arr[1], 20);
        }
        return "";
    }
    """,
    Output({"type": "error_div", "index": ALL}, "style"),
    Input({"type": "error_div", "index": ALL}, "children"),
    prevent_initial_call=True
)

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
    Output({"type": "error_div", "index": "run_simulation_errors"}, "children"),
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
    try:
        errors = web_utils.check_inputs_for_errors(amount_of_men, amount_of_women, amount_of_women_a_man_will_see, amount_of_men_a_woman_will_see)
        if len(errors) <= 0:
            new_simulation = simulation.Simulation(amount_of_men, amount_of_women, amount_of_women_a_man_will_see, amount_of_men_a_woman_will_see)
            thread = Thread(target=new_simulation.run_sim, args=(1,))
            thread.start()
            simulation_id = str(uuid.uuid4())
            simulations.update({simulation_id: new_simulation})
            return simulation_id, ""
        return None, ["Some inputs are not valid", errors]
    except Exception as e:
        return None, ["An exception occurred", str(e)]



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
    Output({"type": "granularity_text", "index": MATCH}, "children"),
    Output({"type": "distribution_graph", "index": MATCH}, "figure"),
    Input({"type": "granularity_slider", "index": MATCH}, "value"),
    State({"type": "figure_index", "index": MATCH}, "children"),
    State("current_simulation_id", "children"),
)
def adjust_granularity(granularity, index, current_simulation_id):
    """There is no prevent_initial_call=True here! -> This also displays the graphs on simulation results load.
    """
    if current_simulation_id is not None:
        current_simulation = simulations[current_simulation_id]
        df_distribution = sim_utils.get_distribution(current_simulation, index, granularity)
        fig = px.bar(df_distribution, x="group_name", y=["men", "women"], barmode='group', title='x')
        fig.layout = page.get_layout_for_figures()
        return granularity, fig
    return dash.no_update


def run_server():
    app.run(debug=True)
