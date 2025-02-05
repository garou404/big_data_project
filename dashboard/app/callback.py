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
    avg_dist_per_week = df_athlete['avg_dist_per_week'].values[0]
    total_distance = df_athlete['total_dist'].values[0]
    average_run_distance = df_athlete['avg_run_dist'].values[0]
    return longest_streak, str(avg_dist_per_week)+" km", str(total_distance)+" km", str(average_run_distance)+" km"

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


@callback(
    Output('all_time_perf_male_grid', 'rowData'),
    Input('distance_all_time_dropdown', 'value')
)
def display_grid_all_time_male(distance):
    df_perf = data_handler.get_df_all_time(distance, "M")
    return df_perf[['athlete', 'duration', 'age_group', 'country', 'pace_str']].to_dict('records')


@callback(
    Output('all_time_perf_female_grid', 'rowData'),
    Input('distance_all_time_dropdown', 'value')
)
def display_grid_all_time_female(distance):
    df_perf = data_handler.get_df_all_time(distance, "F")
    return df_perf[['athlete', 'duration', 'age_group', 'country', 'pace_str']].to_dict('records')

@callback(
    Output('country_representation_wr', 'rowData'),
    Input('url', 'pathname')
)
def display_grid_country_representation_wr(pathname):
    df = data_handler.get_df_country_representation_wr()
    return df.to_dict('records')

@callback(
    Output('country_representation_best_perf', 'rowData'),
    Input('url', 'pathname')
)
def display_grid_country_representation_best_perf(pathname):
    df = data_handler.get_df_country_representation()
    return df.to_dict("records")


@callback(
    Output('athlete_nb_per_country', 'rowData'),
    Input('url', 'pathname')
)
def display_grid_country_representation_best_perf(pathname):
    df = data_handler.get_athlete_per_country()
    return df.to_dict("records")


@callback(
    Output('athletes_nb_per_country', 'figure'),
    Input('url', 'pathname')
)
def display_graph_country_representation(pathname):
    figure = data_handler.get_fig_runner_per_country()
    return figure

@callback(
    Output('athlete_prop_pop_country', 'rowData'),
    Input('url', 'pathname')
)
def display_grid_athlete_prop_pop_country(pathname):
    df = data_handler.get_df_proportion_athlete_pop()
    return df.to_dict("records")

@callback(
    Output('athlete_prop_per_age_group', 'rowData'),
    Input('url', 'pathname')
)
def display_grid_athlete_prop_per_age_group(pathname):
    df = data_handler.get_df_athletes_per_age_group()
    return df.to_dict("records")


@callback(
    Output('athletes_prop_per_age_group', 'figure'),
    Input('url', 'pathname')
)
def display_graph_athlete_prop_per_age_group(pathname):
    figure = data_handler.get_fig_proportion_age_group()
    return figure