# Import Libraries
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import mysql.connector as mysql
import pandas as pd
import csv

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
query = "SELECT muscle, COUNT(*) FROM Exercises GROUP BY muscle"

cursor.execute(query)
records = cursor.fetchall()

# Iterate through 'name' column
x_values = []
y_values = []
for record in records:
    x_values.append(record[0])
    y_values.append(record[1])

app = dash.Dash()

# Define HTML Component
app.layout = html.Div(children=[
    html.H1('Workout Dashboard', style={'textAlign': 'center'}),
    dcc.Graph(id='example',
              figure={
                  'data': [
                      {'x': x_values, 'y': y_values, 'type': 'bar', 'name': 'muscle groups'},

                  ],
                  'layout': {
                      'title': 'Exercises per Muscle Group'
                  }
              }),
    dash_table.DataTable(
        id='table',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('records'),
        style_as_list_view=True,
        page_size=10,
        filter_action='native',
        filter_query='',
        style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
        style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold',
        'textAlign': 'center'
    },
        style_cell={
        'height': 'auto',
        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
        'whiteSpace': 'normal',
        'textAlign': 'left'}
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
