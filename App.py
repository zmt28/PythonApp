# Import Libraries
import csv
import urllib
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import mysql.connector as mysql
import pandas as pd
from dash.dependencies import Input, Output, State

# read CSV file into dataframe
df = pd.read_csv('Exercises.csv')

# Turn dataframe into list of tuples
with open('Exercises.csv') as f:
    values = [tuple(line) for line in csv.reader(f)]

    # Connect to mysql database
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd="bunny564",
        database='Summer_Project'
    )
    # Initialize Cursor
    cursor = db.cursor()

    # Query 'name' column
    query = "SELECT * FROM Exercises"

    cursor.execute(query)
records = cursor.fetchall()

app = dash.Dash(suppress_callback_exceptions=True)
header = dcc.Markdown('🏃🚴 Workout Dashboard 🏋️💪')
# Define HTML Component
app.layout = html.Div([
    html.H1(header, style={'textAlign': 'center'}),

    dcc.Dropdown(id="dropdown", options=[
        {'label': 'Abdominals', 'value': ' abdominals'},
        {'label': 'Abductors', 'value': ' adductors'},
        {'label': 'Quadriceps', 'value': ' quadriceps'},
        {'label': 'Shoulders', 'value': ' shoulders'},
        {'label': 'Chest', 'value': ' chest'},
        {'label': 'Biceps', 'value': ' biceps'},
        {'label': 'Calves', 'value': ' calves'},
        {'label': 'Glutes', 'value': ' glutes'},
        {'label': 'Middle back', 'value': ' middle back'},
        {'label': 'Hamstrings', 'value': ' hamstrings'},
        {'label': 'Lower back', 'value': ' lower back'}
    ],
                 multi=True,
                 style={
                     'color': 'Primary'
                 },
                 value='abdominals',
                 placeholder='Select Muscle Groups'
                 ),
    dcc.Input(
        id="input2", type="number", placeholder="# of Days Per Week", min=1, max=7
    ),

    html.Button(id='submit-button',
                children='Submit'
                ),

    html.Div([html.P(' ')
                 , html.A('Download CSV', id='my-link', download="data.csv",
                          href="",
                          target="_blank")
              ]),

    dash_table.DataTable(
        id="Workout",
        columns=[{'name': i, 'id': i} for i in df.columns],
        style_as_list_view=True,
        style_data={'border': '1px solid blue'},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(230, 230, 230)'}
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'border': '1px solid blue'
        },
        style_cell={
            'height': 'auto',
            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
            'whiteSpace': 'normal',
            'textAlign': 'center'},
    ),
    dash_table.DataTable(
        id='table',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('records'),
        style_as_list_view=True,
        page_size=10,
        filter_action='native',
        style_data={'border': '1px solid blue',
                    },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'}
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'border': '1px solid blue'
        },
        style_cell={
            'height': 'auto',
            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
            'whiteSpace': 'normal',
            'textAlign': 'left'}
    )
])


@app.callback(
    Output('Workout', 'data'),
    [Input('submit-button', 'n_clicks')],
    [State('dropdown', 'value'),
     State('input2', 'value')])
def create_workout(n_clicks, dropdown, input2):
    if n_clicks is not None:
        dff = pd.DataFrame(df[df['muscle'].isin(dropdown)])
        dff = dff.head(input2 *5)
        return dff.to_dict('records')


@app.callback(
    Output('my-link', 'href'),
    [Input('submit-button', 'n_clicks')],
    [State('dropdown', 'value')])
def csv_dwn(n_clicks, value):
    if n_clicks is not None:
        dff = pd.DataFrame(df[df['muscle'].isin(value)])
        csv_string = dff.to_csv(index=False, encoding='utf-8')
        csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + urllib.parse.quote(csv_string)
        return csv_string


if __name__ == '__main__':
    app.run_server(debug=True)
