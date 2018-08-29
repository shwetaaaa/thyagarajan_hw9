import sqlalchemy
import numpy as np
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/<start><br/>"
        f"/api/v1.0/start_end_date/<start>/<end>"
         )


@app.route("/api/v1.0/precipitation")
def precip():
    """Return a list of dates and temperature observations from the last year"""
    # Query all passengers
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).\
            filter(func.strftime(Measurement.date >= last_year)).all()

    # Convert list of tuples into normal list
    all_temp = list(np.ravel(results))

    return jsonify(all_temp)

@app.route("/api/v1.0/stations")
def station():
    """Return a list of stations"""
    # Query all stations
    result = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(result))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of TOBs from the last year"""
    # Query all passengers
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    only_tob = session.query(Measurement.tobs).\
            filter(func.strftime(Measurement.date >= last_year)).all()

    # Convert list of tuples into normal list
    temp = list(np.ravel(only_tob))

    return jsonify(temp)

@app.route("/api/v1.0/start_date/<start>")
def start_time(start):
    """Fetch a list of the minimum temperature, the average temperature, and the max temperature for a given start date, or a 404 if not."""
    # Query all stations
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    # Convert list of tuples into normal list
    all_temps = list(np.ravel(results))
    #canonicalized = Measurement.date
    #if start <= Measurement.date:
    return jsonify(all_temps)

    #return jsonify({"error": f"The start date {start} not found."}), 404
    
@app.route("/api/v1.0/start_end_date/<start>/<end>")
def start_end(start,end):
    """Fetch a list of the minimum temperature, the average temperature, and the max temperature for a given start and end date range, or a 404 if not."""
    # Query all stations
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date<=end).all()

    # Convert list of tuples into normal list
    all_temps = list(np.ravel(results))
    #canonicalized = Measurement.date
    #if start <= Measurement.date:
    return jsonify(all_temps)

if __name__ == "__main__":
    app.run(debug=True)