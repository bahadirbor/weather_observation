from meteostat import Hourly
from datetime import datetime
import pandas as pd
import os

data_root = "../data"


def hourly_to_daily(city, nearest_station_id, starting_time, ending_time, data_root):
    # Data extraction and fetch
    data = Hourly(nearest_station_id, starting_time, ending_time)
    data_frame = data.fetch()

    if data_frame.empty:
        print(f"{nearest_station_id} data not found")

    data_frame.reset_index(inplace=True)
    data_frame["time"] = pd.to_datetime(data_frame["time"])

    # Create year-month-day columns
    data_frame["year"] = data_frame['time'].dt.year
    data_frame["month"] = data_frame['time'].dt.month
    data_frame["day"] = data_frame['time'].dt.day
    data_frame["hour"] = data_frame['time'].dt.hour

    df_new_two = data_frame.groupby(by=["year", "month", "day"])

    daily_temp_stats = df_new_two['temp'].agg(
        daily_temp_mean='mean',
        daily_temp_max='max',
        daily_temp_min='min'
    ).reset_index()

    daily_wing_stats = df_new_two['wspd'].agg(
        daily_wing_speed_mean='mean',
        daily_wing_speed_max='max',
        daily_wing_speed_min='min'
    ).reset_index()

    daily_rhum = df_new_two["rhum"].agg(avg_rhum="mean")
    daily_dwpt = df_new_two["dwpt"].agg(avg_dwpt="mean")
    daily_pres = df_new_two["pres"].agg(avg_pres="mean")

    daily_temp_stats = daily_temp_stats.merge(daily_rhum, on=['year', 'month', 'day'], how='left')
    daily_temp_stats = daily_temp_stats.merge(daily_dwpt, on=['year', 'month', 'day'], how='left')
    daily_temp_stats = daily_temp_stats.merge(daily_wing_stats, on=['year', 'month', 'day'], how='left')
    daily_temp_stats = daily_temp_stats.merge(daily_pres, on=['year', 'month', 'day'], how='left')





# Added cities for weather observation datas
cities = {
    "İstanbul": "17060",
    "Ankara": "LTAB0",
    "İzmir": "17218",
    "Bursa": "17116",
    "Adana": "17352"
}

start_time = datetime(2020, 1, 1)
end_time = datetime(2025, 4, 30)

for city, location in cities:
    hourly_to_daily(city, location, start_time, end_time, data_root)