# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
Base.classes.keys()
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
        f"Welcome to the Climate app API!<br/>"
        f"Available Routes:<br/>"
        f" "
        f"/api/v1.0/precipitation"
         f" "
        f"/api/v1.0/stations"
         f" "

        f"/api/v1.0/tobs"
        f" "

        f"/api/v1.0/<start>"
        f" "

        f"/api/v1.0/<start>/<end>"

    )

if __name__ == "__main__":
    app.run(debug=True)

#Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data)
#to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)


#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Measurement.station).all()
    stations = [station[0] for station in results]
    return jsonify(stations)


#Query the dates and temperature observations of the most-active station for the previous year of data.
#Return a JSON list of temperature observations for the previous year.
#@app.route("/api/v1.0/tobs")
#def tobs():
#    temp_data = session.query(Measurement.date, Measurement.tobs).\
 #   filter(Measurement.station == most_active_station).\
 #       filter(Measurement.date >= year_ago)
 #   temp_observations = [{date: tobs} for date, tobs in temp_data]
 #   return jsonify(temp_observations)



@app.route("/api/v1.0/<start>")
#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>/<end")
def temperature_range(start, end=None):
    # Define the base query to get TMIN, TAVG, TMAX
    if not end:
        # Only a start date is provided
        temp_stats = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start).all()
    else:
        # Both start and end dates are provided
        temp_stats = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Convert to dictionary for JSON response
    temp_data = {
        "TMIN": temp_stats[0][0],
        "TAVG": temp_stats[0][1],
        "TMAX": temp_stats[0][2]
    }

    return jsonify(temp_data)





# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB

