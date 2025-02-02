from dash import Dash, html, dcc
import app.callback


# Initialize the app
dash_app = Dash(__name__)
dash_app.config["suppress_callback_exceptions"] = True

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
              className='col-4 bg-warning-subtle h-100 p-2',
              children=[
                html.Div(
                      className="bg-light", 
                      children=[
                          html.Div(
                              className="text-center pb-3",
                              children=[
                                  html.Label(["INDIVIDUAL"], className="h2")
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
      ]
  )
], className='fluid-container', style={'height': '100vh'})

if __name__ == '__main__':
  dash_app.run(debug=True)