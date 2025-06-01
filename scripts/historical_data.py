from meteostat import Hourly
from datetime import datetime
import pandas as pd
import os
import scipy.stats as stats

data_root = "../data"


def most_common(series):
    # This func used to keep column's mode value
    return stats.mode(series.values, keepdims=False)[0]


def hourly_to_daily(city_name, nearest_station_id, starting_time, ending_time, data_root):
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
    data_frame['prcp'] = data_frame['prcp'].fillna(0)
    data_frame['rainy_hour'] = data_frame['prcp'] > 0

    df_new_two = data_frame.groupby(by=["year", "month", "day"])

    # Create daily temperature data from hourly data
    daily_temp_stats = df_new_two['temp'].agg(
        daily_avg_temp='mean',
        daily_max_temp='max',
        daily_min_temp='min'
    ).reset_index()

    # Create daily wind speed data from hourly data
    daily_wind_stats = df_new_two['wspd'].agg(
        daily_avg_wind_speed='mean',
        daily_max_wind_speed='max',
        daily_min_wind_speed='min'
    ).reset_index()

    # Create relative humidity, dew point, pressure data from hourly data
    daily_rhum = df_new_two["rhum"].agg(avg_relative_humidity="mean")
    daily_dwpt = df_new_two["dwpt"].agg(avg_dew_point="mean")
    daily_pres = df_new_two["pres"].agg(avg_pressure="mean")

    # Create daily precipitation and rainy hours columns
    daily_prcp = df_new_two["prcp"].agg(precipitation_sum="sum")
    daily_rainy_hour = df_new_two["rainy_hour"].agg(rainy_hour_sum="sum")

    # Create wind direction column from hourly wind direction mode
    daily_winddir = df_new_two["wdir"].agg(
        wind_direction=most_common
    )

    # Concatenate all dataframes into daily_temp_stats
    daily_temp_stats = daily_temp_stats.merge(daily_rhum, on=['year', 'month', 'day'], how='left')
    daily_temp_stats = daily_temp_stats.merge(daily_dwpt, on=['year', 'month', 'day'], how='left')
    daily_temp_stats = daily_temp_stats.merge(daily_wind_stats, on=['year', 'month', 'day'], how='left')
    daily_temp_stats = daily_temp_stats.merge(daily_pres, on=['year', 'month', 'day'], how='left')
    daily_temp_stats = daily_temp_stats.merge(daily_winddir, on=['year', 'month', 'day'], how='left')
    daily_temp_stats = daily_temp_stats.merge(daily_prcp, on=['year', 'month', 'day'], how='left')
    daily_temp_stats = daily_temp_stats.merge(daily_rainy_hour, on=['year', 'month', 'day'], how='left')

    # Year, month and day columns converted to date column
    daily_temp_stats['date'] = pd.to_datetime(daily_temp_stats[['year', 'month', 'day']])

    # Columns re-ordered
    new_column_order = ["date", "daily_avg_temp", "daily_max_temp", "daily_min_temp", "daily_avg_wind_speed",
                        "daily_max_wind_speed", "daily_min_wind_speed", "wind_direction", "avg_relative_humidity",
                        "avg_dew_point", "avg_pressure", "precipitation_sum", "rainy_hour_sum"]
    daily_temp_stats = daily_temp_stats[new_column_order]

    daily_temp_stats = daily_temp_stats.round(2)

    daily_temp_stats["year"] = daily_temp_stats["date"].dt.year

    for year, group in daily_temp_stats.groupby(["year"]):
        # Save datas into CSV files and saved year folders
        year = str(year)[1:5]
        year_folder = os.path.join(data_root, year)
        os.makedirs(year_folder, exist_ok=True)

        file_path = os.path.join(year_folder, f"{city_name.lower()}_{year}.csv")
        group.drop(columns=['year'], inplace=False).to_csv(file_path, index=False, float_format='%.2f')


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

for city, location in cities.items():
    hourly_to_daily(city, location, start_time, end_time, data_root)
