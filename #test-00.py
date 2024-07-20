import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table

df = pd.DataFrame(
    [
        ["California", 289, 4395, 15.3, 10826],
        ["Arizona", 48, 1078, 22.5, 2550],
        ["Nevada", 11, 238, 21.6, 557],
        ["New Mexico", 33, 261, 7.9, 590],
        ["Colorado", 20, 118, 5.9, 235],
    ],
    columns=["State", "# Solar Plants", "MW", "Mean MW/Plant", "GWh"],
)
app = dash.Dash('example')

app.layout = html.Div([
    dcc.Dropdown(
        id = 'dropdown-to-show_or_hide-element',
        options=[
            {'label': 'Show element', 'value': 'on'},
            {'label': 'Hide element', 'value': 'off'}
        ],
        value = 'on'
    ),

    # Create Div to place a conditionally visible element inside
    html.Div([
    dash_table.DataTable(
        id="element-to-hide",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        export_format="csv",)
        ], style= {'display': 'block'} # <-- This is the line that will be changed by the dropdown callback
        )
    ])

@app.callback(
   Output(component_id='element-to-hide', component_property='style'),
   [Input(component_id='dropdown-to-show_or_hide-element', component_property='value')])

def show_hide_element(visibility_state):
    if visibility_state == 'on':
        return {'display': 'block'}
    if visibility_state == 'off':
        return {'display': 'none'}

if __name__ == '__main__':
    app.run_server(debug=True)