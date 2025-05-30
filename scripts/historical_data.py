from meteostat import Hourly
from datetime import datetime
import pandas as pd


def hourly_to_daily(nearest_station_id, starting_time, ending_time):
    # Data extraction and fetch
    data = Hourly(nearest_station_id, starting_time, ending_time)
    data_frame = data.fetch()
    data_frame.reset_index(inplace=True)
    data_frame["time"] = pd.to_datetime(data_frame["time"])


# Added cities for weather observation datas
cities = {
    "İstanbul": "17060",
    "Ankara": "LTAB0",
    "İzmir": "17218",
    "Bursa": "17116",
    "Adana": "17352"
}

start_time = datetime(2020, 1, 1)
end_time = datetime(2024, 12, 31)

