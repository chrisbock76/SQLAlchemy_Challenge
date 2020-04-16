import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

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
        f"/api/v1.0/2017-07-01<br/>"
        f"/api/v1.0/2017-07-01/2017-07-31"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    """Return the precipitation data for the last year"""   
    # Calculate the date 1 year ago from last date in database    
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #query for the precipitation in the last year
    precip = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()

    #return the precipitation data
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    """Return all of the stations"""   

    #query for the stations
    stations = session.query(Station.station).all()

    #return the precipitation stations data
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the dates and temperature observations of the most active station for the last year of data"""   
    # Calculate the date 1 year ago from last date in database    
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #query for the tobs data for station 'USC00519281'
    tobs = session.query(Measurement.date, Measurement.tobs).\
        group_by(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()

    #return the tobs data
    return jsonify(tobs)    

@app.route("/api/v1.0/2017-07-01")
def start_date():
    """Return the min temp, the avg temp, and the max temp for a given start date"""   
    #query for the min temp, the avg temp, and the max temp for a given start date
    start = "2017-07-01"
    
    start_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).group_by(Measurement.date).all()

    #return the start_date data
    return jsonify(start_date)

@app.route("/api/v1.0/2017-07-01/2017-07-31")
def date_range():
    """Return the min temp, the avg temp, and the max temp for a given date range"""   
    #query for the min temp, the avg temp, and the max temp for a given date range
    start = "2017-07-01"
    end = "2017-07-31"
    
    DateRange = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()

    #return the date_range data
    return jsonify(DateRange)



if __name__ == '__main__':
    app.run(debug=True)