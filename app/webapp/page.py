from dash import html, dcc
import dash_bootstrap_components as dbc
from plotly.graph_objs import Layout

from simulation import simulation
from simulation.person import *
from webapp import utils


def get_page():
    return html.Div([
        html.Br(),
        html.Div([
            html.H3("Dating Apps Simulation "),
            # html.P(html.I(className="bi bi-arrow-through-heart", style={"font-size": "35px", "color": "red"}))
        ], className="d-flex justify-content-center"),
        html.Hr(),
        html.P([
            "The idea to this website is based on the video of ",
            html.I("Memeable Data"),
            ": ",
            html.A("Why Men Get So Few Matches on Dating Apps", target="_blank",
                   href="https://www.youtube.com/watch?v=x3lypVnJ0HM"),
            ". ",
            """I highly recommend watching his video first in order to better understand the inputs and moreover 
            the results. The conclusion might seem frustrating for men, but it might help to not view dating apps to 
            serious. Meet people in real life! And now have fun with the simulation!""",
            html.Br(),
            "See code on ",
            html.A("GitHub", target="_blank", href="https://github.com/tobitoast4/DatingAppsSimulation"),
            "."
        ]),
        html.Div([
            dbc.Row([
                html.Div([
                    html.Div(className="row-separator-top"),
                    dbc.Row([
                        html.Div([
                            html.Div([
                                html.Div("Amount of men", className="input-fields-text"),
                                html.I(className="fas fa-mars sex-icon", style={"color": "#6fa8dc"}),
                            ], className="d-flex justify-content-start"),
                        ], className="col-9"),
                        html.Div([
                            dcc.Input(id="input_amount_of_men", value=500, type="number",
                                      min=utils.MIN_AMOUNT_OF_USERS_PER_SEX, max=utils.MAX_AMOUNT_OF_USERS_PER_SEX,
                                      className="input-fields-numbers"),
                        ], className="col-3")
                    ]),
                ], className="col-md-6"),
                html.Div([
                    html.Div(className="row-separator-top"),
                    dbc.Row([
                        html.Div([
                            html.Div([
                                html.Div("Amount of women", className="input-fields-text"),
                                html.I(className="fas fa-venus sex-icon", style={"color": "#e66eb4"}),
                            ], className="d-flex justify-content-start"),
                        ], className="col-9"),
                        html.Div([
                            dcc.Input(id="input_amount_of_women", value=500, type="number",
                                      min=utils.MIN_AMOUNT_OF_USERS_PER_SEX, max=utils.MAX_AMOUNT_OF_USERS_PER_SEX,
                                      className="input-fields-numbers"),
                        ], className="col-3")
                    ]),
                ], className="col-md-6")
            ]),
            dbc.Row([
                html.Div([
                    html.Div(className="row-separator-top"),
                    dbc.Row([
                        html.Div([
                            html.Div("Amount of women a man will see in the simulation", className="input-fields-text")
                        ], className="col-9"),
                        html.Div([
                            dcc.Input(id="input_amount_of_women_a_man_will_see", value=100, type="number",
                                      min=utils.MIN_AMOUNT_OF_OTHER_USERS_ONE_USER_WILL_SEE, max=utils.MAX_AMOUNT_OF_USERS_PER_SEX,
                                      className="input-fields-numbers"),
                        ], className="col-3")
                    ]),
                ], className="col-md-6"),
                html.Div([
                    html.Div(className="row-separator-top"),
                    dbc.Row([
                        html.Div([
                            html.Div("Amount of men a woman will see in the simulation", className="input-fields-text")
                        ], className="col-9"),
                        html.Div([
                            dcc.Input(id="input_amount_of_men_a_woman_will_see", value=100, type="number",
                                      min=utils.MIN_AMOUNT_OF_OTHER_USERS_ONE_USER_WILL_SEE, max=utils.MAX_AMOUNT_OF_USERS_PER_SEX,
                                      className="input-fields-numbers"),
                        ], className="col-3")
                    ]),
                ], className="col-md-6")
            ]),
            dbc.Row([
                html.Div([
                    html.Div(className="row-separator-top"),
                    dbc.Row([
                        html.Div([
                            html.Div("Maximum amount of likes for men", className="input-fields-text"),
                            html.I("Leave empty for infinite.", style={"font-size": "12px"})
                        ], className="col-9"),
                        html.Div([
                            dcc.Input(id="input_max_amount_of_likes_for_men", type="number", className="input-fields-numbers"),
                        ], className="col-3")
                    ]),
                ], className="col-md-6"),
                html.Div([
                    html.Div(className="row-separator-top"),
                    dbc.Row([
                        html.Div([
                            html.Div("Maximum amount of likes for women", className="input-fields-text"),
                            html.I("Leave empty for infinite.", style={"font-size": "12px"})
                        ], className="col-9"),
                        html.Div([
                            dcc.Input(id="input_max_amount_of_likes_for_women", type="number", className="input-fields-numbers"),
                        ], className="col-3")
                    ]),
                ], className="col-md-6")
            ]),
            dbc.Row([
                html.Div([
                    html.Div(className="row-separator-top"),
                    dbc.Row([
                        html.Div([
                            html.Div("Formula to determine attractiveness for men", className="input-fields-text"),
                            html.I(className="bi bi-info-circle-fill formula-info-icon")
                        ], className="d-flex justify-content-start"),
                    ]),
                ], className="col-md-6"),
                html.Div([
                    html.Div(className="row-separator-top"),
                    dbc.Row([
                        html.Div([
                            html.Div("Formula to determine attractiveness for women", className="input-fields-text"),
                            html.I(className="bi bi-info-circle-fill formula-info-icon")
                        ], className="d-flex justify-content-start"),
                    ]),
                ], className="col-md-6")
            ]),
            dbc.Row([
                html.Div([
                    html.Div(className="row-separator-top"),
                    dbc.Row([
                        html.Div([
                            dcc.Input(id="input_attractivity_function_for_men",
                                      value="x^6.14", className="input-fields-numbers"),
                        ], className="col-8"),
                        html.Div([
                            dbc.Button("Redraw plot", id="btn_draw_plot_men", className="button-redraw-plot"),
                        ], className="col-4")
                    ]),
                ], className="col-md-6"),
                html.Div([
                    html.Div(className="row-separator-top"),
                    dbc.Row([
                        html.Div([
                            dcc.Input(id="input_attractivity_function_for_women",
                                      value="x^1.17", className="input-fields-numbers"),
                        ], className="col-8"),
                        html.Div([
                            dbc.Button("Redraw plot", id="btn_draw_plot_women", className="button-redraw-plot"),
                        ], className="col-4")
                    ]),
                ], className="col-md-6")
            ]),
            dbc.Row([
                html.Div([
                    html.Canvas(id="canvas_m", width=600, height=600, className="plot-canvas"),
                ], className="col-sm-6"),
                html.Div([
                    html.Canvas(id="canvas_f", width=600, height=600, className="plot-canvas"),
                ], className="col-sm-6")
            ])
        ]),
        html.Hr(),
        html.Div([
            dbc.Button("Run Simulation", id="run_simulation", style={"width": "100%"}),
            html.Div(style={"height": "10px"}),
            dbc.Progress(value=0, id="simulation_progress_bar", animated=True, striped=True),
            html.Div(id="simulation_progress_status_text"),
        ]),
        html.Br(),

        html.Div(id="simulation_results")
    ])


def get_table(sim):
    average_amount_of_likes_male = sim.get_average_number_of_likes_received_by_sex(simulation.SEX_MALE)
    median_amount_of_likes_male = sim.get_median_number_of_likes_received_by_sex(simulation.SEX_MALE)
    average_amount_of_likes_female = sim.get_average_number_of_likes_received_by_sex(simulation.SEX_FEMALE)
    median_amount_of_likes_female = sim.get_median_number_of_likes_received_by_sex(simulation.SEX_FEMALE)
    average_amount_of_matches_male = sim.get_average_number_of_matches_by_sex(simulation.SEX_MALE)
    median_amount_of_matches_male = sim.get_median_number_of_matches_by_sex(simulation.SEX_MALE)
    average_amount_of_matches_female = sim.get_average_number_of_matches_by_sex(simulation.SEX_FEMALE)
    median_amount_of_matches_female = sim.get_median_number_of_matches_by_sex(simulation.SEX_FEMALE)

    table_header = [
        html.Thead(html.Tr([html.Th(""), html.Th("Men"), html.Th("Women")]))
    ]
    row1 = html.Tr([html.Td("Number of likes received (average)", style={"width": "600px"}), html.Td(average_amount_of_likes_male), html.Td(average_amount_of_likes_female)])
    row2 = html.Tr([html.Td("Number of matches (average)"), html.Td(average_amount_of_matches_male), html.Td(average_amount_of_matches_female)])
    row3 = html.Tr([html.Td("Number of likes received (median)"), html.Td(median_amount_of_likes_male), html.Td(median_amount_of_likes_female)])
    row4 = html.Tr([html.Td("Number of matches (median)"), html.Td(median_amount_of_matches_male), html.Td(median_amount_of_matches_female)])

    table_body = [html.Tbody([row1, row2, row3, row4])]
    return dbc.Table(table_header + table_body, bordered=True)


def get_graph(index, title, highest_granularity):
    return html.Div([
        html.Br(),
        html.H6(title),
        # customize modebar see https://plotly.com/python/configuration-options/
        dcc.Graph(id={"type": "distribution_graph", "index": index},
                  config={
                      "displaylogo": False,
                      "modeBarButtonsToRemove": ["toImage", "lasso2d", "autoScale2d"],
                  }),
        html.Div(style={"height": "10px"}),
        dbc.Row([
            html.Div([
                "Granularity"
            ], className="col-2"),
            html.Div([
                html.Div(style={"height": "7px"}),
                dcc.Slider(min=1, max=min(100, highest_granularity), value=min(10, highest_granularity), step=1,
                           marks=None, tooltip={"placement": "bottom"},
                           id={"type": "granularity_slider", "index": index})
            ], className="col-9"),
            html.Div([
                html.Div(10, id={"type": "granularity_text", "index": index})
            ], className="col-1"),
        ]),
        html.Div(index, id={"type": "figure_index", "index": index}, style={"display": "none"})
    ], className="col-lg-6")


def get_layout_for_figures():
    return Layout(
        paper_bgcolor='rgba(148, 148, 148, 255)',
        plot_bgcolor='rgba(148, 148, 148, 255)'
    )


def get_results_div(sim):
    highest_granularity = min(sim.amount_men, sim.amount_women)
    return html.Div([
        html.Br(),
        html.Br(),
        html.H2("Results"),
        get_table(sim),
        dbc.Row([
            get_graph(DICT_KEY_AMOUNT_LIKES_RECEIVED, "Distribution of amount likes received", highest_granularity),
            get_graph(DICT_KEY_AMOUNT_MATCHES, "Distribution of amount matches", highest_granularity),
        ]),
        html.Br(),
    ])
