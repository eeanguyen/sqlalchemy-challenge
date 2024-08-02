# sqlalchemy-challenge

## Background
Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area. The following sections outline the steps that you need to take to accomplish this task.

---
## Overview
This repository provides a analyzation and exploration of Hawaii's climate data that was collected by 9 different stations between Aug 23, 2016 to Aug 23, 2017. Part two of this exploration I took it a step further and created a Flask-based API for accessing climate data from Hawaii. The data includes precipitation measurements, temperature observations, and station information. The data is stored in a SQLite database adn was provided by Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012: An overview of the Global Historical Climatology Network-Daily Database. Journal of Atmospheric and Oceanic Technology, 29, 897-910, https://journals.ametsoc.org/view/journals/atot/29/7/jtech-d-11-00103_1.xml.

## Table of Contents
- [Analysis and Exploration](#analysis-exploration)
- [Database Setup](#database-setup)
- [API Routes](#api-routes)
  - [Homepage](#homepage)
  - [Precipitation](#precipitation)
  - [Stations](#stations)
  - [Temperature Observations](#temperature-observations)
  - [Temperature Stats by Start Date](#temperature-stats-by-start-date)
  - [Temperature Stats by Date Range](#temperature-stats-by-date-range)
  - [Usage](#usage)

## Analysis and Exploration

In this section, you’ll use Python and SQLAlchemy to perform a basic climate analysis and data exploration of the climate database. You will use SQLAlchemy ORM queries, Pandas, and Matplotlib.

### Precipitation Analysis
1. **Find the Most Recent Date**
   - Query the most recent date in the dataset.

2. **Get the Previous 12 Months of Precipitation Data**
   - Filter the data to get the previous 12 months of precipitation data.
   - Select only the "date" and "prcp" values.

3. **Load Data into a Pandas DataFrame**
   - Load the query results into a Pandas DataFrame.
   - Explicitly set the column names and sort by "date".

4. **Plot the Results**
   - Plot the precipitation data using Matplotlib.
   - Use Pandas' DataFrame plot method to visualize the results.
   ![Hawaii_Prcp_Bar](https://github.com/eeanguyen/sqlalchemy-challenge/blob/main/surfsup/images/%20Hawaii%20Precipitation%20Bar%20Chart.png)

5. **Print Summary Statistics**
   - Use Pandas to print summary statistics for the precipitation data.

### Station Analysis
1. **Calculate the Total Number of Stations**
   - Query to get the total number of stations in the dataset.

2. **Find the Most Active Stations**
   - List the stations with observation counts in descending order.
   - Identify the station with the greatest number of observations.

3. **Query Temperature Data for the Most Active Station**
   - Calculate the lowest, highest, and average temperatures for the most active station.
   - Filter by the most active station ID.

4. **Plot Temperature Observations**
   - Query the previous 12 months of TOBS data for the most active station.
   - Plot the results as a histogram with bins=12.
    ![Most_Actice_Station_Bar]https://github.com/eeanguyen/sqlalchemy-challenge/blob/main/surfsup/images/%20Station%20USC00519281%20Histogram.png)

## Database Setup

The SQLite database file (`hawaii.sqlite`) is in the `Resources` directory. This file contains the climate data used by the API.

## API Routes

### Homepage
- **Route:** `/`
- **Description:** Lists all available API routes.

### Precipitation
- **Route:** `/api/v1.0/precipitation`
- **Description:** Returns a JSON dictionary of precipitation data for the last year.

### Stations
- **Route:** `/api/v1.0/stations`
- **Description:** Returns a JSON list of station IDs.

### Temperature Observations
- **Route:** `/api/v1.0/tobs`
- **Description:** Returns a JSON list of temperature observations for the most active station for the last year.

### Temperature Stats by Start Date
- **Route:** `/api/v1.0/<start>`
- **How to:** input date into url using %Y-%m-%d
- **Description:** Returns a JSON list of the minimum, average, and maximum temperature for all dates greater than or equal to the start date.

### Temperature Stats by Date Range
- **Route:** `/api/v1.0/<start>/<end>`
- **How to:** input date into url using %Y-%m-%d/%Y-%m-%d
- **Description:** Returns a JSON list of the minimum, average, and maximum temperature for dates between the start and end date, inclusive.

## Usage

1. Run the Flask application:
    ```bash
    python app.py
    ```

2. Open a web browser and navigate to `http://127.0.0.1:5000/` to access the homepage and available API routes are listed.