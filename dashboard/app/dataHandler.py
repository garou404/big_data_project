import pandas as pd
import glob
import plotly.express as px
import numpy as np
import datetime as dt

def get_bin(value):
    if value >= 7:
        return "> 7:00"
    elif (value < 7) & (value >= 6.5):
        return "7:00 > x > 6:30"
    elif (value < 6.5) & (value >= 6.0):
        return "6:30 > x > 6:00"
    elif (value < 6.0) & (value >= 5.5):
        return "6:00 > x > 5:30"
    elif (value < 5.5) & (value >= 5):
        return "5:30 > x > 5:00"
    elif (value < 5) & (value >= 4.5):
        return "5:00 > x > 4:30"
    elif (value < 4.5) & (value >= 4):
        return "4:30 > x > 4:00"
    elif (value < 4) & (value >= 3.5):
        return "4:00 > x > 3:30"
    elif (value < 3.5) & (value >= 3):
        return "3:30 > x > 3:00"
    elif (value < 3) & (value >= 2.5):
        return "3:00 > x > 2:30"
    elif (value < 2.5):
        return "< 2:30"

class DataHandler:
    data_path = ""
    year = 2019

    df_athletes_per_country = pd.DataFrame()
    df_proportion_per_age_category = pd.DataFrame()
    df_proportion_athlete_per_pop = pd.DataFrame()

    df_athlelte_per_country_wr = pd.DataFrame()
    df_athlelte_per_country = pd.DataFrame()

    df_best_perf_per_athlete = pd.DataFrame()
    df_wr = pd.DataFrame()
    
    df_per_athlete = pd.DataFrame()

    df_running = pd.DataFrame()


    def __init__(self, data_path):
        self.data_path = data_path
        all_files = glob.glob(data_path+ f"per_runner_data_{self.year}" + "/*.csv")  # Get all CSV files
        self.df_per_athlete = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
        self.df_running= pd.read_csv(data_path+f"../running/run_ww_{self.year}_d.csv", index_col="Unnamed: 0")



    def get_fig_pace_distribution(self, athlete_id, distance):
        distance = float(distance)
        athlete_dist_time = self.df_per_athlete.loc[self.df_per_athlete['athlete'] == athlete_id, str(distance)].values[0]
        athlete_pace = float(athlete_dist_time.split('/')[1])/float(athlete_dist_time.split('/')[0])
        paces = self.df_per_athlete[str(distance)].str.split("/", expand=True)[1].astype(float) / self.df_per_athlete[str(distance)].str.split("/", expand=True)[0].astype(float)
        df_paces = pd.DataFrame(data=paces, columns=["pace"])
        df_paces['bin'] = df_paces['pace'].apply(lambda x : get_bin(x))
        bin_athlete = get_bin(athlete_pace)
        df_paces['color'] = "blue"
        df_paces.loc[df_paces['bin'] == bin_athlete, 'color'] = "red"

        distribution = df_paces[['bin', 'color']].value_counts().reset_index()
        distribution.columns = ['Pace Range', 'color', 'Count']

        bin_order = [
            "> 7:00",
            "7:00 > x > 6:30",
            "6:30 > x > 6:00",
            "6:00 > x > 5:30",
            "5:30 > x > 5:00",
            "5:00 > x > 4:30",
            "4:30 > x > 4:00",
            "4:00 > x > 3:30",
            "3:30 > x > 3:00",
            "3:00 > x > 2:30",
            "< 2:30"
        ]

        distribution['Pace Range'] = pd.Categorical(distribution['Pace Range'], categories=bin_order, ordered=True)
        distribution = distribution.sort_values(by='Pace Range')

        fig = px.bar(distribution, x='Pace Range', y='Count', title='Best Pace Distribution',
            labels={'Pace Range': '', 'Count': ''},
            text_auto=True, color='color', color_discrete_map={'red': 'red', 'blue': 'blue'},
            category_orders={'Pace Range': bin_order}
        )

        fig.update_layout(
            margin=dict(l=0, r=20, t=40, b=0),
            paper_bgcolor = 'rgba(0,0,0,0)',
        )
        return fig

    def get_fig_weekly_distance(self, athlete_id, start_date, end_date):
        if self.df_running.empty:
            return px.bar(title="No Data Available")
        df_filtered = self.df_running.loc[(self.df_running['athlete'] == athlete_id)].copy()
        df_filtered['datetime'] = pd.to_datetime(df_filtered['datetime'], format='%Y-%m-%d', errors='coerce')

        df_filtered.set_index('datetime', inplace=True)

        df_weekly = df_filtered.drop(columns=['gender', 'age_group', 'country', 'major', 'athlete']).resample('W').sum().reset_index()
        if start_date:
            df_weekly = df_weekly.loc[(df_weekly['datetime'] > dt.datetime.strptime(start_date, "%Y-%m-%d")) & (df_weekly['datetime'] < dt.datetime.strptime(end_date, "%Y-%m-%d"))]
        try:
            fig = px.bar(df_weekly, x='datetime', y='distance', title='', 
                labels={'datetime': '', 'distance': 'Distance (km)'},
                text_auto=True, color='distance', color_continuous_scale="hot"
            ) #darkmint hot tealgrn ylgnbu spectral blackbody

            fig.update_layout(xaxis_title='Week', yaxis_title='Distance (km)',
                xaxis=dict(tickformat='%b'),
                margin=dict(l=40, r=20, t=10, b=0),
                paper_bgcolor = 'rgba(0,0,0,0)',
                # plot_bgcolor = 'rgba(0,0,0,0)'
            )
            return fig
        except:
            return px.bar(title="No Data Available")
    
    def get_fig_proportion_age_group(self):
        print("test")

    def get_fig_proportion_age_group(self):
        print("test")
    
    def get_fig_runner_per_country(self):
        print("test")

    def get_df_all_time(self, distance, gender):
        print("test")

    def get_df_country_representation_wr(self):
        print("test")

    def get_df_country_representation(self):
        print("test")

    def get_athlete_per_country(self):
        print("test")

    def get_df_proportion_athlete_pop(self):
        print("test")

    def get_data_per_athlete(self, athlete_id):
        df_athlete = self.df_per_athlete[self.df_per_athlete['athlete'] == athlete_id]
        return df_athlete

    def get_data_per_country(self, country):
        print("test")
        # avg run nb/week/athlete - avg dist/run/athlete - avg dist/week/athlete

    