from dash import Dash
import dash_bootstrap_components as dbc


app = Dash( 
        __name__, suppress_callback_exceptions=True, 
        external_stylesheets=[dbc.themes.BOOTSTRAP], 
        meta_tags=[{'name': 'viewport', 
                    'content': 'width=device-width, initial-scale=1.0'}]
                    #prevent_initial_callbacks=True
        )
#if __name__ == '__main__':
#    app.run_server(debug=True)