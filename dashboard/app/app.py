from dash import Dash, html, dcc
import app.callback
import dash_ag_grid as dag



# Initialize the app
dash_app = Dash(__name__)
dash_app.config["suppress_callback_exceptions"] = True

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11','12']
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

column_defs_all_time = [
  {'headerName': 'Athlete', 'field': 'athlete'}, 
  {'headerName': 'Time', 'field': 'duration'}, 
  {'headerName': 'Age group', 'field': 'age_group'}, 
  {'headerName': 'Country', 'field': 'country'}, 
  {'headerName': 'Pace', 'field': 'pace_str'}
]

dash_app.layout = html.Div([
  html.Div([ # HEADER
      html.Label(["Big Data Project"], className='h3')
  ], className="w-100 bg-dark p-2 text-light"),
  html.Div( # CONTENT
      className='row w-100 m-0',
      children=[
          html.Div(
              className='col-4 h-100 p-2',
              children=[
                  html.Div(
                      className="bg-secondary-subtle", #bg-light", 
                      children=[
                          html.Div(
                              className="text-center pb-3",
                              children=[
                                  html.Label(["GLOBAL"], className="h2")
                              ]
                          ),
                          html.Div(className='row m-0', children=[
                            html.Label(className="p-3 pb-1", children=["Athletes repartion per country"])
                          ]),
                          html.Div(className='row m-0', children=[
                            html.Div(style={'height': '30vh'}, className='col-md-7 p-0', children=[
                              dcc.Graph(id='athletes_nb_per_country', className='h-100')
                            ]),
                            html.Div(className="col-md-5", children=[
                              dag.AgGrid(
                                id="athlete_nb_per_country",
                                columnDefs=[{"headerName": "Country", "field": "country"},{"headerName": "Athlete number", "field": "runner_nb_per_country"}],
                                defaultColDef={"sortable": True, "filter": True, "resizable": False, "filter": False},
                                className="ag-theme-alpine compact font",
                                columnSize="responsiveSizeToFit",
                                style={"height": 190}
                              )
                            ])
                          ]),
                          html.Div(className='row m-0', children=[
                            html.Label(className="p-3 pb-1", children=["Global Running Participation"])
                          ]),
                          html.Div(className="col-md-12 px-5 pb-2", children=[
                            dag.AgGrid(
                              id="athlete_prop_pop_country",
                              columnDefs=[
                                {"headerName": "Country", "field": "country"},
                                {
                                  "headerName": "Flag",
                                  "field": "flag_filename",
                                  "cellRenderer": "svgRenderer", 
                                },
                                {"headerName": "Prop of the population running", "field": "runner_proportion"}
                              ],
                              defaultColDef={"sortable": True, "filter": True, "resizable": False, "filter": False},
                              className="ag-theme-alpine compact font",
                              columnSize="responsiveSizeToFit",
                              style={"height": 150}
                            )
                          ]),
                          # html.Div(className="row m-0 p-3", children=[
                          #   dcc.Dropdown(id="country-dropdown", options=["USA"], value="USA")
                          # ]),
                          # html.Div(className="row m-0 ", children=[
                          #   html.Div(className='col-md-6 p-1 d-flex flex-column text-center', children=[
                          #     html.Label(['Longest running streak'], className='custom-font-size'),
                          #     html.Label(id="", className='custom-font-size')
                          #   ]),
                          #   html.Div(className='col-md-6 p-1 d-flex flex-column text-center', children=[
                          #     html.Label(['Avg run distance per week'], className='custom-font-size'),
                          #     html.Label(id="", className='custom-font-size')
                          #   ]),
                          #   html.Div(className='col-md-6 p-1 d-flex flex-column text-center', children=[
                          #     html.Label(['Avg run distance per week'], className='custom-font-size'),
                          #     html.Label(id="", className='custom-font-size')
                          #   ]),
                          #   html.Div(className='col-md-6 p-1 d-flex flex-column text-center', children=[
                          #     html.Label(['Avg run distance per week'], className='custom-font-size'),
                          #     html.Label(id="", className='custom-font-size')
                          #   ]),
                          # ]),
                          html.Div(className='row m-0', children=[
                            html.Label(className="p-3 pb-1", children=["Athletes repartion per age group"])
                          ]),
                          html.Div(className='row m-0 pb-4', children=[
                            html.Div(style={'height': '20vh'}, className='col-md-7 p-0', children=[
                              dcc.Graph(id='athletes_prop_per_age_group', className='h-100')
                            ]),
                            html.Div(className="col-md-5", children=[
                              dag.AgGrid(
                                id="athlete_prop_per_age_group",
                                columnDefs=[{"headerName": "Age group", "field": "age_group"},{"headerName": "Count", "field": "count"}],
                                defaultColDef={"sortable": True, "filter": True, "resizable": False, "filter": False},
                                className="ag-theme-alpine compact font",
                                columnSize="responsiveSizeToFit",
                                style={"height": 100}
                              )
                            ])
                          ]),
                      ]
                  )
              
              ]
          ),
          html.Div(
              className='col-4 h-100 p-2',
              children=[
                html.Div(
                      className="bg-secondary-subtle", #bg-light", 
                      children=[
                          html.Div(
                              className="text-center pb-3",
                              children=[
                                  html.Label(["ALL TIME PERFORMANCES"], className="h2")
                              ]
                          ),
                          html.Div(className="row m-0 px-3 pb-0 display-flex align-center", children=[
                            html.Label(["Distance : "], className='col-md-2 p-0'),
                            html.Div([
                              dcc.Dropdown(id="distance_all_time_dropdown", options=[1.0,1.5,2.0,3.0,5.0,10.0,21.0975,42.195,50.0,100.0], value=10.0)
                            ], style={'width': 100}, className='m-0 p-0')
                          ]),
                          html.Div(className='row m-0', children=[
                              html.Label(className="p-3 pb-1", children=["20 best performances of male athletes"])
                            ]),
                          html.Div(className='row m-0', children=[
                            html.Div(className='col-md-12 py-2 px-2', children=[
                              dag.AgGrid(
                                id="all_time_perf_male_grid",
                                # rowData=df.to_dict("records"),
                                columnDefs=column_defs_all_time,
                                defaultColDef={"sortable": True, "filter": True, "resizable": False, "filter": False},
                                className="ag-theme-alpine compact font",
                                columnSize="responsiveSizeToFit",
                                style={"height": 160}
                              )
                            ]),
                            html.Div(className='row m-0', children=[
                              html.Label(className="p-3 pb-1", children=["20 best performances of female athletes"])
                            ]),
                            html.Div(className='col-md-12 py-2 px-2', children=[
                              dag.AgGrid(
                                id="all_time_perf_female_grid",
                                # rowData=df.to_dict("records"),
                                columnDefs=column_defs_all_time,
                                defaultColDef={"sortable": True, "filter": True, "resizable": False, "filter": False},
                                className="ag-theme-alpine compact font",
                                columnSize="responsiveSizeToFit",
                                style={"height": 160}
                              )
                            ]),
                            html.Div(className='row m-0', children=[
                              html.Div(className='col-md-6 text-center', children=[
                                html.Label(className="p-3 pb-1", children=["Country representation among world records"])
                              ]),
                              html.Div(className='col-md-6 text-center', children=[
                                html.Label(className="p-3 pb-1", children=["Country representation among best performances"])
                              ]),
                            ]),
                            html.Div(className='col-md-6 pt-2 px-3 pb-4', children=[
                              dag.AgGrid(
                                id="country_representation_wr",
                                # rowData=df.to_dict("records"),
                                columnDefs=[
                                  {"headerName": "Country", "field": "country"},
                                  {
                                      "headerName": "Flag",
                                      "field": "flag_filename",
                                      "cellRenderer": "svgRenderer", 
                                  },
                                  {"headerName": "Athlete nb", "field": "athlete"}
                                ],
                                className="ag-theme-alpine compact font",
                                columnSize="responsiveSizeToFit",
                                defaultColDef={"cellRenderer": "markdown", "sortable": True, "filter": True, "resizable": False, "filter": False},
                                style={"height": 150},
                                dangerously_allow_code=True
                              )
                            ]),
                            html.Div(className='col-md-6 pt-2 px-3 pb-4', children=[
                              dag.AgGrid(
                                id="country_representation_best_perf",
                                columnDefs=[
                                  {"headerName": "Country", "field": "country"},
                                  {
                                      "headerName": "Flag",
                                      "field": "flag_filename",
                                      "cellRenderer": "svgRenderer", 
                                  },
                                  {"headerName": "Athlete nb", "field": "athlete"}
                                ],
                                defaultColDef={"sortable": True, "filter": True, "resizable": False, "filter": False},
                                className="ag-theme-alpine compact font",
                                columnSize="responsiveSizeToFit",
                                style={"height": 150}
                              )
                            ]),
                          ])
                      ]
                  )
              ]
          ),
          html.Div(
              className='col-4 h-100 p-2',
              children=[
                html.Div(
                      className="bg-secondary-subtle", #bg-light", 
                      children=[
                          html.Div(
                              className="text-center pb-3",
                              children=[
                                  html.Label(["INDIVIDUAL"], className="h2")
                              ]
                          ),
                          html.Div(
                              className="", 
                              children=[
                                html.Div(className="row m-0 px-3 pb-3", children=[
                                  html.Label(["Athlete id : "], className='col-md-2 p-0'),
                                  html.Div([
                                    dcc.Dropdown(id="athlete_id_dropdown", options=[1, 2, 3, 4, 5, 6, 7, 8 ,9 ,10], value=1)
                                  ], style={'width': 100}, className='m-0 p-0'),
                                ]),
                                html.Div(className="row m-0 ", children=[
                                  html.Div(className='col-md-6 p-1 d-flex flex-column text-center', children=[
                                    html.Label(['Longest running streak'], className='custom-font-size'),
                                    html.Label(id="athlete_streak", className='custom-font-size')
                                  ]),
                                  html.Div(className='col-md-6 p-1 d-flex flex-column text-center', children=[
                                    html.Label(['Total distance'], className='custom-font-size'),
                                    html.Label(id="athlete_avg_run_per_week", className='custom-font-size')
                                  ]),
                                  html.Div(className='col-md-6 p-1 d-flex flex-column text-center', children=[
                                    html.Label(['Avg distance per week'], className='custom-font-size'),
                                    html.Label(id="athlete_avg_run_dist", className='custom-font-size')
                                  ]),
                                  html.Div(className='col-md-6 p-1 d-flex flex-column text-center', children=[
                                    html.Label(['Average run distance'], className='custom-font-size'),
                                    html.Label(id="athlete_majors", className='custom-font-size')
                                  ]),
                                ]),
                                html.Div(className="row m-0 px-3 pb-3 pt-3", children=[
                                  html.Label(["Distance : "], className='col-md-2 p-0'),
                                  html.Div([
                                    dcc.Dropdown(id="distance_athlete_dropdown", options=[5.0,10.0,21.0975,42.195,50.0,100.0], value=10.0)
                                  ], style={'width': 100}, className='m-0 p-0'),
                                ]),
                                html.Div(className="row m-0 p-0", children=[
                                  html.Div(style={'height': '30vh'}, className='p-0', children=[
                                    dcc.Graph(id='pace_distribution', className='h-100')
                                  ])
                                ]),
                                html.Div(className="row m-0", children=[
                                  html.Div(style={'height': '25vh'}, className='p-0', children=[
                                    dcc.Graph(id='weekly_distance', className='h-100')
                                  ]),
                                  html.Div([
                                    dcc.RangeSlider(
                                      id='weekly_distance_slider',
                                      min=0,
                                      max=len(months)-1,
                                      step=1,
                                      marks={i: label for i, label in enumerate(month_labels)},
                                      value=[4, 9]
                                    ),
                                  ])
                                ])
                            ]
                          ),
                      ]
                  )
              ]
          ),
      ]
  ),
  dcc.Location(id='url', refresh=False),
], className='fluid-container', style={'height': '100vh'})

if __name__ == '__main__':
  dash_app.run(debug=True)