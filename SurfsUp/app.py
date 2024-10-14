# Import the dependencies.
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template
import datetime as dt

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
#Base.prepare(autoload_with=engine)
#Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


#################################################
# Flask Routes
@app.route("/")
def home():
      return (
        f"Welcome to the Climate app API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date (e.g., /api/v1.0/2017-01-01)<br/>"
        f"/api/v1.0/start_date/end_date (e.g., /api/v1.0/2017-01-01/2017-12-31)<br/>"
    )



#Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data)
#to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation_route():
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations_route():
    results = session.query(Measurement.station).all()
    #station = list(np.ravel(results))
    stations = [station[0] for station in results]
    return jsonify(stations)


#Query the dates and temperature observations of the most-active station for the previous year of data.
#Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def tobs_route():
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]
    
    temp_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()
    
    temp_observations = [{date: tobs} for date, tobs in temp_data]
    
    return jsonify(temp_observations)




#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

#@app.route("/api/v1.0/<start>")

#def start_date_temp_route(start):
#Functions for min, max, avg temperatures
#sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)]
#Query the results filtering by the start date
#results = session.query(*sel).filter(Measurement.date >=start).all()
#Convert results to a list and return as JSON
#temp_data = list(np.ravel(results))
#return jsonify(temp_data)

@app.route("/api/v1.0/<start>")
def start_date_temp_route(start):
    # Convert the string into a date object
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()

    print(f"{start=} {start_date=}", flush=True)

    # Functions for min, max, avg temperatures
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # Query the results filtering by the start date
    results = session.query(*sel).filter(Measurement.date >= start_date).all()

    print(f"{results=}", flush=True)

    # Convert results to a list and return as JSON
    temp_data = list(np.ravel(results))
    return jsonify(temp_data)

#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>/<end>")
def temp_stats_route(start, end):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    # Convert the result into a list
    temp_data = list(np.ravel(results))
    
    # Return the JSON list of the min, avg, and max temperature
    return jsonify(temp_data)


if __name__ == "__main__":
    app.run(debug=True)