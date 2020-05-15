import dash
import dash_core_components as dcc
import dash_html_components as html
import mysql.connector as mysql
import pandas as pd
import csv

df = pd.read_csv('Exercises.csv')

with open('Exercises.csv') as f:
    values = [tuple(line) for line in csv.reader(f)]

db = mysql.connect(
    host="localhost",
    user="root",
    passwd="bunny564",
    database='Summer_Project'
)

cursor = db.cursor()

query = "SELECT name FROM Exercises"

cursor.execute(query)

records = cursor.fetchall()
x_values = []
for record in records:
    x_values.append(record)

app = dash.Dash()

# Define HTML Componenet
app.layout = html.Div(children=[
    html.H1('Dash tutorials'),
    dcc.Graph(id='example',
              figure={
                  'data': [
                      {'x': x_values, 'y': [5, 6, 7, 2, 1], 'type': 'line', 'name': 'names'},

                  ],
                  'layout': {
                      'title': 'Basic Dash Example'
                  }
              })
])

if __name__ == '__main__':
    app.run_server(debug=True)
