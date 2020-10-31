import datetime as dt
import numpy as np

from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.automap import automap_base
import sqlalchemy

from flask import Flask, jsonify, render_template
app = Flask(__name__)

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite",
                       connect_args={'check_same_thread': False})
conn = engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
Session = sessionmaker(bind=engine)
s = Session()


# Routes
@app.route("/")
def index():
  return render_template("index.html")


@app.route("/api/v1.0/precipitation")
def precipitation():
  prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
  result = s.query(Measurement.date, Measurement.prcp)\
      .filter(Measurement.date > prev_year)\
      .order_by(Measurement.date.desc())\
      .all()
  dict = {date: prcp for date, prcp in result}
  return jsonify(dict)


@app.route("/api/v1.0/stations")
def stations():
  result = s.query(Station.station).all()
  dict = {'stations': [x[0] for x in result]}
  return jsonify(dict)


@app.route("/api/v1.0/tobs")
def tobs():
  start_date = "2016-08-23"
  end_date = "2017-08-23"
  station = "USC00519397"
  result = s.query(Measurement.tobs)\
      .filter(Measurement.date >= start_date)\
      .filter(Measurement.date <= end_date)\
      .filter(Station.station == station)\
      .all()
  result = list(np.ravel(result))
  return jsonify(result)


@app.route("/api/v1.0/temp/<start>/<end>")
@app.route("/api/v1.0/temp/<start>")
def dates(start=None, end=None):
  sel = [func.min(Measurement.tobs), func.avg(
      Measurement.tobs), func.max(Measurement.tobs)]
  if not end:
    result = s.query(*sel)\
        .filter(Measurement.date >= start)\
        .all()
  else:
    result = s.query(*sel)\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date <= end)\
        .all()
  result = list(np.ravel(result))
  return jsonify(result)


if __name__ == '__main__':
    app.run()
