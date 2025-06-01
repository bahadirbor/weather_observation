# Weather Data Pipeline

A Python data processing pipeline designed to collect and process meteorological data from major cities in Turkey. This project transforms hourly weather data into daily statistics, creating analysis-ready datasets.

## 🎯 Project Purpose

This project processes raw hourly weather data from meteorological stations to:
- Automate the collection of weather data
- Convert detailed hourly data into daily summaries
- Provide clean, ready-to-use datasets for further analysis or machine learning tasks
- Generate annual CSV files for specified cities

## 📊 Supported Cities

The project currently collects data for the following Turkish cities:

| City | Station ID |
|------|------------|
| Istanbul | 17060 |
| Ankara | LTAB0 |
| Izmir | 17218 |
| Bursa | 17116 |
| Adana | 17352 |


## 🚀 Usage

### Running the Main Data Pipeline

```python
python historical_data.py
```

This command downloads and processes meteorological data for all cities from Jan 2020 - April 2025.

### Finding Nearby Stations

```python
from nearest_stations import nearest_stations

# List nearby stations using coordinates
nearest_stations(lat=41.0082, lon=28.9784)  # Istanbul coordinates
```

## 📋 Dataset Columns

The generated CSV files contain the following columns:

- `date`: Date
- `daily_avg_temp`: Daily average temperature (°C)
- `daily_max_temp`: Daily maximum temperature (°C)
- `daily_min_temp`: Daily minimum temperature (°C)
- `daily_avg_wind_speed`: Daily average wind speed
- `daily_max_wind_speed`: Daily maximum wind speed
- `daily_min_wind_speed`: Daily minimum wind speed
- `wind_direction`: Dominant wind direction
- `avg_relative_humidity`: Average relative humidity (%)
- `avg_dew_point`: Average dew point (°C)
- `avg_pressure`: Average pressure (hPa)
- `precipitation_sum`: Total precipitation amount (mm)
- `rainy_hour_sum`: Number of rainy hours

## 🔍 Data Processing Workflow

1. **Data Extraction**: Hourly data is downloaded using the Meteostat API
2. **Cleaning**: Missing precipitation data is filled with zeros
3. **Grouping**: Data is grouped by year-month-day
4. **Aggregation**: Statistical summaries are calculated for each group
5. **Merging**: All meteorological parameters are combined into a single table
6. **Storage**: Data is saved to separate CSV files by year

## 📈 Use Cases

- Climate change analysis
- Agricultural planning
- Energy consumption forecasting
- Tourism seasonal analysis
- Urban planning studies
- Academic research

## 📝 Notes

- The Meteostat service may occasionally lack data for specific dates
- Station IDs are sourced from the Meteostat database
- Precipitation data is recorded in millimeters
- All numeric data is rounded to 2 decimal places


## 📄 License

This project is open source software distributed under the Apache License.