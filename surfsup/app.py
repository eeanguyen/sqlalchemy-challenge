### Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

### Database Setup

# Create engine to prepare to reflect
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

### Flask Setup
# Create an app, be sure to pass __name__
app = Flask(__name__)

### Flask Routes
# Homepage
@app.route("/")
def homepage():
    return (
        f"Hawaii Climate Analysis API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[Enter Start Date Y-M-D format] <br/>"
        f"/api/v1.0/[Enter Start Date y-m-d format] / [Enter End Date y-m-d format]"
    )

# Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_date = dt.date(year.year, year.month, year.day)

    query_prcp = session.query(measurement.date, measurement.prcp).filter(measurement.date >= last_date).order_by(measurement.date.desc()).all()

    prcp_dict = dict(query_prcp)

    session.close()

    return jsonify(prcp_dict)

# Stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    query_stations = session.query(station.station).all()
    stations_list = list(np.ravel(query_stations))
    
    session.close()

    return jsonify(stations_list)

# TOBS
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Identify the most-active station
    most_active_station = session.query(measurement.station, func.count(measurement.station))\
                        .group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()[0]
        
    # Calculate the date one year before the last data point in the database
    recent_year_str = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    
    recent_year = dt.datetime.strptime(recent_year_str, "%Y-%m-%d").date()
    prev_year = recent_year - dt.timedelta(days=365)

    # Query the temperature observations of the most-active station for the 2016
    temperature_data = session.query(measurement.date, measurement.tobs)\
                                  .filter(measurement.station == most_active_station)\
                                  .filter(measurement.date >= prev_year)\
                                  .order_by(measurement.date)\
                                  .all()

    # Create a list of dictionaries with `date` and `tobs` as keys and values
    temperature_totals = [{"date": date, "tobs": tobs} for date, tobs in temperature_data]

    session.close()

    return jsonify(temperature_totals)

# Start
@app.route('/api/v1.0/<start>')
def start(start):
    # Convert the start date from string to datetime 
    session = Session(engine)
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()

    # Query for TMIN, TAVG, and TMAX for all dates greater than or equal to the start date (will be a tuple)
    start_query = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs))\
                             .filter(measurement.date >= start_date).all()

    # Create a dictionary for the results to print
    temp_stats = {
            "Start Date": start,
            # TMIN = first row and first column of the result returned by the query
            "TMIN": start_query[0][0],
            # TAVG = first row and second column of the result returned by the query
            "TAVG": start_query[0][1],
            # TMAX = first row and third column of the result returned by the query
            "TMAX": start_query[0][2]
        }

    session.close()

    return jsonify(temp_stats)

# Start / End
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    # Convert the start and end dates from string to datetime 
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    end_date = dt.datetime.strptime(end, "%Y-%m-%d").date()

    # Query for TMIN, TAVG, and TMAX for dates between the start date and end date (will be a tuple)
    start_end_query = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs))\
                                 .filter(measurement.date >= start_date)\
                                 .filter(measurement.date <= end_date).all()
    
    # Create a dictionary for the results to print
    temp_stats = {
            "Start Date": start,
            "End Date": end,
            # TMIN = first row and first column of the result returned by the query
            "TMIN": start_end_query[0][0],
            # TAVG = first row and second column of the result returned by the query
            "TAVG": start_end_query[0][1],
            # TMAX = first row and third column of the result returned by the query
            "TMAX": start_end_query[0][2]
    }
    session.close()

    return jsonify(temp_stats)

if __name__ == "__main__":
    app.run(debug=True)