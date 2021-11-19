# CWRR

Csv Weather Report Reader - a lab work for my university.

## Prerequisites

- python >= 3.8

## Task
Weather observation data are processed.
The records of the main file contain the fields: average daily
temperature, precipitation, weather station code,
wind strength, year, day, month, relative humidity, maximum daytime
temperature, minimum daytime temperature.

The auxiliary file contains the keys: the number of weather 
stations, the average value of the average daily temperature.
Find meteorological stations for which the amount of precipitation 
was recorded to be twice less than the average according
to all data. 

Display information on each of them:

- on the first line:
the highest amount of precipitation, the number of observations, the
average minimum temperature, the weather station;
-  on the following lines, starting with the tab, display 
aggregated data for them (one per line):
day, average humidity (for this day of the year in all months at 
this weather station), year in the following sort: day, year.

## Usage
`<path_to_init>` - `.json` file that has all pathes to other files.

> python3 main.py <path_to_init>