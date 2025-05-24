from meteostat import Stations


def nearest_stations(lat,lon):
    """Function listed nearest stations
    You can choose a station to get data"""
    stations = Stations()
    stations = stations.nearby(lat, lon)
    df_stations = stations.fetch(20)

    df_stations = df_stations[["name", "monthly_end", "daily_end", "hourly_end"]]
    print(df_stations)

