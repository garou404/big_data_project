from dash import Dash, html, dcc
import app.callback


# Initialize the app
dash_app = Dash(__name__)
dash_app.config["suppress_callback_exceptions"] = True

dash_app.layout = html.Div([

], className='fluid-container d-flex h-100')

if __name__ == '__main__':
    dash_app.run(debug=True)