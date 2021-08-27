from flask.wrappers import JSONMixin
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)


app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"/api/v1.0/start(yyyy-mm-dd)/end(yyyy-mm-dd)<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp = session.query(measurement).all()
    session.close()

    prcp_data = []
    for p in prcp:
        prcp_dict = {}
        prcp_dict["date"] = p.date
        prcp_dict["prcp"] = p.prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    station_s = session.query(station.station).all()
    station_list = list(np.ravel(station_s))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    one_year_ago = dt.date(
        2017, 8, 23) - dt.timedelta(days=365)
    tobs_results = session.query(measurement.tobs).filter(
        measurement.date >= one_year_ago).all()
    session.close()
    tobs_list = list(np.ravel(tobs_results))

    return jsonify(tobs_list)


@app.route("/api/v1.0/<date>")
def input(date):
    first_date = dt.datetime.strptime(date, "%Y-%m-%d")
    min_max_mean = session.query(func.min(measurement.tobs), func.max(
        measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date == first_date).all()
    session.close()
    result = list(np.ravel(min_max_mean))

    return jsonify(result)


@app.route("/api/v1.0/<start>/<end>")
def dates(start, end):
    min_max_mean = session.query(func.min(measurement.tobs), func.max(
        measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start, measurement.date <= start).all()
    session.close()
    result = list(np.ravel(min_max_mean))
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
