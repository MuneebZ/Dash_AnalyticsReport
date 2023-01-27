import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load in the data for charging points, vehicles, and the merged data
df_charging_point_melt = pd.read_csv(
    "data/df_charging_point_melt.csv")  # Task 1
df_vehicle_melt = pd.read_csv("data/df_vehicle_melt.csv")  # Task 2

column_types = {'ONS Code [note 6]': str,
                'ONS Geography [note 6]': str,
                'value_x': float,
                'Local Authority / Region Code': str,
                'Local Authority / Region Name': str,
                'value_y': float}

merged_df = pd.read_csv("data/merged_df.csv", dtype=column_types,
                        parse_dates=['date', 'time'])  # Task 3

# Create a new column 'ratio' that is the ratio of charging points to vehicles
merged_df['ratio'] = merged_df['value_y'] / merged_df['value_x']
merged_df['date'] = pd.to_datetime(merged_df['date'], errors='coerce')

# Create the Dash app

app = dash.Dash()

# Create the layout

app.layout = html.Div([
    # Task 1
    html.Div(children=[
        html.H1(
            children='Lower-tier local authorities ranked by highest number of charging points per 100,000 population',
            style={'text-align': 'center',
                   'text-shadow': '1px 1px #000001',
                   'font-size': '3em',
                   'color': '#16447E',
                   'letter-spacing': '1px',
                   'font-family': 'Arial, sans-serif',
                   'line-height': '1.2',
                   'margin': '50px 0'}),
        dcc.Dropdown(id='council-dropdown-1',
                     options=[{'label': i, 'value': i}
                              for i in df_charging_point_melt.sort_values(by='value', ascending=False)[
                                  'Local Authority / Region Name'].unique()],
                     value='Wandsworth'),
        dcc.Graph(id='task-1')
    ]),

    # Task 2
    html.Div(children=[
        html.H1(children='Lower-tier local authorities ranked by highest number of electric vehicles registered',
                style={'text-align': 'center',
                       'text-shadow': '1px 1px #000001',
                       'font-size': '3em',
                       'color': '#16447E',
                       'letter-spacing': '1px',
                       'font-family': 'Arial, sans-serif',
                       'line-height': '1.2',
                       'margin': '50px 0'}),
        dcc.Dropdown(id='council-dropdown-2',
                     options=[{'label': i, 'value': i}
                              for i in df_vehicle_melt.sort_values(by='value', ascending=False)[
                                  'ONS Geography [note 6]'].unique()],
                     value='Lambeth'),
        dcc.Graph(id='task-2')
    ]),

    # Task 3
    html.Div(children=[
        html.H1(
            children='Lower-tier local authorities ranked by highest total number of charge point/electric cars ratio',
            style={'text-align': 'center',
                   'text-shadow': '1px 1px #000001',
                   'font-size': '3em',
                   'color': '#16447E',
                   'letter-spacing': '1px',
                   'font-family': 'Arial, sans-serif',
                   'line-height': '1.2',
                   'margin': '50px 0'}),
        dcc.Dropdown(id='council-dropdown-3',
                     options=[{'label': i, 'value': i}
                              for i in
                              merged_df.sort_values(by='ratio', ascending=False)['ONS Geography [note 6]'].unique()],
                     value='Wandsworth'),
        dcc.Graph(id='task-3')
    ])
])


# Task 1 callback
@app.callback(
    Output(component_id='task-1', component_property='figure'),
    Input(component_id='council-dropdown-1', component_property='value')
)
def update_graph_1(selected_region):
    # 1. Create the first graph using px.line and store it in a variable
    filtered_df_charging_point_melt = df_charging_point_melt[
        df_charging_point_melt['Local Authority / Region Name'] == selected_region]

    fig_charging_points = px.line(filtered_df_charging_point_melt, x="time", y="value",
                                  color='Local Authority / Region Name',
                                  labels={
                                      "time": "Date (in quarters)",
                                      "value": "Charging points per 100,000 population",
                                      "Local Authority / Region Name": "Local Authority / Region Name"
                                  },
                                  title="Charging points per 100,000 population over Time")

    return fig_charging_points


# Task 2 callback
@app.callback(
    Output(component_id='task-2', component_property='figure'),
    Input(component_id='council-dropdown-2', component_property='value')
)
def update_graph_2(selected_region):
    # 2. Create the second graph using px.line and store it in a variable
    filtered_df_charging_point_melt = df_vehicle_melt[
        df_vehicle_melt['ONS Geography [note 6]'] == selected_region]
    fig_electric_cars = px.histogram(filtered_df_charging_point_melt, x="date", y="value", color='ONS Geography [note 6]',
                                     barmode="group",
                                     labels={
                                         "date": "Date (in quarters)",
                                         "value": "Charging points per 100,000 population",
                                         "ONS Geography [note 6]": "Local Authority / Region Name"
                                     },
                                     title="Number of electric vehicles registered over Time", )

    fig_electric_cars.update_layout(bargap=0.2)

    return fig_electric_cars


# Task 3 callback
@app.callback(
    Output(component_id='task-3', component_property='figure'),
    Input(component_id='council-dropdown-3', component_property='value')
)
def update_graph_3(selected_region):
    # 3. Create the third graph using px.line and store it in a variable
    filtered_merged_df = merged_df[
        merged_df['ONS Geography [note 6]'] == selected_region]

    filtered_merged_df['ratio_norm'] = filtered_merged_df['ratio'] / 100000

    fig_ratio = px.line(filtered_merged_df.dropna(), x="date", y="ratio_norm", color='ONS Geography [note 6]',
                        # barmode="group",
                        labels={
                            "date": "Date (in quarters)",
                            "ratio_norm": "Total Number of Charge Points per Electric Cars",
                            "ONS Geography [note 6]": "Local Authority / Region Name"
    },
        title="Total Number of Charge Points per Electric Cars over Time")

    # fig_ratio.update_layout(bargap=0.2)

    return fig_ratio


# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)
