

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
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_end_date"
         )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of date and temperature for last 12 months"""
    # Query date and temp
    
    date_year_ago=dt.date(2017,8,23) - dt.timedelta(days=365)
 
    # Perform a query to retrieve the data and precipitation scores
    tobs_data=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>date_year_ago).all()

    # Convert the query results to a Dictionary
    tobs_data_dict = dict(tobs_data)

    return jsonify(tobs_data_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature for previous year"""
    results=session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23').all()
    tobs_list=[]
    for i in results:
        tobs_dict={}
        tobs_dict['date']=i.date
        tobs_dict['tobs']=i.tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

@app.route("/api/v1.0/start_date/<start>")
def startdt(start):
    """Return min,avg,max temperature for given year"""
    # Query all stations
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    # Convert list of tuples into normal list
    all_temps = list(np.ravel(results))
    #canonicalized = Measurement.date
    #if start <= Measurement.date:
    return jsonify(all_temps)

    #return jsonify({"error": f"Character with start_date {start} not found."}), 404

@app.route("/api/v1.0/start_end_date/<start>/<end>")
def startenddt(start,end):
    """Return min,avg,max temperature for given year"""
    # Query all stations
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date<=end).all()

    # Convert list of tuples into normal list
    all_temps = list(np.ravel(results))
    #canonicalized = Measurement.date
    #if start <= Measurement.date:
    return jsonify(all_temps)


    

if __name__ == '__main__':
    app.run(debug=True)
