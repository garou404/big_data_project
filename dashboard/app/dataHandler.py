import pandas as pd
import glob
import plotly.express as px
import numpy as np
import datetime as dt
import os


country_to_svg = {
        "United States": "us.svg",
    "United Kingdom": "gb.svg",
    "Germany": "de.svg",
    "Japan": "jp.svg",
    "Brazil": "br.svg",
    "Canada": "ca.svg",
    "Mexico": "mx.svg",
    "Netherlands": "nl.svg",
    "Australia": "au.svg",
    "Italy": "it.svg",
    "Indonesia": "id.svg",
    "Norway": "no.svg",
    "Russia": "ru.svg",
    "China": "cn.svg",
    "Taiwan": "tw.svg",
    "Philippines": "ph.svg",
    "Argentina": "ar.svg",
    "Spain": "es.svg",
    "South Africa": "za.svg",
    "Poland": "pl.svg",
    "Costa Rica": "cr.svg",
    "Switzerland": "ch.svg",
    "Finland": "fi.svg",
    "Chile": "cl.svg",
    "South Korea": "kr.svg",
    "Sweden": "se.svg",
    "Ireland": "ie.svg",
    "France": "fr.svg",
    "Austria": "at.svg",
    "Botswana": "bw.svg",
    "Kenya": "ke.svg",
    "Denmark": "dk.svg",
    "Faroe Islands": "fo.svg",
    "Colombia": "co.svg",
    "Iceland": "is.svg",
    "Panama": "pa.svg",
    "Latvia": "lv.svg",
    "Jamaica": "jm.svg",
    "South Africa": "za.svg",
    "Kenya": "ke.svg",
    "Morocco": "ma.svg",
    "Norway": "no.svg",
    "Uganda": "ug.svg",
    "USA": "us.svg",
    "Lithuania": "lt.svg",
    "East Germany": "ddr.svg",  # East Germany no longer exists; usually, its flag is labeled "ddr.svg"
    "Czechoslovakia": "cs.svg",  # Czechoslovakia split; its historical flag is often labeled "cs.svg"
    "Russia": "ru.svg",
    "Austrailia": "au.svg",  # Assuming "Austrailia" is a typo for "Australia"
    "China": "cn.svg",
    "Ethiopia": "et.svg",
    "Japan": "jp.svg"
}

def format_duration(minutes):
    total_seconds = int(minutes * 60)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes:02}:{seconds:02}"

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
        self.df_wr = pd.read_csv("../data/wr/running_wr.csv")
        
        all_files = glob.glob(f"{data_path}runner_nb_per_country_{self.year}" + "/*.csv")
        self.df_athletes_per_country = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
        
        all_files = glob.glob(f"{data_path}runner_prop_per_country_{self.year}" + "/*.csv")
        self.df_proportion_athlete_per_pop = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True).dropna()

        all_files = glob.glob(f"{data_path}runner_prop_per_age_category_{self.year}" + "/*.csv")
        self.df_proportion_per_age_category = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True).dropna()

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
            fig = px.bar(df_weekly, x='datetime', y='distance', title='Weekly Running Distance: Kilometers Tracked', 
                labels={'datetime': '', 'distance': 'Distance (km)'},
                text_auto=True, color='distance', color_continuous_scale="hot"
            ) #darkmint hot tealgrn ylgnbu spectral blackbody

            fig.update_layout(xaxis_title='', yaxis_title='Distance (km)', 
                xaxis=dict(tickformat='%b'),
                margin=dict(l=25, r=20, t=30, b=0),
                paper_bgcolor = 'rgba(0,0,0,0)',
                # plot_bgcolor = 'rgba(0,0,0,0)'
            )
            return fig
        except:
            return px.bar(title="No Data Available")
    
    # def get_fig_proportion_athlete_pop(self):
    #     if not self.df_proportion_athlete_per_pop.empty:
    #         return self.df_proportion_athlete_per_pop

    def get_fig_proportion_age_group(self):
        if not self.df_proportion_per_age_category.empty:
            fig = px.pie(self.df_proportion_per_age_category, 
             values='count', 
             names='age_group', 
             title='',
			 )
            fig.update_layout(
                margin=dict(l=0, r=20, t=10, b=0),
                paper_bgcolor = 'rgba(0,0,0,0)',
            )
            return fig
        else:
            return px.pie(title="No Data Available")

    
    def get_fig_runner_per_country(self):
        if not self.df_athletes_per_country.empty:
            fig = px.pie(self.df_athletes_per_country.head(15), 
             values='runner_nb_per_country', 
             names='country', 
             title='',
			 )
            fig.update_layout(
                margin=dict(l=0, r=20, t=10, b=0),
                paper_bgcolor = 'rgba(0,0,0,0)',
            )
            return fig
        else:
            return px.pie(title="No Data Available")

    def get_df_all_time(self, distance, gender):

        path = f"{self.data_path}/all_time_performances_{self.year}/"
        all_files = glob.glob(path + "/*.csv")  # Get all CSV files
        df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
        df.drop(columns='_c0', inplace=True)
        
        df_wr_filtered = self.df_wr.loc[(self.df_wr['distance'] == distance) & (self.df_wr['gender'] == gender)].copy()
        df_wr_filtered.rename(columns={"world_record": "pace_str", "athlete_age": "age_group"}, inplace=True)
        df_wr_filtered = df_wr_filtered[['athlete', 'age_group', 'country', 'distance', 'duration']]
        df_wr_filtered['pace'] = df_wr_filtered['duration'] / df_wr_filtered['distance']
        df_wr_filtered['pace_str'] = (df_wr_filtered['pace'] - df_wr_filtered['pace'].astype(int))*60
        df_wr_filtered['pace_str'] = df_wr_filtered['pace'].astype(int).astype(str)+":"+df_wr_filtered['pace_str'].astype(int).astype(str).str.zfill(2)
        df_wr_filtered['duration'] = df_wr_filtered['duration'].apply(format_duration)
        df_filtered = df.loc[(df['best distance'] == distance) & (df['gender'] == gender)]
        df_filtered['pace_str'] = df_filtered['pace_min'].astype(str) +':'+ df_filtered['pace_sec'].astype(int).astype(str).str.zfill(2)
        df_filtered = df_filtered[['athlete', 'distance', 'duration', 'age_group', 'country', 'pace', 'pace_str']]
        df_filtered['duration'] = df_filtered['duration'].apply(format_duration)
        df_perf = pd.concat([df_filtered, df_wr_filtered]).sort_values(by=['pace'])
        df_perf['age_group'] = df_perf['age_group'].astype(str)
        return df_perf

    def get_df_country_representation_wr(self):
        if not self.df_wr.empty:
            df_wr_filtered = self.df_wr.groupby("country")['athlete'].count().reset_index().sort_values(by=["athlete"], ascending=False).copy()
            df_wr_filtered['flag_filename'] = df_wr_filtered['country'].map(lambda x: f"/assets/flags/flags/4x3/{country_to_svg.get(x, 'xx')}")
            return df_wr_filtered
        return None

    def get_df_country_representation(self):
        path = f"{self.data_path}/all_time_performances_{self.year}/"
        all_files = glob.glob(path + "/*.csv")
        df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
        df.drop(columns='_c0', inplace=True)
        df = df.groupby("country")['athlete'].count().reset_index().sort_values(by=["athlete"], ascending=False)
        df['flag_filename'] = df['country'].map(lambda x: f"/assets/flags/flags/4x3/{country_to_svg.get(x, 'xx')}")
        return df


    def get_athlete_per_country(self):
        if not self.df_athletes_per_country.empty:
            return self.df_athletes_per_country
        else:
            return pd.DataFrame()
    
    def get_df_proportion_athlete_pop(self):
        if not self.df_proportion_athlete_per_pop.empty:
            df = self.df_proportion_athlete_per_pop.copy()
            df['flag_filename'] = df['country'].map(lambda x: f"/assets/flags/flags/4x3/{country_to_svg.get(x, 'xx')}")
            return df
        else:
            return pd.DataFrame()
        
    def get_data_per_athlete(self, athlete_id):
        df_athlete = self.df_per_athlete[self.df_per_athlete['athlete'] == athlete_id]
        return df_athlete

    def get_data_per_country(self, country):
        print("test")
        # avg run nb/week/athlete - avg dist/run/athlete - avg dist/week/athlete

    def get_df_athletes_per_age_group(self):
        if not self.df_proportion_per_age_category.empty:
            return self.df_proportion_per_age_category.sort_values(by=['count'], ascending=False)
        else:
            return pd.DataFrame()