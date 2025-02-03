from dash import dcc, html, Input, Output, State, callback, ALL, MATCH, ctx, no_update
from app.dataHandler import DataHandler

year = 2019
data_handler = DataHandler(f"../data/processed_data/")

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11','12']
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

@callback(
    Output("athlete_streak", "children"),
    Output("athlete_avg_run_dist", "children"),
    Output("athlete_avg_run_per_week", "children"),
    Output("athlete_majors", "children"),
    Input("athlete_id_dropdown", "value")
)
def display_data_per_athlete(athlete_id):
    df_athlete = data_handler.get_data_per_athlete(athlete_id)
    longest_streak = df_athlete['longest_streak'].values
    avg_dist_per_week = df_athlete['avg_dist_per_week'].values
    total_distance = df_athlete['total_dist'].values
    return longest_streak, avg_dist_per_week, total_distance, None

@callback(
    Output("pace_distribution", "figure"),
    Input("athlete_id_dropdown", "value"),
    Input("distance_athlete_dropdown", "value"),
)
def plot_graph_pace_distribution(athlete_id, distance):
    figure = data_handler.get_fig_pace_distribution(athlete_id, distance)
    return figure

@callback(
    Output("weekly_distance", "figure"),
    Input("athlete_id_dropdown", "value"),
    Input("weekly_distance_slider", "value"),
)
def plot_graph_weekly_distance(athlete_id, distance):
    start_date = str(year)+"-"+months[distance[0]] + "-01"
    end_date = str(year)+"-"+months[distance[1]] + "-28"  # Approximate end of the month
    if athlete_id:
        figure = data_handler.get_fig_weekly_distance(athlete_id, start_date, end_date)
        return figure
    return no_update