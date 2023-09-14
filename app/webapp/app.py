import time
from threading import Thread

from flask import render_template
import dash
from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL, callback, clientside_callback
import dash_bootstrap_components as dbc
import plotly.express as px
import uuid

from webapp import page
from simulation import simulation
from simulation import utils as sim_utils
from simulation.person import DICT_KEY_AMOUNT_LIKES_RECEIVED, DICT_KEY_AMOUNT_MATCHES
from webapp import utils as web_utils
from webapp import cleanup

simulations = {}


class DashApp(Dash):
    def __init__(self, name, update_title, external_stylesheets):
        super().__init__(name, update_title=update_title, external_stylesheets=external_stylesheets)
        self.title = "Dating Apps Simulation"
        self._favicon = "favicon.svg"
        self.layout = html.Div(children=[
            html.Meta(name="viewport", content="width=device-width, initial-scale=1"),
            html.Meta(name="color-scheme", content="light only"),
            html.Div([
                page.get_page(),
                html.Div(id="empty-div-1"),
                html.Div(id="empty-div-2"),
                html.Div(id="current_simulation_id", children=None, style={"display": "none"}),
                html.Div(id="progress_interval_container")
            ], className="main-page-padding", id="page"),
            html.Div(id="notify-holder", className="notify-container"),
            html.Div(id={"type": "error_div", "index": "start_simulation_errors"}, children="", style={"display": "none"}),
            html.Div(id={"type": "error_div", "index": "run_simulation_errors"}, children="", style={"display": "none"}),
        ])
        # starts the task to remove old simulations
        cleanup.start_clean_up_task(simulations)


# Use dbc.icons.BOOTSTRAP or dbc.icons.FONT_AWESOME for icons (see https://stackoverflow.com/a/76015777/14522363)
app = DashApp(__name__, update_title=None, external_stylesheets=[
    dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME, dbc.themes.SLATE
])
server = app.server


@server.route('/plotting')
def plotting():
    return render_template("function_plot.html")  # this has to be under ./templates/


clientside_callback(
    """
    function(children) {
        for (let i = 0; i < children.length; i++) {
            arr = children[i];
            if (arr.length > 1) {
                showNotify("error", arr[0], arr[1], 20);
            }
        }
        return "";
    }
    """,
    Output({"type": "error_div", "index": ALL}, "style"),
    Input({"type": "error_div", "index": ALL}, "children"),
    prevent_initial_call=True
)

clientside_callback(  # TODO: move setUpInfoIcons(); to somewhere else
    """
    function(n_clicks, value) {
        setUpInfoIcons();
        
        try {
            draw("canvas_m", value, 1);
        }
        catch(err) {
            showNotify("error", "Error while plotting", err.message, 20);
        }
        return "";
    }
    """,
    Output("empty-div-1", "children"),
    Input("btn_draw_plot_men", "n_clicks"),
    State("input_attractivity_function_for_men", "value")
)

clientside_callback(
    """
    function(n_clicks, value) {
        try {
            draw("canvas_f", value, 2);
        }
        catch(err) {
            showNotify("error", "Error while plotting", err.message, 20);
        }
        return "";
    }
    """,
    Output("empty-div-2", "children"),
    Input("btn_draw_plot_women", "n_clicks"),
    State("input_attractivity_function_for_women", "value")
)


@callback(
    Output("current_simulation_id", "children"),
    Output({"type": "error_div", "index": "start_simulation_errors"}, "children"),
    Output("progress_interval_container", "children"),
    Input("run_simulation", "n_clicks"),
    State("input_amount_of_men", "value"),
    State("input_amount_of_women", "value"),
    State("input_amount_of_women_a_man_will_see", "value"),
    State("input_amount_of_men_a_woman_will_see", "value"),
    State("input_max_amount_of_likes_for_men", "value"),
    State("input_max_amount_of_likes_for_women", "value"),
    State("input_attractivity_function_for_men", "value"),
    State("input_attractivity_function_for_women", "value"),
    prevent_initial_call=True
)
def button_click_run_simulation(n_clicks, amount_of_men, amount_of_women, amount_of_women_a_man_will_see, amount_of_men_a_woman_will_see,
                                max_amount_of_likes_for_men, max_amount_of_likes_for_women, attractivity_function_for_men,
                                attractivity_function_for_women):
    try:
        errors = web_utils.check_inputs_for_errors(amount_of_men, amount_of_women, amount_of_women_a_man_will_see,
            amount_of_men_a_woman_will_see, max_amount_of_likes_for_men, max_amount_of_likes_for_women)
        attractivity_function_for_men = sim_utils.parse_equation(attractivity_function_for_men)
        attractivity_function_for_women = sim_utils.parse_equation(attractivity_function_for_women)
        if len(errors) <= 0:
            new_simulation = simulation.Simulation(amount_of_men, amount_of_women, amount_of_women_a_man_will_see, amount_of_men_a_woman_will_see,
                max_amount_of_likes_for_men, max_amount_of_likes_for_women, attractivity_function_for_men, attractivity_function_for_women)
            thread = Thread(target=new_simulation.run_sim, args=(1,))
            thread.start()
            simulation_id = str(uuid.uuid4())
            simulations.update({simulation_id: new_simulation})
            return simulation_id, "", dcc.Interval(id="progress_interval", n_intervals=0, interval=500, disabled=False)
        return None, ["Some inputs are not valid", errors], None
    except Exception as e:
        return None, ["An exception occurred", str(e)], None



@callback(
    Output("simulation_progress_bar", "value"),
    Output("simulation_progress_bar", "label"),
    Output("simulation_progress_status_text", "children"),
    Output("simulation_progress_bar", "className"),
    Output("run_simulation", "children"),
    Output({"type": "error_div", "index": "run_simulation_errors"}, "children"),
    Output("progress_interval", "disabled"),
    Input("progress_interval", "n_intervals"),
    State("current_simulation_id", "children")
)
def update_progress(n, current_simulation_id):
    if current_simulation_id is not None:
        try:
            current_simulation = simulations[current_simulation_id]
        except KeyError:
            return 0, "", "The simulation does not exist anymore.", "", "Run Simulation", "", True
        if current_simulation.latest_error is not None:
            return 0, "", "", "", "Run Simulation", ["Error in simulation", current_simulation.latest_error], True
        progress = current_simulation.progress.current_progress_in_percent()
        progress_text = current_simulation.progress.current_progress_status_text
        if current_simulation.timestamp_finished is not None:
            return progress, f"{progress} %" if progress >= 5 else "", progress_text, "hidden", "Rerun Simulation", "", True
        # only add text after 5% progress to ensure text isn't squashed too much
        return progress, f"{progress} %" if progress >= 5 else "", progress_text, "", "Rerun Simulation", "", False
    return 0, "", "", "", "Run Simulation", "", False


@callback(
    Output("simulation_results", "children"),
    Input("progress_interval", "n_intervals"),
    State("current_simulation_id", "children"),
)
def show_results(n, current_simulation_id):
    try:
        sim = simulations[current_simulation_id]
        if sim.timestamp_finished is not None:
            return page.get_results_div(sim)
    except KeyError:
        pass  # TODO: show error that simulation is gone
    return dash.no_update


@callback(
    Output({"type": "granularity_text", "index": MATCH}, "children"),
    Output({"type": "distribution_graph", "index": MATCH}, "figure"),
    Output({"type": "dataframe_store", "index": MATCH}, "data"),
    Input({"type": "granularity_slider", "index": MATCH}, "value"),
    State({"type": "figure_index", "index": MATCH}, "children"),
    State("current_simulation_id", "children"),
)
def adjust_granularity(granularity, index, current_simulation_id):
    """There is no prevent_initial_call=True here! -> This also displays the graphs on simulation results load.
    """
    if current_simulation_id is not None:
        try:
            current_simulation = simulations[current_simulation_id]
        except KeyError:
            return dash.no_update  # TODO: show error that simulation is gone
        df_distribution = sim_utils.get_distribution(current_simulation, index, granularity)
        group_color = {"men": "#6fa8dc", "women": "#e66eb4"}
        fig = px.bar(df_distribution, x="group_name", y=["men", "women"], barmode='group', title='x',
                     color_discrete_map=group_color)
        fig.layout = page.get_layout_for_figures()
        return granularity, fig, df_distribution.to_dict("records")
    return dash.no_update


@callback(
    Output('table_of_users', 'rowData'),
    Output('table_of_users_amount_rows', 'children'),
    Input({"type": "distribution_graph", "index": ALL}, 'selectedData'),
    State({"type": "dataframe_store", "index": ALL}, "data"),
    State("current_simulation_id", "children"),
)
def filter_table_data(selected_data_sets, data_sets, current_simulation_id):
    if current_simulation_id is not None:
        try:
            current_simulation = simulations[current_simulation_id]
        except KeyError:
            return dash.no_update  # TODO: show error that simulation is gone
        user_ids = set()
        for i in range(len(selected_data_sets)):
            selected_data_set = selected_data_sets[i]
            data_set = data_sets[i]
            if selected_data_set is not None:
                for point in selected_data_set["points"]:
                    if point["curveNumber"] == 0:
                        selected_group_sex = "user_ids_of_men"
                    else:  # point["curveNumber"] == 1
                        selected_group_sex = "user_ids_of_women"
                    selected_group = point["x"]  # this value is for example '90 - 100'
                    for group in data_set:  # iterating the different groups e.g. 0 - 10, 10 - 20, ... 90 - 100 for granularity 10
                        if group["group_name"] == selected_group:
                            user_ids.update(group[selected_group_sex])
        return current_simulation.get_users_by_ids(user_ids), f"Amount of rows: {len(user_ids)}"
    return dash.no_update