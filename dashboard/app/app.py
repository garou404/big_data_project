from dash import Dash, html, dcc
import app.callback
import dash_ag_grid as dag



# Initialize the app
dash_app = Dash(__name__)
dash_app.config["suppress_callback_exceptions"] = True

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11','12']
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

column_defs_all_time = ['athlete', 'duration', 'age_group', 'country', 'pace_str']

dash_app.layout = html.Div([
  html.Div([ # HEADER
      html.Label(["Big Data Project"])
  ], className="w-100 bg-dark p-3 text-light"),
  html.Div( # CONTENT
      className='row w-100 m-0',
      children=[
          html.Div(
              className='col-4 bg-primary-subtle h-100 p-2',
              children=[
                  html.Div(
                      className="bg-light", 
                      children=[
                          html.Div(
                              className="text-center pb-3",
                              children=[
                                  html.Label(["GLOBAL"], className="h2")
                              ]
                          ),
                          html.Div(
                              className="", 
                              children=["other section 1"]
                          ),
                          html.Div(
                              className="", 
                              children=["other section 2"]
                          ),
                          html.Div(
                              className="", 
                              children=["other section 3"]
                          ),
                      ]
                  )
              
              ]
          ),
          html.Div(
              className='col-4 bg-success-subtle h-100 p-2',
              children=[
                html.Div(
                      className="bg-light", 
                      children=[
                          html.Div(
                              className="text-center pb-3",
                              children=[
                                  html.Label(["ALL TIME PERFORMANCES"], className="h2")
                              ]
                          ),
                          html.Div(className="row m-0 p-3", children=[
                            dcc.Dropdown(id="distance_all_time_dropdown", options=[1.0,1.5,2.0,3.0,5.0,10.0,21.0975,42.195,50.0,100.0], value=10.0)
                          ]),
                          html.Div(className='row m-0', children=[
                            html.Div(className='col-md-12 py-1 px-2', children=[
                              dag.AgGrid(
                                id="all_time_perf_male_grid",
                                # rowData=df.to_dict("records"),
                                columnDefs=[{"headerName": col, "field": col} for col in column_defs_all_time],
                                defaultColDef={"sortable": True, "filter": True, "resizable": False, "filter": False},
                                className="ag-theme-alpine compact font",
                                columnSize="responsiveSizeToFit",
                                style={"height": 140}
                              )
                            ]),
                            html.Div(className='col-md-12 py-1 px-2', children=[
                              dag.AgGrid(
                                id="all_time_perf_female_grid",
                                # rowData=df.to_dict("records"),
                                columnDefs=[{"headerName": col, "field": col} for col in column_defs_all_time],
                                defaultColDef={"sortable": True, "filter": True, "resizable": False, "filter": False},
                                className="ag-theme-alpine compact font",
                                columnSize="responsiveSizeToFit",
                                style={"height": 140}
                              )
                            ]),
                            html.Div(className='col-md-6 py-1 px-2', children=[
                              dag.AgGrid(
                                id="country_representation_wr",
                                # rowData=df.to_dict("records"),
                                columnDefs=[
                                  {"headerName": "Country", "field": "country"},
                                  {
                                      "headerName": "Flag",
                                      "field": "flag_filename",
                                      "cellRenderer": "svgRenderer",  # Custom cell renderer
                                  },
                                  {"headerName": "athlete nb", "field": "athlete"}
                                ],
                                className="ag-theme-alpine compact font",
                                columnSize="responsiveSizeToFit",
                                defaultColDef={"cellRenderer": "markdown", "sortable": True, "filter": True, "resizable": False, "filter": False},
                                style={"height": 140},
                                dangerously_allow_code=True
                              )
                            ]),
                            html.Div(className='col-md-6 py-1 px-2', children=[
                              dag.AgGrid(
                                id="country_representation_best_perf",
                                # rowData=df.to_dict("records"),
                                columnDefs=[{"headerName": col, "field": col} for col in column_defs_all_time],
                                defaultColDef={"sortable": True, "filter": True, "resizable": False, "filter": False},
                                className="ag-theme-alpine compact font",
                                columnSize="responsiveSizeToFit",
                                style={"height": 140}
                              )
                            ]),
                          ])
                      ]
                  )
              ]
          ),
          html.Div(
              className='col-4 bg-warning-subtle h-100 p-2',
              children=[
                html.Div(
                      className="bg-light", 
                      children=[
                          html.Div(
                              className="text-center pb-1",
                              children=[
                                  html.Label(["INDIVIDUAL"], className="h2")
                              ]
                          ),
                          html.Div(
                              className="", 
                              children=[
                                html.Div(className="row m-0 px-3 pb-2", children=[
                                  dcc.Dropdown(id="athlete_id_dropdown", options=[1, 2, 3, 4, 5, 6, 7, 8 ,9 ,10], value=1)
                                ]),
                                html.Div(className="row m-0 ", children=[
                                  html.Div(className='col-md-6 p-1 d-flex flex-column text-center', children=[
                                    html.Label(['longest running streak'], className='custom-font-size'),
                                    html.Label(id="athlete_streak", className='custom-font-size')
                                  ]),
                                  html.Div(className='col-md-6 p-1 d-flex flex-column text-center', children=[
                                    html.Label(['avg run distance per week'], className='custom-font-size'),
                                    html.Label(id="athlete_avg_run_dist", className='custom-font-size')
                                  ]),
                                  html.Div(className='col-md-6 p-1 d-flex flex-column text-center', children=[
                                    html.Label(['avg run distance per week'], className='custom-font-size'),
                                    html.Label(id="athlete_avg_run_per_week", className='custom-font-size')
                                  ]),
                                  html.Div(className='col-md-6 p-1 d-flex flex-column text-center', children=[
                                    html.Label(['avg run distance per week'], className='custom-font-size'),
                                    html.Label(id="athlete_majors", className='custom-font-size')
                                  ]),
                                ]),
                                html.Div(className="row m-0 px-3 py-1", children=[
                                  dcc.Dropdown(id="distance_athlete_dropdown", options=[5.0,10.0,21.0975,42.195,50.0,100.0], value=10.0)
                                ]),
                                html.Div(className="row m-0 p-0", children=[
                                  html.Div(style={'height': '30vh'}, className='p-0', children=[
                                    dcc.Graph(id='pace_distribution', className='h-100')
                                  ])
                                ]),
                                html.Div(className="row m-0", children=[
                                  html.Div(style={'height': '30vh'}, className='p-0', children=[
                                    dcc.Graph(id='weekly_distance', className='h-100')
                                  ]),
                                  html.Div([
                                    dcc.RangeSlider(
                                        id='weekly_distance_slider',
                                        min=0,
                                        max=len(months)-1,
                                        step=1,
                                        marks={i: label for i, label in enumerate(month_labels)},
                                        value=[0, len(months)-1]
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