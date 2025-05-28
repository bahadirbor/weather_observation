from meteostat import Hourly
from datetime import datetime
import pandas as pd

#Added cities for weather observation datas
cities = {
    "İstanbul": "17060",
    "Ankara": "LTAB0",
    "İzmir": "17218",
    "Bursa": "17116",
    "Adana": "17352"
}

start_time = datetime(2020,1,1)
end_time = datetime(2024,12,31)

