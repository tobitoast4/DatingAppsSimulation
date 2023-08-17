from dash import html, dcc
import dash_bootstrap_components as dbc

def get_table():
    table_header = [
        html.Thead(html.Tr([html.Th(""), html.Th("Men"), html.Th("Women")]))
    ]

    row1 = html.Tr([html.Td("Number of likes (average)"), html.Td("50.1"), html.Td("12.5")])
    row2 = html.Tr([html.Td("Number of likes (median)"), html.Td(""), html.Td("")])
    row3 = html.Tr([html.Td("Number of matches (average)"), html.Td("6.26"), html.Td("3.12")])
    row4 = html.Tr([html.Td("Number of matches (median)"), html.Td(""), html.Td("")])

    table_body = [html.Tbody([row1, row2, row3, row4])]

    return dbc.Table(table_header + table_body, bordered=True)


def get_page():
    return html.Div([
        html.Br(),
        html.Div([
            html.H1("Dating Simulation"),
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
                            dcc.Input(id="input1", value=500, type="number", min=0, max=10000,
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
                            dcc.Input(id="input2", value=500, type="number", min=0, max=10000,
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
                            html.Div("Amount of women a men will see in the simulation:", className="input-fields-text")
                        ], className="col-9"),
                        html.Div([
                            dcc.Input(id="input11", value=100, type="number", min=0, max=10000,
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
                            dcc.Input(id="input21", value=100, type="number", min=0, max=10000,
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
                            dcc.Input(id="input111", type="number", min=0, max=10000, className="input-fields-numbers"),
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
                            dcc.Input(id="input211", type="number", min=0, max=10000, className="input-fields-numbers"),
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
            dbc.Progress(value=80, id="animated-progress", animated=True, striped=True),
        ]),
        html.Br(),
        get_table()
    ])