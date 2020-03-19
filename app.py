import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from datetime import datetime

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/><br/>"
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/><br/>"
        f"Date format for start/end dates should be MM-DD-YYYY"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates and precipiation"""
    # Query all precipitation
    results = session.query(Measurement.date,Measurement.prcp).all()
    
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    session.close()

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    results = session.query(Station.station,Station.name).all()
    
    all_stations = []
    for station, name in results:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        all_stations.append(stations_dict)

    session.close()

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Create variables for start and end dates
    results1 = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    
    for row in results1:
        end_date = row
    
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    start_date = end_date - dt.timedelta(days=365)

    # Query all temperature for one year since last date posted
    
    results = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date <= end_date).\
            filter(Measurement.date >= start_date).\
            order_by(Measurement.date.desc()).\
            all()
    
    all_tobs = []
    
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    session.close()

    return jsonify(all_tobs)

@app.route("/api/v1.0/temp/<start>")
def tempstart(start):
    
    start = datetime.strptime(start, '%m-%d-%Y')
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query MIN, AVG, MAX of temperatures = dates equal or greater than start date
    results = list(\
        session.query(Measurement).\
        filter(Measurement.date >= start).\
        values(func.min(Measurement.tobs),\
           func.avg(Measurement.tobs),\
           func.max(Measurement.tobs)))
            
    session.close()
    
    return jsonify(results)

    return jsonify({"error": f"No data for temp from {start} found."}), 404

@app.route("/api/v1.0/temp/<start>/<end>")
def temp(start,end):
    
    start = datetime.strptime(start, '%m-%d-%Y')
    end = datetime.strptime(end, '%m-%d-%Y')
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query MIN, AVG, MAX of temperatures of dates within start and end dates
    results = list(\
        session.query(Measurement).\
        filter(Measurement.date <= end).\
        filter(Measurement.date >= start).\
        values(func.min(Measurement.tobs),\
           func.avg(Measurement.tobs),\
           func.max(Measurement.tobs)))
            
    session.close()
    
    return jsonify(results)

    return jsonify({"error": f"No data for {start} - {end} found."}), 404


if __name__ == '__main__':
    app.run(debug=True)