from flask import Flask
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import jsonify
import numpy as np

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# We can view all of the classes that automap found
Base.classes.keys()

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route('/api/v1.0/precipitation')
def precip():
    data = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=dt.date(2016, 8, 23)).all()
    precip_dict = {date : precip for date,precip in data} 
    return jsonify(precip_dict)


@app.route('/api/v1.0/stations')
def stations():
    stat = session.query(Station.station).all()
    stat_list = list(np.ravel(stat))
    return jsonify(stat_list)
        
@app.route('/api/')
def temps():
    temp_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=dt.date(2016, 8, 23)).all()
    temp_dict = {date : temp for date,temp in temp_data}
    return jsonify(temp_dict)

@app.route('/api/v1.0/<start>')
def start_date(start):
    year = int(start[0:4])
    month = int(start[5:7])
    day = int(start[8:10])
    temp_start = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date>=dt.date(year, month, day)).all()
    start_date_list = list(np.ravel(temp_start))
    return jsonify(start_date_list)

@app.route('/api/v1.0/<start>/<end>')
def between_date(start, end):
    year_start = int(start[0:4])
    month_start = int(start[5:7])
    day_start = int(start[8:10])
    year_end = int(end[0:4])
    month_end = int(end[5:7])
    day_end = int(end[8:10])
    temp_between = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date>=dt.date(year_start, month_start, day_start)).filter(Measurement.date<=dt.date(year_end, month_end, day_end)).all()
    between_date_list = list(np.ravel(temp_between))
    return jsonify(between_date_list)

if __name__ == "__main__":
    app.run(debug=True)
