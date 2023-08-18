from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.graph_objs import Layout
import pandas as pd
from app.simulation import simulation
from app.simulation import utils

layout_for_figures = Layout(
    paper_bgcolor='rgba(148, 148, 148, 255)',
    plot_bgcolor='rgba(148, 148, 148, 255)'
)

def get_page():
    return html.Div([
        html.Br(),
        html.Div([
            html.H1("Dating Apps Simulation"),
        ], className="d-flex justify-content-center"),
        html.Hr(),
        html.Div([
            dbc.Row([
                html.Div([
                    html.Div(className="row-separator-top"),
                    dbc.Row([
                        html.Div([
                            html.Div("Amount of men:", className="input-fields-text")
                        ], className="col-9"),
                        html.Div([
                            dcc.Input(id="input_amount_of_men", value=500, type="number", min=0, max=1000000,
                                      className="input-fields-numbers"),
                        ], className="col-3")
                    ]),
                ], className="col-md-6"),
                html.Div([
                    html.Div(className="row-separator-top"),
                    dbc.Row([
                        html.Div([
                            html.Div("Amount of women:", className="input-fields-text")
                        ], className="col-9"),
                        html.Div([
                            dcc.Input(id="input_amount_of_women", value=500, type="number", min=0, max=9999999,
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
                            html.Div("Amount of women a man will see in the simulation:", className="input-fields-text")
                        ], className="col-9"),
                        html.Div([
                            dcc.Input(id="input_amount_of_women_a_man_will_see", value=100, type="number", min=0, max=9999999,
                                      className="input-fields-numbers"),
                        ], className="col-3")
                    ]),
                ], className="col-md-6"),
                html.Div([
                    html.Div(className="row-separator-top"),
                    dbc.Row([
                        html.Div([
                            html.Div("Amount of men a woman will see in the simulation:", className="input-fields-text")
                        ], className="col-9"),
                        html.Div([
                            dcc.Input(id="input_amount_of_men_a_woman_will_see", value=100, type="number", min=0, max=9999999,
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
                            html.Div("Maximum amount of likes for men:", className="input-fields-text")
                        ], className="col-9"),
                        html.Div([
                            dcc.Input(id="input_max_amount_of_likes_for_men", type="number", min=0, max=9999999, className="input-fields-numbers"),
                        ], className="col-3")
                    ]),
                ], className="col-md-6"),
                html.Div([
                    html.Div(className="row-separator-top"),
                    dbc.Row([
                        html.Div([
                            html.Div("Maximum amount of likes for women:", className="input-fields-text")
                        ], className="col-9"),
                        html.Div([
                            dcc.Input(id="input_max_amount_of_likes_for_women", type="number", min=0, max=9999999, className="input-fields-numbers"),
                        ], className="col-3")
                    ]),
                ], className="col-md-6")
            ]),
            dbc.Row([
                html.Div([
                    html.Div(className="row-separator-top"),
                    dbc.Row([
                        html.Div("Formula to determine attractivity for men:", className="input-fields-text")
                    ]),
                ], className="col-md-6"),
                html.Div([
                    html.Div(className="row-separator-top"),
                    dbc.Row([
                        html.Div("Formula to determine attractivity for women:", className="input-fields-text")
                    ]),
                ], className="col-md-6")
            ]),
            dbc.Row([
                html.Div([
                    html.Div(className="row-separator-top"),
                    dbc.Row([
                        html.Div([
                            dcc.Input(id="input_attractivity_function_for_men",
                                      value="Math.pow(x, 6.14)", className="input-fields-numbers"),
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
                                      value="Math.pow(x, 1.17)", className="input-fields-numbers"),
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
            html.Div(id="simulation_progress_status_text")
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


def get_results_div(sim):
    df_amount_likes_received = utils.get_distribution_amount_likes_received(sim)
    df_amount_matches = utils.get_distribution_amount_matches(sim)
    fig1 = px.bar(df_amount_likes_received, x="group_name", y=["men", "women"], barmode='group', title='x')
    fig1.layout = layout_for_figures
    fig2 = px.bar(df_amount_matches, x="group_name", y=["men", "women"], barmode='group', title='x')
    fig2.layout = layout_for_figures

    return html.Div([
        html.Br(),
        html.Br(),
        html.H2("Results"),
        get_table(sim),
        dbc.Row([
            html.Div([
                html.Br(),
                html.H6("Distribution of amount likes received"),
                dcc.Graph(figure=fig1),
                html.Div(style={"height": "10px"}),
                dbc.Row([
                    html.Div([
                        "Granularity"
                    ], className="col-2"),
                    html.Div([
                        html.Div(style={"height": "7px"}),
                        dcc.Slider(id="granularity_slider_for_fig1", min=1, max=20, value=10, step=1, marks=None, tooltip={"placement": "bottom"})
                    ], className="col-9"),
                    html.Div([
                        html.Div(10, id="granularity_text_for_fig1", style={"text-align": "end"})
                    ], className="col-1"),
                ])
            ], className="col-lg-6"),
            html.Div([
                html.Br(),
                html.H6("Distribution of amount matches"),
                dcc.Graph(figure=fig2),
                html.Div(style={"height": "10px"}),
                dbc.Row([
                    html.Div([
                        "Granularity"
                    ], className="col-2"),
                    html.Div([
                        html.Div(style={"height": "7px"}),
                        dcc.Slider(id="granularity_slider_for_fig1", min=1, max=20, value=10, step=1, marks=None, tooltip={"placement": "bottom"})
                    ], className="col-9"),
                    html.Div([
                        html.Div(10, id="granularity_text_for_fig1", style={"text-align": "end"})
                    ], className="col-1"),
                ])
            ], className="col-lg-6"),
        ]),
        html.Br(),
    ])