import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html

# Load in the data for charging points, vehicles, and the merged data
df_charging_point_melt = pd.read_csv("df_charging_point_melt.csv")  # Task 1
df_vehicle_melt = pd.read_csv("df_vehicle_melt.csv")  # Task 2

column_types = {'ONS Code [note 6]': str,
                'ONS Geography [note 6]': str,
                'value_x': float,
                'Local Authority / Region Code': str,
                'Local Authority / Region Name': str,
                'value_y': float}

merged_df = pd.read_csv("merged_df.csv", dtype=column_types, parse_dates=['date', 'time'])  # Task 3

# Create a new column 'ratio' that is the ratio of charging points to vehicles
merged_df['ratio'] = merged_df['value_y'] / merged_df['value_x']
merged_df['date'] = pd.to_datetime(merged_df['date'], errors='coerce')

app = dash.Dash(__name__)

# 1. Create the first graph using px.line and store it in a variable
fig_charging_points = px.line(df_charging_point_melt, x="time", y="value", color='Local Authority / Region Name',
                              labels={
                                  "time": "Date (in quarters)",
                                  "value": "Charging points per 100,000 population",
                                  "Local Authority / Region Name": "Local Authority / Region Name"
                              },
                              title="Charging points per 100,000 population over Time")

# 2. Create the second graph using px.line and store it in a variable
fig_electric_cars = px.line(df_vehicle_melt.dropna(), x="date", y="value", color='ONS Geography [note 6]',
                            labels={
                                "date": "Date (in quarters)",
                                "value": "Charging points per 100,000 population",
                                "ONS Geography [note 6]": "Local Authority / Region Name"
                            },
                            title="Number of electric vehicles registered over Time")

# 3. Create the third graph using px.line and store it in a variable
fig_ratio = px.line(merged_df.dropna(), x="date", y="ratio", color='ONS Geography [note 6]',
                    labels={
                        "date": "Date (in quarters)",
                        "ratio": "Total Number of Charge Points per Electric Cars",
                        "ONS Geography [note 6]": "Local Authority / Region Name"
                    },
                    title="Total Number of Charge Points per Electric Cars over Time")

app.layout = html.Div([
    # Use dcc.Graph to display the first graph
    dcc.Graph(
        id='charging-points-graph',
        figure=fig_charging_points
    ),
    # Use dcc.Graph to display the second graph
    dcc.Graph(
        id='electric-cars-graph',
        figure=fig_electric_cars
    ),
    # Use dcc.Graph to display the third graph
    dcc.Graph(
        id='ratio-graph',
        figure=fig_ratio
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)